# Security

Report suspected vulnerabilities privately to the maintainer before opening a
public issue. Use GitHub's private vulnerability reporting when it is enabled;
otherwise use the maintainer's contact address in the Git author metadata.
Include the affected version, a minimal reproducer and the observed impact.
Do not include real credentials or private game data in a public report.

Game Design provides source methods and synthetic examples. Reading a skill
does not authorize commands, dependencies, client installation or publication.
Review scripts before running them and provide only the access the task needs.
Run unfamiliar game content and tools in an environment appropriate for their
inputs. The JSON schemas validate specific example contracts; they do not turn
arbitrary source code into trusted input.

The release smoke verifies archive paths, regular files, checksums, version and
the shipped East Gate consumer. A matching checksum detects changed bytes; it
does not independently identify a publisher or prove every program safe.
The repository's release audits scan publication candidates and history. Their
results do not establish game quality, client permissions or human experience.
