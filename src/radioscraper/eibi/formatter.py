from radioscraper.eibi.model import StationData


def format_regularity(station: StationData) -> str:
    days = ""
    if isinstance(station.regularity, list):
        for day in station.regularity:
            days += str(day)
    elif isinstance(station.regularity, str):
        days = station.regularity
    return days

def format_language(station: StationData) -> str:
    language = ""
    if isinstance(station.language, list):
        language = " ".join(station.language)
    return language