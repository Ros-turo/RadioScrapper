from dataclasses import dataclass, Field
from datetime import time
from typing import List, Literal, Iterator, Self, Generator


@dataclass
class StationData:
    frequency: float | int
    start_time: time
    end_time: time
    regularity: List[int] | Literal["irregular"] | Literal["Last7"]
    station: str
    language: List[str] | None = None

    @property
    def is_day_bridging(self) -> bool:
        return True if self.start_time > self.end_time else False

    def get_attribute(self, attribute: str) -> str | None:
        try:
            value = self.__getattribute__(attribute)
        except KeyError:
            return None
        else:
            return str(value)



class Broadcast:

    def __init__(self) -> None:
        self.broadcast_list: List[StationData] = []

    def __str__(self) -> str:
        return str(self.broadcast_list)

    def __len__(self) -> int:
        return len(self.broadcast_list)

    def __add__(self, other: object) -> 'Broadcast':
        if isinstance(other, Broadcast):
            broadcast = Broadcast()
            broadcast.broadcast_list = self.broadcast_list + other.broadcast_list
            return broadcast
        return NotImplemented

    def __getitem__(self, index: int) -> StationData:
        return self.broadcast_list[index]

    def __iter__(self) -> Generator[StationData, None, None]:
        for station in self.broadcast_list:
            yield station

    def append_station(self, station: StationData) -> None:
        self.broadcast_list.append(station)

    def remove_station(self, station: StationData) -> None:
        self.broadcast_list.remove(station)