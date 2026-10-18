import pandas as pd

from radioscraper.settings import settings


class CSVWriter:

    def __init__(self, fn:str = settings.CSV_FILENAME) -> None:
        self.filename = fn

    def write_bytes(self, data: bytes) -> None:
        with open(self.filename, "wb") as f:
            f.write(data)


class PandasRepo:

    def __init__(self, fn:str) -> None:
        self.df = pd.read_csv(fn)