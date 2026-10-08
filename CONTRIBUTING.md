# Contributing

Read [AGENTS.md](AGENTS.md), select the owning skill, and establish the current
game or package revision before changing it. Keep general research, coding,
testing and audit methods with the separately maintained Assay project. Read
the actual method required for the task; a name in metadata is not its content.

A subject-method change should identify the game relation it affects, a
research or local design basis, a concrete construction or revision, and a
nearby lawful alternative. Do not turn one example into a universal requirement
or add checklists to compensate for unclear wording. Follow references when
they serve the task.

Use `VERSION` and `catalog.json` for release identity and inventory. Regenerate
derived projections through the repository's release tooling after changing
them. Change the Assay binding only after reviewing the dependency delta and
using its update tool with the explicit source root and intended revision; do
not refresh it merely to hide a compatibility failure.

Use established parsers and scoped deterministic checks for observable
properties. Run the relevant repository and example checks, preserving adverse
results. These checks cannot demonstrate discovery or better design decisions.
Any future model or human evaluation needs its own agreed inputs, isolation and
resources; preparing evaluation materials does not authorize running them.

The source checks used by CI are:

```bash
python -B tools/check.py
python -B -m unittest discover -s tests -v
python -B -m unittest discover -s examples/adaptation -p 'test_*.py' -v
python -B -m unittest discover -s examples/analysis-lab -p 'test_*.py' -v
python -B -m unittest discover -s examples/godot-episode -p 'test_*.py' -v
python -B -m unittest discover -s examples/design-studies/harbour-of-echoes -p 'test_*.py' -v
```

Install `requirements-dev.txt` in an isolated Python environment first. The
Godot command above checks the report contract; the native engine qualification
has its own [runtime and command](examples/godot-episode/README.md). Release
history, build and archive smoke checks are described in [releases](docs/releases.md).

No installer, automatic download, network callback or global hook runs when a
skill is read. Preserve foreign work, use new output paths, and do not infer
authority to publish or change a live game from a design request. Local source
edits, client installation and publication are separate actions.
