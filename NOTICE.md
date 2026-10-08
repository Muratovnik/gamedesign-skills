# Third-party material and sources

The original Game Design methods, code and examples use the root MIT license.
Public research and design accounts are linked at the relevant claims; their
text, games and artwork are not licensed by this package.

`tools/vendor/plugin.schema.json` is an unchanged technical schema from the
[Agent Plugins specification](https://github.com/agentplugins/agent-plugins-spec),
commit `ff8ab5e392cc87bd88d87c060815a87490e51003`, path
`schemas/1.0.0/plugin.schema.json`. That repository's `LICENSE.md` licenses
schemas and software under Apache License 2.0. The license is included as
[Apache-2.0.txt](tools/vendor/Apache-2.0.txt). Only the schema and required
license are redistributed; this does not claim client operational conformance.

Assay is a separate methodological dependency, not copied game-design content.
Godot, Python and the Python packages listed in `requirements-dev.txt` are
external technical dependencies and are not bundled as binaries. Users obtain
them under their respective licenses. No third-party game-design skill or
framework supplied the structure or content of the original implementation.

The repository pins [Release Kit](https://github.com/Muratovnik/release-kit)
0.31.0 as `.github/relkit.pyz` for publication checks. It is separately licensed
under MIT; its full license and author notice are included in the zipapp's
distribution metadata. It is maintainer tooling, outside the installed skills.
