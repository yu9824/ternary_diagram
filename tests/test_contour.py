import pandas as pd
import pytest

from ternary_diagram import TernaryDiagram


@pytest.fixture
def prepare_data() -> pd.DataFrame:
    df_contour = pd.read_csv(
        "https://raw.githubusercontent.com/yu9824/ternary_diagram/main/example/contour/example_contour.csv"  # noqa
    )
    return df_contour


def test_scatter(prepare_data):
    df_contour: pd.DataFrame = prepare_data
    td = TernaryDiagram(materials=df_contour.columns[:3])
    td.scatter(df_contour.iloc[:, :3], df_contour.loc[:, "z"])
