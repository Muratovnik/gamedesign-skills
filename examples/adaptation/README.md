# East Gate: preserve an operation across language and layout

An original two-version microgame for adapting an existing artifact. Read the verse, use its
guide, and choose one of four directions. A correct choice opens the gate and
gives a ferryman token; a wrong direction returns to the verse without loss.
The separate ferry consumer requires the saved direction and an unspent token,
then spends the token and starts a voyage. No score or timer is needed.

The English four-line version spells EAST. The Russian six-line version spells
ВОСТОК. The target presents one line at a time; players may permanently pin whole
lines to compare them. Pinning preserves the task of finding the operation and
applying it. It is not a simulated measurement of reading or memory demand.

The JSON files are the actual consumed content, not examples of a proposed
format. The CLI is a small game consumer with a text view, pin and direction actions. It
checks the input record types, revision, clue-to-exit relation and the later sign
before accepting data. Malformed content or saved action records return a
structured `invalid` result with exit 2 and create no game output. An actual
wrong direction is a valid executed turn with a closed gate, not malformed data.
This deliberately narrow consumer is not a general story engine or a mobile UI.

From this directory, use a new output path:

```bash
python3 consumer.py --artifact fixtures/east-gate-ru.json --expect-revision east-gate-ru-2 --pin 1 --pin 2 --pin 3 --pin 4 --pin 5 --pin 6 --choose east --output /tmp/east-gate-run.json
python3 consumer.py --operation view --artifact fixtures/east-gate-ru.json --expect-revision east-gate-ru-2 --line 1 --output /tmp/east-gate-line1.json
python3 consumer.py --operation enter-ferry --artifact fixtures/east-gate-ru.json --expect-revision east-gate-ru-2 --state /tmp/east-gate-run.json --output /tmp/east-gate-voyage.json
python3 -m unittest discover -s . -p 'test_*.py' -v
```

The `view` operation emits the guide, one visible target line, the next line ID
and allowed actions. Request that next ID to browse the next line; the source
version emits its four lines together. These are actual serialized text views,
not a rendered mobile interface. The default play command applies the supplied
pin and choice sequence. It does not claim that a human actually read the views.
`enter-ferry` reopens the saved result in another process, verifies the content
digest and direction/token, and returns a consumed-token state. Reusing that
post-voyage state is rejected.

Inspect the result's notebook, gate, token and voyage. Choose `north` to
exercise a legitimate wrong turn. Change the first target line to a literal
translation starting with С to produce a broken operation; the consumer refuses
that artifact instead of recording a successful localization. Rewriting it with
a different meaningful В line is a valid alternative. The original source file
stays available for comparison.

The corresponding method and research transfer are in
[adaptation](../../skills/game-design/references/adaptation.md). Language quality,
screen-reader behavior, actual small-screen layout and human inference are open
observations; the included deterministic checks prove only the declared content
and action relations. Collect a consented target-device session through the
[environment contract](../../skills/game-design/references/environment-contracts.md)
when those properties are required.
