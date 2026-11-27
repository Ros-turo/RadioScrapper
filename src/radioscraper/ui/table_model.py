from typing import Callable, List, Any

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QPersistentModelIndex, QObject
from PySide6.QtGui import QColor, QFont

from radioscraper.eibi.model import Broadcast, StationData
from radioscraper.eibi.formatter import format_regularity, format_language


class BroadcastTableModel(QAbstractTableModel):

    COLUMNS: list[tuple[str, Callable[[StationData], str | float]]] = [
        ("kHz", lambda s: s.frequency),
        ("Station", lambda s: s.station),
        ("Time", lambda s: f"{s.start_time.strftime("%H:%M")}-{s.end_time.strftime("%H:%M")}"),
        ("Days", lambda s: format_regularity(s)),
        ("Language", lambda s: format_language(s))
    ]

    def __init__(self, rows: Broadcast, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.rows = rows
        self.setup_font()


    def setup_font(self) -> None:
        self.mono = QFont()
        self.mono.setFamilies(["IBM Plex Mono", "DejaVu Sans Mono", "monospace"])
        self.mono.setStyleHint(QFont.StyleHint.Monospace)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.rows)

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex  = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.COLUMNS)

    def headerData(
            self,
            section: int,
            orientation: Qt.Orientation,
            role: int = Qt.ItemDataRole.DisplayRole
    ) -> str | None:

        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section][0]
        return None


    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> str | float | None | QColor | QFont:
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            station = self.rows[index.row()]
            getter = self.COLUMNS[index.column()][1]
            return getter(station)
        if role == Qt.ItemDataRole.ForegroundRole:
            station = self.rows[index.row()]
            if station.regularity == "irregular":
                return QColor("#8C877C")  # ztlumené nepravidelné
            if index.column() == 0:
                return QColor("#F2A93B")  # jantarová frekvence
        if role == Qt.ItemDataRole.FontRole and index.column() in (0, 2):
            return self.mono  # frekvence a čas monospace
        return None
