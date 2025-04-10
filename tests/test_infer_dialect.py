import csv
import pytest
from cwutils.datasets._base import _infer_dialect


def test_dir_input(tmp_path) -> None:
    with pytest.raises(IsADirectoryError):
        _infer_dialect(tmp_path)


def test_delimiter(data_path) -> None:

    with data_path.open("r", encoding="utf-8") as csv_file:
        first_row = csv_file.readline()
        dialect = csv.Sniffer().sniff(first_row)

    assert dialect.delimiter == ","


def test_return_type(data_path) -> None:
    dialect = _infer_dialect(data_path)
    assert issubclass(dialect, csv.Dialect)
