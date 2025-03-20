#test_map_markers_page_ui.py
import pytest
from pytest_check import check
from page_objects.dashboard.map_markers_page import MapMarkersPage
from page_objects.common.base_page import BasePage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def map_markers_page(logged_in_browser):
    logger.debug("Starting map_markers_page fixture")
    map_markers_pages = []
    for login_page in logged_in_browser:
        driver = login_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Map Markers page on {driver.name}")
        logger.info("=" * 80)
        
        # Navigate to Map Markers page
        base_page.go_map_markers_page()
        # Verify that we're on the Map Markers page
        map_markers_page = MapMarkersPage(driver)
        if map_markers_page.verify_page_title_present():
            logger.info("Successfully navigated to Map Markers page")
            map_markers_pages.append(map_markers_page)
        else:
            logger.error(f"Failed to navigate to Map Markers page on {driver.name}")
        
    logger.info(f"map_markers_page fixture: yielding {len(map_markers_pages)} map markers page(s)")
    yield map_markers_pages
    logger.debug("map_markers_page fixture: finished")
    
class TestMapMarkersPageUI(TestBasePageUI):
    
    @pytest.mark.UI 
    @pytest.mark.map_markers
    @pytest.mark.debug
    def test_map_markers_page_title(self, map_markers_page):
        """_summary_

        Args:
            map_markers_page (_type_): _description_
        """
        logger.debug("Starting test_map_markers_page_title")
        for mp in map_markers_page:
            title = mp.verify_page_title_present()
            check.equal(title, True, "Title does not match")
            logger.info("Verificaiton Successful :: Map Markers Page Title found")

    @pytest.mark.UI
    @pytest.mark.map_markers 
    @pytest.mark.debug
    def test_map_markers_page_nav_elements(self, map_markers_page):
        """_summary_

        Args:
            map_markers_page (_type_): _description_
        """
        return super().test_page_nav_elements(map_markers_page)

    @pytest.mark.UI
    @pytest.mark.map_markers
    @pytest.mark.debug
    def test_page_admin_elements(self, map_markers_page):
        """_summary_

        Args:
            map_markers_page (_type_): _description_

        Returns:
            _type_: _description_
        """
        return super().test_page_admin_elements(map_markers_page)
    
    @pytest.mark.UI
    @pytest.mark.map_markers
    @pytest.mark.debug
    def test_page_definition_elements(self, map_markers_page):
        """_summary_

        Args:
            map_markers_page (_type_): _description_

        Returns:
            _type_: _description_
        """
        return super().test_page_definition_elements(map_markers_page)