#test_devices_page_ui.py
import pytest
from pytest_check import check
from page_objects.admin_menu.devices_page import DevicesPage
from page_objects.common.base_page import BasePage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def devices_page(logged_in_browser):
    logger.debug("Starting devices_page fixture")
    device_pages = []
    for login_page in logged_in_browser:
        driver = login_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Devices page on {driver.name}")
        logger.info("=" * 80)
        
        # Navigate to Device page
        base_page.click_admin_button()
        base_page.go_devices_page()
        # Verify that we're on the Device page
        devices_page = DevicesPage(driver)
        if devices_page.verify_page_title_present():
            logger.info("Successfully navigated to Device page")
            device_pages.append(devices_page)
        else:
            logger.error(f"Failed to navigate to Devices page on {driver.name}")
        
    logger.info(f"devices_page fixture: yielding {len(device_pages)} devices page(s)")
    yield device_pages
    logger.debug("device_page fixture: finished")
    
class TestDevicesPageUI(TestBasePageUI):
    
    @pytest.mark.UI 
    @pytest.mark.devices
    def test_devices_page_title(self, devices_page):
        """_summary_

        Args:
            devices_page (_type_): _description_
        """
        logger.debug("Starting test_devices_page_title")
        for dp in devices_page:
            title = dp.verify_page_title_present()
            check.equal(title, True, "Devices title does not match")
            logger.info("Verification Successful :: Devices Page Title found")
            
    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.navigation
    def test_devices_page_nav_elements(self, devices_page):
        """_summary_

        Args:
            devices_page (_type_): _description_
        """
        return super().test_page_nav_elements(devices_page)
    
    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.navigation
    def test_devices_page_admin_elements(self, devices_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        return super().test_page_admin_elements(devices_page)
    
    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.navigation
    def test_devices_page_definition_elements(self, devices_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        return super().test_page_definition_elements(devices_page)
    
    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.search
    def test_devices_search_elements(self, devices_page):
        """_summary_

        Args:
            devices_page (_type_): _description_

        Returns:
            _type_: _description_
        """
        for dp in devices_page:
            all_elements, missing_elements = dp.verify_all_devices_search_elements_present()
            check.is_true(all_elements, f"Missing device search elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Device Search Elements found")
    
    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.table
    def test_devices_table_elements(self, devices_page):
        """_summary_

        Args:
            devices_page (_type_): _description_
        """
        for dp in devices_page:
            all_elements, missing_elements = dp.verify_all_device_table_elements_present()
            check.is_true(all_elements, f"Missing device table elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Device Table Elements found")
    
    # Currently Devices page impliments pagination differently that all other pages.
    # This test will be implemented when the pagination is updated to match the rest of the pages
    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.pagination
    def test_devices_pagination_elements(self, devices_page):
        """_summary_

        Args:
            devices_page (_type_): _description_
        """
        return super().test_page_pagination_elements(devices_page)
    
    