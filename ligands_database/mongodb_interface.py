"""Module to create, query and update a Mongodb."""

from pymongo import MongoClient
from typing import NamedTuple, Optional
import pandas as pd


class DatabaseConfig(NamedTuple):
    """Data to store the database configuration."""

    db_name: str
    host: Optional[str]
    port: Optional[int]


def store_in_db(db_config: DatabaseConfig, collection_name: str, df: pd.DataFrame) -> object:
    """Store a pandas `df` in the database specified in `db_config`."""
    db = connect_to_db(db_config)
    collection = db[collection_name]
    return collection.insert_one(df.to_dict()).inserted_id


def connect_to_db(db_config: DatabaseConfig) -> MongoClient:
    """Connect to a mongodb using `db_config`."""
    client = MongoClient(db_config.host, db_config.port)
    db = client[db_config.db_name]

    return db
