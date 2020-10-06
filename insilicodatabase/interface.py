"""Module to create, query and update a Mongodb.

API
---
.. autoclass:: DatabaseConfig
.. autofunction:: connect_to_db
.. autofunction:: fetch_properties_from_collection
.. autofunction:: fetch_one_from_collection
.. autofunction:: store_data_in_collection
.. autofunction:: store_dataframe_in_mongo

"""

__all__ = ["DatabaseConfig", "connect_to_db",
           "fetch_data_from_collection",
           "fetch_properties_from_collection",
           "store_data_in_collection",
           "store_dataframe_in_mongo"]

from typing import Any, Dict, Iterable, List, Mapping, NamedTuple, Optional

from pymongo import MongoClient
from pymongo.database import Database

from .dataframe import read_data_from_csv, sanitize_dataframe


class DatabaseConfig(NamedTuple):
    """Data to store the database configuration."""

    db_name: str
    host: Optional[str] = "localhost"
    port: Optional[int] = 27017


def connect_to_db(db_config: DatabaseConfig) -> MongoClient:
    """Connect to a mongodb using `db_config`.

    Parameters
    ----------
    db_config
        NamedTuple with the configuration to connect to the database

    Returns
    -------
        MongoClient

    """
    client = MongoClient(db_config.host, db_config.port)

    return client[db_config.db_name]


def fetch_data_from_collection(
        mongodb: Database, collection_name: str, query: Dict[str, str] = {}) -> Iterable[Any]:
    """Return the data stored in a given collection."""
    collection = mongodb[collection_name]
    return collection.find(query)


def fetch_one_from_collection(
        mongodb: Database, collection_name: str, query: Dict[str, str] = {}) -> Iterable[Any]:
    """Return a single entry stored in a given collection."""
    collection = mongodb[collection_name]
    return collection.find_one(query)


def store_data_in_collection(
        mongodb: Database, collection_name: str, data: Mapping[str, Any]) -> int:
    """Store the given ``data`` into ``collection_name`` in ``db``."""
    collection = mongodb[collection_name]
    entry = collection.find_one({"_id": data["_id"]})
    if entry is not None:
        return entry["_id"]

    return collection.insert_one(data).inserted_id


def store_dataframe_in_mongo(
        db_config: DatabaseConfig, collection_name: str, path_csv: str,
        clean: bool = True) -> List[int]:
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
