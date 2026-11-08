import datetime

import pytest

from radioscraper.eibi.filtering import yesterday_broadcast, today_broadcast, today_broadcast_on_air, \
    yesterday_broadcast_on_air
from radioscraper.eibi.model import Broadcast, StationData


@pytest.fixture
def mock_broadcast() -> Broadcast:
    station_data = [
        StationData(frequency=21760.0, start_time=datetime.time(11, 0), end_time=datetime.time(11, 45), regularity="irregular", station='Radio Vaticana', language=['Mandarin']),
        StationData(frequency=21760.0, start_time=datetime.time(12, 30), end_time=datetime.time(12, 50), regularity=[0, 1, 2, 3, 4, 5, 6], station='Radio Vaticana', language=['Russian']),
        StationData(frequency=21775.0, start_time=datetime.time(11, 0), end_time=datetime.time(11, 45), regularity=[5], station='Radio Vaticana', language=['Mandarin']),
        StationData(frequency=21780.0, start_time=datetime.time(23, 0), end_time=datetime.time(14, 0), regularity=[0, 1, 2, 3, 4, 5, 6], station='CNR1 Jammer/Firedrake', language=['Mandarin']),
        StationData(frequency=21780.0, start_time=datetime.time(0, 0), end_time=datetime.time(23, 59), regularity=[0, 1, 2, 3, 4, 5, 6], station='Sound of Hope', language=['Mandarin']),]
    broadcast = Broadcast()
    for station in station_data:
        broadcast.append_station(station)
    return broadcast

# TODO: testovat i negaci

def test_today_stations(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    today_weekday = today.weekday()
    today_broadcast_list = today_broadcast(mock_broadcast, target_day=today)
    for station in today_broadcast_list:
        assert isinstance(station.regularity, list)
        assert today_weekday in station.regularity

def test_today_broadcast_on_air(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    now = today.time()
    on_air_today = today_broadcast_on_air(mock_broadcast, target_day=today)
    for station in on_air_today:
        assert station.start_time <= now <= station.end_time


def test_yesterday_stations(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_weekday = yesterday.weekday()
    yesterday_broadcast_list = yesterday_broadcast(mock_broadcast, today)
    for station in yesterday_broadcast_list:
        assert isinstance(station.regularity, list)
        assert yesterday_weekday in station.regularity


def test_yesterday_broadcast_on_air(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    now = today.time()
    on_air_yesterday = yesterday_broadcast_on_air(mock_broadcast, today)
    for station in on_air_yesterday:
        assert now <= station.end_time