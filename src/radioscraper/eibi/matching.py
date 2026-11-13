from radioscraper.eibi.model import StationData


def match_station_name(station_data: StationData, matching_name: str) -> bool:
    return station_data.station.casefold() == matching_name.casefold()