from playwright.sync_api import sync_playwright

# Flask base URL
BASE_URL = "http://127.0.0.1:5000"

# Automate at least two realistic user flow：
# i. Add a new book to the catalog (fill title, author, ISBN, copies)
# ii. Verify the book appears in the catalog


def test_add_book_flow():
    # i. Add a new book to the catalog (fill title, author, ISBN, copies)
    # ii. Verify the book appears in the catalog
    test_title = "E2E Test Book"
    test_author = "Test Author"
    test_isbn = "1234567890123"   # 13 digits, passes validation
    test_total_copies = "5"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # i. Add a new book to the catalog (fill title, author, ISBN, copies)
        page.goto(f"{BASE_URL}/add_book")
        page.fill('input[name="title"]', test_title)
        page.fill('input[name="author"]', test_author)
        page.fill('input[name="isbn"]', test_isbn)
        page.fill('input[name="total_copies"]', test_total_copies)
        page.press('input[name="total_copies"]', "Enter")
        
         # ii. Verify the book appears in the catalog
        page.wait_for_timeout(1000)
        page.goto(f"{BASE_URL}/catalog")
        body_text = page.text_content("body")
        
        assert test_title in body_text

        browser.close()


def test_catalog_page_loads():
    """Include assertions verifying that expected UI elements/text appear. """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/catalog")
        assert page.url.endswith("/catalog")

        body_text = page.text_content("body")
        assert "Book Catalog" in body_text
        assert "The Great Gatsby" in body_text

        browser.close()

