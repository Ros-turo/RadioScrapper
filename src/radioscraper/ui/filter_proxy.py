from typing import cast

from PySide6.QtCore import QSortFilterProxyModel, QModelIndex, QPersistentModelIndex, QObject

from radioscraper.eibi.matching import match_station_name
from radioscraper.ui.table_model import BroadcastTableModel


class BroadcastFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent : QObject | None=None) -> None:
        super().__init__(parent)
        self._text = ""

    def set_text(self, text: str) -> None:
        self._text = text
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex | QPersistentModelIndex) -> bool:
        model = cast(BroadcastTableModel, self.sourceModel())
        station = model.rows[source_row]
        return match_station_name(station, self._text)