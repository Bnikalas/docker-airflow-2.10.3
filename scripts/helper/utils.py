"""
scripts/helper/utils.py
=======================
General-purpose utility functions for Airflow DAGs.
"""

import os
import logging

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/usr/local/airflow")
DATA_DIR     = os.path.join(AIRFLOW_HOME, "data")
SQL_DIR      = os.path.join(AIRFLOW_HOME, "scripts", "sql")


def get_data_path(filename: str) -> str:
    """Return the absolute path to a file inside the data directory."""
    path = os.path.join(DATA_DIR, filename)
    log.debug("Resolved data path: %s", path)
    return path


def get_sql_path(filename: str) -> str:
    """Return the absolute path to a SQL script inside the sql directory."""
    path = os.path.join(SQL_DIR, filename)
    log.debug("Resolved SQL path: %s", path)
    return path


# ---------------------------------------------------------------------------
# SQL helpers
# ---------------------------------------------------------------------------

def read_sql(filename: str) -> str:
    """
    Read and return the contents of a SQL file from the sql directory.

    Args:
        filename: Name of the .sql file (e.g. 'load_users.sql')

    Returns:
        SQL string ready to be executed.

    Example::

        from helper.utils import read_sql

        sql = read_sql("load_users.sql")
    """
    path = get_sql_path(filename)
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    log.info("Loaded SQL from: %s", path)
    return sql


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def list_data_files(extension: str = None) -> list:
    """
    List all files in the data directory, optionally filtered by extension.

    Args:
        extension: File extension to filter by (e.g. '.csv', '.json').
                   If None, returns all files.

    Returns:
        List of filenames (not full paths).
    """
    files = os.listdir(DATA_DIR)
    if extension:
        files = [f for f in files if f.endswith(extension)]
    return sorted(files)


def read_data_file(filename: str) -> str:
    """Read and return the raw text content of a file in the data directory."""
    path = get_data_path(filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
