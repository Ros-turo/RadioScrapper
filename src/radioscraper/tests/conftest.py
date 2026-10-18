import os
from typing import Generator

import pytest

from radioscraper.database import CSVWriter


@pytest.fixture
def mozilla_user_agent() -> dict[str,str]:
    return {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0"}

@pytest.fixture
def string_mock_data() -> str:
    return "name,age\nEva,20\nAdam,25"


@pytest.fixture
def csv_data(string_mock_data: str) -> bytes:
    return string_mock_data.encode()

@pytest.fixture
def csv_file(csv_data: bytes) -> Generator[str, None, None]:
    test_writer = CSVWriter("test.csv")
    test_writer.write_bytes(csv_data)
    yield "test.csv"
    os.remove("test.csv")
