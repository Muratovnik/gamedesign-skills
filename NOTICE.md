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

Assay is a separate methodological dependency, not copied runtime game-design content.
Godot, Python and the Python packages listed in `requirements-dev.txt` are
external technical dependencies and are not bundled as binaries. Users obtain
them under their respective licenses. No third-party game-design skill or
framework supplied the structure or content of the original implementation.

The comparative extension adds original adapters and synthetic examples; it does
not copy a third-party game-design skill, framework, template, test or art asset.
Its idea-level provenance and exact source/terms checks are recorded in the
[external comparison](docs/research/2026-10-08/comparison.md). The optional
technical dependencies are obtained separately and are not bundled:

- [SciPy 1.17.0](https://github.com/scipy/scipy/blob/8c75ae75176236f233824e9a0483c26a69e6dfec/LICENSE.txt),
  BSD-3-Clause, Enthought and SciPy developers. Its bundled licenses include
  [HiGHS](https://github.com/scipy/HiGHS/blob/222cce79a2bca866dbfbcd91b55da11336ae88f4/LICENSE.txt),
  MIT. The qualified numerical environment uses
  [NumPy 2.3.5](https://github.com/numpy/numpy/blob/c3d60fc8393f3ca3306b8ce8b6453d43737e3d90/LICENSE.txt),
  BSD-3-Clause, NumPy developers.
- [inkjs 2.4.0](https://github.com/y-lohse/inkjs/blob/edccead8700e9f21be9825d87d8645d8c82a9936/LICENSE.md),
  MIT, copyright 2017 inkle Ltd. and inkjs contributors.
- [glTF-Validator 2.0.0-dev.3.10](https://github.com/KhronosGroup/glTF-Validator/blob/bcd52cc4ba5f333b2999a58f67cc05ddf28b4fb1/LICENSE),
  Apache-2.0, Khronos Group, with the package's bundled
  [NOTICES](https://github.com/KhronosGroup/glTF-Validator/blob/bcd52cc4ba5f333b2999a58f67cc05ddf28b4fb1/NOTICES).

The repository distributes version declarations/locks and calls public APIs.
If these dependencies are redistributed later, retain their full licenses,
copyright notices and bundled third-party notices; the Game Design MIT license
does not replace those terms.

Research evidence archives retain original command output, including excerpts
read from Assay 0.17.2, inkjs 2.4.0 and glTF-Validator 2.0.0-dev.3.10. These
read records are not installed methods or a second maintained implementation.
The [model evidence archive](docs/reviews/2026-10-08-comparison/behavior-evidence.zip)
includes Assay's and inkjs's full MIT licenses and glTF-Validator's Apache-2.0
license and bundled NOTICES beside an attribution index. Assay's copyright is
Nikolai Muratov and contributors. The archive preserves the read output without
relicensing its source excerpts under the original examples' license.

A separate fresh-install check also resolved and exercised
[NumPy 2.5.3](https://github.com/numpy/numpy/tree/dd88c0c19b54ad9ed3533224221285bf0873249a).
Its installed metadata declares `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0`;
the core project license alone is not an inventory of bundled obligations.
The [retained metadata and license-file identities](docs/reviews/2026-10-08-comparison/clean-matrix-dependency-terms.json)
identify that external installation. No NumPy implementation or wheel is bundled.

The native qualification workflow obtains Codex CLI 0.159.2 and Claude Code
2.1.289 as external maintainer tools. Codex's package is Apache-2.0; Claude's
package refers to [Anthropic's legal agreements](https://code.claude.com/docs/en/legal-and-compliance)
and is not licensed here as MIT. Neither client binary is redistributed.

The repository pins [Release Kit](https://github.com/Muratovnik/release-kit)
0.31.0 as `.github/relkit.pyz` for publication checks. It is separately licensed
under MIT; its full license and author notice are included in the zipapp's
distribution metadata. It is maintainer tooling, outside the installed skills.
