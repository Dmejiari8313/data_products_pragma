"""Application configuration for the Movies EDA dashboard.

Centralizes the configurable CSV path resolution and the default values used by
the presentation controls, so no module hard-codes these settings.
"""

from __future__ import annotations

import os
from pathlib import Path

#: Environment variable used to override the dataset path.
CSV_PATH_ENV_VAR: str = "MOVIES_CSV_PATH"

#: Default dataset file name, resolved against the repository root.
DEFAULT_CSV_FILENAME: str = "movies.csv"

#: Default number of categories to show in the "Top N" rankings.
DEFAULT_TOP_N: int = 10

#: Minimum and maximum selectable values for the "Top N" control.
TOP_N_MIN: int = 5
TOP_N_MAX: int = 30


def get_repo_root() -> Path:
    """Return the repository root directory.

    The root is resolved as the parent of the ``src`` directory that contains
    this package.

    Returns
    -------
    pathlib.Path
        Absolute path to the repository root.
    """
    return Path(__file__).resolve().parents[2]


def get_csv_path() -> Path:
    """Resolve the dataset CSV path.

    The path is read from the :data:`CSV_PATH_ENV_VAR` environment variable when
    set; otherwise it falls back to :data:`DEFAULT_CSV_FILENAME` located at the
    repository root.

    Returns
    -------
    pathlib.Path
        Absolute path to the CSV dataset to load.
    """
    env_value = os.environ.get(CSV_PATH_ENV_VAR)
    if env_value:
        return Path(env_value).expanduser().resolve()
    return get_repo_root() / DEFAULT_CSV_FILENAME
