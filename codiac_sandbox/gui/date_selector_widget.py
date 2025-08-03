from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QDateEdit,
    QPushButton,
    QLabel,
)
from PySide6.QtCore import QDate, Qt

from codiac_sandbox.puzzle_types import CryptographBase
from codiac_sandbox.selection.save_as_date import save_as_new_file


class DateSelectorWidget(QWidget):
    def __init__(self, puzzle: CryptographBase | None) -> None:
        super().__init__()
        self.puzzle = puzzle

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
        self.confirm_button.clicked.connect(self.confirm_date)
        controls_layout.addWidget(self.confirm_button)
        controls_layout.addWidget(self.date_edit)

        main_layout.addLayout(controls_layout)

        # Warning/message label below
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.message_label)

        self.setLayout(main_layout)
        self.setWindowTitle("Date Selector")

        self.on_date_changed(self.date_edit.date())

    def on_date_changed(self, selected_date: QDate) -> None:
        if selected_date.dayOfWeek() == 7:
            self.message_label.setStyleSheet("color: red;")
        else:
            self.message_label.setText("")

    def confirm_date(self) -> None:
        if self.puzzle is None:
            raise Exception("No puzzle selected!")
        save_as_new_file(puzzle=self.puzzle, date=self.date_edit.date())
