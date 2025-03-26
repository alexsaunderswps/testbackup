#test_video_catalogues_page_ui.py
import pytest
from pytest_check import check 
from page_objects.dashboard.video_catalogues_page import VideoCataloguesPage
from page_objects.common.base_page import BasePage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def video_catalogue_page(logged_in_browser):
    logger.debug("Starting video_catalogue_page fixture")
    video_catalogue_pages = []
    for login_page in logged_in_browser:
        driver = login_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Video Catalogues page on {driver.name}")
        logger.info("=" * 80)
    
        # Navigate to Video Catalogues page
        base_page.go_video_catalogues_page()
        # Verify that we're on the Video Catalogues page
        video_catalogue_page = VideoCataloguesPage(driver)
        if video_catalogue_page.verify_page_title_present():
            logger.info("Successfully navigated to Video Catalogues page")
            video_catalogue_pages.append(video_catalogue_page)
        else:
            logger.error(f"Failed to navigate to Video Catalogues page on {driver.name}")
    logger.info(f"video_catalogue_page fixture: yielding {len(video_catalogue_pages)} video catalogue page(s)")
    yield video_catalogue_pages
    logger.debug("video_catalogue_page fixture: finished")
    
class TestVideoCataloguesPageUI(TestBasePageUI):
    
    @pytest.mark.UI 
    @pytest.mark.catalogue
    def test_video_catalogue_page_title(self, video_catalogue_page):
        """_summary_

        Args:
            video_catalogue_page (_type_): _description_
        """
        logger.debug("Starting video_catalogue_page_title")
        for vcp in video_catalogue_page:
            title = vcp.verify_page_title_present()
            check.equal(title, True, "Title does not match")
            logger.info("Verification Successful :: Video Catalogues Page Title found")
        
    @pytest.mark.UI 
    @pytest.mark.catalogue
    @pytest.mark.navigation
    def test_catalogue_page_nav_elements(self, video_catalogue_page):
        """_summary_

        Args:
            video_catalogue_page (_type_): _description_
        """
        return super().test_page_nav_elements(video_catalogue_page)
    
    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.navigation
    def test_catalogue_page_admin_elements(self, video_catalogue_page):
        """_summary_

        Args:
            video_catalogue_page (_type_): _description_
        """
        return super().test_page_admin_elements(video_catalogue_page)

    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.navigation
    def test_catalogue_page_defintion_elements(self, video_catalogue_page):
        """_summary_

        Args:
            video_catalogue_page (_type_): _description_
        """
        return super().test_page_definition_elements(video_catalogue_page)
    
    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.table
    def test_video_catalogue_search_elements(self, video_catalogue_page):
        """_summary_

        Args:
            video_catalogue_page (_type_): _description_
        """
        for vcp in video_catalogue_page:
            all_elements_present, missing_elements = vcp.verify_all_catalgoue_search_elements_present()
            check.is_true(all_elements_present, f"Missing elements: {', '.join(missing_elements)} on Video Catalogues page")
            logger.info("Verification Successful :: All Video Catalogue search elements found")
            
    @pytest.mark.UI 
    @pytest.mark.catalogue
    @pytest.mark.table
    def test_video_catalogue_table_elements(self, video_catalogue_page):
        """_summary_

        Args:
            video_catalogue_page (_type_): _description_
        """
        for vcp in video_catalogue_page:
            all_elements_present, missing_elements = vcp.verify_all_catalogue_table_elements_present()
            check.is_true(all_elements_present, f"Missing elements: {', '.join(missing_elements)} on Video Catalogues page")
            logger.info("Verification Successful :: All Video Catalogue table elements found")

