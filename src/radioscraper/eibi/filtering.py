from datetime import time, datetime, timedelta

from radioscraper.eibi.model import Broadcast


# def on_air(broadcast: Broadcast, target_day: datetime, return_irregularity: bool = True) -> Broadcast:
#     #TODO: filtraci pro dnesni,
#     #TODO: vcerejsi
#     #TODO: neregularni data


def today_broadcast(origin_broadcast: Broadcast, target_day: datetime) -> Broadcast:
    today_broadcast_instance = Broadcast()
    today_weekday = target_day.weekday()
    for station in origin_broadcast:
        if (isinstance(station.regularity, list)) and (today_weekday in station.regularity):
            today_broadcast_instance.append_station(station)
    return today_broadcast_instance

def yesterday_broadcast(origin_broadcast: Broadcast, target_day: datetime) -> Broadcast:
    yesterday_broadcast_instance = Broadcast()
    yesterday_weekday = (target_day - timedelta(days=1)).weekday()
    for station in origin_broadcast:
        if isinstance(station.regularity, list):
            if yesterday_weekday in station.regularity:
                yesterday_broadcast_instance.append_station(station)
    return yesterday_broadcast_instance