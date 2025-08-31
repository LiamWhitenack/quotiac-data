import json
import os

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QDateEdit,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from codiac_sandbox.puzzle_types import CryptographBase
from codiac_sandbox.selection.save_as_date import save_as_new_file

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
THEME = [
    "Fact",  # Monday
    "Historical",  # Tuesday
    "Wisdom",  # Wednesday
    "Riddle/Pun",  # Thursday
    "Wildcard",  # Friday
    "Literature/Film",  # Saturday
    "Religious",  # Sunday
]


class DateSelectorWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        main_layout = QVBoxLayout()

        # Horizontal layout for date edit and confirm button
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignLeft)  # type: ignore

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFixedWidth(100)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.on_date_changed)

        self.confirm_button = QPushButton("Save")
        self.confirm_button.setFixedWidth(100)
        controls_layout.addWidget(self.confirm_button)
        controls_layout.addWidget(self.date_edit)

        main_layout.addLayout(controls_layout)

        # Message list instead of a single label
        self.message_list = QListWidget()
        self.message_list.setMaximumHeight(100)
        main_layout.addWidget(self.message_list)

        self.setLayout(main_layout)
        self.setWindowTitle("Date Selector")

        self.on_date_changed(self.date_edit.date())

    def on_date_changed(self, selected_date: QDate) -> None:
        self.message_list.clear()  # Clear old messages if needed
        self.message_list.addItem(DAYS_OF_WEEK[selected_date.dayOfWeek() - 1])
        self.message_list.addItem(f"Theme: {THEME[selected_date.dayOfWeek() - 1]}")
        date_string = f"resources/by-date/{selected_date.year():04d}{selected_date.month():02d}{selected_date.day():02d}.json"
        if os.path.exists(date_string):
            with open(date_string) as f:
                self.message_list.addItem("Puzzle already chosen for that date!")
                self.message_list.addItem(json.load(f)["string_to_encrypt"])

    def confirm_date(self, puzzle: CryptographBase) -> None:
        save_as_new_file(puzzle=puzzle, date=self.date_edit.date())
        with open("resources/master-puzzle-list.json") as f:
            puzzles = json.load(f)
            puzzle_data = next(
                p for p in puzzles if p["string_to_encrypt"] == puzzle.string_to_encrypt
            )
            puzzle_data["used"] = True
        with open("resources/master-puzzle-list.json", "w") as f:
            json.dump(puzzles, f, indent=2)

        self.message_list.clear()
        self.message_list.addItem("Puzzle saved successfully.")
