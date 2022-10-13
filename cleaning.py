"""
This is the code for assignment 1
"""
# importing argparse and pandas library
from pathlib import Path
import argparse
import pandas as pd


# Passing the TSV file to
# read_csv() function
# with tab separator

def load_data():
    """Reads the data and returns it as a pandas DataFrame"""
    filepath = Path.cwd()/"life_expectancy/data/eu_life_expectancy_raw.tsv"
    df = pd.read_csv(filepath, sep="\t")
    return df

PARSER = argparse.ArgumentParser()
PARSER.add_argument("region", help="Choose the region you want to filter in ISO format",type=str)
REGION = PARSER.parse_args()


def clean_data(data, region = "PT"):
    """
    Splits the first column, drops it and shuffles the new columns to the beginning.
    Unpivots/melts the years into a new column.
    Converts the years into int and the values into float, while eliminating the NaN's.
    """
    df = data.copy()
    first_column = df.columns[0]
    column_splits = ["unit", "sex", "age", "region"]
    df[column_splits] = df[first_column].str.split(",", expand=True)
    df = df.drop(first_column, axis=1)
    column_names = column_splits + list(df.columns[:-4])
    df = df.reindex(columns=column_names)
    year_values = list(filter(lambda x: x not in column_splits, df.columns.tolist()))
    df = df.melt(id_vars=column_splits, value_vars=year_values, var_name='year', value_name='value')
    df["year"] = df["year"].astype(int)
    df = df[df.value.str.strip() != ':']
    df["value"] = df["value"].str.replace(r'[a-zA-z]', '').astype(float) #This cleans a few values that contain some letters
    df = df[df["region"]==region]

    return df



def save_data(data, region="PT"):
    """Saves the data with the name of the chosen region, with no index."""
    data.to_csv(region.lower()+"_life_expectancy.csv",index=False)


if __name__ == "__main__": # pragma: no cover
    DATA = load_data()
    CLEAN_DATA = clean_data(DATA, REGION.region)
    save_data(CLEAN_DATA, REGION.region)
