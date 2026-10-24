import csv
from typing import Generator

import pytest
import os
from radioscraper.http_layer import StationAPI


class MockAPI(StationAPI):

    def get_data(self) -> str:
        return "Name;Age;Nationality\r\nRos;21;UA"

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
    data = mock_api.get_data()
    mock_api.write_data_to_csv("test.csv", data)
    yield
    os.remove("test.csv")

def test_eibi_parser_init(test_mock_data: None) -> None:
    pass
