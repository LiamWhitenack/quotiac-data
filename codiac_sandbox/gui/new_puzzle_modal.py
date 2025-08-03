import inspect

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QPushButton,
    QWidget,
)

from codiac_sandbox.crud.create import get_puzzle_parameters, save_puzzle
from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES
from PySide6.QtWidgets import QSizePolicy


class AddPuzzleDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Puzzle")
        self.setMinimumWidth(450)

        self._layout = QVBoxLayout(self)

        self.type_selector = QComboBox()
        self.type_selector.addItems(PUZZLE_CLASSES.keys())  # type: ignore
        self._layout.addWidget(QLabel("Select Puzzle Type"))
        self._layout.addWidget(self.type_selector)

        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)

        # Set form widget size policy to expand horizontally, fixed vertically
        self.form_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # type: ignore

        self._layout.addWidget(self.form_widget)

        # Add stretch below to push all widgets to top
        self._layout.addStretch(1)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.save_puzzle)
        self._layout.addWidget(self.submit_button)

        self.type_selector.currentTextChanged.connect(self.update_form)

        self.update_form(self.type_selector.currentText())

    def update_form(self, puzzle_type: str):
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if widget := item.widget():
                widget.setParent(None)

        self.fields: dict[str, QLineEdit | QTextEdit] = {}

        for name, param in get_puzzle_parameters(puzzle_type).items():  # type: ignore
            if name == "used":
                continue
            field: QLineEdit = QLineEdit()
            if name in ["quote", "lyrics", "question", "phrase"]:
                field.setFixedHeight(300)
            field.setFixedWidth(300)

            # Make fields stretch horizontally
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # type: ignore[attr-defined]

            placeholder = (
                str(param.annotation)
                if param.annotation != inspect.Parameter.empty
                else ""
            )
            if param.default != inspect.Parameter.empty:
                placeholder += f" (default: {param.default})"
            field.setPlaceholderText(placeholder.strip())
            self.fields[name] = field
            self.form_layout.addRow(QLabel(name), field)

    def save_puzzle(self) -> None:
        save_puzzle(
            PUZZLE_CLASSES[self.type_selector.currentText()],
            {k: v.text() for k, v in self.fields.items()},  # type: ignore
        )
        self.update_form(self.type_selector.currentText())
