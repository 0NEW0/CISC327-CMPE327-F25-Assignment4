import library_service as svc
from library_service import borrow_book_by_patron

def _book(avail=1):
    return {"id": 1, "title": "Alpha", "available_copies": avail}

def test_valid(monkeypatch):
    """Valid borrow should succeed."""
    mp = monkeypatch.setattr
    mp(svc, "get_book_by_id", lambda _:_book(2))
    mp(svc, "get_patron_borrow_count", lambda _ : 3)
    mp(svc, "insert_borrow_record", lambda *_: True)
    mp(svc, "update_book_availability", lambda *_: True)
    ok, msg = borrow_book_by_patron("123456", 1)
    assert ok and "due date" in msg.lower()

def test_bad_patron_len():
    """Patron ID must be 6 digits."""
    ok, msg = borrow_book_by_patron("12345", 1)
    assert not ok and "6" in msg

def test_bad_patron_nondigit():
    """Patron ID must be digits only."""
    ok, msg = borrow_book_by_patron("12a456", 1)
    assert not ok and ("6" in msg or "invalid" in msg.lower())

def test_book_not_found(monkeypatch):
    """Book must exist."""
    monkeypatch.setattr(svc, "get_book_by_id", lambda _ : None)
    ok, msg = borrow_book_by_patron("123456", 99)
    assert not ok and "not found" in msg.lower()

def test_not_available(monkeypatch):
    """Book must have available copies > 0."""
    monkeypatch.setattr(svc, "get_book_by_id", lambda _ : _book(0))
    ok, msg = borrow_book_by_patron("123456", 1)
    assert not ok and "available" in msg.lower()

def test_limit_gt_5_blocks(monkeypatch):
    """Over 5 books should be blocked."""
    mp = monkeypatch.setattr
    mp(svc, "get_book_by_id", lambda _ : _book(1))
    mp(svc, "get_patron_borrow_count", lambda _ : 6)
    ok, msg = borrow_book_by_patron("123456", 1)
    assert not ok and ("limit" in msg.lower() or "5" in msg)

def test_insert_fail(monkeypatch):
    """Insert record failure should return error."""
    mp = monkeypatch.setattr
    mp(svc, "get_book_by_id", lambda _ : _book(1))
    mp(svc, "get_patron_borrow_count", lambda _ : 1)
    mp(svc, "insert_borrow_record", lambda *_: False)
    ok, msg = borrow_book_by_patron("123456", 1)
    assert not ok and ("create" in msg.lower() or "database" in msg.lower())

def test_update_fail(monkeypatch):
    """Availability update failure should return error."""
    mp = monkeypatch.setattr
    mp(svc, "get_book_by_id", lambda _ : _book(1))
    mp(svc, "get_patron_borrow_count", lambda _ : 1)
    mp(svc, "insert_borrow_record", lambda *_: True)
    mp(svc, "update_book_availability", lambda *_: False)
    ok, msg = borrow_book_by_patron("123456", 1)
    assert not ok and ("availability" in msg.lower() or "database" in msg.lower())
