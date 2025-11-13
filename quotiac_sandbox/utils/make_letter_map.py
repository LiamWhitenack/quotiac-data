from random import choices, sample

import json

with open("resources/icon-list.json", "r") as file:
    icons: list[str] = json.load(file)


def get_new_letter_map(quote: str) -> dict[str, str]:
    return {
        char: icon
        for char, icon in zip(
            set(quote.lower()).intersection("qwertyuiopasdfghjklzxcvbnm"),
            sample(icons, 26),
        )
    }
