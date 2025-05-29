#test_videos_page_ui.py
import pytest
from pytest_check import check
from fixtures.dashboard.videos_fixtures import videos_page
from utilities.utils import logger, get_browser_name

class TestVideoPageUI:
    """
    Test suite for the Videos page UI elements.

    This class follows the established pattern for Playwright-based UI testing,
    using the modern fixture-based approach and the verify_ui_elements pattern
    for consistent element verification across different browsers.
    """
    
    @pytest.mark.UI
    @pytest.mark.video
    def test_video_page_title(self, videos_page):
        """
        Test that the Videos page title is present and correct.

        This test verifies that when users navigate to the Videos page,
        they see the correct page title, which is essential for user orientation
        and navigation feedback.
        
        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_video_page_title")
        for vp in videos_page:
            title = vp.verify_page_title_present()
            check.is_true(title, "Videos title does not match")
            logger.info("Verification Successful :: Videos Page Title found")
    
    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.navigation
    def test_video_page_nav_elements(self, videos_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Videos page.

        Navigation consistency is crucial for user experience. This test ensures
        that all standard navigation elements (logo, menu items, etc.) are present
        and accessible on the Videos page, maintaining consistency across the application.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(videos_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing videos navigation elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Videos Navigation Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.navigation
    def test_video_page_admin_elements(self, videos_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Videos page.

        The Admin dropdown provides access to administrative functions. This test
        ensures that all expected admin menu items are available when accessed
        from the Videos page, maintaining administrative workflow consistency.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(videos_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing videos admin elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Videos Admin Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.navigation
    def test_video_page_definition_elements(self, videos_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Videos page.

        The Definitions dropdown provides access to configuration and reference data.
        This test verifies that users can access all definition-related functions
        from the Videos page, ensuring complete functionality is available.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(videos_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing videos definition elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Videos Definition Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.action
    @pytest.mark.video
    def test_video_page_action_elements(self, videos_page):
        """
        Test that all video action elements are present and functional.

        This test ensures that the search button, clear search button, and Add Video Button
        are all present and properly labeled for user interaction.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
        """
        for vp in videos_page:
            all_elements, missing_elements = vp.verify_all_videos_action_elements_present()
            check.is_true(all_elements, f"Action elements missing from Videos Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Action elements found on Videos Page")

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.table 
    def test_video_table_elements(self, videos_page):
        """
        Test that all videos table elements are present and properly structured.

        The videos table is the primary interface for viewing video information.
        This test verifies that all expected columns (Thumbnail, Name, Organization, Decription,
        Country) are present, ensuring users can access all relevant video data.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
        """
        logger.info("Starting test_video_table_elements")
        for vp in videos_page:
            vp.page.wait_for_timeout(2000)
            all_elements, missing_elements = vp.verify_all_video_table_elements_present()
            check.is_true(all_elements, f"Table elements missing from Videos Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Video Table Elements found on Videos Page")

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.table
    def test_video_table_rows(self, videos_page):
        """_summary_

        Args:
            videos_page (_type_): _description_
        """
        for vp in videos_page:
            vp.page.wait_for_timeout(2000)
            row_count = vp.count_table_rows()
            logger.info(f"Verification Successful :: Able to count all table rows. {row_count} Rows found")

    @pytest.mark.video
    @pytest.mark.table
    #@pytest.mark.debug
    def test_video_name_retreval(self, videos_page):
        for vp in videos_page:
            vp.page.wait_for_timeout(2000)
            vp.get_video_name_values()
            
            
    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.pagination
    def test_videos_pagination_elements(self, videos_page, verify_ui_elements):
        """
        Test that pagination elements are correctly displayed on the Videos page.

        When there are many videos, pagination becomes essential for usability.
        This test ensures that pagination controls are present and properly
        configured based on the number of videos and page size settings.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.pagination_elements(videos_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing videos pagination elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Videos Pagination Elements found on {get_browser_name(page)}")

# TODO - check videos_page.py for Todo items before writing tests here

