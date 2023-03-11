""" Projects constants """
from __future__ import annotations

import os
from enum import Enum

SYMBOLS = ["IBM", "AAPL"]
API_KEY = os.environ.get("FINANCIAL_KEY", "demo")


class DatabaseEnum(str, Enum):
    NAME = "stock_computing"
    SERVER = f"postgresql://postgres:postgres@db:5432/stock_computing"
    HOST = "db"
    USER = "postgres"
    PASSWORD = "postgres"
    DEFAULT = "postgres"
    DRIVER = "postgresql"
    PORT = 5432
    ISOLATION_LEVEL = "AUTOCOMMIT"


# DB = "sqlite:///financial_data.db"


class TimeFunctions(str, Enum):
    TIME_SERIES_WEEKLY = "TIME_SERIES_WEEKLY"


TimeFunctionsMap = {TimeFunctions.TIME_SERIES_WEEKLY: "WeeklyTimeSeries"}
