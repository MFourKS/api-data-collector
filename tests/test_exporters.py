import csv
import io
import json

import pytest

from collector.exporters import get_exporter
from collector.models import UserReport


def sample():
    return [UserReport(1, "Иван", "ivan@ex.com", "Acme", 2, 6.0, ["Первый", "Второй"])]


def test_json():
    data = json.loads(get_exporter("json").render(sample()))
    assert data[0]["name"] == "Иван"
    assert data[0]["post_titles"] == ["Первый", "Второй"]


def test_csv():
    rows = list(csv.DictReader(io.StringIO(get_exporter("csv").render(sample()))))
    assert rows[0]["post_titles"] == "Первый | Второй"
    assert rows[0]["posts_count"] == "2"


def test_txt_and_md():
    assert "Иван" in get_exporter("txt").render(sample())
    assert "## Иван" in get_exporter("md").render(sample())


def test_unknown_format():
    with pytest.raises(ValueError):
        get_exporter("xml")
