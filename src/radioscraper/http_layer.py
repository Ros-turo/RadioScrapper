import requests
from requests import Request

from radioscraper.exceptions import InvalidURL
from radioscraper.settings import settings

class StationAPI:

    def __init__(self, url:str = settings.STATION_DB_URL) -> None:
        self.station_url = self._valid_url(url)

    def get_data(self) -> None:
        response = requests.get(self.station_url)
        response.raise_for_status()
        self._save_data(response.content)


    def _save_data(self, data: bytes) -> None:
        with open("stations.csv", "wb") as f:
            f.write(data)


    def _valid_url(self, url: str) -> str:
        try:
            requests.Session().prepare_request(Request(url=url, method="GET"))
        except requests.exceptions.MissingSchema:
            raise InvalidURL(url=url)
        return url