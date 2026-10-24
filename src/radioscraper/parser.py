import csv
from datetime import datetime, time
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
    def get_time(self, time_row: str) -> tuple[time, time]: ...
    #
    # @abstractmethod
    # def get_station(self, station_row: str) -> str: ...
    #
    # @abstractmethod
    # def get_language(self, language_row: str) -> str: ...
    #
    # @abstractmethod
    # def get_frequency(self, frequency_row: str) -> float | int: ...
    #
    # @abstractmethod
    # def get_regularity(self, days_row: str) -> str: ...


class EibiParser(Parser):

    def parse_file(self) -> Broadcast:
        broadcast = Broadcast()
        with open(self.fn) as file:
            reader = csv.reader(file, delimiter=';')
            reader.__next__()
            for row in reader:
                station_data = self.parse_row(row)
                broadcast.append_station(station_data)

        return broadcast

    def parse_row(self, row: list) -> StationData:
        frequency = row[0]
        start_time, end_time = self.get_time(row[1])
        return StationData()

    def get_time(self, time_row: str) -> tuple[time, time]:
        start_time, end_time = time_row.split('-')

        start_time = time(int(start_time[:2]), int(start_time[2:]))

        if end_time[:2] == "24":
            end_time = "2359"
        end_time = time(int(end_time[:2]), int(end_time[2:]))

        return start_time, end_time