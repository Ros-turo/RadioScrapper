import pytest
import os
from radioscraper.eibi.http_layer import EibiAPI
from radioscraper.eibi.parser import EibiParser


@pytest.fixture
def mozilla_user_agent() -> dict[str,str]:
    return {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0"}

@pytest.fixture
def eibi_test_csv_station() -> str:
    eibi_api = EibiAPI()
    if os.path.exists("test_station.csv"):
        pass
    else:
        eibi_data_bytes = eibi_api.get_station_data()
        eibi_api.write_data_to_csv("test_station.csv", eibi_data_bytes)
    return "test_station.csv"

@pytest.fixture
def eibi_test_parser(eibi_test_csv_station: str) -> EibiParser:
    return EibiParser(eibi_test_csv_station)
