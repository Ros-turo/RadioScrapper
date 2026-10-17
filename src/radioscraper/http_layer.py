import requests
from requests import Request
from abc import ABC, abstractmethod
from radioscraper.exceptions import InvalidURL
from radioscraper.settings import settings

class StationAPI(ABC):
    
    @abstractmethod
    def get_data(self) -> bytes: ...
    
    
class EibiAPI(StationAPI):
    
    def __init__(self) -> None:
        self.url = settings.EIBI_URL
        
        
    def get_data(self) -> bytes:
        response = requests.get(self.url)
        response.raise_for_status()
        return response.content
