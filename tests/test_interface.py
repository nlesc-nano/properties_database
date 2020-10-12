"""Module to test the interface to Mongodb."""


from typing import List

import numpy as np
from pymongo import MongoClient

from insilicodatabase.interface import (DatabaseConfig, connect_to_db,
                                        fetch_many_from_collection,
                                        fetch_one_from_collection,
                                        store_dataframe_in_mongo,
                                        store_one_in_collection,
                                        update_many_in_collection,
                                        update_one_in_collection)

from .utils_test import PATH_TEST

DB_NAME = "test_mutations"
COLLECTION_NAME = "candidates"


def add_candidates(mongodb: MongoClient) -> List[int]:
    """Check that the interface is working."""
    # read data from file
    path_data = PATH_TEST / "candidates.csv"

    return store_dataframe_in_mongo(mongodb, COLLECTION_NAME, path_data)


def get_client():
    """Return client to MongoDB."""
    db_config = DatabaseConfig(DB_NAME)
    return connect_to_db(db_config)


def test_one_insertion():
    """Check that a single entry is stored correctly."""
    mongodb = get_client()

    index = 314159265
    data = {"_id": index, "value": "foo", "bar": "tux"}

    try:
        reply = store_one_in_collection(mongodb, COLLECTION_NAME, data)
        assert index == reply
    finally:
        collection = mongodb[COLLECTION_NAME]
        collection.drop()


def test_many_insertions():
    """Check that the interface is working."""
    # Connect to the database
    mongodb = get_client()

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
    mongodb = get_client()
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


def test_update_many():
    """Check the update functions."""
    mongodb = get_client()
    ids = add_candidates(mongodb)
    pi = 3.14159265
    golden = 1.618
    query_one = {"_id": {"$eq": ids[0]}}
    query_many = {"_id": {"$in": ids}}
    try:
        # Update all the entries
        update_many_in_collection(mongodb, COLLECTION_NAME, query_many, {"$set": {"scscore": pi}})
        data = list(fetch_many_from_collection(mongodb, COLLECTION_NAME, query=query_many))
        assert all(np.isclose(entry["scscore"], pi) for entry in data)

        # Update a single entry
        update_one_in_collection(mongodb, COLLECTION_NAME, query_one, {"$set": {"scscore": golden}})
        one = fetch_one_from_collection(mongodb, COLLECTION_NAME, query_one)
        assert np.isclose(one["scscore"], golden)

    finally:
        collection = mongodb[COLLECTION_NAME]
        collection.drop()
