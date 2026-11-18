from typing import Literal

import pytest
from datetime import datetime, time, timezone

from mypy.typeops import true_only

from radioscraper.eibi.matching import match_station_name, match_language, is_on_air
from radioscraper.eibi.model import StationData

ALL_DAYS = [0,1,2,3,4,5,6]
MON_NOON = datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc)
SUN_LATE = datetime(2026, 11, 15, 23, 59, 30, tzinfo=timezone.utc)


def make_station(start: time, end: time, regularity: list[int] | Literal["irregular"] | Literal["Last7"]=ALL_DAYS) -> StationData:
    return StationData(frequency=1000, start_time=start, end_time=end,
                       regularity=regularity, station="BBC", language=["English"])

@pytest.fixture
def station_BBC() -> StationData:
    return StationData(frequency=1000, start_time=time(12, 00), end_time=time(15, 00), station="BBC",
                       regularity="irregular", language=["English"])

@pytest.fixture
def target_day_monday_12_am() -> datetime:
    return datetime(year=2026, month=11, day=2, hour=12)

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

#TODO: is_on_air - regularity_list_today, reg_list_yest, reg_irr_briding, rag_iir_not_bridging, reg_Last7
@pytest.mark.parametrize(
    "station, expected_value",
    [
        (
            make_station(time(11, 00), time(15, 00)),
            True
        ),
        (
                make_station(time(11, 00), time(12, 00)),
            True
        ),
        (
            make_station(time(11, 00), time(15, 00), [1]),
            False
        ),
        (
                make_station(time(23,59), time(15, 00),[6]),
            True
        ),
        (
                make_station(time(23,59), time(11, 00),[6]),
            False
        ),
        (
                make_station(time(00,00), time(23, 59),[0]),
            True)
    ],
    ids=["every_day_in_time", "every_day_in_end_time_bound", "not_monday_in_right_time", "sunday_with_bridging_in_right_time", "sunday_with_bridging_before_end_time", "all_monday"]
)
def test_is_on_air_regularity_list(station: StationData, target_day_monday_12_am: datetime, expected_value:bool) -> None:
    asserting_value = is_on_air(station, target_day_monday_12_am)
    assert asserting_value == expected_value



@pytest.mark.parametrize(
    "station, expected_value",
    [
            (
                    StationData(frequency=1000, start_time=time(11, 00), end_time=time(15, 00), station="BBC",
                                regularity="irregular", language=["English"]),
                    True
            ),
            (
                    StationData(frequency=1000, start_time=time(11, 00), end_time=time(11, 30), station="BBC",
                                regularity="irregular", language=["English"]),
                    False
            ),
            (
                    StationData(frequency=1000, start_time=time(12, 30), end_time=time(15, 00), station="BBC",
                                regularity="irregular", language=["English"]),
                    False
            ),
            (
                    StationData(frequency=1000, start_time=time(23, 59), end_time=time(23, 58), station="BBC",
                                regularity="irregular", language=["English"]),
                    True
            ),
            (
                    StationData(frequency=1000, start_time=time(23, 59), end_time=time(11, 00), station="BBC",
                                regularity="irregular", language=["English"]),
                    False
            ),
    ],
    ids=["irregular_not_bridging_in_right_time", "irregular_not_bridging_before_start_time", "irregular_not_bridging_after_end_time",
         "irregular_bridging_all_day",  "irregular_bridging_after_end_time"]
)
def test_is_on_air_irregular(station: StationData, target_day_monday_12_am: datetime, expected_value: bool) -> None:
    asserting_value = is_on_air(station, target_day_monday_12_am)
    assert asserting_value == expected_value

# # udelat v podobe:
# @pytest.mark.parametrize(
#     "station, now, expected",
#     [
#         (make_station(time(23, 59), time(15, 0), [6]), SUN_LATE, True),    # právě začalo
#         (make_station(time(23, 59), time(15, 0), [0]), MON_NOON, False),   # začalo v neděli, ta v seznamu není
#         (make_station(time(0, 0), time(23, 59), [6]), SUN_LATE, True),     # poslední minuta dne
#
#     ],
# )
# def test_is_on_air(station: StationData, now: datetime, expected:bool) -> None:
#     assert is_on_air(station, now) == expected