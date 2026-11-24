from requests import HTTPError

from radioscraper.eibi.http_layer import StationAPI, EibiAPI, station_stream_url
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


def test_station_stream_url() -> None:
    frequency = 1000
    url = station_stream_url(frequency)
    assert url == f'{settings.STREAM_SITE_URL}?tune={frequency}am'
