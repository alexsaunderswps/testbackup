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

class TestVideoPageUI:
    
    @pytest.mark.UI
    @pytest.mark.video
    #@pytest.mark.debug
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
    #@pytest.mark.debug
    def test_video_page_nav_elements(self, videos_page):
        logger.info("Starting test_video_page_nav_elements")
        all_browsers_passed = True
            
        for index, vp in enumerate(videos_page):
            logger.info(f"Testing video page nav elements on browser {index + 1}: {vp.driver.name}")
            all_elements = vp.verify_all_nav_elements_present()
            if all_elements:
                logger.info(f"Verification Successful :: All Navigation elements found on Videos Page for {vp.driver.name}")
            else:
                logger.error(f"Verification failed :: Some elements missing from Videos Page for {vp.driver.name}")
                all_browsers_passed = False
        logger.info("Finished test_video_page_nav_elements")
        assert all_browsers_passed, "One or more browsers failed the navigation elements check"        
        

    @pytest.mark.UI
    @pytest.mark.video
    #@pytest.mark.debug
    def test_video_page_definition_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        for vp in videos_page:
            all_elements = vp.verify_all_definition_links_present()
            check.is_true(all_elements, "Navigation elements missing from Videos Page")
            logger.info("Verification Successful :: All Navigation elements found on Videos Page")
    
    @pytest.mark.UI
    @pytest.mark.video
    #@pytest.mark.debug
    def test_video_page_search_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        for vp in videos_page:
            
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
        for vp in videos_page:
            
            all_elements = vp.verify_all_video_pagination_elements_present()
            check.is_true(all_elements, "Navigation elements missing from Videos Page")
            logger.info("Verification Successful :: All Navigation elements found on Videos Page")    

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.table 
    @pytest.mark.debug
    def test_video_table_elements(self, videos_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        for vp in videos_page:
            
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
