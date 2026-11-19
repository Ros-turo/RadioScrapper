from datetime import datetime, timedelta, time
from typing import List, Literal

from radioscraper.eibi.model import StationData


def match_station_name(station_data: StationData, matching_name: str) -> bool:
    if not matching_name:
        return True
    return matching_name.casefold() in station_data.station.casefold()

def match_language(station_data: StationData, matching_language: str) -> bool:
    if not matching_language:
        return True
    elif station_data.language is None:
        return False
    for language in station_data.language:
        if matching_language.casefold() in language.casefold():
            return True
    return False

def is_target_day_in_regularity(regularity: List[int], target_day: datetime) -> bool:
    weekday = target_day.weekday()
    return weekday in regularity

def is_today_station_on_air(regularity: List[int], station_data: StationData, today: datetime) -> bool:
    air_time = today.time()
    if is_target_day_in_regularity(regularity, today):
        if station_data.start_time <= air_time and (station_data.is_day_bridging or air_time <= station_data.end_time):
            return True
    return False

def is_yesterday_station_on_air(regularity: List[int], station_data: StationData, yesterday: datetime) -> bool:
    air_time = yesterday.time()
    if is_target_day_in_regularity(regularity, yesterday) and station_data.is_day_bridging:
        if air_time <= station_data.end_time:
            return True
    return False


def is_irregular_station_on_air(station_data: StationData, air_time: time) -> bool:
    if station_data.is_day_bridging:
        return station_data.start_time <= air_time or air_time <= station_data.end_time
    else:
        return station_data.start_time <= air_time <= station_data.end_time

def is_on_air(station_data: StationData, target_day: datetime) -> bool:
    regularity = station_data.regularity
    air_time = target_day.time()
    on_air = False
    if isinstance(regularity, list):
        today = target_day
        yesterday = target_day - timedelta(days=1)
        if (is_today_station_on_air(regularity, station_data, today) or
            is_yesterday_station_on_air(regularity, station_data,  yesterday)):
           on_air = True
    else:
        match regularity:
            case "irregular":
                on_air = is_irregular_station_on_air(station_data, air_time)
            case "Last7":
                #TODO: udelat rozvrh na Last7
                on_air = False

    return on_air