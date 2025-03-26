#test_iucnstatus_page_ui.py
import pytest
from pytest_check import check 
from page_objects.definitions_menu.iucn_status_page import IUCNStatusPage
from page_objects.common.base_page import BasePage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def iucnstatus_page(logged_in_browser):
    """_summary_

    Args:
        logged_in_browser (_type_): _description_
    """
    logger.debug("Starting iucnstatus_page fixture")
    iucnstatus_pages = []
    for login_page in logged_in_browser:
        driver = login_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to IUCN Status page on {driver.name}")
        logger.info("=" * 80)
        
        # Navigate to IUCN Status page
        base_page.click_definitions_button()
        base_page.go_iucnstatus_page()
        # Verfify that we're on the IUCN Status page
        iucnstatus_page = IUCNStatusPage(driver)
        if iucnstatus_page.verify_iucn_page_title_present():
            logger.info("Successfully navigated to IUCN Status page")
            iucnstatus_pages.append(iucnstatus_page)
        else:
            logger.error(f"Failed to navigate to IUCN Status page on {driver.name}")
            
    logger.info(f"iucnstatus_page fixture: yielding {len(iucnstatus_pages)} iucnstatus page(s)")
    yield iucnstatus_pages
    logger.debug("iucnstatus_page fixture: finished")
    
class TestIUCNStatusPageUI(TestBasePageUI):
    
    @pytest.mark.UI 
    @pytest.mark.iucn_status
    def test_iucnstatus_page_title(self, iucnstatus_page):
        """_summary_

        Args:
            iucnstatus_page (_type_): _description_
        """
        logger.debug("Starting test_iucnstatus_page_title")
        for ip in iucnstatus_page:
            title = ip.verify_iucn_page_title_present()
            check.is_true(title, "Title does not match")
            logger.info("Verification Successful :: IUCN Status Page Title found")
            
    @pytest.mark.UI
    @pytest.mark.iucn_status
    @pytest.mark.navigation
    def test_iucn_page_nav_elements(self, iucnstatus_page):
        """_summary_

        Args:
            iucnstatus_page (_type_): _description_
        """
        return super().test_page_nav_elements(iucnstatus_page)
    
    @pytest.mark.UI 
    @pytest.mark.iucn_status
    @pytest.mark.navigation
    def test_iucn_admin_elements(self, iucnstatus_page):
        """_summary_

        Args:
            iucnstatus_page (_type_): _description_
        """
        return super().test_page_admin_elements(iucnstatus_page)
    
    @pytest.mark.UI
    @pytest.mark.iucn_status
    @pytest.mark.navigation
    def test_iucn_definition_elements(self, iucnstatus_page):
        """_summary_

        Args:
            iucnstatus_page (_type_): _description_
        """
        return super().test_page_definition_elements(iucnstatus_page)
    
    @pytest.mark.UI 
    @pytest.mark.iucn_status
    @pytest.mark.table
    def test_iucn_table_elements(self, iucnstatus_page):
        """_summary_

        Args:
            iucnstatus_page (_type_): _description_
        """
        for ip in iucnstatus_page:
            all_elements, missing_elements = ip.verify_iucn_page_table_elements_present()
            check.is_true(all_elements, f"Table elements missing from IUCN Status Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: IUCN Status Table elements found")