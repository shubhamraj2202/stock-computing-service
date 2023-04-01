from typing import List

from stock_computing_service.helpers import _map
from stock_computing_service.transform.transform import FinancialData, transform


class TestTransform:
    """Test Data Transformation of the Service"""

    def test_transform(self, extracted_data):
        transformed_data: List[FinancialData] = transform(extracted_data)

        def _assert(data):
            assert isinstance(data, FinancialData)

        _map(lambda data: _assert(data), transformed_data)

    # Todo: Add more validation
