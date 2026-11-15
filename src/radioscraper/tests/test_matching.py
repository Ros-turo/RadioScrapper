import pytest
from datetime import datetime, time

from mypy.typeops import true_only

from radioscraper.eibi.matching import match_station_name, match_language
from radioscraper.eibi.model import StationData


@pytest.fixture
def station_BBC() -> StationData:
    return StationData(frequency=1000, start_time=time(12, 00), end_time=time(15, 00), station="BBC",
                       regularity="irregular", language=["English"])


@pytest.mark.parametrize(
    "matching_name, expected_value",
    [
        ("BBC", True),
        ("bbc", True),
        ("not_bbc", False),
        ("", True),
        ("bc", True)
    ])
def test_match_station_name(station_BBC: StationData, matching_name: str, expected_value: bool) -> None:
    asserting_value = match_station_name(station_BBC, matching_name)
    assert asserting_value == expected_value

@pytest.mark.parametrize(
    "matching_language, expected_value",
    [
        ("en", True),
        ("En", True),
        ("English", True),
        ("english", True),
        (" ", False),
        ("france", False)
    ]
)
def test_match_language_with_language_list_one_value(
        station_BBC: StationData,
        matching_language: str,
        expected_value: bool
) -> None:
    asserting_value = match_language(station_BBC, matching_language)
    assert asserting_value == expected_value

#TODO: empty list value, none value