import importlib
import os
from cwutils.datasets._base import _return_resource
import pytest


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


def test_return_type(default_data_module, example_csv_name) -> None:
    path = _return_resource(default_data_module, example_csv_name)
    assert isinstance(path, os.PathLike)


def test_return_value(default_data_module, example_csv_name) -> None:
    path = _return_resource(default_data_module, example_csv_name)
    test_value = importlib.resources.files(default_data_module) / example_csv_name
    assert path == test_value


def test_nonexistent_module_input(nonexistent_module_name, example_csv_name) -> None:
    with pytest.raises(ModuleNotFoundError):
        _return_resource(nonexistent_module_name, example_csv_name)


def test_nonexistent_file_input(default_data_module, nonexistent_file_name) -> None:
    with pytest.raises(FileNotFoundError):
        _return_resource(default_data_module, nonexistent_file_name)


def test_wrong_is_file(default_data_module, tmpdir) -> None:
    with pytest.raises(AssertionError):
        _return_resource(default_data_module, tmpdir)
