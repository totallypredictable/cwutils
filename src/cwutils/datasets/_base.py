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
    """Checks if the resource at the given path exists and returns the `data_path`.
    Otherwise returns `None`.
    """

    assert isinstance(
        data_module, (str, types.ModuleType)
    ), f"data_module={data_module} is of incorrect type!"
    assert isinstance(
        data_file_name, str
    ), f"data_file_name={data_file_name} is of incorrect type!"

    try:
        data_path = resources.files(data_module) / data_file_name
        if not data_path.exists():
            raise FileNotFoundError(
                f"The file {data_file_name} at the given path does not exist!"
            )
        elif os.path.isdir(data_path):
            raise IsADirectoryError("The file name you provided points to a directory!")
        elif not data_path.is_file():
            raise ValueError("The given path does not point to a file!")
        else:
            return data_path
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            f"The module {data_module} not found! Make sure it's installed in your ENV."
        )


def _infer_dialect(data_path: str | pathlib.PosixPath | os.PathLike) -> csv.Dialect:
    """Infers and returns the dialect of the input text."""

    assert isinstance(
        data_path, (str, pathlib.PosixPath, os.PathLike)
    ), "data_path is not one of correct type!"

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
    """Reads the csv at the given path and converts it to and returns it as a dataframe"""

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
    """Loads `data_file_name` from `data_module with `importlib.resources`.

    Parameters
    ----------
    data_file_name : str
        Name of csv file to be loaded from `data_module/data_file_name`.
        For example `advertising.csv`.

    target : str or int, optional, default=None
        Name or the index of the target column.

    data_module : str or module, default='cwutils.datasets.data'
        Module where data lives. The default is `'cwutils.datasets.data'`.

    descr_file_name : str, optional, default=None
        Name of rst file to be loaded from `descr_module/descr_file_name`.
        For example `'advertising.rst'`. See also :func:`load_descr`.
        If not None, also returns the corresponding description of
        the dataset.

    separate_target : bool, optional, default=False
        If true, split the dataset into design matrix of shape (n_samples, n_features)
        and target column of shape (n_samples,) and return them separately.
        Return the entire dataset otherwise.

    encoding: str, optional, default=`utf-8`
        Test encoding of the CSV file.

    Returns
    -------
    design matrix : :class:`pd.DataFrame` of shape (n_samples, n_features)
        A 2D data frame with each row representing one sample and each column
        representing the features of a given sample.

    target : :class:`pd.Series` of shape (n_samples,)
        A 1D series holding target variables for all the samples in `data`.
        For example, target[0] is the name of the target[0] class.

    descr : str, optional
        Description of the dataset (the content of `descr_file_name`).
        Only returned if `descr_file_name` is not None.
    """

    data_path = _return_resource(data_module, data_file_name)
    dialect = _infer_dialect(data_path)
    dialect = None if dialect.delimiter == "," else dialect

    df = _convert_to_dataframe(data_path, dialect=dialect, encoding=encoding, **kwargs)

    if target:
        if isinstance(target, str):
            assert (
                target in df.columns
            ), f"{target} is not in the columns of the dataset!"

    if separate_target:
        try:
            target_series = pd.Series(df.loc[:, target])
            if descr_file_name is None:
                return df.drop(target, axis=1), target_series
            else:
                assert descr_module is not None
                descr = load_descr(
                    descr_module=descr_module, descr_file_name=descr_file_name
                )
                return df.drop(target, axis=1), target_series, descr
        except KeyError:
            raise KeyError(
                f"Specified target name `{target}` is not in the columns of the dataset."
            )
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
    descr_file_name : str, default=None
        Name of rst file to be loaded from `descr_module/descr_file_name`.
        For example `'advertising.rst'`. See also :func:`load_descr`.
        If not None, also returns the corresponding description of
        the dataset.

    descr_module : str or module, default='cwutils.datasets.descr'
        Module where `descr_file_name` lives. See also :func:`load_descr`.
        The default  is `'cwutils.datasets.descr'`.

    encoding : str, default="utf-8"
        Name of the encoding that `descr_file_name` will be decoded with.
        The default is 'utf-8'.

    Returns
    -------
    fdescr : str
        Content of `descr_file_name`.
    """
    path = resources.files(descr_module) / descr_file_name
    return path.read_text(encoding=encoding)


def main():
    df, target = load_csv_data(
        "advertising.csv", target="Clicked on Ad", separate_target=True
    )
    print(df, target, sep="\n")


if __name__ == "__main__":
    main()
