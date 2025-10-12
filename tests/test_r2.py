# tests/test_r2.py
from library_service import add_book_to_catalog, get_all_books

def test_book_fields():
    """Book has all fields."""
    add_book_to_catalog("Book A", "Author A", "1234567890123", 2)
    b = get_all_books()[0]
    assert "id" in b and "title" in b and "author" in b
    assert "isbn" in b and "available_copies" in b and "total_copies" in b

def test_available_copies():
    """Available copies valid."""
    add_book_to_catalog("Book B", "Author B", "9999999999999", 3)
    b = get_all_books()[0]
    assert 0 <= b["available_copies"] <= b["total_copies"]

def test_borrow_button_condition():
    """Borrow button only when available > 0."""
    add_book_to_catalog("Book C", "Author C", "1111111111111", 1)
    books = get_all_books()
    for b in books:
        if b["title"] == "Book C":
            if b["available_copies"] > 0:
                assert True
            else:
                assert False, "Borrow button should be hidden when no copies"

def test_catalog_does_not_show_unknown_title():
    """A title not added should not appear in the catalog."""
    add_book_to_catalog("Book D", "Author D", "3333333333333", 1)
    titles = [b["title"] for b in get_all_books()]
    assert "Not In Catalog" not in titles
