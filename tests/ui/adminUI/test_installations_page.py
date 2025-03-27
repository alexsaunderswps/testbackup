#test_installations_page.py
import pytest
from pytest_check import check
from page_objects.admin_menu.installations_page import InstallationsPage
from page_objects.common.base_page import BasePage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def installations_page(logged_in_browser):
    logger.debug("Staring installations_page fixture")
    installation_pages = []
    for installation_page in logged_in_browser:
        driver = installation_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Installations page on {driver.name}")
        logger.info("=" * 80)
        
        #Navigate to Installations page
        base_page.click_admin_button()
        base_page.go_installations_page()
        # Verify that we're on the Installations page
        installations_page = InstallationsPage(driver)
        if installations_page.verify_page_title_present():
            logger.info("Successfully navigated to Installations page")
            installation_pages.append(installations_page)
        else:
            logger.error(f"Failed to navigate to Installations page on {driver.name}")
            
    logger.info(f"installations_page fixture: yielding {len(installation_pages)} installations page(s)")
    yield installation_pages
    logger.debug("installations_page fixture: finished")
    
class TestInstallationsPageUI(TestBasePageUI):
    
    @pytest.mark.UI 
    @pytest.mark.installations
    def test_installations_page_title(self, installations_page):
        """_summary_

        Args:
            installations_page (_type_): _description_
        """
        logger.debug("Starting test_installations_page_title")
        for ip in installations_page:
            title = ip.verify_page_title_present()
            check.equal(title, True, "Installations title does not match")
            logger.info("Verification Successful :: Installations Page Title found")
            
    @pytest.mark.UI 
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_nav_elements(self, installations_page):
        """_summary_

        Args:
            installations_page (_type_): _description_
        """
        assert self._verify_page_nav_elements(installations_page)
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_admin_elements(self, installations_page):
        """_summary_

        Args:
            installations_page (_type_): _description_
        """
        assert self._verify_page_admin_elements(installations_page)
    
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_definition_elements(self, installations_page):
        """_summary_

        Args:
            installations_page (_type_): _description_
        """
        assert self._verify_page_definition_elements(installations_page)
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.search
    def test_installations_search_elements(self, installations_page):
        """_summary_

        Args:
            installations_page (_type_): _description_
        """
        for ip in installations_page:
            all_elements, missing_elements = ip.verify_all_installations_search_elements_present()
            check.is_true(all_elements, f"Missing installations search elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Installations Search Elements found")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.table
    def test_installations_table_elements(self, installations_page):
        """_summary_

        Args:
            installations_page (_type_): _description_
        """
        for ip in installations_page:
            all_elements, missing_elements = ip.verify_all_installation_table_elements_present()
            check.is_true(all_elements, f"Missing installations table elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Installations Table Elements found")
            
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.pagination
    def test_installations_pagination_elements(self, installations_page):
        """_summary_

        Args:
            installations_page (_type_): _description_
        """
        assert self._verify_page_pagination_elements(installations_page)