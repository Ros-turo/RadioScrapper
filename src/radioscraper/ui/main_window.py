from PySide6.QtCore import QModelIndex, QUrl, QTimer
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, \
    QComboBox, QTableView, QCheckBox, QHeaderView

from radioscraper.eibi.http_layer import station_stream_url
from radioscraper.eibi.model import Broadcast
from radioscraper.eibi.parser import language_json_to_dict
from radioscraper.ui.filter_proxy import BroadcastFilterProxyModel
from radioscraper.ui.table_model import BroadcastTableModel
from datetime import datetime, timezone


def filling_language_combo_box(combo_box: QComboBox) -> None:
    language_data = language_json_to_dict()
    combo_box.addItem("Any language", userData=None)
    for language in language_data.values():
        combo_box.addItem(language, userData=language)

class MainWindow(QMainWindow):
    def __init__(self, broadcast: Broadcast) -> None:
        super().__init__()
        self.broadcast = broadcast

        self.setWindowTitle("Radio Scraper")
        self.resize(1000, 600)

        self.setup_table()

        self.filters = QHBoxLayout()
        self.fill_filters_box()

        self.setup_clock()
        self.setup_timer()

        self.root = QVBoxLayout()
        self.root.addLayout(self.filters)
        self.root.addWidget(self.table, stretch=1)

        central = QWidget()
        central.setLayout(self.root)
        self.setCentralWidget(central)

        self.statusBar().showMessage(f"Ready")


    def fill_filters_box(self) -> None:
        self.set_station_searcher()
        self.set_language_combo_box()
        self.set_now_check_box()
        self.add_widgets_to_filters_box()

    def set_station_searcher(self) -> None:
        self.search = QLineEdit(placeholderText="Station")
        self.search.textChanged.connect(self.proxy.set_text)

    def set_language_combo_box(self) -> None:
        self.language = QComboBox(placeholderText="Language")
        filling_language_combo_box(self.language)
        self.language.currentIndexChanged.connect(
            lambda _: self.proxy.set_language(self.language.currentData())
        )

    def set_now_check_box(self) -> None:
        self.now_check_box = QCheckBox("NOW")
        self.now_check_box.toggled.connect(self.on_now_toggled)

    def on_now_toggled(self, checked: bool) -> None:
        set = datetime.now(timezone.utc) if checked else None
        self.proxy.set_now(set)

    def add_widgets_to_filters_box(self) -> None:
        self.filters.addWidget(QLabel("Station: "))
        self.filters.addWidget(self.search, stretch=1)
        self.filters.addWidget(QLabel("Language: "))
        self.filters.addWidget(self.language, stretch=1)
        self.filters.addWidget(self.now_check_box)

    def setup_clock(self) -> None:
        self.clock = QLabel()
        self.statusBar().addPermanentWidget(self.clock)

    def setup_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualize_now)
        self.timer.start(1_000)

    def actualize_now(self) -> None:
        #TODO: nechat clock kazdou vterinu ale proxy jednou za minutu
        now = datetime.now(timezone.utc)
        self.clock.setText(f" UTC {now.strftime('%H:%M')} · Local {now.astimezone().strftime('%H:%M')}")
        if self.now_check_box.isChecked():
            self.proxy.set_now(now)


    def setup_table(self) -> None:
        self.table = QTableView()
        self.model = BroadcastTableModel(self.broadcast, self)
        self.proxy = BroadcastFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.doubleClicked.connect(self.open_stream)
        self.table.setColumnWidth(0, 75)

        self.table.resizeColumnToContents(1)
        self.table.resizeColumnToContents(4)

        self.table.horizontalHeader().setStretchLastSection(True)

    def open_stream(self, proxy_index: QModelIndex) -> None:
        source_index = self.proxy.mapToSource(proxy_index)
        station = self.model.rows[source_index.row()]
        self.statusBar().showMessage(f"{station.frequency} | {station.station}")
        url = station_stream_url(station.frequency)
        QDesktopServices.openUrl(QUrl(url))
