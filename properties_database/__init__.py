import logging

from .__version__ import __version__
from .cli import main
from .interface.mongodb_interface import (DatabaseConfig, connect_to_db,
                                          fetch_properties_from_collection)

logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = ["DatabaseConfig", "connect_to_db", "fetch_properties_from_collection",  "main"]
