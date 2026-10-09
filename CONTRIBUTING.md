# Contributing

This repository owns the seven Game Design methods and their examples. General
research, implementation, testing and audit methods belong to the separately
maintained [Assay project](https://github.com/Muratovnik/assay). Before changing
a method, read [AGENTS.md](AGENTS.md), choose its owning skill and inspect the
game or package revision that the change affects.

For a subject-method change, show the affected game relationship, the local
design basis, a concrete construction or revision, and a nearby legitimate
alternative. Preserve expressive play without victory, permanent assistance,
purposeful repetition and accepted endings where they fit the design. Do not
turn one example into a universal requirement.

## Run the maintainer checks

Use Python 3.11 or newer from the repository root. These checks use the isolated
development dependencies in `requirements-dev.txt`; they do not run model
comparisons or establish human experience. In Bash:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -B tools/check.py
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B -m unittest discover -s examples/adaptation -p 'test_*.py' -v
.venv/bin/python -B -m unittest discover -s examples/analysis-lab -p 'test_*.py' -v
.venv/bin/python -B -m unittest discover -s examples/godot-episode -p 'test_*.py' -v
.venv/bin/python -B -m unittest discover -s examples/design-studies/harbour-of-echoes -p 'test_*.py' -v
```

On Windows, create the environment with `py -3.11 -m venv .venv`, install with
`.venv\Scripts\python -m pip install -r requirements-dev.txt`, then run the
same checks by replacing `.venv/bin/python` with `.venv\Scripts\python`.
`tools/check.py` checks local structure, links, schemas and generated metadata;
the test commands check their named deterministic examples. The Godot-example
tests check its report contract. Running its native engine check requires a
separately obtained Godot version; see the
[Godot episode guide](examples/godot-episode/README.md). The
[release guide](docs/releases.md) describes archive preparation and smoke checks.

## Package ownership

`VERSION` and `catalog.json` define release identity and the seven-entry
inventory. If either changes, regenerate derived client projections with
`python tools/render.py` and check them with `python tools/render.py --check`.
Do not edit generated marketplace or plugin files by hand. The Assay binding is
version-specific; review the dependency change and use its update tool with the
explicit source root and intended revision instead of refreshing it to hide a
compatibility failure.

Keep maintenance tools and tests outside the seven runtime skill directories.
No installer, automatic download, network callback or global hook runs when a
skill is read. Preserve unrelated work. Client installation and publication are
separate owner actions; a source edit does not authorize either.
