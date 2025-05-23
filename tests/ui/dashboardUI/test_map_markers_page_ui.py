#test_map_markers_page_ui.py
import pytest
from pytest_check import check
from fixtures.dashboard.mapmarkers_fixtures import map_markers_page
from utilities.utils import logger, get_browser_name

class TestMapMarkersPageUI:
    """
    Test suite for the Map Markers page UI elements.

    This class follows the established pattern for Playwright-based UI testing,
    using the modern fixture-based approach and the verify_ui_elements pattern
    for consistent element verification across different browsers.
    """
    
    @pytest.mark.UI
    @pytest.mark.map_markers
    def test_map_markers_page_title(self, map_markers_page):
        """
        Test that the Map Markers page title is present and correct.

        This test verifies that when users navigate to the Map Markers page,
        they see the correct page title, which is essential for user orientation
        and navigation feedback.
        
        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_map_markers_page_title")
        for mmp in map_markers_page:
            title = mmp.verify_page_title_present()
            check.is_true(title, "Map Markers title does not match")
            logger.info("Verification Successful :: Map Markers Page Title found")
    
    @pytest.mark.UI
    @pytest.mark.map_markers
    @pytest.mark.navigation
    def test_map_markers_page_nav_elements(self, map_markers_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Map Markers page.

        Navigation consistency is crucial for user experience. This test ensures
        that all standard navigation elements (logo, menu items, etc.) are present
        and accessible on the Map Markers page, maintaining consistency across the application.

        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(map_markers_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing map markers navigation elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Map Markers Navigation Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.map_markers
    @pytest.mark.navigation
    def test_map_markers_page_admin_elements(self, map_markers_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Map Markers page.

        The Admin dropdown provides access to administrative functions. This test
        ensures that all expected admin menu items are available when accessed
        from the Map Markers page, maintaining administrative workflow consistency.

        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(map_markers_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing map markers admin elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Map Markers Admin Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.map_markers
    @pytest.mark.navigation
    def test_map_markers_page_definition_elements(self, map_markers_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Map Markers page.

        The Definitions dropdown provides access to configuration and reference data.
        This test verifies that users can access all definition-related functions
        from the Map Markers page, ensuring complete functionality is available.

        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(map_markers_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing map markers definition elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Map Markers Definition Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.action
    @pytest.mark.map_markers
    def test_map_markers_action_elements(self, map_markers_page):
        """
        Test that all map marker action elements are present and functional.

        This test ensures that the core tab, custom tab, and Add Map Marker button
        are all present and properly labeled for user interaction.

        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
        """
        for mmp in map_markers_page:
            all_elements, missing_elements = mmp.verify_all_map_markers_action_elements_present()
            check.is_true(all_elements, f"Action elements missing from Map Markers Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Action elements found on Map Markers Page")

    @pytest.mark.UI
    @pytest.mark.map_markers
    @pytest.mark.table 
    def test_map_markers_core_table_elements(self, map_markers_page):
        """
        Test that all core map markers table elements are present and properly structured.

        The core map markers table is the primary interface for viewing core marker information.
        This test verifies that all expected columns (Icon, Name, Description, Videos,
        Location) are present, ensuring users can access all relevant core marker data.

        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
        """
        logger.info("Starting test_map_markers_core_table_elements")
        for mmp in map_markers_page:
            mmp.page.wait_for_timeout(2000)
            all_elements, missing_elements = mmp.verify_all_core_map_markers_table_elements_present()
            check.is_true(all_elements, f"Core table elements missing from Map Markers Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Core Map Markers Table Elements found on Map Markers Page")

    @pytest.mark.UI
    @pytest.mark.map_markers
    @pytest.mark.table 
    def test_map_markers_custom_table_elements(self, map_markers_page):
        """
        Test that all custom map markers table elements are present and properly structured.

        The custom map markers table provides access to organization-specific markers.
        This test verifies that all expected columns (Icon, Name, Description, Videos,
        Organization, Location) are present, ensuring users can access all relevant custom marker data.

        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
        """
        logger.info("Starting test_map_markers_custom_table_elements")
        for mmp in map_markers_page:
            mmp.page.wait_for_timeout(2000)
            all_elements, missing_elements = mmp.verify_all_custom_map_markers_table_elements_present()
            check.is_true(all_elements, f"Custom table elements missing from Map Markers Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Custom Map Markers Table Elements found on Map Markers Page")

    @pytest.mark.UI
    @pytest.mark.map_markers
    @pytest.mark.table
    def test_map_markers_table_rows(self, map_markers_page):
        """
        Test that map markers table rows can be counted and are accessible.

        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
        """
        for mmp in map_markers_page:
            mmp.page.wait_for_timeout(2000)
            row_count = mmp.count_table_rows()
            logger.info(f"Verification Successful :: Able to count all table rows. {row_count} Rows found")

    @pytest.mark.map_markers
    @pytest.mark.table
    def test_map_markers_name_retrieval(self, map_markers_page):
        """
        Test that map marker names can be retrieved from the table.

        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
        """
        for mmp in map_markers_page:
            mmp.page.wait_for_timeout(2000)
            mmp.get_map_marker_name_values()
            
    @pytest.mark.UI
    @pytest.mark.map_markers
    @pytest.mark.pagination
    def test_map_markers_pagination_elements(self, map_markers_page, verify_ui_elements):
        """
        Test that pagination elements are correctly displayed on the Map Markers page.

        When there are many map markers, pagination becomes essential for usability.
        This test ensures that pagination controls are present and properly
        configured based on the number of markers and page size settings.

        Args:
            map_markers_page: The MapMarkersPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.pagination_elements(map_markers_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing map markers pagination elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Map Markers Pagination Elements found on {get_browser_name(page)}")