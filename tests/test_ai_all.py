# tests/test_ai_all.py
import pytest
from datetime import datetime
from library_service import (
    add_book_to_catalog,
    borrow_book_by_patron,
    return_book_by_patron,
    calculate_late_fee_for_book,
    search_books_in_catalog,
    get_patron_status_report,
)
from database import get_book_by_isbn  # fetch book_id by ISBN


# --- R1: Catalog management ----------------------------------------------------

def test_r1_add_book_valid_then_duplicate():
    # Use a fixed ISBN. If it already exists from a previous run, the first insert may fail,
    # but the second insert must fail with a duplicate message.
    isbn = "8000000000000"
    add_book_to_catalog("Clean Code", "Robert Martin", isbn, 2)
    ok2, msg2 = add_book_to_catalog("Another Title", "Bob", isbn, 1)  # duplicate ISBN
    assert ok2 is False and "exists" in msg2.lower()


@pytest.mark.parametrize(
    "title,author,isbn,copies,expect_substr",
    [
        ("", "A",        "8000000000001", 1, "title"),
        ("A", "",        "8000000000002", 1, "author"),
        ("A"*201, "B",   "8000000000003", 1, "title"),
        ("A", "B"*101,   "8000000000004", 1, "author"),
        ("A", "B",       "123",           1, "13"),       # ISBN must be 13 digits
        ("A", "B",       "8000000000005", 0, "positive"), # copies must be positive
    ],
)
def test_r1_add_book_validation_errors(title, author, isbn, copies, expect_substr):
    ok, msg = add_book_to_catalog(title, author, isbn, copies)
    assert ok is False and expect_substr in msg.lower()


# --- R3: Borrow ----------------------------------------------------------------

def test_r3_borrow_valid_flow_smoke():
    isbn = "8000000000010"
    add_book_to_catalog("Domain-Driven Design", "Eric Evans", isbn, 1)
    rec = get_book_by_isbn(isbn)
    book_id = rec["id"]
    ok, msg = borrow_book_by_patron("123456", book_id)
    assert isinstance(ok, bool) and isinstance(msg, str)


def test_r3_borrow_invalid_patron_id():
    isbn = "8000000000011"
    add_book_to_catalog("Refactoring", "Martin Fowler", isbn, 1)
    rec = get_book_by_isbn(isbn)
    book_id = rec["id"]
    ok, msg = borrow_book_by_patron("12a456", book_id)
    assert ok is False and "invalid" in msg.lower()


# --- R4: Return ----------------------------------------------------------------

def test_r4_return_valid_includes_tokens():
    isbn = "8000000000020"
    add_book_to_catalog("Effective Python", "Brett Slatkin", isbn, 1)
    rec = get_book_by_isbn(isbn)
    book_id = rec["id"]

    # use a fresh patron id to avoid hitting borrow limit from previous tests
    patron = "111111"

    ok_borrow, _ = borrow_book_by_patron(patron, book_id)
    assert ok_borrow is True  # ensure the borrow actually happened

    ok, msg = return_book_by_patron(patron, book_id)
    assert ok is True
    assert "returned" in msg.lower()
    assert ("late" in msg.lower()) or ("$" in msg)



def test_r4_return_not_borrowed_branch():
    # Sentinel book_id that should always mean "not borrowed" per tests/spec
    ok, msg = return_book_by_patron("123456", 999)
    assert ok is False and "not borrowed" in msg.lower()


# --- R5: Late fee --------------------------------------------------------------

def test_r5_late_fee_schema_and_bounds():
    # We only check the response shape and bounds here
    data = calculate_late_fee_for_book("123456", 1)
    assert set(data.keys()) >= {"fee_amount", "days_overdue", "status"}
    assert isinstance(data["fee_amount"], (int, float)) and data["fee_amount"] <= 15.0
    assert isinstance(data["days_overdue"], int) and data["days_overdue"] >= 0
    assert data["status"] in {"on-time", "late"}


# --- R6: Search ----------------------------------------------------------------

def test_r6_search_title_author_isbn_end_to_end():
    isbn = "8000000000030"
    add_book_to_catalog("Test Driven Development", "Li Hua", isbn, 1)

    # title: case-insensitive partial match
    res_t = search_books_in_catalog("driven", "title")
    assert isinstance(res_t, list) and len(res_t) >= 1
    assert any("driven" in r.get("title", "").lower() for r in res_t)

    # author: case-insensitive partial match
    res_a = search_books_in_catalog("li", "author")
    assert isinstance(res_a, list) and len(res_a) >= 1
    assert any("li" in r.get("author", "").lower() for r in res_a)

    # isbn: exact match
    res_i = search_books_in_catalog(isbn, "isbn")
    assert isinstance(res_i, list) and len(res_i) >= 1
    assert all(r.get("isbn") == isbn for r in res_i)


def test_r6_invalid_type_returns_empty_list():
    res = search_books_in_catalog("anything", "unknown")
    assert isinstance(res, list) and len(res) == 0


# --- R7: Status report ---------------------------------------------------------

def test_r7_status_report_shape_and_consistency():
    rep = get_patron_status_report("123456")
    assert set(rep.keys()) == {
        "currently_borrowed",
        "history",
        "books_borrowed_count",
        "total_late_fees",
    }
    assert isinstance(rep["currently_borrowed"], list)
    assert isinstance(rep["history"], list)
    assert isinstance(rep["books_borrowed_count"], int)
    assert isinstance(rep["total_late_fees"], (int, float))
    assert rep["books_borrowed_count"] == len(rep["currently_borrowed"])
