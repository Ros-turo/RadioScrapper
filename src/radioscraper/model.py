from dataclasses import dataclass

@dataclass
class StationData:
    pass


class Broadcast:

    def __init__(self) -> None:
        self.broadcast_list = []

    def append_station(self, station: StationData) -> None:
        self.broadcast_list.append(station)

