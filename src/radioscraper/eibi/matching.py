from radioscraper.eibi.model import StationData


def match_station_name(station_data: StationData, matching_name: str) -> bool:
    if not matching_name:
        return True
    return matching_name.casefold() in station_data.station.casefold()