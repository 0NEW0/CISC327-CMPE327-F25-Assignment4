import pytest
from library_service import add_book_to_catalog


def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    assert success == False
    assert "13 digits" in message

def test_add_book_title_missing():
    """Title is required."""
    success, message = add_book_to_catalog("", "Author", "1234567890123", 5)
    assert success == False
    assert "title" in message.lower()

def test_add_book_title_too_long():
    """Title > 200 characters should fail."""
    long_title = "A" * 201
    success, message = add_book_to_catalog(long_title, "Author", "1234567890123", 5)
    assert success == False
    assert "title" in message.lower()

def test_add_book_author_missing():
    """Author is required."""
    success, message = add_book_to_catalog("Book", "", "1234567890123", 5)
    assert success == False
    assert "author" in message.lower()

def test_add_book_author_too_long():
    """Author > 100 characters should fail."""
    long_author = "B" * 101
    success, message = add_book_to_catalog("Book", long_author, "1234567890123", 5)
    assert success == False
    assert "author" in message.lower()

def test_add_book_isbn_not_all_digits():
    """ISBN must be exactly 13 digits (not letters)."""
    success, message = add_book_to_catalog("Book", "Author", "12345abc90123", 5)
    assert success == False
    assert "13 digits" in message

def test_add_book_isbn_too_long():
    """ISBN > 13 digits should fail."""
    success, message = add_book_to_catalog("Book", "Author", "12345678901234", 5)
    assert success == False
    assert "13 digits" in message

def test_add_book_total_copies_zero():
    """Total copies must be positive."""
    success, message = add_book_to_catalog("Book", "Author", "1234567890123", 0)
    assert success == False
    assert "positive" in message.lower()

def test_add_book_total_copies_negative():
    """Total copies must be positive."""
    success, message = add_book_to_catalog("Book", "Author", "1234567890123", -2)
    assert success == False
    assert "positive" in message.lower()

def test_add_book_total_copies_not_integer():
    """Total copies must be a positive integer."""
    success, message = add_book_to_catalog("Book", "Author", "1234567890123", "five")
    assert success == False
    assert "positive integer" in message.lower()
