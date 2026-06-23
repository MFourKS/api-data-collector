# API Data Collector
Асинхронно качает данные с
https://jsonplaceholder.typicode.com/, собирает отчёт по каждому юзеру
и пишет в файл. Форматы: json, csv, txt, md.

## Что в отчёте

Берём `/users` и `/posts`, на каждого пользователя считаем:

- user_id
- name
- email
- company
- posts_count — сколько постов
- average_post_length — средняя длина тела поста
- post_titles — заголовки постов

## Запуск

```
pip install -r requirements.txt

python main.py --format json --output output/report.json
python main.py --format csv  --output output/report.csv
python main.py --format txt  --output output/report.txt
python main.py --format md   --output output/report.md
```

Аргументы:
- `--format` — json / csv / txt / md (обязательный)
- `--output` — путь к файлу, папки создаются сами (обязательный)
- `--base-url` — если надо дёрнуть другой API

## Логи

Пишутся в консоль (INFO) и в `logs/collector.log` (DEBUG, там же видно запросы
к API). Файл создаётся сам.

## Ошибки

- косяки HTTP заворачиваются в `ApiError`
- на 5xx и сетевые сбои делается несколько повторов с задержкой
- на 4xx не повторяем — это ошибка запроса
- коды возврата: 0 ок, 1 ошибка API, 2 остальное

## Тесты

```
pip install -r requirements-dev.txt
pytest
```

HTTP-клиент в тестах подменяется заглушкой, в сеть не ходим.

## Структура

```
main.py              - CLI и настройка логов
collector/
  models.py          - User, Post, UserReport
  api.py             - HTTP-клиент (+ заглушка для тестов) и источники /users, /posts
  report.py          - build_reports(), считает отчёт
  exporters.py       - json/csv/txt/md
tests/
output/              - примеры результата
```

=================Кратĸо описано, ĸаĸ в проеĸте применены ООП и SOLID===============

Разнёс по ролям: модели, клиент API, источники, сборка отчёта, экспортёры.
Получение данных, обработка и запись лежат отдельно и не лезут друг в друга.

- каждый класс делает что-то одно: HttpxClient ходит в сеть, build_reports
  считает, экспортёры пишут файлы
- новый формат добавляется новым классом-наследником Exporter + строчкой в
  словаре EXPORTERS, старый код не трогается
- HttpClient — абстракция
- зависимости передаются снаружи (клиент в источники, формат выбирается в main)
