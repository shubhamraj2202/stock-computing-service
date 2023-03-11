""" Contains logic to Sync Finanical data into Database"""
from __future__ import annotations

from typing import Dict, List

from stock_computing_service.database import upsert_all
from stock_computing_service.extract.extract import RawStock, extract_stock
from stock_computing_service.transform.transform import FinancialData, transform


async def sync() -> List[FinancialData]:
    """Extract/Transforms/Load the finaical data into DB"""
    extracted_data: Dict[str, RawStock] = await extract_stock()
    transformed_data: List[FinancialData] = transform(extracted_data)
    await upsert_all(transformed_data, all_at_once=False)
    return transformed_data
