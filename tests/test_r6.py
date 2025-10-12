import pytest
from library_service import search_books_in_catalog
from library_service import add_book_to_catalog

def test_search_title_partial_case_insensitive():
    """Partial, case-insensitive search by title should return matches."""
    results = search_books_in_catalog("test", "title")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "test" in results[0]["title"].lower() 

def test_search_author_partial_case_insensitive():
    """Partial, case-insensitive search by author should return matches."""
    add_book_to_catalog("Any Title", "Li", "abcdefghijklm", 1)
    
    results = search_books_in_catalog("li", "author")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "li" in results[0]["author"].lower()

def test_search_isbn_exact_match():
    """ISBN search should return exact matches only."""
    results = search_books_in_catalog("1234567890123", "isbn")
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(r["isbn"] == "1234567890123" for r in results)
    
def test_search_invalid_type_returns_empty_list():
    """Unknown search type should yield empty list."""
    results = search_books_in_catalog("anything", "unknown")
    assert isinstance(results, list)
    assert len(results) == 0

