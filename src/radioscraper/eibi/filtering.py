from datetime import time, datetime, timedelta

from radioscraper.eibi.model import Broadcast, StationData


def on_air_without_bridging(broadcast: Broadcast, target_time: time) -> Broadcast:
    on_air_broadcast = Broadcast()
    for station in broadcast:
        if station.start_time <= target_time <= station.end_time:
            on_air_broadcast.append_station(station)
    return on_air_broadcast

def on_air_irregular(station: StationData, target_time:time) -> bool:
    if station.regularity == "irregular":
        match station.is_day_bridging:
            case True:
                return True if station.start_time >= target_time <= station.end_time else False
            case False:
                return True if station.start_time <= target_time <= station.end_time else False
    raise NotImplementedError

def target_day_broadcast(origin_broadcast: Broadcast, target_day: datetime) -> Broadcast:
    target_dat_broadcast_instance = Broadcast()
    target_day_weekday = target_day.weekday()
    for station in origin_broadcast:
        if (isinstance(station.regularity, list)) and (target_day_weekday in station.regularity):
            target_dat_broadcast_instance.append_station(station)
    return target_dat_broadcast_instance

def today_broadcast_on_air(origin_broadcast: Broadcast, today: datetime) -> Broadcast:
    now = today.time()
    today_broadcast_list = target_day_broadcast(origin_broadcast, today)
    on_air_broadcast = on_air_without_bridging(today_broadcast_list, now)
    return on_air_broadcast


def yesterday_broadcast_on_air(origin_broadcast: Broadcast, yesterday: datetime) -> Broadcast:
    yesterday_on_air_broadcast = Broadcast()
    air_time = yesterday.time()
    yesterday_broadcast_list = target_day_broadcast(origin_broadcast, yesterday)
    for station in yesterday_broadcast_list:
        if air_time <= station.end_time:
            yesterday_on_air_broadcast.append_station(station)
    return yesterday_on_air_broadcast


def get_irregular_broadcast(origin_broadcast: Broadcast) -> Broadcast:
    irregular_broadcast_instance = Broadcast()
    for station in origin_broadcast:
        if station.regularity == "irregular":
            irregular_broadcast_instance.append_station(station)
    return irregular_broadcast_instance

def irregular_broadcast_on_air(origin_broadcast: Broadcast, target_time: time) -> Broadcast:
    on_air = Broadcast()
    irregular_broadcast = get_irregular_broadcast(origin_broadcast)
    for station in irregular_broadcast:
        if on_air_irregular(station, target_time):
            on_air.append_station(station)
    return on_air



# def on_air(broadcast: Broadcast, target_day: datetime, return_irregularity: bool = True) -> Broadcast:
#     today_on_air = today_broadcast_on_air(broadcast, target_day)
#     #TODO: vcerejsi
#     #TODO: neregularni data