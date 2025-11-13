import inspect

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from quotiac_sandbox.crud.create import get_puzzle_parameters, save_puzzle
from quotiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES


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
        # Clear previous form
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if widget := item.widget():
                widget.setParent(None)

        self.fields: dict[str, QLineEdit | QTextEdit | list[QLineEdit]] = {}

        for name, param in get_puzzle_parameters(puzzle_type).items():  # type: ignore
            if name == "used":
                continue

            # Handle List/Set types with dynamic entry fields
            if puzzle_type in {"List", "Set"} and param.annotation in (
                list[str],
                set[str],
            ):
                container = QWidget()
                v_layout = QVBoxLayout(container)
                v_layout.setContentsMargins(0, 0, 0, 0)
                v_layout.setSpacing(4)

                entries: list[QLineEdit] = []

                def add_entry():
                    entry = QLineEdit()
                    entry.setPlaceholderText("str")
                    entry.setFixedWidth(300)
                    entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                    v_layout.insertWidget(v_layout.count() - 1, entry)
                    entries.append(entry)

                add_button = QPushButton("Add Item")
                add_button.clicked.connect(add_entry)

                # Start with one entry field
                add_entry()
                v_layout.addWidget(add_button)

                self.fields[name] = entries
                self.form_layout.addRow(QLabel(name), container)
                continue

            # Regular single-line or multi-line field
            field: QLineEdit | QTextEdit
            if name in ["quote", "lyrics", "question", "phrase"]:
                field = QTextEdit()
                field.setFixedHeight(300)
            else:
                field = QLineEdit()

            field.setFixedWidth(300)
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

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
        puzzle_type = self.type_selector.currentText()

        # Convert all field values properly
        data: dict[str, str | list[str]] = {}
        for key, value in self.fields.items():
            if isinstance(value, list):  # for List/Set types
                data[key] = [v.text() for v in value if v.text().strip()]
            elif hasattr(value, "toPlainText"):  # QTextEdit
                data[key] = value.toPlainText()
            else:  # QLineEdit
                data[key] = value.text()

        save_puzzle(PUZZLE_CLASSES[puzzle_type], data)
        self.update_form(puzzle_type)
