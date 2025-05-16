#test_users_page.py (Playwright version)
import pytest
from pytest_check import check
from page_objects.admin_menu.users_page import UsersPage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.utils import get_browser_name, logger

@pytest.fixture
def users_page(logged_in_page):
    """
    Fixture that provides the Users page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[UsersPage]: A list of UsersPage objects for each logged-in browser instance
    """
    logger.debug("Staring users_page fixture")
    user_pages = []
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Users page on {get_browser_name(page)}")
        logger.info("=" * 80)

        # Navigate to Users page
        page.get_by_role("button", name="Admin").click()
        page.get_by_role("link", name="Users").click()
        
        # Create the page object
        users_page = UsersPage(page)
        
        # Verify that we're on the Users page
        if users_page.verify_page_title():
            logger.info("Successfully navigated to Users page")
            user_pages.append(users_page)
        else:
            logger.error(f"Failed to navigate to Users page on {get_browser_name(page)}")

    logger.info(f"users_page fixture: yielding {len(user_pages)} users page(s)")
    yield user_pages
    logger.debug("users_page fixture: finished")
    
class TestUsersPageUI(TestBasePageUI):
    
    @pytest.mark.UI 
    @pytest.mark.users
    def test_users_page_title(self, users_page):
        """
        Test that the Users page title is present.
        
        Args:
            users_page: The UsersPage fixture
        """
        logger.debug("Starting test_users_page_title")
        for up in users_page:
            title = up.verify_page_title()
            check.is_true(title, "Users title does not match")
            logger.info("Verification Successful :: Users Page Title found")
            
    @pytest.mark.UI 
    @pytest.mark.users
    @pytest.mark.navigation
    def test_users_page_nav_elements(self, users_page):
        """
        Test that all navigation elements are present on the Users page.
        
        Args:
            users_page: The UsersPage fixture
        """
        for up in users_page:
            all_elements, missing_elements = up.verify_all_nav_elements_present()
            check.is_true(all_elements, f"Missing navigation elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All navigation elements found")

    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.navigation
    def test_user_page_admin_elements(self, users_page):
        """
        Test that all admin elements are present in the Admin dropdown on the Users page.
        
        Args:
            users_page: The UsersPage fixture
        """
        for up in users_page:
            all_elements, missing_elements = up.verify_all_admin_links_present()
            check.is_true(all_elements, f"Missing admin elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All admin elements found")
    
    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.navigation
    def test_user_page_definition_elements(self, users_page):
        """
        Test that all definition elements are present in the Definitions dropdown on the Users page.
        
        Args:
            users_page: The UsersPage fixture
        """
        for up in users_page:
            all_elements, missing_elements = up.verify_all_definition_links_present()
            check.is_true(all_elements, f"Missing definition elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All definition elements found")
    
    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.table
    def test_users_page_action_elements(self, users_page):
        """
        Test that the Add User button is present on the Users page.
        
        Args:
            users_page: The UsersPage fixture
        """
        logger.debug("Starting test_users_page_action_elements")
        for up in users_page:
            all_elements, missing_elements = up.verify_action_elements_present()
            check.is_true(all_elements,  f"Users Add user link not found: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: Users Action Elements found")
            
    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.table
    def test_users_page_table_elements(self, users_page):
        """
        Test that all table elements are present on the Users page.
        
        Args:
            users_page: The UsersPage fixture
        """
        logger.debug("Starting test_users_page_table_elements")
        for up in users_page:
            all_elements, missing_elements = up.verify_all_users_table_elements_present()
            check.is_true(all_elements, f"Missing Users Table Elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: Users Table Elements found")