"""
Lightweight Postgres connection helper.
"""
from typing import Any, Mapping, Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

import config

_engine: Optional[Engine] = None


def get_engine() -> Engine:
    """Create (or reuse) a SQLAlchemy engine using the configured connection string."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            config.POSTGRES_CONNECTION_STRING,
            pool_pre_ping=True,
        )
    return _engine


def run_query(query: str, params: Optional[Mapping[str, Any]] = None) -> pd.DataFrame:
    """
    Execute a SQL query and return the results as a DataFrame.

    Args:
        query: Raw SQL string to execute.
        params: Optional mapping of parameters.
    """
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params)

