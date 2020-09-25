"""Module to perform some actions on a dataframe.

API
---
.. autofunction:: read_data_from_csv
.. autofunction:: sanitize_dataframe

"""

import pandas as pd


def read_data_from_csv(input_file: str):
    """Read data from a csv file."""
    # Read data and Reset index from 0
    return pd.read_csv(input_file).reset_index(drop=True)


def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Sanitize a dataframe before storing it in the database."""
    # Remove unnamed columns
    new = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Create a columns with indices
    new.reset_index(inplace=True)

    # rename the index column as _id
    new.rename(columns={"index": "_id"}, inplace=True)

    return new
