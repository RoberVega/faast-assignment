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
# added this comment to solicitate a pull request
def load_data():
    """Reads the data and returns it as a pandas DataFrame"""
    filepath = Path.cwd()/"life_expectancy/data/eu_life_expectancy_raw.tsv"
    original_df = pd.read_csv(filepath, sep="\t")
    return original_df


def clean_data(data, region = "PT"):
    """
    Splits the first column, drops it and shuffles the new columns to the beginning.
    Unpivots/melts the years into a new column.
    Converts the years into int and the values into float, while eliminating the NaN's.
    """
    original_df = data.copy()
    first_column = original_df.columns[0]
    column_splits = ["unit", "sex", "age", "region"]
    original_df[column_splits] = original_df[first_column].str.split(",", expand=True)
    split_df = original_df.drop(first_column, axis=1)
    column_names = column_splits + list(split_df.columns[:-4])
    shuffled_df = split_df.reindex(columns=column_names)
    year_values = list(filter(lambda x: x not in column_splits, shuffled_df.columns.tolist()))
    melted_df = shuffled_df.melt(id_vars=column_splits,
                                value_vars=year_values,
                                var_name='year',
                                value_name='value')
    melted_df["year"] = melted_df["year"].astype(int)
    clean_df = melted_df[melted_df.value.str.strip() != ':']
    #The following cleans a few values that contain some letters
    clean_df["value"] = clean_df["value"].str.replace(r'[a-zA-z]','').astype(float)
    filtered_df = clean_df[clean_df["region"]==region]

    return filtered_df



def save_data(data, region="PT"):
    """Saves the data with the name of the chosen region, with no index."""
    data.to_csv(region.lower()+"_life_expectancy.csv",index=False)


if __name__ == "__main__": # pragma: no cover
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("region",
                        help="Choose the region you want to filter in ISO format",
                        type=str)
    REGION = PARSER.parse_args()
    DATA = load_data()
    CLEAN_DATA = clean_data(DATA, REGION.region)
    save_data(CLEAN_DATA, REGION.region)
