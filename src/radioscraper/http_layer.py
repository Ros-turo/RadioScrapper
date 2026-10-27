import requests
from abc import ABC, abstractmethod
from radioscraper.settings import settings


class StationAPI(ABC):
    
    @abstractmethod
    def get_station_data(self) -> bytes | str: ...

    @abstractmethod
    def write_data_to_csv(self, fn: str, data: bytes | str) -> None: ...
    
    
class EibiAPI(StationAPI):
    
    def __init__(self) -> None:
        self.station_url = settings.EIBI_URL
        self.readme_url = settings.EIBI_README

    def get_station_data(self) -> bytes:
        response = requests.get(self.station_url)
        response.raise_for_status()
        return response.content

    def get_readme_data(self) -> str:
        response = requests.get(self.readme_url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def bytes_to_str(data: bytes) -> str:
        return data.decode("latin-1")

    def write_data_to_csv(self, fn: str, data: bytes | str) -> None:
        if isinstance(data, bytes):
            data = self.bytes_to_str(data)
        with open(fn, "w", encoding='latin-1') as f:
            f.write(data)

    def write_readme(self) -> None:
        data = self.get_readme_data()
        with open(settings.EIBI_README_FILE, "w", encoding="utf-8") as f:
            f.write(data)
        return None