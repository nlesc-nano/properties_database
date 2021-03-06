"""Module to create, query and update a Mongodb.

API
---
.. autoclass:: DatabaseConfig
.. autofunction:: connect_to_db
.. autofunction:: fetch_many_from_collection
.. autofunction:: fetch_one_from_collection
.. autofunction:: store_many_in_collection
.. autofunction:: store_one_in_collection
.. autofunction:: store_dataframe_in_mongo
.. autofunction:: update_one_in_collection
.. autofunction:: update_many_in_collection

"""

__all__ = ["DatabaseConfig", "connect_to_db",
           "fetch_many_from_collection",
           "fetch_one_from_collection",
           "store_many_in_collection",
           "store_one_in_collection",
           "store_dataframe_in_mongo",
           "update_one_in_collection",
           "update_many_in_collection"
           ]

from typing import Any, Dict, Iterable, List, NamedTuple, Optional

import pandas as pd
from pymongo import MongoClient
from pymongo.database import Database


class DatabaseConfig(NamedTuple):
    """Data to store the database configuration."""
    db_name: str
    host: Optional[str] = "localhost"
    port: Optional[int] = 27017
    username: Optional[str] = None
    password: Optional[str] = None


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
    client = MongoClient(
        host=db_config.host, port=db_config.port,
        username=db_config.username, password=db_config.password)

    return client[db_config.db_name]


def fetch_many_from_collection(
        mongodb: Database, collection_name: str, query: Dict[str, str] = {}) -> Iterable[Any]:
    """Return the data stored in a given collection."""
    collection = mongodb[collection_name]
    return collection.find(query)


def fetch_one_from_collection(
        mongodb: Database, collection_name: str, query: Dict[str, str] = {}) -> Iterable[Any]:
    """Return a single entry stored in a given collection."""
    collection = mongodb[collection_name]
    return collection.find_one(query)


def store_many_in_collection(
        mongodb: Database, collection_name: str, data: List[Dict[str, Any]]) -> List[int]:
    """Store the given ``data`` array into ``collection_name`` in ``db``.

    Returns
    -------
    List of Object identifiers

    """
    collection = mongodb[collection_name]
    return collection.insert_many(data).inserted_ids


def store_one_in_collection(
        mongodb: Database, collection_name: str, data: Dict[str, Any]) -> int:
    """Store the given ``data`` Dict into ``collection_name`` in ``db``.

    Returns
    -------
    List of Object identifiers

    """
    collection = mongodb[collection_name]
    return collection.insert_one(data).inserted_id


def update_one_in_collection(
        mongodb: Database, collection_name: str, query: Dict[str, Any],
        update: Dict[str, Any]) -> None:
    """Update one from ``collection_name`` entry that matches ``query`` using ``update``."""
    collection = mongodb[collection_name]
    collection.update_one(query, update)


def update_many_in_collection(
        mongodb: Database, collection_name: str, query: Dict[str, Any],
        update: Dict[str, Any]) -> None:
    """Update many from ``collection_name`` entry that matches ``query`` using ``update``."""
    collection = mongodb[collection_name]
    collection.update_many(query, update)


def store_dataframe_in_mongo(
        mongodb: MongoClient, collection_name: str, path_csv: str) -> List[int]:
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
    data = pd.read_csv(path_csv, index_col=0)
    data.reset_index(inplace=True)
    data.rename(columns={"index": "_id"}, inplace=True)

    return store_many_in_collection(mongodb, collection_name, data.to_dict("records"))
