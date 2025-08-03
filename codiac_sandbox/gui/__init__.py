from collections.abc import Callable
from typing import Any
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from codiac_sandbox.gui.new_puzzle_modal import AddPuzzleDialog
from codiac_sandbox.gui.view_puzzles import PuzzleUI


class MainWindow(QWidget):
    def __init__(self, serve: Callable[[dict[str, Any]], None]) -> None:
        super().__init__()
        self.setWindowTitle("Quotes by Category")
        self.setGeometry(250, 250, 1000, 500)

        main_layout = QVBoxLayout()

        # Top controls
        self.add_puzzle_button = QPushButton("Add Puzzle")
        self.add_puzzle_button.clicked.connect(self.open_add_puzzle_dialog)

        top_controls_layout = QHBoxLayout()
        top_controls_layout.addWidget(self.add_puzzle_button)
        main_layout.addLayout(top_controls_layout)

        # Puzzle UI
        self.puzzle_ui = PuzzleUI(serve=serve)
        main_layout.addLayout(self.puzzle_ui._layout)  # type: ignore

        self.setLayout(main_layout)

    def open_add_puzzle_dialog(self) -> None:
        AddPuzzleDialog().exec()
