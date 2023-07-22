from ternary_diagram import TernaryDiagram
import pytest
import pandas as pd


@pytest.fixture
def prepare_data() -> pd.DataFrame:
    df_mono_scatter = pd.read_csv(
        "https://raw.githubusercontent.com/yu9824/ternary_diagram/main/example/mono_scatter/example_mono_scatter.csv"
    )
    return df_mono_scatter


def test_mono_scatter(prepare_data):
    df_mono_scatter: pd.DataFrame = prepare_data
    print(df_mono_scatter)
    td = TernaryDiagram(materials=df_mono_scatter.columns)
    td.scatter(df_mono_scatter)
