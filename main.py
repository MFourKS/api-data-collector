
# python main.py --format json --output output/report.json
# python main.py --format csv  --output output/report.csv


import argparse
import asyncio
import logging
import sys
from pathlib import Path

from collector.api import ApiError, HttpxClient, Posts, Users
from collector.exporters import EXPORTERS, get_exporter
from collector.report import build_reports

BASE_URL = "https://jsonplaceholder.typicode.com"

log = logging.getLogger("main")


def setup_logging(log_file="logs/collector.log"):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"

    file_h = logging.FileHandler(log_file, encoding="utf-8")
    file_h.setLevel(logging.DEBUG)

    console_h = logging.StreamHandler()
    console_h.setLevel(logging.INFO)

    logging.basicConfig(level=logging.DEBUG, format=fmt, handlers=[file_h, console_h])


async def collect(fmt, output, base_url):
    client = HttpxClient(base_url)
    try:
        users_src = Users(client)
        posts_src = Posts(client)
        # оба запроса независимы — пускаем разом
        users, posts = await asyncio.gather(users_src.load(), posts_src.load())
    finally:
        await client.close()

    log.info("пользователей: %d, постов: %d", len(users), len(posts))

    reports = build_reports(users, posts)
    get_exporter(fmt).save(reports, Path(output))
    log.info("сохранил в %s", output)


def main():
    parser = argparse.ArgumentParser(description="API Data Collector")
    parser.add_argument("--format", required=True, choices=list(EXPORTERS))
    parser.add_argument("--output", required=True)
    parser.add_argument("--base-url", default=BASE_URL)
    args = parser.parse_args()

    setup_logging()

    try:
        asyncio.run(collect(args.format, args.output, args.base_url))
    except ApiError as e:
        log.error("API не ответил как надо: %s", e)
        return 1
    except Exception as e:
        log.exception("что-то пошло не так: %s", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
