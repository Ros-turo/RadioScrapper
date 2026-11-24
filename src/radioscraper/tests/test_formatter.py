import pytest

from radioscraper.eibi.formatter import format_language, format_regularity
from radioscraper.eibi.model import StationData, EVERY_DAY
from radioscraper.tests.conftest import make_station


@pytest.mark.parametrize(
    "station, expected",
    [
        (make_station(language=["English"]), "English"),
        (make_station(language=None), ""),
        (make_station(language=["English", "Russia"]), "English Russia"),
    ],
    ids=["one value", "empty string", "two values"],
)
def test_format_language(station: StationData, expected: str) -> None:
    formatted_language = format_language(station)

    assert formatted_language == expected

@pytest.mark.parametrize(
    "station, expected",
    [
        (make_station(regularity=[0]), "Mo"),
        (make_station(regularity=[6,5]), "Sa Su"),
        (make_station(regularity="irregular"), "irregular"),
        (make_station(regularity="Last7"), "Last Sunday"),
        (make_station(regularity=EVERY_DAY), "Every day"),
        (make_station(regularity=[6,5,4,3,2,1,0]), "Every day"),
    ],
    ids=["one value", "reversed weekend", "irregular", "Last7", "Every day", "reversed Every day"],
)
def test_format_regularity(station: StationData, expected: str) -> None:
    formatted_regularity = format_regularity(station)

    assert formatted_regularity == expected
