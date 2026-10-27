import csv
from datetime import time
from typing import Generator, List

import pytest
import os
from radioscraper.eibi.http_layer import StationAPI
from radioscraper.eibi.parser import EibiParser


class MockAPI(StationAPI):

    def get_station_data(self) -> str:
        return ("kHz:75;Time(UTC):93;Days:59;ITU:49;Station:201;Lng:49;Target:62;Remarks:135;P:35;Start:60;Stop:60;\r\n"
                "16.3;0000-2400;;IND;VTX1 Indian Navy;;SAs;v;1;;")

    def write_data_to_csv(self, fn: str, data: bytes | str) -> None:
        if isinstance(data, str):
            with open(fn, "w") as f:
                writer = csv.writer(f, delimiter=";")
                rows_to_write = [row.split(";") for row in data.split("\r\n")]
                writer.writerows(rows_to_write)
        elif isinstance(data, bytes):
            raise NotImplementedError

@pytest.fixture
def test_mock_data() -> Generator[None, None, None]:
    mock_api = MockAPI()
    data = mock_api.get_station_data()
    mock_api.write_data_to_csv("test.csv", data)
    yield
    os.remove("test.csv")

def test_eibi_parser_init(test_mock_data: None) -> None:
    parser = EibiParser(fn="test.csv")
    broadcast = parser.parse_file()
    print(broadcast)

@pytest.mark.parametrize(
    argnames=["mock_time", "excepted_tuple"],
    argvalues=[
        ("1200-1300", (time(12,00), time(13, 00))),
        ("0730-1000", (time(7, 30), time(10, 00))),
        ("0000-2400", (time(0,0), time(23,59)))
    ])
def test_eibi_parser_get_time(test_mock_data: None, mock_time:str, excepted_tuple: tuple[time, time]) -> None:
    parser = EibiParser(fn="test.csv")
    returned_tuple = parser.get_time(mock_time)

    assert returned_tuple == excepted_tuple


@pytest.mark.parametrize(
    argnames=["mock_days", "expected_value"],
    argvalues=[(None, [0,1,2,3,4,5,6]),
               ("Mo-Fr", [1,2,3,4,5]),
               ('Th', [4]),
               ("Wa", "irregular"),
               ("SaSu", [0,6]),
               ("irr", "irregular"),
               ("harm", "irregular"),
               ("Last7", "Last7"),
               ("MF-15", "irregular")]
)
def test_eibi_parser_get_regularity(
        test_mock_data: None,
        mock_days:str,
        expected_value: List[int] | str
) -> None:
    parser = EibiParser(fn="test.csv")
    regularity = parser.get_regularity(mock_days)

    assert regularity == expected_value

## tests na get_language

## tests na LanguageParser
