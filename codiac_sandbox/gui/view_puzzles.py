import json
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from codiac_sandbox.gui.date_selector_widget import DateSelectorWidget
from codiac_sandbox.puzzle_types import CryptographBase
from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES, from_json

ALPHABET = set("qwertyuiopasdfghjklzxcvbnm ")


class PuzzleUI(QWidget):
    from PySide6.QtGui import QBrush, QColor

    def __init__(self) -> None:
        self._layout = QVBoxLayout()

        self.puzzle: CryptographBase | None = None
        self.quotes: list[dict[str, Any]]
        self.categories: set[str]
        self.get_quotes_and_categories()
        self.active_category = min(self.categories)
        self.search_for = ""

        self.build_lists()

        self.date_selector = DateSelectorWidget()
        self.date_selector.confirm_button.clicked.connect(self.save_puzzle)
        self.detail_view_layout.addWidget(self.date_selector)
        self._layout.addWidget(self.date_selector)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.category_combo)
        top_bar_layout.addWidget(self.search_bar)
        self._layout.addLayout(top_bar_layout)

        # Main content layout (quote list + detail view)
        self.main_content_layout = QHBoxLayout()
        self._layout.addLayout(self.main_content_layout)

        self.main_content_layout.addWidget(self.quotes_on_display)
        self.main_content_layout.addWidget(self.detail_scroll_area)

        self.display_quotes()

    def get_quotes_and_categories(self) -> None:
        with open("resources/master-puzzle-list.json") as f:
            json_data = json.load(f)
            self.quotes = json_data
            self.categories = {data["type"] for data in json_data}

    def set_category(self, category: str) -> None:
        self.active_category = category
        self.display_quotes()

    def set_search_for(self, text: str) -> None:
        self.search_for = text
        self.display_quotes()

    def build_lists(self) -> None:
        self.category_combo = QComboBox()
        self.category_combo.addItems(sorted(self.categories))
        self.category_combo.currentTextChanged.connect(self.set_category)
        self.category_combo.setMaximumWidth(200)

        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self.set_search_for)
        self.search_bar.setMaximumWidth(600)

        self.quotes_on_display = QListWidget()
        self.quotes_on_display.itemClicked.connect(self.display_quote_details)
        self.quotes_on_display.setFixedWidth(450)  # Set fixed width here

        # Container for labels in the detail view
        self.detail_view_container = QWidget()
        self.detail_view_layout = QVBoxLayout()
        self.detail_view_container.setLayout(self.detail_view_layout)
        self.detail_view_layout.setAlignment(Qt.AlignTop)  # type: ignore[attr-defined]

        # Wrap it in a scroll area
        self.detail_scroll_area = QScrollArea()
        self.detail_scroll_area.setWidgetResizable(True)
        self.detail_scroll_area.setWidget(self.detail_view_container)

    def display_quotes(self) -> None:
        def display_quote(quote: dict[str, Any]) -> bool:
            if not self.search_for:
                return quote["type"] == self.active_category and not quote["used"]
            lowercase_wiothout_punctuation = "".join(
                char for char in quote["string_to_encrypt"].lower() if char in ALPHABET
            )
            return self.search_for.lower() in lowercase_wiothout_punctuation

        self.get_quotes_and_categories()

        self.quotes_on_display.clear()
        for i, quote in enumerate(filter(display_quote, self.quotes)):
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

            self.quotes_on_display.addItem(item)
            self.quotes_on_display.setItemWidget(item, widget)

            item.setData(256, quote)

    def save_puzzle(self) -> None:
        if self.puzzle is None:
            return
        self.date_selector.confirm_date(self.puzzle)

    def display_quote_details(self, item: QListWidgetItem) -> None:
        # Clear previous widgets
        for i in reversed(range(self.detail_view_layout.count())):
            child = self.detail_view_layout.itemAt(i).widget()
            if child:
                child.deleteLater()

        puzzle_data: dict[str, Any] = item.data(256)
        self.puzzle = from_json(PUZZLE_CLASSES[puzzle_data.pop("type")], puzzle_data)

        for key, value in self.puzzle.to_json().items():
            if key in ["string_to_encrypt", "type"]:
                continue
            label = QLabel(f"<b>{key.replace('_', ' ').title()}:</b> {value}")
            label.setTextFormat(Qt.RichText)  # type: ignore[attr-defined]
            label.setWordWrap(True)
            self.detail_view_layout.addWidget(label)
