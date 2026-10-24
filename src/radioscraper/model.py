from dataclasses import dataclass
from datetime import datetime


@dataclass
class StationData:
    frequency: float | int | None = None
    start: datetime | None = None
    end: datetime | None = None
    regularity: int | None = None
    station: str | None = None
    language: str | None = None


class Broadcast:

    def __init__(self) -> None:
        self.broadcast_list = []

    def append_station(self, station: StationData) -> None:
        self.broadcast_list.append(station)

