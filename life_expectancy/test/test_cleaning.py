"""Tests for the cleaning module"""
import pandas as pd
import pytest

from life_expectancy.cleaning import clean_data
from . import OUTPUT_DIR

@pytest.fixture(scope="session")
def pt_life_expectancy_raw() -> pd.DataFrame:
    """Fixture to load the raw data and use it for the function"""
    filepath = OUTPUT_DIR / "eu_life_expectancy_raw.tsv"
    return pd.read_csv(filepath, sep="\t")


def test_clean_data(pt_life_expectancy_expected, pt_life_expectancy_raw: pd.DataFrame):
    """Run the `clean_data` function and compare the output to the expected output"""
    pt_life_expectancy_actual = clean_data(pt_life_expectancy_raw,"PT").reset_index(drop=True)

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
