import csv
import json
from pathlib import Path
from typing import Union, List, Dict, Any, Iterable


def _row_key(row: Dict[str, Any], unique_fields: Iterable[str]) -> tuple:
    return tuple(row.get(field) for field in unique_fields)


def remove_duplicates_from_csv(
    csv_file: str,
    unique_fields: Iterable[str],
    encoding: str = "utf-8"
) -> None:
    path = Path(csv_file)
    if not path.exists():
        return

    with open(path, newline="", encoding=encoding) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    seen = set()
    unique_rows = []

    for row in rows:
        key = _row_key(row, unique_fields)
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)

    with open(path, "w", newline="", encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_rows)


def json_to_csv(
    data: Union[str, Dict[str, Any], List[Dict[str, Any]]],
    output_file: str,
    unique_fields: Iterable[str] | None = None,
    encoding: str = "utf-8"
) -> None:

    if isinstance(data, str):
        data = json.loads(data)

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list) or not data:
        raise ValueError("JSON inválido")

    fieldnames = set()
    for row in data:
        if not isinstance(row, dict):
            raise ValueError("JSON inválido")
        fieldnames.update(row.keys())

    fieldnames = sorted(fieldnames)

    path = Path(output_file)
    file_exists = path.exists()

    with open(path, "a", newline="", encoding=encoding) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(data)

    if unique_fields:
        remove_duplicates_from_csv(
            output_file,
            unique_fields=unique_fields,
            encoding=encoding
        )