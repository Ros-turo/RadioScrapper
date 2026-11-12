from typing import Callable, List, Any

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QPersistentModelIndex, QObject
from PySide6.QtGui import QColor

from radioscraper.eibi.model import Broadcast, StationData
from radioscraper.eibi.formatter import format_regularity, format_language


class BroadcastTableModel(QAbstractTableModel):

    COLUMNS: list[tuple[str, Callable[[StationData], str | float]]] = [
        ("kHz", lambda s: s.frequency),
        ("Station", lambda s: s.station),
        ("Time", lambda s: f"{s.start_time.strftime("%H:%M")} - {s.end_time.strftime("%H:%M")}"),
        ("Days", lambda s: format_regularity(s)),
        ("Language", lambda s: format_language(s))
    ]

    def __init__(self, rows: Broadcast, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.rows = rows

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


    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> str | float | None:
        index.isValid()
        if role == Qt.ItemDataRole.DisplayRole:
            station = self.rows[index.row()]
            getter = self.COLUMNS[index.column()][1]
            return getter(station)
        if role == Qt.ItemDataRole.ToolTipRole:
            return "hello"
        return None
