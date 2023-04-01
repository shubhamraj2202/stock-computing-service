""" Conftest"""
from __future__ import annotations

import json
from typing import Any, Dict

import pytest

from stock_computing_service.constants import TimeFunctions, TimeFunctionsMap
from stock_computing_service.extract.extract import RawStock
from stock_computing_service.helpers import sanetize_dict

# TODO: Make  it hashmap for storing multiple symbol
sample_raw_resp_filepath: str = "tests/resource/sample_response.json"
test_symbol = "IBM"


@pytest.fixture(scope="session")
def raw_response() -> Dict[str, Any]:
    """Returns sample raw response of stock data"""
    return {test_symbol: json.load(open(sample_raw_resp_filepath))}


@pytest.fixture(scope="session")
def extracted_data(raw_response: Dict[str, Any]) -> Dict[str, RawStock]:
    """Returns extracted stock data"""
    data: Dict[str, Any] = sanetize_dict(raw_response)
    return {
        symbol: RawStock(**stock_data)
        for symbol, stock_data in data.items()
        if TimeFunctionsMap[TimeFunctions.TIME_SERIES_WEEKLY] in stock_data
    }
