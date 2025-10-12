import pytest
from library_service import get_patron_status_report


def test_status_has_required_fields():
    """Report should include current loans, total fees, count, and history."""
    data = get_patron_status_report("123456")
    assert isinstance(data, dict)
    assert "currently_borrowed" in data
    assert "total_late_fees" in data
    assert "books_borrowed_count" in data
    assert "history" in data

def test_status_types_and_nonnegative():
    """Types should match spec; counts/fees non-negative."""
    data = get_patron_status_report("123456")
    assert isinstance(data["currently_borrowed"], list)
    assert isinstance(data["history"], list)
    assert isinstance(data["books_borrowed_count"], int)
    assert isinstance(data["total_late_fees"], (int, float))
    assert data["books_borrowed_count"] >= 0
    assert data["total_late_fees"] >= 0.0

def test_status_current_items_include_due_dates():
    """Each current loan should carry a due date field."""
    data = get_patron_status_report("123456")
    if data["currently_borrowed"]:
        item = data["currently_borrowed"][0]
        assert "due_date" in item

def test_status_count_matches_currently_borrowed_length():
    """Books borrowed count should match currently borrowed length."""
    data = get_patron_status_report("123456")
    assert data["books_borrowed_count"] == len(data["currently_borrowed"])
