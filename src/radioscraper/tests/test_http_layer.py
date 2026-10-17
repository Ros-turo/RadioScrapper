import pytest

from radioscraper.exceptions import InvalidURL
from radioscraper.http_layer import StationAPI, EibiAPI
from radioscraper.settings import settings
import os

def test_init_eibi_api_instance() -> None:
    api = EibiAPI()
    assert isinstance(api, StationAPI)
    assert api.url == settings.EIBI_URL


