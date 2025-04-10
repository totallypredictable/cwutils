import pytest
import csv
import pandas as pd
from importlib import resources
import pathlib


@pytest.fixture(scope="module")
def default_data_module() -> str:
    return "cwutils.datasets.data"


@pytest.fixture(scope="module")
def default_descr_module() -> str:
    return "cwutils.datasets.descr"


@pytest.fixture(scope="module")
def correct_csv_name() -> str:
    return "advertising_synth.csv"


@pytest.fixture(scope="module")
def nonexistent_file_name() -> str:
    return "thisfiledoesnotexist.csv"


@pytest.fixture(scope="module")
def full_path_advertising_csv(
    default_data_module, correct_csv_name
) -> pathlib.PosixPath:
    return resources.files(default_data_module).joinpath(correct_csv_name)


@pytest.fixture(scope="module")
def advertising_csv_as_dataframe(full_path_advertising_csv) -> pd.DataFrame:
    return pd.read_csv(full_path_advertising_csv)


@pytest.fixture(scope="module")
def advertising_target_as_series(advertising_csv_as_dataframe) -> pd.Series:
    return advertising_csv_as_dataframe["sales"]


@pytest.fixture(scope="module")
def nonexistent_module_name() -> str:
    return "thismoduledoesnotexist"


@pytest.fixture(scope="module")
def example_csv_rows() -> list[list, ...]:
    return [["C1", "C2", "C3", "C4", "C5"], ["Random", "Cell", "Value", "Spam", "Lmao"]]


@pytest.fixture(scope="module")
def data_path(
    tmp_path_factory, correct_csv_name, nonexistent_module_name, example_csv_rows
):
    # Create a posixpath at which a csv file will be created
    data_path = tmp_path_factory.mktemp(nonexistent_module_name) / correct_csv_name
    with data_path.open("w", encoding="utf-8") as csv_file:
        spamwriter = csv.writer(csv_file, delimiter=",")
        spamwriter.writerow(example_csv_rows[0])
        spamwriter.writerow(example_csv_rows[1])
    return data_path
