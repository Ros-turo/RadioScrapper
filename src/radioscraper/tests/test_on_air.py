import datetime

import pytest

from radioscraper.eibi.filtering import on_air, yesterday_broadcast
from radioscraper.eibi.model import Broadcast, StationData


@pytest.fixture
def mock_broadcast() -> Broadcast:
    station_data = [
        StationData(frequency=21760.0, start_time=datetime.time(11, 0), end_time=datetime.time(11, 45), regularity="irregular", station='Radio Vaticana', language=['Mandarin']),
        StationData(frequency=21760.0, start_time=datetime.time(12, 30), end_time=datetime.time(12, 50), regularity=[0, 1, 2, 3, 4, 5, 6], station='Radio Vaticana', language=['Russian']),
        StationData(frequency=21775.0, start_time=datetime.time(11, 0), end_time=datetime.time(11, 45), regularity=[6], station='Radio Vaticana', language=['Mandarin']),
        StationData(frequency=21780.0, start_time=datetime.time(23, 0), end_time=datetime.time(14, 0), regularity=[0, 1, 2, 3, 4, 5, 6], station='CNR1 Jammer/Firedrake', language=['Mandarin']),
        StationData(frequency=21780.0, start_time=datetime.time(0, 0), end_time=datetime.time(23, 59), regularity=[0, 1, 2, 3, 4, 5, 6], station='Sound of Hope', language=['Mandarin']),]
    broadcast = Broadcast()
    for station in station_data:
        broadcast.append_station(station)
    return broadcast

def test_filtering_on_air(mock_broadcast: Broadcast) -> None:
    now = datetime.datetime.now().time()
    filtered_broadcast = on_air(mock_broadcast, air_time=now)
    for station in filtered_broadcast:
        if not station.is_day_bridging:
            assert station.start_time <= now <= station.end_time
        else:
            assert station.start_time >= now >= station.end_time
    print(filtered_broadcast)

def test_yesterday_stations(mock_broadcast: Broadcast) -> None:
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_weekday = yesterday.weekday()
    # yesterday_broadcast_list = yesterday_broadcast(mock_broadcast, today)
    #TODO: dodelat ..
