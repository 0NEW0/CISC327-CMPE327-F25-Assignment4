import pytest
from library_service import calculate_late_fee_for_book


def test_late_fee_response_schema():
    """API/service should return dict with fee and days."""
    data = calculate_late_fee_for_book("123456", 1)
    assert isinstance(data, dict)
    assert "fee_amount" in data
    assert "days_overdue" in data

def test_late_fee_numeric_and_capped():
    """fee is numeric and capped at $15.00 per book."""
    data = calculate_late_fee_for_book("123456", 1)
    assert isinstance(data["fee_amount"], (int, float))
    assert isinstance(data["days_overdue"], int)
    assert data["fee_amount"] <= 15.00

def test_late_fee_days_nonnegative():
    """Days overdue should not be negative."""
    data = calculate_late_fee_for_book("123456", 1)
    assert data["days_overdue"] >= 0
    
def test_late_fee_includes_status_message():
    """Response should include a status field."""
    data = calculate_late_fee_for_book("123456", 1)
    assert "status" in data

