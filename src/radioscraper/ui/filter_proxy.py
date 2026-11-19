from datetime import datetime
from typing import cast

from PySide6.QtCore import QSortFilterProxyModel, QModelIndex, QPersistentModelIndex, QObject

from radioscraper.eibi.matching import match_station_name, match_language, is_on_air
from radioscraper.ui.table_model import BroadcastTableModel


class BroadcastFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent : QObject | None=None) -> None:
        super().__init__(parent)
        self._text = ""
        self._language: str  = ""
        self._now: datetime | None = None

    def set_text(self, text: str) -> None:
        self._text = text
        self.invalidateFilter()

    def set_language(self, language: str) -> None:
        self._language = language
        self.invalidateFilter()

    def set_now(self, now: datetime | None) -> None:
        self._now = now
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex | QPersistentModelIndex) -> bool:
        model = cast(BroadcastTableModel, self.sourceModel())
        station = model.rows[source_row]
        return match_station_name(station, self._text) and match_language(station, self._language) and (self._now is None or is_on_air(station, self._now))