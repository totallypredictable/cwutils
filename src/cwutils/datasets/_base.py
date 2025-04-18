import csv
import pandas as pd
from importlib import resources
import types
import pathlib
import os

DATA_MODULE = "cwutils.datasets.data"
DESCR_MODULE = "cwutils.datasets.descr"


def _return_resource(
    data_module: str | types.ModuleType, data_file_name: str
) -> os.PathLike:
    """Check if the resource at the given path exists and return the `data_path`.
    Otherwise return `None`.
    """

    assert isinstance(
        data_module, (str, types.ModuleType)
    ), f"{data_module=} is of incorrect type!"
    assert isinstance(data_file_name, str), f"{data_file_name=} is of incorrect type!"

    try:
        data_path = resources.files(data_module) / data_file_name
        if not data_path.exists():
            raise FileNotFoundError(
                f"{data_file_name=} at the given path does not exist!"
            )
        elif os.path.isdir(data_path):
            raise IsADirectoryError(f"{data_file_name} points to a directory!")
        else:
            return data_path
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            f"{data_module=} not found! Make sure it's installed in your ENV."
        )


def _infer_dialect(data_path: str | pathlib.PosixPath | os.PathLike) -> csv.Dialect:
    """Infer and return the dialect of the input text."""

    assert isinstance(
        data_path, (str, pathlib.PosixPath, os.PathLike)
    ), f"{data_path=} is not one of correct type!"

    if not isinstance(data_path, pathlib.PosixPath):
        data_path = pathlib.PosixPath(data_path)

    with data_path.open("r", encoding="utf-8") as csv_file:
        first_row = csv_file.readline()
        dialect = csv.Sniffer().sniff(first_row)

    return dialect


def _convert_to_dataframe(
    data_path: str | os.PathLike,
    *,
    dialect: None | csv.Dialect | dict = None,
    encoding: str = "utf-8",
    **kwargs,
) -> pd.DataFrame:
    """Read the csv at the given path and convert it to and return it as a dataframe"""

    return pd.read_csv(data_path, encoding=encoding, dialect=dialect, **kwargs)


def load_csv_data(
    data_file_name: str,
    /,
    target: str | int | None = None,
    *,
    data_module: str | types.ModuleType = DATA_MODULE,
    descr_file_name: str | None = None,
    descr_module: str | types.ModuleType = DESCR_MODULE,
    separate_target: bool = False,
    encoding: str = "utf-8",
    **kwargs,
) -> tuple[...]:
    """Load `data_file_name` from `data_module with `importlib.resources`.

    Parameters
    ----------
    data_file_name : str
        Name of csv file to be loaded from `data_module/data_file_name`.
        For example `advertising.csv`.

    target : str or int, default=None.
        Name or the index of the target column.
        If int, must be between [0, len(df.columns)-1].

    data_module : str or module, default='cwutils.datasets.data'
        Module where data lives. The default is :mod:`cwutils.datasets.data`.

    descr_file_name : str, default=None
        Name of rst file to be loaded from `descr_module/descr_file_name`.
        For example `'advertising.rst'`. See also :func:`load_descr`.
        If not None, also returns the corresponding description of
        the dataset.

    separate_target : bool, default=False
        If true, split the dataset into design matrix of shape (n_samples, n_features)
        and target column of shape (n_samples,) and return them separately.
        Return the entire dataset otherwise.

    encoding: str, default='utf-8'
        Test encoding of the CSV file.

    **kwargs :
        Additional keyword arguments will be passed to :func:`pd.read_csv`

    Returns
    -------
    design matrix : :class:`pd.DataFrame` of shape (n_samples, n_features)
        A 2D data frame with each row representing one sample and each column
        representing the features of a given sample.

    target : :class:`pd.Series` of shape (n_samples,)
        A 1D series holding target variables for all the samples in `data`.
        For example, target[0] is the name of the target[0] class.

    descr : str
        Returned only if `descr_file_name` is not None.
        Description of the dataset (the content of `descr_file_name`).
    """

    data_path = _return_resource(data_module, data_file_name)
    dialect = _infer_dialect(data_path)
    dialect = None if dialect.delimiter == "," else dialect

    df = _convert_to_dataframe(data_path, dialect=dialect, encoding=encoding, **kwargs)

    if target:
        if isinstance(target, str):
            assert (
                target in df.columns
            ), f"{target=} is not in the columns of the dataset!"
        elif isinstance(target, int):
            assert target in list(range(len(df.columns)))
            target = df.columns[target]

    if separate_target:
        target_series = pd.Series(df.loc[:, target])
        if descr_file_name is None:
            return df.drop(target, axis=1), target_series
        else:
            assert descr_module is not None
            descr = load_descr(
                descr_module=descr_module, descr_file_name=descr_file_name
            )
            return df.drop(target, axis=1), target_series, descr
    else:
        if descr_file_name is None:
            return df
        else:
            assert separate_target is not None
            descr = load_descr(
                descr_module=descr_module, descr_file_name=descr_file_name
            )
            return df, descr


def load_descr(descr_file_name, *, descr_module=DESCR_MODULE, encoding="utf-8"):
    """Load `descr_file_name` from `descr_module` with `importlib.resources`.

    Parameters
    ----------
    descr_file_name : str
        Name of rst file to be loaded from `descr_module/descr_file_name`.
        For example `'advertising.rst'`.

    descr_module : str or module, default='cwutils.datasets.descr'
        Module where `descr_file_name` lives. See also :func:`load_descr`.
        The default  is :mod:`cwutils.datasets.descr`.

    encoding : str, default='utf-8'
        Name of the encoding that `descr_file_name` will be decoded with.
        The default is 'utf-8'.

    Returns
    -------
    fdescr : str
        Content of `descr_file_name`.
    """
    path = resources.files(descr_module) / descr_file_name
    return path.read_text(encoding=encoding)
