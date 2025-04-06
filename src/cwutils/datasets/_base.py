import csv
import pandas as pd
from importlib import resources

DATA_MODULE = "cwutils.datasets.data"
DESCR_MODULE = "cwutils.datasets.descr"

def load_csv_data(
    data_file_name,
    /,
    target,
    *,
    data_module=DATA_MODULE,
    descr_file_name=None,
    descr_module=DESCR_MODULE,
    separate_target = False,
    encoding="utf-8",
    **kwargs,
):
    """Loads `data_file_name` from `data_module with `importlib.resources`.

    Parameters
    ----------
    data_file_name : str
        Name of csv file to be loaded from `data_module/data_file_name`.
        For example `advertising.csv`.
    
    target : str or int
        Name or the index of the target column.

    data_module : str or module, default='cwutils.datasets.data'
        Module where data lives. The default is `'cwutils.datasets.data'`.

    descr_file_name : str, default=None
        Name of rst file to be loaded from `descr_module/descr_file_name`.
        For example `'advertising.rst'`. See also :func:`load_descr`.
        If not None, also returns the corresponding description of 
        the dataset.
    
    separate_target : bool, default=False
        If true, split the dataset into design matrix of shape (n_samples, n_features) 
        and target column of shape (n_samples,) and return them separately. 
        Return the entire dataset otherwise.

    encoding: str, optional
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

    data_path = resources.files(data_module) / data_file_name
    with data_path.open("r", encoding="utf-8") as csv_file:
        first_row = csv_file.readline()
        dialect = csv.Sniffer().sniff(first_row)

    
    dialect = None if dialect.delimiter == "," else dialect

    df = pd.read_csv(data_path, encoding=encoding, dialect=dialect, **kwargs)
    if separate_target:
        try:
            target_series = pd.Series(df.loc[:, target])
            if descr_file_name is None:
                return df.drop(target, axis=1), target_series
            else:
                assert descr_module is not None
                descr = load_descr(descr_module=descr_module, descr_file_name=descr_file_name)
                return df.drop(target, axis=1), target_series, descr
        except KeyError:
            raise KeyError(f"Specified target name `{target}` is not in the columnd of the dataset.")
    else:
        if descr_file_name is None:
            return df
        else:
            assert separate_target is not None
            descr = load_descr(descr_module=descr_module, descr_file_name=descr_file_name)
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
    pass

if __name__ == "__main__":
    main()
