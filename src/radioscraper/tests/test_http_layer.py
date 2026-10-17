import pytest
from requests import HTTPError

from radioscraper.exceptions import InvalidURL
from radioscraper.http_layer import StationAPI, EibiAPI
from radioscraper.settings import settings
import os

def test_init_eibi_api_instance() -> None:
    api = EibiAPI()
    assert isinstance(api, StationAPI)
    assert api.url == settings.EIBI_URL

def test_eibi_api_get_data() -> None:
    api = EibiAPI()
    try:
        response = api.get_data()
        assert isinstance(response, bytes)
    except HTTPError:
        pass
