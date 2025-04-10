from cwutils.datasets._base import load_csv_data
import pytest
import pandas as pd


@pytest.mark.xfail(strict=True)
def test_nonexistent_file_name(nonexistent_file_name) -> None:
    load_csv_data(nonexistent_file_name, target="C5")


def test_with_correct_path(correct_csv_name) -> None:
    load_csv_data(correct_csv_name)


@pytest.mark.xfail(strict=True)
def test_incorrect_target(correct_csv_name) -> None:
    load_csv_data(correct_csv_name, target="notvalidtarget")


def test_correct_target(
    default_data_module,
    correct_csv_name,
    advertising_csv_as_dataframe,
    advertising_target_as_series,
) -> None:
    df, target_series = load_csv_data(
        correct_csv_name,
        data_module=default_data_module,
        target="sales",
        separate_target=True,
    )
    pd.testing.assert_series_equal(advertising_target_as_series, target_series)


def test_descr() -> None:
    load_csv_data("iris.csv", descr_file_name="iris.rst")


def test_descr_name_none() -> None:
    load_csv_data(
        "iris.csv", descr_file_name="iris.rst", target="species", separate_target=True
    )


def test_incorrect_target_name() -> None:
    with pytest.raises(AssertionError):
        load_csv_data("iris.csv", target="dontexist", separate_target=True)


def test_correct_target_idx() -> None:
    load_csv_data("iris.csv", target=4, separate_target=True)
