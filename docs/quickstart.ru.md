# Быстрый старт

Game Design — набор навыков для AI-агентов, которые проектируют и изменяют
игры. Можно установить пакет в Codex или Claude Code либо читать его
исходники без регистрации.

## Установка из GitHub

Для установки нужен клиент с поддержкой плагинов. Команды одинаковы для Bash
и Windows PowerShell. Если marketplace `game-design-source` уже существует,
сначала проверьте его источник и настройки.

**Codex:**

```bash
codex plugin marketplace add Muratovnik/gamedesign-skills
codex plugin add game-design@game-design-source
codex plugin list --marketplace game-design-source --json
```

**Claude Code:** запустите команды из каталога игрового проекта, чтобы
`--scope local` относился к нему.

```bash
claude plugin marketplace add Muratovnik/gamedesign-skills --scope local
claude plugin install game-design@game-design-source --scope local
claude plugin details game-design
```

Проверьте, что клиент показывает навыки Game Design, и начните новую сессию.
Команды с GitHub соответствуют документации менеджеров; тесты проекта пока
подтверждают установку из локального каталога на Linux, но не этот
GitHub-маршрут. Подробности, ограничения, обновление и удаление:
[установка](installation.md) и
[совместимость](compatibility.md#native-client-qualification).

## Первая задача

Для знакомства с навыком не нужны исходники игры. Отправьте агенту:

> Используй навык `gameplay-design` из Game Design. В игре с видом сверху
> противник готовит удар 0,6 секунды и поражает одну клетку. Предупреждение
> появляется только за 0,1 секунды до удара. Пересмотри предупреждение и
> правила реакции игрока. Укажи точные интервалы, допустимые действия и
> сценарий неудачной реакции для проверки. Код не изменяй.

Ожидается конкретное игровое правило и проверяемый негативный сценарий,
а не список общих принципов. Это пример запроса, не запись о запуске модели
или плейтесте.

Для своей игры дайте агенту текущие правила или файлы, сформулируйте
изменение и границы разрешённых действий. Можно прямо указать подходящий
навык или обратиться к [карте возможностей](traceability.md). Установка
сама по себе не доказывает автоматический выбор метода.

## Работа с исходниками без установки

Скачайте [исходный архив v0.2.0](https://github.com/Muratovnik/gamedesign-skills/releases/tag/v0.2.0)
или используйте checkout репозитория. Передайте агенту абсолютный путь к
пакету и каталогу игры, текущий артефакт, цель и разрешённые действия.
Попросите прочитать нужный `skills/<name>/SKILL.md` и связанные материалы.
Для этого не нужны Python и регистрация плагина в клиенте.

## Отдельный исполняемый пример

[East Gate](../examples/adaptation/README.md) — игровая загадка на двух
языках, проверяемая Python-потребителем. Этот пример показывает связь
игровой подсказки и действий, но не заменяет применение навыка к собственной
игре. Для запуска нужен Python 3.11 или новее. Из корня пакета `game-design/`
в Bash:

```bash
mkdir -p tmp
python3 examples/adaptation/consumer.py \
  --artifact examples/adaptation/fixtures/east-gate-ru.json \
  --expect-revision east-gate-ru-2 \
  --pin 1 --pin 2 --pin 3 --pin 4 --pin 5 --pin 6 \
  --choose east \
  --output tmp/east-gate-result.json
```

Успешный результат содержит `status: executed` и `gate: open`. Файл
`tmp/east-gate-result.json` должен быть новым: потребитель не перезаписывает
существующий. Команды для Windows PowerShell и сценарии неверного
направления или повреждённого содержимого приведены в
[руководстве East Gate](../examples/adaptation/README.md#run-the-example).

## Assay для задач, которым он нужен

Общие методы исследования и инженерии поддерживаются отдельно в Assay.
Текущая привязка Game Design требует исходник Assay 0.17.2 с commit
`94c517b0aac9ba2575086bf9aead1cc828aadb0d`; пакет его не устанавливает.
Когда конкретной задаче нужен внешний метод, откройте
[контракт потребителя и Assay](../skills/game-design/references/consumer-and-assay-contract.md)
для проверки разрешённого источника и условий `--provider-state enabled`.

Для других примеров — Godot, матрицы стратегий,
[Ink](../examples/ink-episode/README.md) и
[glTF/GLB](../examples/gltf-artifacts/README.md) — см.
[путеводитель](examples.md). Их зависимости подготавливаются по необходимости.
