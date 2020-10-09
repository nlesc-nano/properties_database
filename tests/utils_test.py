"""Functions use for testing."""

from pathlib import Path

import pkg_resources as pkg

__all__ = ["PATH_INSILICODATABASE", "PATH_TEST"]

# Environment data
PATH_INSILICODATABASE = Path(pkg.resource_filename('insilicodatabase', ''))
ROOT = PATH_INSILICODATABASE.parent

PATH_TEST = ROOT / "tests" / "files"
