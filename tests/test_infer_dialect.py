import csv
import pytest
from cwutils.datasets._base import _infer_dialect


# TODO: Shared fixtures


@pytest.fixture(scope="session")
def data_path(tmp_path_factory):
    # Create a posixpath at which a csv file will be created
    data_path = tmp_path_factory.mktemp("data") / "fake.csv"
    with data_path.open("w", encoding="utf-8") as csv_file:
        spamwriter = csv.writer(csv_file, delimiter=",")
        spamwriter.writerow(["Spam"] * 2 + ["Baked Beans"])
        spamwriter.writerow(["Spam", "Lovely Spam", "Wonderful Spam"])
    return data_path


@pytest.fixture
def example_csv_name() -> str:
    return "advertising_synth.csv"


@pytest.fixture
def default_data_module() -> str:
    return "cwutils.datasets.data"


@pytest.fixture
def default_descr_module() -> str:
    return "cwutils.datasets.descr"


@pytest.fixture
def nonexistent_module_name() -> str:
    return "thismoduledoesnotexist"


@pytest.fixture
def nonexistent_file_name() -> str:
    return "thisfiledoesnotexist.csv"


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
