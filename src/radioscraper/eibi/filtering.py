from datetime import time, datetime

from radioscraper.eibi.model import Broadcast


def on_air(broadcast: Broadcast, air_time: time) -> Broadcast:
    filtered_broadcast = Broadcast()
    #TODO: dodelat zvlast filtraci pro dnesni(is_day_bridging = false), vcerejsi(is_day_bridging = true) a neregularni data
    for station in broadcast:
        if not station.is_day_bridging:
            if station.start_time <= air_time <= station.end_time:
                filtered_broadcast.append_station(station)
        else:
            if station.start_time >= air_time >= station.end_time:
                filtered_broadcast.append_station(station)
    return filtered_broadcast

def yesterday_broadcast(broadcast: Broadcast, today: datetime) -> Broadcast:
    raise NotImplementedError