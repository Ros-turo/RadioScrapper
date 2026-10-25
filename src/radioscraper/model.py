from dataclasses import dataclass
from datetime import time

@dataclass
class StationData:
    frequency: float | int | None = None
    start_time: time | None = None
    end_time: time | None = None
    regularity: list[int] | str | None = None
    station: str | None = None
    language: str | None = None


class Broadcast:

    def __init__(self) -> None:
        self.broadcast_list = []

    def __str__(self) -> str:
        return str(self.broadcast_list)

    def append_station(self, station: StationData) -> None:
        self.broadcast_list.append(station)

