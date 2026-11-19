from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, \
    QComboBox, QTableView, QCheckBox

from radioscraper.eibi.model import Broadcast
from radioscraper.eibi.parser import language_json_to_dict
from radioscraper.ui.filter_proxy import BroadcastFilterProxyModel
from radioscraper.ui.table_model import BroadcastTableModel
from datetime import datetime, timezone


def filling_language_combo_box(combo_box: QComboBox) -> None:
    language_data = language_json_to_dict()
    for language in language_data.values():
        combo_box.addItem(language)

class MainWindow(QMainWindow):
    def __init__(self, broadcast: Broadcast) -> None:
        super().__init__()
        self.setWindowTitle("Radio Scraper")
        self.resize(1000, 600)

        self.table = QTableView()
        self.model = BroadcastTableModel(broadcast, self)
        self.proxy = BroadcastFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)

        self.filters = QHBoxLayout()
        self.fill_filters_box()

        self.root = QVBoxLayout()
        self.root.addLayout(self.filters)
        self.root.addWidget(self.table, stretch=1)

        central = QWidget()
        central.setLayout(self.root)
        self.setCentralWidget(central)

        self.statusBar().showMessage("Ready")

    def fill_filters_box(self) -> None:
        self.set_station_searcher()
        self.set_language_combo_box()
        self.set_now_check_box()
        self.add_widgets_to_filters_box()

    def add_widgets_to_filters_box(self) -> None:
        self.filters.addWidget(QLabel("Station: "))
        self.filters.addWidget(self.search, stretch=1)
        self.filters.addWidget(QLabel("Language: "))
        self.filters.addWidget(self.language, stretch=1)
        self.filters.addWidget(self.now_check_box)

    def set_station_searcher(self) -> None:
        self.search = QLineEdit(placeholderText="Station")
        self.search.textChanged.connect(self.proxy.set_text)

    def set_language_combo_box(self) -> None:
        self.language = QComboBox(placeholderText="Language")
        filling_language_combo_box(self.language)
        self.language.currentTextChanged.connect(self.proxy.set_language)

    def set_now_check_box(self) -> None:
        self.now_check_box = QCheckBox("NOW")
        self.now_check_box.setChecked(True)
        self.now_check_box.toggled.connect(self.on_now_toggled)

    def on_now_toggled(self, checked: bool) -> None:
        set = datetime.now(timezone.utc) if checked else None
        self.proxy.set_now(set)
