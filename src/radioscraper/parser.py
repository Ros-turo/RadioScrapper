from datetime import datetime
import os
from abc import ABC, abstractmethod

from radioscraper.model import Broadcast, StationData


class Parser(ABC):

    def __init__(self, fn: str):
        self.fn = self._is_file_exists(fn)

    def _is_file_exists(self, fn: str) -> str:
        if os.path.isfile(fn):
            return fn
        raise FileNotFoundError(fn)

    @abstractmethod
    def parse_file(self) -> Broadcast: ...

    @abstractmethod
    def parse_row(self, row) -> StationData: ...

    @abstractmethod
    def get_time(self, time_row: str) -> tuple[datetime, datetime]: ...

    @abstractmethod
    def get_station(self, station_row: str) -> str: ...

    @abstractmethod
    def get_language(self, language_row: str) -> str: ...

    @abstractmethod
    def get_frequency(self, frequency_row: str) -> float | int: ...

    @abstractmethod
    def get_regularity(self, days_row: str) -> str: ...
