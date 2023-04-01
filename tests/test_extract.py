from typing import Dict

import pytest

from stock_computing_service.extract.extract import RawStock, extract_stock

pytest_plugins = ("pytest_asyncio",)


class TestExtract:
    """Test data extraction part for stock computing"""

    @pytest.mark.asyncio
    async def test_extract(self):
        extracted_data: Dict[str, RawStock] = await extract_stock()
        assert isinstance(extracted_data, dict)

    # Todo: Add more validation
