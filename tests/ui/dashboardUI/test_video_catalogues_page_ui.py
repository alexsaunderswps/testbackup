#test_video_catalogues_page_ui.py (Playwright version)
import math
import pytest
from datetime import datetime
from pytest_check import check
from fixtures.dashboard.videocatalogues_fixtures import video_catalogue_page, video_catalogue_conditional_pagination_data
from utilities.utils import logger, get_browser_name

class TestVideoCataloguesPageUI:
    """
    Test suite for the Video Catalogues page UI elements.

    This class follows the established pattern for Playwright-based UI testing,
    using the modern fixture-based approach and the verify_ui_elements pattern
    for consistent element verification across different browsers.
    """
    
    @pytest.mark.UI
    @pytest.mark.catalogue
    def test_video_catalogue_page_title(self, video_catalogue_page):
        """
        Test that the Video Catalogues page title is present and correct.

        This test verifies that when users navigate to the Video Catalogues page,
        they see the correct page title, which is essential for user orientation
        and navigation feedback.
        
        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_video_catalogue_page_title")
        for vcp in video_catalogue_page:
            title = vcp.verify_page_title_present()
            check.is_true(title, "Video Catalogues title does not match")
            logger.info("Verification Successful :: Video Catalogues Page Title found")
    
    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.navigation
    def test_video_catalogue_page_nav_elements(self, video_catalogue_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Video Catalogues page.

        Navigation consistency is crucial for user experience. This test ensures
        that all standard navigation elements (logo, menu items, etc.) are present
        and accessible on the Video Catalogues page, maintaining consistency across the application.

        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(video_catalogue_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing video catalogues navigation elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Video Catalogues Navigation Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.navigation
    def test_video_catalogue_page_admin_elements(self, video_catalogue_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Video Catalogues page.

        The Admin dropdown provides access to administrative functions. This test
        ensures that all expected admin menu items are available when accessed
        from the Video Catalogues page, maintaining administrative workflow consistency.

        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(video_catalogue_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing video catalogues admin elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Video Catalogues Admin Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.navigation
    def test_video_catalogue_page_definition_elements(self, video_catalogue_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Video Catalogues page.

        The Definitions dropdown provides access to configuration and reference data.
        This test verifies that users can access all definition-related functions
        from the Video Catalogues page, ensuring complete functionality is available.

        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(video_catalogue_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing video catalogues definition elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Video Catalogues Definition Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.action
    @pytest.mark.catalogue
    def test_video_catalogue_action_elements(self, video_catalogue_page):
        """
        Test that all video catalogue search elements are present and functional.

        This test ensures that the search input, search button, and Add Video Catalogue button
        are all present and properly labeled for user interaction.

        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
        """
        for vcp in video_catalogue_page:
            all_elements, missing_elements = vcp.verify_all_video_catalogues_action_elements_present()
            check.is_true(all_elements, f"Action elements missing from Video Catalogues Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Action elements found on Video Catalogues Page")

    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.table 
    def test_video_catalogue_table_elements(self, video_catalogue_page):
        """
        Test that all video catalogue table elements are present and properly structured.

        The video catalogues table is the primary interface for viewing catalogue information.
        This test verifies that all expected columns (Name, Organization, Description,
        Last Edited By, Last Edited Date) are present, ensuring users can access all relevant data.

        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
        """
        logger.info("Starting test_video_catalogue_table_elements")
        for vcp in video_catalogue_page:
            vcp.page.wait_for_timeout(2000)
            all_elements, missing_elements = vcp.verify_all_video_catalogues_table_elements_present()
            check.is_true(all_elements, f"Table elements missing from Video Catalogues Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Video Catalogue Table Elements found on Video Catalogues Page")

    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.table
    def test_video_catalogue_table_rows(self, video_catalogue_page):
        """
        Test that video catalogue table rows can be counted and are accessible.

        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
        """
        for vcp in video_catalogue_page:
            vcp.page.wait_for_timeout(2000)
            row_count = vcp.count_table_rows()
            logger.info(f"Verification Successful :: Able to count all table rows. {row_count} Rows found")

    @pytest.mark.catalogue
    @pytest.mark.table
    def test_video_catalogue_name_retreval(self, video_catalogue_page):
        """
        Test that video catalogue names can be retrieved from the table.

        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
        """
        for vcp in video_catalogue_page:
            vcp.page.wait_for_timeout(2000)
            vcp.get_video_catalogue_name_values()
            
    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.search
    def test_video_catalogue_search_with_no_match_shows_empty_table(self, video_catalogue_page):
        """
        Verify that searching for a name that matches no catalogues results in an
        empty table rather than an error.

        Uses a deliberately unmatchable search term so the test is not coupled
        to any specific catalogue that may or may not exist in the QA environment.

        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
        """
        no_match_name = "ZZZZZ_WILDXR_TEST_NO_MATCH_ZZZZZ"

        logger.info("Starting test_video_catalogue_search_with_no_match_shows_empty_table")
        for vcp in video_catalogue_page:
            vcp.search_catalogues(no_match_name)

            row_count = vcp.count_table_rows()
            check.equal(
                row_count,
                0,
                f"Expected 0 rows for no-match search on {get_browser_name(vcp.page)}, "
                f"got {row_count}"
            )
            if row_count == 0:
                logger.info(
                    f"Verification Successful :: No-match search returns empty table "
                    f"on {get_browser_name(vcp.page)}"
                )

    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.pagination
    def test_video_catalogue_pagination_elements(self, video_catalogue_page, verify_ui_elements):
        """
        Test that pagination elements are correctly displayed on the Video Catalogues page.

        When there are many video catalogues, pagination becomes essential for usability.
        This test ensures that pagination controls are present and properly
        configured based on the number of catalogues and page size settings.

        Args:
            video_catalogue_page: The VideoCataloguesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.pagination_elements(video_catalogue_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing video catalogue pagination elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Video Catalogue Pagination Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.catalogue
    @pytest.mark.pagination
    @pytest.mark.conditional_data
    @pytest.mark.debug
    def test_video_catalogue_pagination_elements_with_sufficient_data(self, video_catalogue_page, video_catalogue_conditional_pagination_data, verify_ui_elements):
        """
        Test pagination elements when we ensure sufficient data exists.

        This test:
        1. Checks if enough video catalogues exist for pagination
        2. Creates test data only if needed
        3. Skips if sufficient data already exists (to avoid unnecessary data creation)
        Args:
            video_catalogue_page: The VideoCataloguePage fixture
            video_catalogue_conditional_pagination_data: Fixture that conditionally creates test data
            verify_ui_elements: The fixture providing UI element verification functions
        """
        video_catalogue_ids, data_was_created = video_catalogue_conditional_pagination_data

        if not data_was_created:
            logger.info("Test skipped - sufficient existing data for pagination testing")
            pytest.skip("Sufficient video catalogues already exist for pagination testing")

        logger.info(f"Test executed with {len(video_catalogue_ids)} newly created video catalogues")

        # Same verification logic as the original test
        for vp in video_catalogue_page:
            # Refresh to ensure our test data is loaded
            vp.page.reload()
            vp.page.wait_for_load_state("networkidle")

            # Verify pagination elements are present
            results = verify_ui_elements.pagination_elements([vp])
            for page, all_elements, missing_elements in results:
                check.is_true(all_elements, 
                            f"Missing pagination elements with test data: {', '.join(missing_elements)}")
            
            # Additional verification that our test data contributed to pagination
            counts = vp.get_pagination_counts()
            check.is_not_none(counts, "Should have pagination counts with sufficient test data")
            
            if counts:
                current_start, current_end, total_records = counts
                check.greater_equal(total_records, len(video_catalogue_ids),
                                "Total records should include our test video catalogues")

                # Verify we actually have pagination (more than one page)
                page_size = current_end - current_start + 1
                total_pages = math.ceil(total_records / page_size)
                check.greater(total_pages, 1, "Should have multiple pages with sufficient data")
            
            logger.info(f"Verification Successful :: Pagination elements verified with test data on {get_browser_name(vp.page)}")