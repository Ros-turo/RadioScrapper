from typing import List

import pytest

from radioscraper.eibi.formatter import format_language
from radioscraper.eibi.model import StationData
from radioscraper.tests.conftest import make_station


@pytest.mark.parametrize(
    "station, expected",
    [
        (make_station(language=["English"]), "English"),
        (make_station(language=None), ""),
        (make_station(language=["English", "Russia"]), "English Russia"),
    ]
)
def test_format_language(station: StationData, expected: str) -> None:
    formatted_language = format_language(station)

    assert formatted_language == expected
