import json

from PySide6.QtCore import QDate

from quotiac_sandbox.puzzle_types import CryptographBase
from quotiac_sandbox.utils.update_puzzle_list import save_puzzle_types


def save_as_new_file(puzzle: CryptographBase, date: QDate) -> None:
    with open(
        f"resources/by-date/{date.year():04d}{date.month():02d}{date.day():02d}.json",
        "w",
    ) as fp:
        json.dump(puzzle.to_json(to_read_from_frontend=True), fp, indent=2)
    save_puzzle_types()
