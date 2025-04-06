import csv
import numpy as np
from importlib import resources

DATA_MODULE = "cwutils.datasets.data"
DESCR_MODULE = "cwutils.datasets.descr"

def load_csv_data(
    data_file_name,
    *,
    data_module=DATA_MODULE,
    descr_file_name=None,
    descr_module=DESCR_MODULE,
    encoding="utf-8",
):
    """Loads `data_file_name` from `data_module with `importlib.resources`.

    Parameters
    ----------
    data_file_name : str
        Name of csv file to be loaded from `data_module/data_file_name`.
        For example `advertising.csv`.

    data_module : str or module, default='cwutils.datasets.data'
        Module where data lives. The default is `'cwutils.datasets.data'`.

    descr_file_name : str, default=None
        Name of rst file to be loaded from `descr_module/descr_file_name`.
        For example `'advertising.rst'`. See also :func:`load_descr`.
        If not None, also returns the corresponding description of 
        the dataset.

    Returns
    -------
    data: ndarray of shape (n_sampoles, n_features)
        A 2D array with each row representing one sample and each column 
        representing the features of a given sample.

    target: ndarray of shape (n_samples,)
        A 1D array holding target variables for all the samples in `data`.
        For example, target[0] is the name of the target[0] class.

    descr: str, optional
        Description of the dataset (the content of `descr_file_name`).
        Only returned if `descr_file_name` is not None.

    encoding: str, optional
        Test encoding of the CSV file.
    """

    data_path = resources.files(data_module) / data_file_name
    with data_path.open("r", encoding="utf-8") as csv_file:
        data_file = csv.reader(csv_file)
        temp = next(data_file)
        n_samples = int(temp[0])
        n_features = int(temp[1])
        target_names = np.array(temp[2:])
        data = np.empty((n_samples, n_features))
        target = np.empty((n_samples,), dtype=int)

        for i, ir in enumerate(data_file):
            data[i] = np.asarray(ir[:-1], dtype=np.float64)
            target[i] = np.asarray(ir[-1], dtype=int)

    if descr_file_name is None:
        return data, target, target_names
    else:
        assert descr_module is not None
        descr = load_descr(descr_module=descr_module, descr_file_name=descr_file_name)
        return data, target, target_names, descr

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
