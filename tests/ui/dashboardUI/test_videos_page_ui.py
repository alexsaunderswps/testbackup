#test_videos_page_ui.py
import pytest
from pytest_check import check
from fixtures.dashboard.videos_fixtures import videos_page
from utilities.utils import logger, get_browser_name

class TestVideoPageUI:
    """
    Test suite for the Videos page UI elements.

    The Videos page renders a responsive grid of video cards. Each card contains
    a thumbnail image, video name (h2), overview text, organization name, and
    country name. There is no table structure on this page.

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

        This test ensures that the Search button, Clear search button, and Add Video
        link are all present and properly labeled for user interaction.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
        """
        for vp in videos_page:
            all_elements, missing_elements = vp.verify_all_videos_action_elements_present()
            check.is_true(all_elements, f"Action elements missing from Videos Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Action elements found on Videos Page")

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.grid
    def test_video_grid_elements(self, videos_page):
        """
        Test that all video grid and card elements are present and properly structured.

        The Videos page renders a responsive grid of video cards rather than a table.
        This test verifies that the grid container, individual video cards, and the
        expected card content elements (thumbnails, names, overviews, organizations,
        countries) are all present and rendered correctly.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
        """
        logger.info("Starting test_video_grid_elements")
        for vp in videos_page:
            vp.page.wait_for_timeout(2000)
            all_elements, missing_elements = vp.verify_all_video_grid_elements_present()
            check.is_true(all_elements, f"Grid elements missing from Videos Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Video Grid Elements found on Videos Page")

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.grid
    def test_video_card_count(self, videos_page):
        """
        Test that video cards are rendered in the grid and can be counted.

        Verifies that at least one video card is present in the grid after the
        page has loaded, confirming that video data is being fetched and rendered.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
        """
        for vp in videos_page:
            vp.page.wait_for_timeout(2000)
            card_count = vp.count_video_cards()
            check.greater(card_count, 0, "Expected at least one video card in the grid")
            logger.info(f"Verification Successful :: Found {card_count} video cards in the grid")

    @pytest.mark.video
    @pytest.mark.grid
    def test_video_name_retrieval(self, videos_page):
        """
        Test that video names can be retrieved from the card grid.

        Reads the h2 title element from each visible video card and confirms
        that a non-empty list of names is returned, validating that card name
        elements are accessible and populated with data.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
        """
        for vp in videos_page:
            vp.page.wait_for_timeout(2000)
            video_names = vp.get_video_name_values()
            check.greater(len(video_names), 0, "Expected to retrieve at least one video name from the grid")
            logger.info(f"Verification Successful :: Retrieved {len(video_names)} video names from the grid")

    @pytest.mark.UI
    @pytest.mark.video
    @pytest.mark.search
    def test_video_search_modal_opens_and_shows_filter_fields(self, videos_page):
        """
        Verify that clicking the Search button opens the VideoSearchModal overlay
        and that all expected filter fields are present inside it.

        The VideoSearchModal is a React overlay that is completely removed from the
        DOM when closed. This test confirms that the modal mounts correctly and
        exposes all 11 expected elements: the heading, name and overview text inputs,
        five filter-category labels (Country, Resolution, Species, Tags, Statuses),
        the Reset and Apply action buttons, and the × close button.

        After verification the modal is closed so subsequent tests start from a clean state.

        Args:
            videos_page: The VideosPage fixture providing page objects for each browser
        """
        logger.info("Starting test_video_search_modal_opens_and_shows_filter_fields")
        for vp in videos_page:
            vp.open_search_modal()

            all_elements, missing_elements = vp.verify_all_search_modal_elements_present()
            check.is_true(
                all_elements,
                f"Missing VideoSearchModal elements on {get_browser_name(vp.page)}: "
                f"{', '.join(missing_elements)}"
            )
            if all_elements:
                logger.info(
                    f"Verification Successful :: All VideoSearchModal elements found "
                    f"on {get_browser_name(vp.page)}"
                )

            vp.close_search_modal()

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

# TODO - with names, check sort functionality
# TODO - check if published column should be populated
# TODO - gather other card data if needed (overview, org, country values)
# TODO - with card names, verify sort order changes when sort buttons are clicked
# TODO - Check search functionality - modal window interaction
