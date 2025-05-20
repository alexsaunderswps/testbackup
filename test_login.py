#test_login.py

import pytest

def test_successful_login(logged_in_page):
    """
    Verify that the logged_in_page fixture is working correcly by checking for elements that should only be visible after successful login.
    """
    for page in logged_in_page:
        # Check that logout button is visible (confirming that we've logged in)
        assert page.get_by_role("button", name="LOG OUT").is_visible(), "Not logged in - logout button is not visible"
        print("Login Test passed successfully.")