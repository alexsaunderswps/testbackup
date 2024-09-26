#test_videos_page_ui.py
import pytest
from pytest_check import check
from page_objects.dashboard.videos_page import VideosPage
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger


# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def videos_page(logged_in_browser):
    driver, wait = logged_in_browser
    logger.info(f"Navigating to Videos page on {driver.name}")
    return VideosPage(driver)

class TestVideoPageUI:
    
    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.debug
    def test_video_page_nav_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        vp = videos_page
        
        all_elements = vp.verify_all_nav_elements_present()
        check.is_true(all_elements, "Navigation elements missing from Videos Page")
        logger.info("Verification Successful :: All Navigation elements found on Videos Page")

    @pytest.mark.UI
    @pytest.mark.video 
    def test_video_page_definition_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        vp = videos_page
        
        all_elements = vp.verify_all_definition_links_present()
        check.is_true(all_elements, "Navigation elements missing from Videos Page")
        logger.info("Verification Successful :: All Navigation elements found on Videos Page")
    
    @pytest.mark.UI
    @pytest.mark.video 
    def test_video_page_search_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        vp = videos_page
        
        all_elements = vp.verify_all_video_search_elements_present()
        check.is_true(all_elements, "Navigation elements missing from Videos Page")
        logger.info("Verification Successful :: All Navigation elements found on Videos Page")
        
    @pytest.mark.UI
    @pytest.mark.video 
    def test_video_pagination_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        vp = videos_page
        
        all_elements = vp.verify_all_video_pagination_elements_present()
        check.is_true(all_elements, "Navigation elements missing from Videos Page")
        logger.info("Verification Successful :: All Navigation elements found on Videos Page")    

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.table 
    def test_video_table_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        vp = videos_page
        
        all_elements = vp.verify_all_video_table_elements_present()
        check.is_true(all_elements, "Navigation elements missing from Videos Page")
        logger.info("Verification Successful :: All Navigation elements found on Videos Page")   
        
    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.table
    def test_video_table_rows(self, videos_page):
        """_summary_

        Args:
            videos_page (_type_): _description_
        """
        vp = videos_page
        row_count = vp.count_table_rows()
        logger.info(f"Verificaiton Successful :: Able to count all table rows. {row_count} Rows found")
        

    def test_video_name_retreval(self, videos_page):
        vp = videos_page
        vp.get_video_name_values()
        
if __name__ == "__main__":
    TV = TestVideoPageUI()