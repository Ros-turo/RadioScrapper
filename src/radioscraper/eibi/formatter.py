from typing import List

from radioscraper.eibi.model import StationData, EVERY_DAY
from radioscraper.eibi.parser import Weekday


def format_regularity(station: StationData) -> str:
    match station.regularity:
        case list(station.regularity) as regularity:
            return format_list_regularity(regularity)
        case "irregular":
            return "irregular"
        case "Last7":
            return "Last Sunday"
        case _ :
            return ""

def format_list_regularity(regularity: List[int]) -> str:
    if set(regularity) == set(EVERY_DAY):
        return "Every day"
    return " ".join(Weekday(day).name for day in sorted(regularity))

def format_language(station: StationData) -> str:
    language = ""
    if isinstance(station.language, list):
        language = " ".join(station.language)
    return language