from datetime import datetime, timezone
from typing import TypeVar

from PySide6.QtCore import QModelIndex, Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from radioscraper.eibi.http_layer import station_stream_url
from radioscraper.eibi.model import Broadcast
from radioscraper.eibi.parser import language_json_to_dict
from radioscraper.ui.filter_proxy import BroadcastFilterProxyModel
from radioscraper.ui.table_model import BroadcastTableModel

W = TypeVar("W", bound=QWidget)


def named(widget: W, name: str) -> W:
    """Nastaví widgetu objectName (pro selektory #name v theme.qss) a vrátí ho."""
    widget.setObjectName(name)
    return widget


def filling_language_combo_box(combo_box: QComboBox) -> None:
    language_data = language_json_to_dict()
    combo_box.addItem("Any language", userData=None)
    for language in language_data.values():
        combo_box.addItem(language, userData=language)


class MainWindow(QMainWindow):
    def __init__(self, broadcast: Broadcast) -> None:
        super().__init__()
        self.broadcast = broadcast
        self._last_minute: datetime | None = None

        self.setWindowTitle("Radio Scraper")
        self.resize(1200, 760)

        self.setup_table()
        header = self.setup_header()
        filter_bar = self.setup_filter_bar()

        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(header)
        root.addWidget(filter_bar)
        root.addWidget(self.table, stretch=1)

        central = QWidget()
        central.setLayout(root)
        self.setCentralWidget(central)

        self.statusBar().showMessage("Ready")

        self.setup_timer()
        self.actualize_now()

    def setup_header(self) -> QWidget:
        header = named(QWidget(), "header")
        title = named(QLabel("Radio Scraper"), "appTitle")
        subtitle = named(QLabel("Shortwave schedule · EiBi"), "appSubtitle")
        self.clock_utc = named(QLabel(), "clockUtc")
        self.clock_local = named(QLabel(), "clockLocal")

        names = QVBoxLayout()
        names.setSpacing(2)
        names.addWidget(title)
        names.addWidget(subtitle)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(28, 16, 28, 16)
        layout.addLayout(names)
        layout.addStretch()
        layout.addWidget(named(QLabel("UTC"), "clockCaption"))
        layout.addWidget(self.clock_utc)
        layout.addSpacing(16)
        layout.addWidget(named(QLabel("LOCAL"), "clockCaption"))
        layout.addWidget(self.clock_local)
        return header

    def setup_filter_bar(self) -> QWidget:
        filter_bar = named(QWidget(), "filterBar")

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search station…")
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self.proxy.set_text)

        self.language = QComboBox()
        filling_language_combo_box(self.language)
        self.language.setCurrentIndex(0)
        self.language.setMinimumWidth(220)
        self.language.currentIndexChanged.connect(
            lambda _: self.proxy.set_language(self.language.currentData())
        )

        self.now_toggle = named(QPushButton("● ON AIR NOW"), "nowToggle")
        self.now_toggle.setCheckable(True)
        self.now_toggle.setChecked(True)
        self.now_toggle.toggled.connect(self.on_now_toggled)

        layout = QHBoxLayout(filter_bar)
        layout.setContentsMargins(28, 14, 28, 14)
        layout.setSpacing(12)
        layout.addWidget(self.search, stretch=1)
        layout.addWidget(self.language)
        layout.addWidget(self.now_toggle)
        return filter_bar

    def on_now_toggled(self, checked: bool) -> None:
        self.proxy.set_now(datetime.now(timezone.utc) if checked else None)

    def setup_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualize_now)
        self.timer.start(1_000)

    def actualize_now(self) -> None:
        now = datetime.now(timezone.utc)
        self.clock_utc.setText(f"{now:%H:%M}")
        self.clock_local.setText(f"{now.astimezone():%H:%M}")

        minute = now.replace(second=0, microsecond=0)
        if minute != self._last_minute:
            self._last_minute = minute
            if self.now_toggle.isChecked():
                self.proxy.set_now(now)

    def setup_table(self) -> None:
        self.table = QTableView()
        self.model = BroadcastTableModel(self.broadcast, self)
        self.proxy = BroadcastFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)

        self.table.setSortingEnabled(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table.setWordWrap(False)
        self.table.doubleClicked.connect(self.open_stream)

        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setResizeContentsPrecision(200)
        header.setStretchLastSection(False)
        for column in (0, 2, 3, 4):
            self.table.resizeColumnToContents(column)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def open_stream(self, proxy_index: QModelIndex) -> None:
        source_index = self.proxy.mapToSource(proxy_index)
        station = self.model.rows[source_index.row()]
        self.statusBar().showMessage(f"{station.frequency:g} kHz · {station.station}")
        url = station_stream_url(station.frequency)
        QDesktopServices.openUrl(QUrl(url))