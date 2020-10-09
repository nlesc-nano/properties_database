"""Module to test the interface to Mongodb."""


from typing import List

import pandas as pd
from pymongo import MongoClient

from insilicodatabase.interface import (DatabaseConfig, connect_to_db,
                                        store_many_in_collection)

from .utils_test import PATH_TEST


def add_candidates(mongodb: MongoClient) -> List[int]:
    """Check that the interface is working."""
    # read data from file
    path_data = PATH_TEST / "candidates.csv"
    data = pd.read_csv(path_data, index_col=0)
    data.reset_index(inplace=True)
    data.rename(columns={"index": "_id"}, inplace=True)

    return store_many_in_collection(
        mongodb, "candidates", data.to_dict("records"))


def test_many_insertions():
    """Check that the interface is working."""
    # Connect to the database
    db_config = DatabaseConfig("test_mutations")
    mongodb = connect_to_db(db_config)

    expected_ids = {76950, 43380, 26717, 70, 47561, 32800, 37021, 2449, 63555, 72987}
    try:
        ids = add_candidates(mongodb)
        print("received ids: ", ids)
        assert all(index in expected_ids for index in ids)
    finally:
        collection = mongodb["candidates"]
        collection.drop()


