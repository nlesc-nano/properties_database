import logging

from .__version__ import __version__
from .cli import main

logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = ["main"]
