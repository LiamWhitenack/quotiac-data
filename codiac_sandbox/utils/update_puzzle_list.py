import json
import os
from datetime import date, timedelta


def save_puzzle_types() -> None:
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    current_date = max(one_year_ago, date(2025, 8, 15))
    end_date = today + timedelta(days=365)

    puzzle_types: dict[str, str] = {}

    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        file_name = f"{date_str}.json"

        puzzle_type: str | None = None
        for folder in ("by-date", "auto-generated"):
            if os.path.exists((path := f"resources/{folder}/{file_name}")):
                with open(path, "r") as f:
                    data: dict[str, str] = json.load(f)
                    puzzle_type = data.get("puzzle_type")
            if puzzle_type is not None:
                puzzle_types[date_str] = puzzle_type
                break

        current_date += timedelta(days=1)

    with open("resources/puzzle-list.json", "w") as f:
        json.dump(puzzle_types, f, indent=4)
