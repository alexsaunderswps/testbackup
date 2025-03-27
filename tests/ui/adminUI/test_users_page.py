#test_users_page.py
import pytest
from pytest_check import check
from page_objects.admin_menu.users_page import UsersPage
from page_objects.common.base_page import BasePage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def users_page(logged_in_browser):
    logger.debug("Staring users_page fixture")
    user_pages = []
    for user_page in logged_in_browser:
        driver = user_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Users page on {driver.name}")
        logger.info("=" * 80)
        
        #Navigate to Users page
        base_page.click_admin_button()
        base_page.go_users_page()
        # Verify that we're on the Users page
        users_page = UsersPage(driver)
        if users_page.verify_page_title_present():
            logger.info("Successfully navigated to Users page")
            user_pages.append(users_page)
        else:
            logger.error(f"Failed to navigate to Users page on {driver.name}")
            
    logger.info(f"users_page fixture: yielding {len(user_pages)} users page(s)")
    yield user_pages
    logger.debug("users_page fixture: finished")
    
class TestUsersPageUI(TestBasePageUI):
    
    @pytest.mark.UI 
    @pytest.mark.users
    def test_users_page_title(self, users_page):
        """_summary_

        Args:
            users_page (_type_): _description_
        """
        logger.debug("Starting test_users_page_title")
        for up in users_page:
            title = up.verify_page_title_present()
            check.equal(title, True, "Users title does not match")
            logger.info("Verification Successful :: Users Page Title found")
            
    @pytest.mark.UI 
    @pytest.mark.users
    @pytest.mark.navigation
    def test_users_page_nav_elements(self, users_page):
        """_summary_

        Args:
            users_page (_type_): _description_
        """
        assert self._verify_page_nav_elements(users_page)
    
    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.navigation
    def test_user_page_admin_elements(self, users_page):
        """_summary_

        Args:
            users_page (_type_): _description_
        """
        assert self._verify_page_admin_elements(users_page)
    
    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.navigation
    def test_user_page_definition_elements(self, users_page):
        """_summary_

        Args:
            users_page (_type_): _description_
        """
        assert self._verify_page_definition_elements(users_page)
    
    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.table
    def test_users_page_search_elements(self, users_page):
        """_summary_

        Args:
            users_page (_type_): _description_
        """
        logger.debug("Starting test_users_page_search_elements")
        for up in users_page:
            all_elements, missing_elements = up.verify_add_user_link_present()
            check.is_true(all_elements,  f"Users Add user link not found: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: Users Action Elements found")
            
    @pytest.mark.UI
    @pytest.mark.users
    @pytest.mark.table
    def test_users_page_table_elements(self, users_page):
        """_summary_

        Args:
            users_page (_type_): _description_
        """
        logger.debug("Starting test_users_page_table_elements")
        for up in users_page:
            all_elements, missing_elements = up.verify_all_users_table_elements_present()
            check.is_true(all_elements, f"Missing Users Table Elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: Users Table Elements found")