import os

from radioscraper.database import CSVWriter, PandasRepo


def test_csv_writer_write_bytes_to_file(csv_dumb_data: bytes) -> None:
    writer = CSVWriter(fn="test.csv")
    writer.write_bytes(csv_dumb_data)
    assert os.path.exists(writer.filename)
    os.remove("test.csv")


def test_csv_writer_write_array_to_file(

)-> None:
    ...

def test_pandas_repo_init(csv_dumb_file: str, string_mock_data: str) -> None:
    repo = PandasRepo(fn=csv_dumb_file)
    table = repo.df
    table_row = table.iloc[0]
    data = string_mock_data.split("\n")[1:]
    row = data[0].split(",")
    assert table_row["name"] == row[0]
    assert str(table_row["age"]) == row[1]
