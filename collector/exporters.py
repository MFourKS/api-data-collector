import csv
import io
import json
from abc import ABC, abstractmethod
from pathlib import Path


class Exporter(ABC):
    ext = ""

    def save(self, reports, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.render(reports), encoding="utf-8")

    @abstractmethod
    def render(self, reports) -> str:
        ...


class JsonExporter(Exporter):
    ext = ".json"

    def render(self, reports):
        return json.dumps([r.as_dict() for r in reports], ensure_ascii=False, indent=2)


class CsvExporter(Exporter):
    ext = ".csv"

    def render(self, reports):
        buf = io.StringIO()
        cols = ["user_id", "name", "email", "company",
                "posts_count", "average_post_length", "post_titles"]
        w = csv.DictWriter(buf, fieldnames=cols)
        w.writeheader()
        for r in reports:
            row = r.as_dict()
            row["post_titles"] = " | ".join(row["post_titles"])  # список -> одна ячейка
            w.writerow(row)
        return buf.getvalue()


class TxtExporter(Exporter):
    ext = ".txt"

    def render(self, reports):
        out = []
        for r in reports:
            titles = "\n".join(f"    - {t}" for t in r.post_titles) or "    (постов нет)"
            out.append(
                f"{r.name} <{r.email}>\n"
                f"  компания: {r.company}\n"
                f"  постов: {r.posts_count}, средняя длина: {r.average_post_length}\n"
                f"  заголовки:\n{titles}"
            )
        return "\n\n".join(out) + "\n"


class MarkdownExporter(Exporter):
    ext = ".md"

    def render(self, reports):
        lines = ["# Отчёт по пользователям", ""]
        for r in reports:
            lines += [
                f"## {r.name} (#{r.user_id})",
                f"- email: {r.email}",
                f"- компания: {r.company}",
                f"- постов: {r.posts_count}",
                f"- средняя длина поста: {r.average_post_length}",
                "- заголовки:",
            ]
            lines += [f"  - {t}" for t in r.post_titles] or ["  - (постов нет)"]
            lines.append("")
        return "\n".join(lines)


EXPORTERS = {
    "json": JsonExporter,
    "csv": CsvExporter,
    "txt": TxtExporter,
    "md": MarkdownExporter,
}


def get_exporter(fmt):
    if fmt not in EXPORTERS:
        raise ValueError(f"нет такого формата: {fmt}. есть: {', '.join(EXPORTERS)}")
    return EXPORTERS[fmt]()
