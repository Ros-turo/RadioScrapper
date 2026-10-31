
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QPersistentModelIndex, QObject

from radioscraper.eibi.model import Broadcast


class BroadcastTableModel(QAbstractTableModel):

    COLUMNS = ["Frequency", "Station", "Start", "End", "Days", "Language"]

    def __init__(self, rows: Broadcast, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.rows = rows

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return len(self.rows)

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex  = QModelIndex()) -> int:
        return len(self.COLUMNS)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> str | float | None:
        if role == Qt.ItemDataRole.DisplayRole:
            station = self.rows[index.row()]
            match index.column():
                case 0:
                    return station.frequency
                case 1:
                    return station.station
                case 2:
                    return station.start_time.strftime('%H:%M')
                case 3:
                    return station.end_time.strftime('%H:%M')
                case 4:
                    if isinstance(station.regularity, str):
                        return station.regularity
                    else:
                        return "".join(map(str, station.regularity))
                case 5:
                    if isinstance(station.regularity, str):
                        return station.regularity
                    else:
                        return "".join(map(str, station.regularity))
        return None
