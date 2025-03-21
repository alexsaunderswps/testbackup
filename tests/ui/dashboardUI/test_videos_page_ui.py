#test_videos_page_ui.py
import pytest
from pytest_check import check
from page_objects.dashboard.videos_page import VideosPage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger


# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def videos_page(logged_in_browser):
    logger.debug("Starting videos_page fixture")
    video_pages = []
    for login_page in logged_in_browser:
        driver = login_page.driver
        logger.info(80 * "-")
        logger.info(f"Navigating to Videos page on {driver.name}")
        video_pages.append(VideosPage(driver))
    logger.info(f"videos_page fixture: yielding {len(video_pages)} video page(s)")
    logger.info(80 * "-")
    yield video_pages
    logger.debug("videos_page fixture: finished")

class TestVideoPageUI(TestBasePageUI):
    
    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.debug
    def test_video_page_title(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        logger.debug("Starting test_video_page_title")
        for vp in videos_page:
            title = vp.verify_page_title_present()
            check.equal(title, True, "Title does not match")
            logger.info("Verification Successful :: Videos Page Title found")
    
    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.navigation
    @pytest.mark.debug
    def test_video_page_nav_elements(self, videos_page):
        """_summary_

        Args:
            videos_page (_type_): _description_
        """
        return super().test_page_nav_elements(videos_page)
        
    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.navigation
    @pytest.mark.debug
    def test_video_page_admin_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        return super().test_page_admin_elements(videos_page)

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.navigation
    @pytest.mark.debug
    def test_video_page_definition_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        return super().test_page_definition_elements(videos_page)
    
    @pytest.mark.UI
    @pytest.mark.search
    @pytest.mark.video
    #@pytest.mark.debug
    def test_video_page_search_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        for vp in videos_page:
            
            all_elements, missing_elements = vp.verify_all_video_search_elements_present()
            check.is_true(all_elements, f"Search elements missing from Videos Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Navigation elements found on Videos Page")
        
    @pytest.mark.UI
    @pytest.mark.pagination
    @pytest.mark.video
    #@pytest.mark.debug
    def test_video_pagination_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        return super().test_page_pagination_elements(videos_page)

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.table 
    #@pytest.mark.debug
    def test_video_table_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        for vp in videos_page:
            
            all_elements, missing_elements = vp.verify_all_video_table_elements_present()
            check.is_true(all_elements, f"Table elements missing from Videos Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Navigation elements found on Videos Page")   
        
    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.table
    def test_video_table_rows(self, videos_page):
        """_summary_

        Args:
            videos_page (_type_): _description_
        """
        for vp in videos_page:
            row_count = vp.count_table_rows()
            logger.info(f"Verificaiton Successful :: Able to count all table rows. {row_count} Rows found")
            
    @pytest.mark.video
    @pytest.mark.table
    #@pytest.mark.debug
    def test_video_name_retreval(self, videos_page):
        for vp in videos_page:
            vp.get_video_name_values()

# TODO - check videos_page.py for Todo items before writing tests here

        
if __name__ == "__main__":
    TV = TestVideoPageUI()
