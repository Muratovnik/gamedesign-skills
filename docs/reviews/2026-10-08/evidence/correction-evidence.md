# Свидетельства correction-прохода

Архив: [correction-evidence.zip](correction-evidence.zip). Точный состав,
размеры и SHA-256: [correction-evidence-manifest.json](correction-evidence-manifest.json).
Все 567 членов заново прочитаны и сверены; исходные результаты review находятся
в отдельном неизменённом [baseline archive](baseline-evidence.zip).

Опубликованная исправленная реализация: `7b385469b95ffe40562e7161ea9c3cab7bec2b94`.
Проверенный локальный commit `5f3d0951b18dd5c87a5e077c8560d555a1c03c2d`
имеет то же Git tree; [запись передачи](github-transfer.json) связывает оба SHA.
Raw receipts сохраняют первоначальные локальные идентификаторы.
[correction-identity.json](correction-identity.json) содержит 151 файл этого
снимка до добавления данной записи и correction evidence. Основной документ —
[game-design-own-baseline.md](../game-design-own-baseline.md).

Пути ниже относятся к содержимому ZIP. Абсолютные paths/argv в сырых записях
сохраняют происхождение; для другой машины нужно выбрать собственные source и
output directories. Записи не являются конфигурацией установки.

| Содержимое | Что искать |
| --- | --- |
| `technical/correction.md` | Dispositions GD-T01–05, изменения, проверки и точные raw labels |
| `technical/correction/logs/replay-*` | 14 повторов исходных probes; argv/cwd/child exit code и исходные stdout/stderr |
| `technical/correction/logs/pre-relation-*`, `post-relation-*` | Три дополнительные пары несогласованного saved owner/history, до и после усиления GD-T03 |
| `technical/correction/results/`, `fixtures/` | Фактические state/SQLite/WAV/CSV результаты и новые synthetic inputs; это не model или native observations |
| `technical/correction/evidence-summary.json` | Хеши неизменённых входов и native source, сравнение кодов и артефактов, 55 целевых тестов |
| `integration/correction/` | Dispositions GD-I01/02, исторический семифайловый Assay delta с проверкой хешей, binder before/after, metadata и document gates |
| `domain/correction.md` | Ранний/поздний отказ и rack-state: адресная логическая проверка authored материала; не эксперимент |
| `integrated-checks/` | Общий source gate и пять test suites: 78 tests PASS; 55 выше входят в них, не прибавляются повторно |
| `integrated-checks/assay-owners/` | Реальный binder check всех 14 owner-наборов текущей привязки |
| `native-baseline/` | Исходный default-30s suite: import timeout, exit 2, execution не достигнут |
| `native-diagnostic-minimal/`, `native-diagnostic-episode/` | Следующие диагностические импорты с успешным завершением; первый timeout не перезаписан |
| `native-runtime/baseline-harness-override.json` и `native-baseline-harness/.../qualify.py` | Единственная timeout-only замена 30→55 в отдельной baseline harness, diff и hashes |
| `native-baseline-55/`, `native-candidate-55/` | Две suites по шести одинаковым fixtures, 12/12 ожидаемых кодов в каждой; reports, реальные save JSON, source и native logs |
| `native-runtime/comparison.json` | Сверка входов, source hashes, сохранённого и конечного состояния двух suites |
| `native-first-tick/` и `native-runtime/first-tick-*` | Адресное native наблюдение warning перед resolution на tick 1 |
| `native-runtime/download-source.json`, `runtime.json` | Официальное происхождение, asset/binary SHA-256 и версия Godot; большой binary не включён |
| `native-client-isolation/native-outcome.md` | Достигнутые и недоступные клиентские границы, исходные ошибки и отказ procfs mount |
| `native-client-isolation/evidence-allowlist.txt` | 27 сохранённых records/launchers; без скопированного binary, profiles и cache |
| `final-checks/` | Реальные staged/history audit, source build и archive smoke исправленного code commit; 151/151 byte comparison |
| `review-exposure-audit.json`, `.stderr` | Первоначальный отказ exposure gate на raw synthetic SQLite/fixture path и основание узкого ZIP-исключения |

Не включены воспроизводимые editor caches, runtime binaries, пустые временные
каталоги и полные исходные вложения требований. Последние идентифицированы
отдельным [baseline manifest](baseline-identity.json). Точный отбор отражён
в manifest и сохранённом `build_correction_evidence.py`.

Этот архив закрывает code/correction evidence на момент фиксации. Последующие
delivery/PR CI результаты ещё не существовали и не могут быть частью этого
снимка. Они относятся к своему commit. Модельных и человеческих испытаний здесь
нет; modified report controls явно синтетические, ручной walkthrough не назван
экспериментом.
