from requests import HTTPError

from radioscraper.eibi.http_layer import StationAPI, EibiAPI
from radioscraper.settings import settings

def test_init_eibi_api_instance() -> None:
    api = EibiAPI()
    assert isinstance(api, StationAPI)
    assert api.station_url == settings.EIBI_URL

def test_eibi_api_get_data() -> None:
    api = EibiAPI()
    try:
        response = api.get_station_data()
        assert isinstance(response, bytes)
    except HTTPError:
        pass
