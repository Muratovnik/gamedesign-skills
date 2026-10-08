# East Gate: adapt a clue across language and layout

East Gate is a small two-version game for exploring what must survive when an
artifact changes. In English, four verse lines spell `EAST`; in Russian, six
lines spell `ВОСТОК`. The player reads a guide, chooses a direction, and can
open the gate by finding the direction encoded by the verse. The later ferry
scene uses that saved direction and spends the ferryman token. A wrong direction
returns the player to the verse without loss.

The files in `fixtures/` are playable inputs to the adjacent Python consumer.
It checks that the clue resolves to the declared exit and that the later sign
still points to that exit. The English fixture presents all four target lines
together. The Russian fixture presents one line at a time and allows pinning
lines in a notebook; pinning makes comparison available while the player works
out the clue. The consumer serializes text views and actions;
it does not render a phone screen or establish reading difficulty, language
quality, accessibility, or human inference.

## Run the example

You need Python 3.11 or later. No third-party package is needed. Run commands
from the Game Design repository root so the fixture paths below resolve. Give
each command a new output filename under the ignored `tmp/` directory; the
consumer refuses to overwrite an existing file.

In Bash, create the ignored scratch parent if it does not exist, then make a
fresh run directory and execute the play, view, and ferry steps in order:

```bash
mkdir -p tmp/reader-runs
RUN=$(mktemp -d tmp/reader-runs/east-gate-XXXXXX)
python3 examples/adaptation/consumer.py \
  --artifact examples/adaptation/fixtures/east-gate-ru.json \
  --expect-revision east-gate-ru-2 \
  --pin 1 --pin 2 --pin 3 --pin 4 --pin 5 --pin 6 --choose east \
  --output "$RUN/gate.json"
python3 examples/adaptation/consumer.py --operation view \
  --artifact examples/adaptation/fixtures/east-gate-ru.json \
  --expect-revision east-gate-ru-2 --line 1 --output "$RUN/line-1.json"
python3 examples/adaptation/consumer.py --operation enter-ferry \
  --artifact examples/adaptation/fixtures/east-gate-ru.json \
  --expect-revision east-gate-ru-2 --state "$RUN/gate.json" \
  --output "$RUN/voyage.json"
```

On Windows PowerShell, create the ignored scratch parent and run directory, then
use the Python launcher (or replace `py -3` with the path to your Python 3
executable):

```powershell
$null = New-Item -ItemType Directory -Force tmp\reader-runs
$run = Join-Path (Resolve-Path tmp\reader-runs) ("east-gate-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory $run | Out-Null
py -3 examples/adaptation/consumer.py --artifact examples/adaptation/fixtures/east-gate-ru.json --expect-revision east-gate-ru-2 --pin 1 --pin 2 --pin 3 --pin 4 --pin 5 --pin 6 --choose east --output (Join-Path $run gate.json)
py -3 examples/adaptation/consumer.py --operation view --artifact examples/adaptation/fixtures/east-gate-ru.json --expect-revision east-gate-ru-2 --line 1 --output (Join-Path $run line-1.json)
py -3 examples/adaptation/consumer.py --operation enter-ferry --artifact examples/adaptation/fixtures/east-gate-ru.json --expect-revision east-gate-ru-2 --state (Join-Path $run gate.json) --output (Join-Path $run voyage.json)
```

The play result should show an open gate, the six pinned lines in its notebook,
and an unspent `ferryman` token. The view result contains the guide, visible
line, next line ID, direction choices, and permitted actions. Since this
fixture uses a one-line carousel, request the returned next line ID to continue
browsing. The ferry result should mark the voyage started and the token spent.
The ferry step reopens the saved result in a separate process, checks its
content digest and direction, and accepts only the open gate with an unspent
token.

To inspect a valid wrong turn, rerun the play command in a separate fresh
directory with `--choose north`: the gate remains closed and no token is
awarded. A malformed or stale artifact, or an invalid saved action, instead
returns a structured `invalid` result and exit code 2 without a game output.
That is different from a valid wrong turn, which executes normally. The
included deterministic relations show what this consumer accepts; they are not
a measurement of how a person reads or solves the clue.

The adaptation method and its transfer guidance are in
[Adaptation](../../skills/game-design/references/adaptation.md). For a
consented target-device session, use the
[environment contract](../../skills/game-design/references/environment-contracts.md).
