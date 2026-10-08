"""Render the two published Loom phrases; no playback or participant claims."""

import argparse
from array import array
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import wave


SAMPLE_RATE = 24_000
PEAK_AMPLITUDE = 0.25 * 32767
RAMP_SAMPLES = 120  # A chosen 5 ms attack/release at this sample rate.
NOTES = ("C4", "E4", "G4")
MIDI_NOTES = (60, 64, 67)
FREQUENCIES = tuple(440 * 2 ** ((note - 69) / 12) for note in MIDI_NOTES)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_score(path):
    score = json.loads(path.read_text(encoding="utf-8"))
    if score.get("artifact_id") != "sound-and-light-loom":
        raise ValueError("Expected the sound-and-light-loom score")
    if score.get("beat_seconds") != 1:
        raise ValueError("This realization uses one-second beats")
    phrases = score.get("phrases", [])
    if [phrase.get("id") for phrase in phrases] != ["phrase-a", "phrase-b"]:
        raise ValueError("Expected both published phrases, in A/B order")
    for phrase in phrases:
        sections = phrase.get("sections", [])
        if not sections:
            raise ValueError(f"Empty phrase: {phrase['id']}")
        for section in sections:
            if type(section.get("beats")) is not int or section["beats"] < 1:
                raise ValueError("Each section needs a positive integer beat count")
            for control in ("u", "v"):
                if type(section.get(control)) is not int or section[control] not in (0, 1, 2):
                    raise ValueError(f"Control {control} must be 0, 1 or 2")
            if type(section.get("sound")) is not bool:
                raise ValueError("Each section needs an explicit sound/rest state")
        if sum(section["beats"] for section in sections) != 12:
            raise ValueError(f"Expected twelve beats in {phrase['id']}")
    return score


def put_tone(samples, start, end, frequency):
    length = end - start
    for offset in range(length):
        gain = min(1.0, offset / RAMP_SAMPLES, (length - 1 - offset) / RAMP_SAMPLES)
        phase = 2 * math.pi * frequency * offset / SAMPLE_RATE
        samples[start + offset] = round(PEAK_AMPLITUDE * gain * math.sin(phase))


def render_phrase(phrase, directory):
    samples = array("h", [0]) * (12 * SAMPLE_RATE)
    if samples.itemsize != 2:
        raise ValueError("This PCM16 writer requires a two-byte Python short")
    visual_rows = []
    beat_cursor = 0
    for section in phrase["sections"]:
        u, v = section["u"], section["v"]
        pulse_count = 2 ** v
        first = beat_cursor * SAMPLE_RATE
        last = (beat_cursor + section["beats"]) * SAMPLE_RATE
        if section["sound"] and v == 0:
            # Keep a held sparse section continuous across its beat boundaries.
            put_tone(samples, first, last, FREQUENCIES[u])
        for local_beat in range(section["beats"]):
            beat = beat_cursor + local_beat
            if section["sound"] and v > 0:
                slot_samples = SAMPLE_RATE // pulse_count
                for pulse in range(pulse_count):
                    start = beat * SAMPLE_RATE + pulse * slot_samples
                    put_tone(samples, start, start + slot_samples // 2, FREQUENCIES[u])
            visual_rows.append({
                "beat": beat + 1,
                "start_seconds": beat,
                "end_seconds": beat + 1,
                "u": u,
                "v": v,
                "sound": str(section["sound"]).lower(),
                "note_when_sounding": NOTES[u],
                "pitch_when_sounding_hz": round(FREQUENCIES[u], 9),
                "pulses_per_beat_when_sounding": pulse_count,
                "circle_radius_units": u + 1,
                "dots": pulse_count,
            })
        beat_cursor += section["beats"]

    wav_path = directory / f"{phrase['id']}.wav"
    if sys.byteorder != "little":
        samples.byteswap()
    with wav_path.open("xb") as destination:
        with wave.open(destination, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(SAMPLE_RATE)
            wav.writeframes(samples.tobytes())

    csv_path = directory / f"{phrase['id']}-visual-timeline.csv"
    with csv_path.open("x", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=visual_rows[0].keys())
        writer.writeheader()
        writer.writerows(visual_rows)
    return wav_path, csv_path


def reopen_wav(path, phrase):
    with wave.open(str(path), "rb") as wav:
        channels, width, rate, frames, compression, _ = wav.getparams()
        if (channels, width, rate, frames, compression) != (1, 2, SAMPLE_RATE, 12 * SAMPLE_RATE, "NONE"):
            raise ValueError(f"Unexpected reopened WAV format or duration: {path.name}")
        pcm_bytes = wav.readframes(frames)
    if len(pcm_bytes) != frames * width * channels:
        raise ValueError(f"Truncated PCM data: {path.name}")
    samples = array("h")
    samples.frombytes(pcm_bytes)
    if sys.byteorder != "little":
        samples.byteswap()
    nonzero = sum(sample != 0 for sample in samples)
    if not nonzero:
        raise ValueError(f"No nonzero samples: {path.name}")
    section_results = []
    cursor = 0
    for section in phrase["sections"]:
        end = cursor + section["beats"] * SAMPLE_RATE
        section_nonzero = sum(sample != 0 for sample in samples[cursor:end])
        if bool(section_nonzero) != section["sound"]:
            raise ValueError(f"Declared sound/rest was not preserved: {path.name}")
        section_results.append({
            "start_seconds": cursor / SAMPLE_RATE,
            "end_seconds": end / SAMPLE_RATE,
            "sound": section["sound"],
            "nonzero_samples": section_nonzero,
        })
        cursor = end
    return {
        "format": "mono PCM16 little-endian",
        "sample_rate_hz": rate,
        "sample_count": len(samples),
        "frame_count": frames,
        "duration_seconds": frames / rate,
        "nonzero_samples": nonzero,
        "peak_absolute_sample": max(abs(sample) for sample in samples),
        "sections": section_results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--score", type=Path, default=Path(__file__).with_name("loom-score.json"))
    parser.add_argument("--output-dir", type=Path, required=True, help="A new directory; existing paths are rejected")
    args = parser.parse_args()
    try:
        score_path = args.score.resolve()
        score = read_score(score_path)
        output_dir = args.output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=False)
        outputs = []
        for phrase in score["phrases"]:
            wav_path, csv_path = render_phrase(phrase, output_dir)
            outputs.append({
                "phrase_id": phrase["id"],
                "wav": {"file": wav_path.name, "sha256": sha256(wav_path)},
                "visual_timeline": {"file": csv_path.name, "sha256": sha256(csv_path), "rows": 12},
                "reopened_wav": reopen_wav(wav_path, phrase),
            })
        receipt = {
            "receipt_format": "loom-render-1",
            "artifact_id": score["artifact_id"],
            "score_revision": score["revision"],
            "score": {"file": score_path.name, "sha256": sha256(score_path)},
            "renderer": {"file": Path(__file__).name, "sha256": sha256(Path(__file__))},
            "python_version": sys.version.split()[0],
            "rendering_choices": {
                "beat_seconds": 1,
                "tone": "sine, phase reset at each sounding interval",
                "u_notes": dict(zip(NOTES, FREQUENCIES)),
                "pitch_formula": "440 * 2 ** ((midi_note - 69) / 12), midi notes 60/64/67",
                "density_mapping": "2 ** v; sustained across the section at v=0",
                "active_fraction_for_v_1_or_2": 0.5,
                "peak_fraction_of_positive_pcm16_range": 0.25,
                "linear_attack_and_release_seconds": RAMP_SAMPLES / SAMPLE_RATE,
            },
            "outputs": outputs,
            "scope": "Synthetic authored audio plus timed visual-state data; WAV reopened as PCM samples.",
            "limits": [
                "No listening, participant observation or musical-quality comparison was performed.",
                "No live input, device playback, output latency or continuous-control behavior was measured.",
                "The CSV records circle/dot states; it is not a rendered visual animation.",
            ],
        }
        receipt_path = output_dir / "receipt.json"
        with receipt_path.open("x", encoding="utf-8") as destination:
            json.dump(receipt, destination, indent=2, ensure_ascii=False)
            destination.write("\n")
        print(json.dumps({"output_dir": str(output_dir), "receipt_sha256": sha256(receipt_path), "outputs": outputs}, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Loom render stopped: {error}\n")


if __name__ == "__main__":
    main()
