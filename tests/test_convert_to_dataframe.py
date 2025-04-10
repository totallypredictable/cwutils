import pandas as pd
from cwutils.datasets._base import _convert_to_dataframe


def test_expected_return(data_path) -> None:
    df = _convert_to_dataframe(data_path)
    df_test = pd.read_csv(data_path)
    pd.testing.assert_frame_equal(df, df_test)


def test_datapath_as_str(data_path) -> None:
    data_path_str = str(data_path)
    df = _convert_to_dataframe(data_path_str)
    df_test = pd.read_csv(data_path)
    pd.testing.assert_frame_equal(df, df_test)
