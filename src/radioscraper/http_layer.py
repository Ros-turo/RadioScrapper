import requests

from radioscraper.settings import settings

class StationAPI:

    def __init__(self) -> None:
        self.station_url = settings.STATION_DB_URL

    def get_data(self) -> None:
        response = requests.get(self.station_url)
        response.raise_for_status()
        self._save_data(response.content)


    def _save_data(self, data: bytes) -> None:
        with open("stations.csv", "wb") as f:
            f.write(data)