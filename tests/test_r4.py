import pytest
from library_service import return_book_by_patron
from library_service import borrow_book_by_patron

def test_return_valid():
    """Returning a borrowed book should succeed and mention returned."""
    borrow_book_by_patron("123456", 1)
    success, message = return_book_by_patron("123456", 1)
    assert success == True
    assert "returned" in message.lower()   
    
def test_return_invalid_patron_id():
    """Invalid patron ID should not succeed."""
    success, message = return_book_by_patron("12a456", 1)
    assert success == False

def test_return_not_borrowed():
    """If the patron didn't borrow this book, show an error."""
    success, message = return_book_by_patron("123456", 999)
    assert success == False
    assert "not borrowed" in message.lower() 

def test_return_shows_late_fee():
    """Late returns should display late fee information."""
    success, message = return_book_by_patron("123456", 1)
    assert "late" in message.lower() or "$" in message

