import json
from datetime import datetime, timedelta
from random import choice

from codiac_sandbox.utils.puzzle_classes import parse_puzzle
from codiac_sandbox.utils.update_puzzle_list import save_puzzle_types

tomorrow = datetime.now() + timedelta(days=3)

date_string = tomorrow.strftime("%Y%m%d")

with open("resources/master-puzzle-list.json", "r") as read:
    with open(f"resources/auto-generated/{date_string}.json", "w") as write:
        puzzle = parse_puzzle(choice(json.load(read)))
        data = puzzle.to_json(to_read_from_frontend=True)

        json.dump(data, write, indent=2)

save_puzzle_types()
