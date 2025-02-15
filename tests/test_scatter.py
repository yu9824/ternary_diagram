import pandas as pd
import pytest

from ternary_diagram import TernaryDiagram


@pytest.fixture
def prepare_data() -> pd.DataFrame:
    df_scatter = pd.read_csv(
        "https://raw.githubusercontent.com/yu9824/ternary_diagram/main/example/scatter/example_scatter.csv"  # noqa
    )
    return df_scatter


def test_scatter(prepare_data):
    df_scatter: pd.DataFrame = prepare_data
    td = TernaryDiagram(materials=df_scatter.columns[:3])
    td.scatter(df_scatter.iloc[:, :3], df_scatter.loc[:, "z"])
