"""
scripts/helper/db_helpers.py
============================
Database helper functions for Airflow DAGs.
Uses the Airflow PostgresHook to run queries against the configured connection.
"""

import logging
import pandas as pd

from airflow.providers.postgres.hooks.postgres import PostgresHook

log = logging.getLogger(__name__)


def get_hook(conn_id: str = "postgres_default") -> PostgresHook:
    """Return a PostgresHook for the given Airflow connection ID."""
    return PostgresHook(postgres_conn_id=conn_id)


def execute_query(sql: str, conn_id: str = "postgres_default", parameters: dict = None) -> None:
    """
    Execute a SQL statement (INSERT / UPDATE / DELETE / DDL) on the database.

    Args:
        sql:        SQL string to execute.
        conn_id:    Airflow connection ID (default: 'postgres_default').
        parameters: Optional dict of bind parameters.

    Example::

        from helper.db_helpers import execute_query
        from helper.utils import read_sql

        execute_query(read_sql("create_table.sql"))
    """
    hook = get_hook(conn_id)
    hook.run(sql, parameters=parameters)
    log.info("Executed query on connection '%s'.", conn_id)


def fetch_records(sql: str, conn_id: str = "postgres_default", parameters: dict = None) -> list:
    """
    Run a SELECT query and return results as a list of dicts.

    Args:
        sql:        SELECT SQL string.
        conn_id:    Airflow connection ID.
        parameters: Optional bind parameters.

    Returns:
        List of row dicts.

    Example::

        from helper.db_helpers import fetch_records

        rows = fetch_records("SELECT * FROM my_table WHERE status = %(status)s",
                             parameters={"status": "active"})
    """
    hook = get_hook(conn_id)
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(sql, parameters or {})
    columns = [desc[0] for desc in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    log.info("Fetched %d rows from connection '%s'.", len(rows), conn_id)
    return rows


def fetch_dataframe(sql: str, conn_id: str = "postgres_default", parameters: dict = None) -> pd.DataFrame:
    """
    Run a SELECT query and return results as a pandas DataFrame.

    Args:
        sql:        SELECT SQL string.
        conn_id:    Airflow connection ID.
        parameters: Optional bind parameters.

    Returns:
        pandas DataFrame.

    Example::

        from helper.db_helpers import fetch_dataframe

        df = fetch_dataframe("SELECT * FROM sales WHERE year = %(year)s",
                             parameters={"year": 2024})
    """
    hook = get_hook(conn_id)
    df = hook.get_pandas_df(sql, parameters=parameters)
    log.info("Fetched DataFrame with shape %s from connection '%s'.", df.shape, conn_id)
    return df
