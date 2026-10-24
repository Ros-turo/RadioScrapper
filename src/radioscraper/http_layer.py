import requests
from abc import ABC, abstractmethod
from radioscraper.settings import settings


class StationAPI(ABC):
    
    @abstractmethod
    def get_data(self) -> bytes | str: ...

    @abstractmethod
    def write_data_to_csv(self, fn: str, data: bytes | str) -> None: ...
    
    
class EibiAPI(StationAPI):
    
    def __init__(self) -> None:
        self.url = settings.EIBI_URL

    def get_data(self) -> bytes:
        response = requests.get(self.url)
        response.raise_for_status()
        return response.content

    @staticmethod
    def bytes_to_str(data: bytes) -> str:
        return data.decode("latin-1")

    def write_data_to_csv(self, fn: str, data: bytes | str) -> None:
        if isinstance(data, bytes):
            data = self.bytes_to_str(data)
        with open(fn, "w") as f:
            f.write(data)
