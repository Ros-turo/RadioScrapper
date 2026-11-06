from datetime import time

from radioscraper.eibi.model import Broadcast


def on_air(broadcast: Broadcast, air_time: time) -> Broadcast:
    filtered_broadcast = Broadcast()
    for station in broadcast:
        if not station.is_day_bridging:
            if station.start_time <= air_time <= station.end_time:
                filtered_broadcast.append_station(station)
        else:
            if station.start_time >= air_time >= station.end_time:
                filtered_broadcast.append_station(station)
    return filtered_broadcast