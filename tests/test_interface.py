"""Module to test the interface to Mongodb."""


from typing import List

import pandas as pd
from pymongo import MongoClient

from insilicodatabase.interface import (DatabaseConfig, connect_to_db,
                                        fetch_many_from_collection,
                                        fetch_one_from_collection,
                                        store_many_in_collection)

from .utils_test import PATH_TEST

DB_NAME = "test_mutations"
COLLECTION_NAME = "candidates"


def add_candidates(mongodb: MongoClient) -> List[int]:
    """Check that the interface is working."""
    # read data from file
    path_data = PATH_TEST / "candidates.csv"
    data = pd.read_csv(path_data, index_col=0)
    data.reset_index(inplace=True)
    data.rename(columns={"index": "_id"}, inplace=True)

    return store_many_in_collection(
        mongodb, COLLECTION_NAME, data.to_dict("records"))


def test_many_insertions():
    """Check that the interface is working."""
    # Connect to the database
    db_config = DatabaseConfig(DB_NAME)
    mongodb = connect_to_db(db_config)

    expected_ids = {76950, 43380, 26717, 70, 47561, 32800, 37021, 2449, 63555, 72987}
    try:
        ids = add_candidates(mongodb)
        print("received ids: ", ids)
        assert all(index in expected_ids for index in ids)
    finally:
        collection = mongodb[COLLECTION_NAME]
        collection.drop()


def test_fetch_functions():
    """Check the fetch functions."""
    db_config = DatabaseConfig(DB_NAME)
    mongodb = connect_to_db(db_config)
    ids = set(add_candidates(mongodb))
    try:
        # Fetch indices must be the same than the inserted objects indices
        data = list(fetch_many_from_collection(mongodb, COLLECTION_NAME, query={}))
        assert all(entry["_id"] in ids for entry in data)
        index = ids.pop()
        one = fetch_one_from_collection(mongodb, COLLECTION_NAME, query={"_id": index})
        assert index == one["_id"]
    finally:
        collection = mongodb[COLLECTION_NAME]
        collection.drop()
