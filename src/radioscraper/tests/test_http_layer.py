import pytest

from radioscraper.exceptions import InvalidURL
from radioscraper.http_layer import StationAPI
from radioscraper.settings import settings
import os

def test_init_station_api_instance() -> None:
    api = StationAPI()
    assert isinstance(api, StationAPI)
    assert api.station_url == settings.STATION_DB_URL

def test_init_station_api_instance_with_unexist_url() -> None:
    with pytest.raises(InvalidURL):
        StationAPI(url="not-exits")

def test_get_data_return_csv_file()-> None:
    api = StationAPI()
    api.get_data()
    assert os.path.exists("stations.csv")
    os.remove("stations.csv")

