from datetime import time, datetime, timedelta

from radioscraper.eibi.model import Broadcast


def on_air(broadcast: Broadcast, target_day: datetime) -> Broadcast:
    target_time = target_day.time()
    filtered_broadcast = Broadcast()
    #TODO: dodelat zvlast filtraci pro dnesni(is_day_bridging = false), vcerejsi(is_day_bridging = true) a neregularni data
    for station in broadcast:
        if not station.is_day_bridging:
            if station.start_time <= target_time <= station.end_time:
                filtered_broadcast.append_station(station)
        else:
            if station.start_time >= target_time >= station.end_time:
                filtered_broadcast.append_station(station)
    return filtered_broadcast

def yesterday_broadcast(origin_broadcast: Broadcast, target_day: datetime) -> Broadcast:
    yesterday_broadcast_instance = Broadcast()
    yesterday_weekday = (target_day - timedelta(days=1)).weekday()
    for station in origin_broadcast:
        if isinstance(station.regularity, list):
            if yesterday_weekday in station.regularity:
                yesterday_broadcast_instance.append_station(station)
    return yesterday_broadcast_instance