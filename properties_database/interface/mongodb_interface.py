"""Module to create, query and update a Mongodb.

API
---
.. autoclass:: DatabaseConfig
.. autofunction:: store_dataframe_in_mongo

"""

from typing import List, NamedTuple, Optional

from pymongo import MongoClient

from ..dataframe import read_data_from_csv, sanitize_dataframe


class DatabaseConfig(NamedTuple):
    """Data to store the database configuration."""

    db_name: str
    host: Optional[str] = "localhost"
    port: Optional[int] = 27017


def store_dataframe_in_mongo(db_config: DatabaseConfig, collection_name: str, path_csv: str, clean: bool = True) -> List[int]:
    """Store a pandas dataframe in the database specified in `db_config`.

    Parameters
    ----------
    db_config
        Database configuration
    collection_name
        Collection name
    path_df
        Path to the csv file containing the data
    
    Returns
    -------
    List of the inserted objects indices

    """
    db = connect_to_db(db_config)
    collection = db[collection_name]
    df = read_data_from_csv(path_csv)
    if clean:
        df = sanitize_dataframe(df)

    return collection.insert_many(df.to_dict("records")).inserted_ids


def connect_to_db(db_config: DatabaseConfig) -> MongoClient:
    """Connect to a mongodb using `db_config`."""
    client = MongoClient(db_config.host, db_config.port)
    db = client[db_config.db_name]

    return db
