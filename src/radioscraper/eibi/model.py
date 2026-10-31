from dataclasses import dataclass, Field
from datetime import time
from typing import List


@dataclass
class StationData:
    frequency: float | int
    start_time: time
    end_time: time
    regularity: List[int] | str
    station: str
    language: List[str] | None = None


class Broadcast:

    def __init__(self) -> None:
        self.broadcast_list: List[StationData] = []

    def __str__(self) -> str:
        return str(self.broadcast_list)

    def __len__(self) -> int:
        return len(self.broadcast_list)

    def __getitem__(self, index: int) -> StationData:
        return self.broadcast_list[index]

    def append_station(self, station: StationData) -> None:
        self.broadcast_list.append(station)

