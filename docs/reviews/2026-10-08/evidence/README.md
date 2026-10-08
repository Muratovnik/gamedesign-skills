# Исходные свидетельства review

Исходные файлы находятся в [baseline-evidence.zip](baseline-evidence.zip); точный состав и хеши — в [baseline-evidence-manifest.json](baseline-evidence-manifest.json). Архив заново открыт, каждый член сверен по SHA-256. Пути ниже относятся к содержимому архива.

Эти файлы сохранены до correction-прохода и не заменяются исправленными результатами. Они относятся к исходному Game Design `f9f6bac0ee767597692d5c17d1eecc90f6788aa8`, кроме явно обозначенной копии binding 0.17.2. Абсолютные пути и argv в receipts описывают исходную среду; они не означают наличие такой среды у будущего читателя.

- [baseline-identity.json](baseline-identity.json) — исходный commit/tree, хеши 139 файлов и 12 переданных оснований, отсутствие model budget.
- `baseline/commands.json` — локальная структура и 18 distribution tests, исходные stdout/stderr и версии зависимостей рядом.
- `technical/logs/` — argv, cwd, environment, exit codes, исходный timeout и stdout/stderr всех адресных технических проверок. `technical/fixtures/` содержат минимальные изменённые входы, `technical/results/` — фактические отчёты и созданные файлы. Старый native report также остаётся в исходном дереве, его изменение для probe не является новым native run.
- `integration/logs/` — упаковка, binder и native CLI help. `integration/layout-report.json` и `integration/archive-inventory.json` сохраняют проверенную файловую границу, `integration/assay-delta.json` — сравнение per-owner bytes.

GD-T01: пары `telemetry-valid` / `telemetry-invalid-definition`. GD-T02: `recover-valid` / `recover-no-knowledge` и `choose-valid` / `choose-no-knowledge` (отказ конкретной карточки не обязательно означает общий exit 1). GD-T03: `assess-recorded-valid` / `assess-missing-state-events`. GD-T04: `adaptation-without-pins-*`. GD-T05: `loom-valid` / `loom-wrong-root`. GD-I02: `bind-owner-only`, `bind-missing-resource`, `bind-changed-resource`, `bind-disabled`, `bind-symlink-loop`.

`capture.py` и подготовительные scripts — сохранённые средства адресного воспроизведения с путями той сессии; они не добавляют публичный runtime contract. Сценарии authored gamebook разобраны по правилам, без исполнения interpreter и без подмены человеческого playtest. Избыточный начальный preflight перечислил имена вне заданных roots; их содержимое не читалось и не использовалось, сам посторонний список сюда не копируется. Изоляция в целом задавалась инструкцией, не OS sandbox.
