import datetime

import pytest

from radioscraper.eibi.on_air import target_day_broadcast, today_broadcast_on_air, \
    yesterday_broadcast_on_air, get_irregular_broadcast, on_air_irregular, irregular_broadcast_on_air, on_air_total_stations
from radioscraper.eibi.model import Broadcast, StationData


@pytest.fixture
def mock_broadcast() -> Broadcast:
    station_data = [

        StationData(frequency=21860.0, start_time=datetime.time(11, 0), end_time=datetime.time(10, 59),
                    regularity="irregular", station='Radio Vaticana', language=['English']),
        StationData(frequency=21760.0, start_time=datetime.time(11, 0), end_time=datetime.time(11, 45),
                    regularity="irregular", station='Radio Vaticana', language=['Mandarin']),
        StationData(frequency=21760.0, start_time=datetime.time(12, 30), end_time=datetime.time(12, 50),
                    regularity=[0, 1, 2, 3, 4, 5, 6], station='Radio Vaticana', language=['Russian']),
        StationData(frequency=21775.0, start_time=datetime.time(23, 0), end_time=datetime.time(17, 45),
                    regularity=[5], station='Radio Vaticana', language=['Mandarin']),
        StationData(frequency=21780.0, start_time=datetime.time(23, 0), end_time=datetime.time(14, 0),
                    regularity=[0, 1, 2, 3, 4, 5, 6], station='CNR1 Jammer/Firedrake', language=['Mandarin']),
        StationData(frequency=21780.0, start_time=datetime.time(0, 0), end_time=datetime.time(23, 59),
                    regularity=[0, 1, 2, 3, 4, 5, 6], station='Sound of Hope', language=['Mandarin']),]
    broadcast = Broadcast()
    for station in station_data:
        broadcast.append_station(station)
    return broadcast

# TODO: testovat i negaci

def test_today_stations(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    today_weekday = today.weekday()
    today_broadcast_list = target_day_broadcast(mock_broadcast, target_day=today)
    for station in today_broadcast_list:
        assert isinstance(station.regularity, list)
        assert today_weekday in station.regularity

def test_today_broadcast_on_air(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    now = today.time()
    on_air_today = today_broadcast_on_air(mock_broadcast, today=today)
    for station in on_air_today:
        assert station.start_time <= now <= station.end_time


def test_yesterday_stations(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_weekday = yesterday.weekday()
    yesterday_broadcast_list = target_day_broadcast(mock_broadcast, yesterday)
    for station in yesterday_broadcast_list:
        assert isinstance(station.regularity, list)
        assert yesterday_weekday in station.regularity


def test_yesterday_broadcast_on_air(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_weekday = yesterday.weekday()
    now = today.time()
    on_air_yesterday = yesterday_broadcast_on_air(mock_broadcast, yesterday)
    for station in mock_broadcast:
        if isinstance(station.regularity, list) and yesterday_weekday in station.regularity and station.end_time >= now:
            assert station in on_air_yesterday


def test_get_irregular_on_air(mock_broadcast: Broadcast) -> None:
    irregular_broadcast = get_irregular_broadcast(mock_broadcast)
    for station in mock_broadcast:
        if station.regularity == "irregular":
            assert station in irregular_broadcast


def test_irregular_on_air(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    now = today.time()
    irregular_on_air = irregular_broadcast_on_air(mock_broadcast, target_time=now)
    print(irregular_on_air)
    for station in mock_broadcast:
        if not station.regularity == "irregular":
            continue
        match station.is_day_bridging:
            case True:
                if station.start_time >= now <= station.end_time:
                    print("yes")
                    assert station in irregular_on_air
            case False:
                if station.start_time <= now <= station.end_time:
                    assert station in irregular_on_air

def test_on_air_total_stations_with_irregular(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    now = today.time()

    today_weekday = today.weekday()
    yesterday_weekday = (today - datetime.timedelta(days=1)).weekday()

    assertation_broadcast = on_air_total_stations(mock_broadcast, today, True)
    print(assertation_broadcast)

    for station in mock_broadcast:
        if station.regularity == "Last7":
            raise NotImplementedError
        elif station.regularity == "irregular" and on_air_irregular(station, target_time=now):
            assert station in assertation_broadcast
            assertation_broadcast.remove_station(station)
        elif isinstance(station.regularity, list):
            if yesterday_weekday in station.regularity and station.end_time >= now:
                assert station in assertation_broadcast
                assertation_broadcast.remove_station(station)
            if (today_weekday in station.regularity and station.start_time <= now <= station.end_time):
                assert station in assertation_broadcast
                assertation_broadcast.remove_station(station)
        else:
            assert station not in assertation_broadcast
    assert len(assertation_broadcast) == 0
