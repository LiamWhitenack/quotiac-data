from collections.abc import Callable
from typing import Any
from PySide6.QtWidgets import (
    QVBoxLayout,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QWidget,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtWidgets import QScrollArea
from PySide6.QtGui import QColor, QBrush

from PySide6.QtCore import Qt
import json

from codiac_sandbox.gui.date_selector_widget import DateSelectorWidget
from codiac_sandbox.puzzle_types import CryptographBase
from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES, from_json


class PuzzleUI(QWidget):
    def __init__(self, serve: Callable[[dict[str, Any]], None]) -> None:
        self._layout = QVBoxLayout()
        self.serve = serve

        self.puzzle: CryptographBase | None = None

        self.load_quotes()
        self.build_lists()

        self._layout.addWidget(self.category_combo)

        # Main content layout (quote list + detail view)
        self.main_content_layout = QHBoxLayout()
        self._layout.addLayout(self.main_content_layout)

        self.main_content_layout.addWidget(self.quote_list)
        self.main_content_layout.addWidget(self.detail_scroll_area)

        self.display_quotes(list(self.quotes_by_category)[0])

    def load_quotes(self) -> None:
        with open("resources/master-puzzle-list.json") as f:
            self.quotes_by_category: dict[str, list[dict[str, Any]]] = {}
            for q in json.load(f):
                self.quotes_by_category[q["type"]] = self.quotes_by_category.get(
                    q["type"], []
                ) + [q]
        self.quotes_by_category = {
            k: v for k, v in sorted(self.quotes_by_category.items())
        }

    def build_lists(self) -> None:
        self.category_combo = QComboBox()
        self.category_combo.addItems(list(self.quotes_by_category))
        self.category_combo.currentTextChanged.connect(self.display_quotes)
        self.category_combo.setMaximumWidth(200)

        self.quote_list = QListWidget()
        self.quote_list.itemClicked.connect(self.display_quote_details)
        self.quote_list.setFixedWidth(450)  # Set fixed width here

        # Container for labels in the detail view
        self.detail_view_container = QWidget()
        self.detail_view_layout = QVBoxLayout()
        self.detail_view_container.setLayout(self.detail_view_layout)
        self.detail_view_layout.setAlignment(Qt.AlignTop)  # type: ignore[attr-defined]

        # Wrap it in a scroll area
        self.detail_scroll_area = QScrollArea()
        self.detail_scroll_area.setWidgetResizable(True)
        self.detail_scroll_area.setWidget(self.detail_view_container)

    from PySide6.QtGui import QColor, QBrush

    def display_quotes(self, category: str) -> None:
        self.quote_list.clear()
        for i, quote in enumerate(self.quotes_by_category[category]):
            text = quote["string_to_encrypt"]

            label = QLabel(text)
            label.setWordWrap(True)
            label.setStyleSheet("padding: 4px;")
            label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)  # type: ignore[attr-defined]
            label.setFixedWidth(280)
            label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # type: ignore[attr-defined]

            h_layout = QHBoxLayout()
            h_layout.setAlignment(Qt.AlignLeft)  # type: ignore[attr-defined]
            h_layout.addWidget(label)
            h_layout.setContentsMargins(0, 0, 0, 0)
            h_layout.setSpacing(6)

            widget = QWidget()
            widget.setLayout(h_layout)

            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())

            # Set background tint on the QListWidgetItem, not the widget
            if i % 2 == 1:
                item.setBackground(
                    QBrush(QColor("#725656"))
                )  # Light gray for alternating rows

            self.quote_list.addItem(item)
            self.quote_list.setItemWidget(item, widget)

            item.setData(256, quote)

    def display_quote_details(self, item: QListWidgetItem) -> None:
        # Clear previous widgets
        for i in reversed(range(self.detail_view_layout.count())):
            child = self.detail_view_layout.itemAt(i).widget()
            if child:
                child.deleteLater()

        puzzle_data: dict[str, Any] = item.data(256)
        self.puzzle = from_json(PUZZLE_CLASSES[puzzle_data.pop("type")], puzzle_data)

        # Create a new date selector fresh for this puzzle
        self.date_selector = DateSelectorWidget(self.puzzle, self.serve)
        self.detail_view_layout.addWidget(self.date_selector)

        for key, value in self.puzzle.to_json().items():
            if key in ["string_to_encrypt", "type"]:
                continue
            label = QLabel(f"<b>{key.replace('_', ' ').title()}:</b> {value}")
            label.setTextFormat(Qt.RichText)  # type: ignore[attr-defined]
            label.setWordWrap(True)
            self.detail_view_layout.addWidget(label)
