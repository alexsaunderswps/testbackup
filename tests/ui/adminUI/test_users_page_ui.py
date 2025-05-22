#test_users_page.py (Playwright version)
import pytest
from pytest_check import check
from fixtures.admin_menu.users_fixtures import users_page
from utilities.utils import get_browser_name, logger

class TestUsersPageUI:
    
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
    def test_users_page_nav_elements(self, users_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Users page.
        
        Args:
            users_page: The UsersPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(users_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing navigation elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All navigation elements found")

    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.navigation
    def test_user_page_admin_elements(self, users_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Users page.
        
        Args:
            users_page: The UsersPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(users_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing admin elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All admin elements found")
    
    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.navigation
    def test_user_page_definition_elements(self, users_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Users page.
        
        Args:
            users_page: The UsersPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(users_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing definition elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All definition elements found")
    
    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.navigation
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