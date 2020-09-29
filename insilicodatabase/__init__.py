"""Library API."""
import logging

from .__version__ import __version__
from .interface import (DatabaseConfig, connect_to_db,
                        fetch_properties_from_collection)

logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = ["DatabaseConfig", "__version__", "connect_to_db", "fetch_properties_from_collection"]
