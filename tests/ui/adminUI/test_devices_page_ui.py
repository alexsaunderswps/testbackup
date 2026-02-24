#test_devices_page_ui.py (Playwright version)
import pytest
from pytest_check import check
from fixtures.admin_menu.devices_fixtures import devices_page
from utilities.utils import logger, get_browser_name

# A device known to exist in the QA environment. Update here if the device is
# renamed or replaced.
KNOWN_DEVICE_NAME = "Alex's QA Headset - F7V07HK - Managed"

class TestDevicesPageUI:
    """
    Test suite for the Devices page UI elements.
    
    This class follows the established pattern for Playwright-based UI testing,
    using the modern fixture-based approach and the verify_ui_elements pattern
    for consistent element verification across different browsers.
    """
    
    @pytest.mark.UI 
    @pytest.mark.devices
    def test_devices_page_title(self, devices_page):
        """
        Test that the Devices page title is present and correct.
        
        This test verifies that when users navigate to the Devices page,
        they see the correct page title, which is essential for user orientation
        and navigation feedback.
        
        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_devices_page_title")
        for dp in devices_page:
            title = dp.verify_page_title_present()
            check.is_true(title, "Devices title does not match")
            logger.info("Verification Successful :: Devices Page Title found")
            
    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.navigation
    def test_devices_page_nav_elements(self, devices_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Devices page.
        
        Navigation consistency is crucial for user experience. This test ensures
        that all standard navigation elements (logo, menu items, etc.) are present
        and accessible on the Devices page, maintaining consistency across the application.
        
        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(devices_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing devices navigation elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Devices Navigation Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.navigation
    def test_devices_page_admin_elements(self, devices_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Devices page.
        
        The Admin dropdown provides access to administrative functions. This test
        ensures that all expected admin menu items are available when accessed
        from the Devices page, maintaining administrative workflow consistency.
        
        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(devices_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing devices admin elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Devices Admin Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.navigation
    def test_devices_page_definition_elements(self, devices_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Devices page.
        
        The Definitions dropdown provides access to configuration and reference data.
        This test verifies that users can access all definition-related functions
        from the Devices page, ensuring complete functionality is available.
        
        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(devices_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing devices definition elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Devices Definition Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.action
    def test_devices_action_elements(self, devices_page):
        """
        Test that all device action elements are present and functional.

        Action functionality is essential for users managing large numbers of devices.
        This test ensures that the search text box, search button, and Lookup Device Button
        are all present and properly labeled for user interaction.

        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
        """
        logger.info("Starting test_devices_action_elements")
        for dp in devices_page:
            all_elements, missing_elements = dp.verify_all_devices_action_elements_present()
            check.is_true(all_elements, f"Missing device action elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Device Action Elements found")

    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.table
    def test_devices_table_elements(self, devices_page):
        """
        Test that all device table elements are present and properly structured.
        
        The devices table is the primary interface for viewing device information.
        This test verifies that all expected columns (Name, Serial Number, Installation,
        Organization) are present, ensuring users can access all relevant device data.
        
        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
        """
        logger.info("Starting test_devices_table_elements")
        for dp in devices_page:
            all_elements, missing_elements = dp.verify_all_device_table_elements_present()
            check.is_true(all_elements, f"Missing device table elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Device Table Elements found")
    
    
    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.table
    def test_devices_table_data_presence(self, devices_page):
        """
        Verify that the Devices table contains at least one row of data.

        Checks that the table is not just structurally present (covered by
        test_devices_table_elements) but also populated with device records.
        This catches scenarios where the table renders correctly but the API
        fails to return data.

        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
        """
        logger.info("Starting test_devices_table_data_presence")
        for dp in devices_page:
            row_count = dp.count_table_rows()
            check.greater(
                row_count,
                0,
                f"Devices table should contain data, found {row_count} rows "
                f"on {get_browser_name(dp.page)}"
            )
            logger.info(
                f"Verification Successful :: Devices table has {row_count} rows "
                f"on {get_browser_name(dp.page)}"
            )

    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.search
    def test_devices_search_with_no_match_shows_empty_table(self, devices_page):
        """
        Verify that searching for a name that matches no devices results in an
        empty table rather than an error.

        Uses a deliberately unmatchable search term so the test is not coupled
        to any specific device that may or may not exist in the QA environment.

        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
        """
        no_match_name = "ZZZZZ_WILDXR_TEST_NO_MATCH_ZZZZZ"

        logger.info("Starting test_devices_search_with_no_match_shows_empty_table")
        for dp in devices_page:
            dp.search_devices(no_match_name)

            row_count = dp.count_table_rows()
            check.equal(
                row_count,
                0,
                f"Expected 0 rows for no-match search on {get_browser_name(dp.page)}, "
                f"got {row_count}"
            )
            if row_count == 0:
                logger.info(
                    f"Verification Successful :: No-match search returns empty table "
                    f"on {get_browser_name(dp.page)}"
                )

    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.search
    def test_devices_search_clears_to_show_results(self, devices_page):
        """
        Verify that clearing the search input and re-searching returns data
        after a no-match search has emptied the table.

        This confirms that the search state resets correctly — a bug in the
        search implementation could leave the table empty even after the filter
        is cleared.

        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
        """
        no_match_name = "ZZZZZ_WILDXR_TEST_NO_MATCH_ZZZZZ"

        logger.info("Starting test_devices_search_clears_to_show_results")
        for dp in devices_page:
            # Step 1: Search for a no-match term to empty the table.
            dp.search_devices(no_match_name)
            check.equal(
                dp.count_table_rows(),
                0,
                f"Expected 0 rows after no-match search on {get_browser_name(dp.page)}"
            )

            # Step 2: Clear the filter and search again to restore results.
            dp.search_devices("")

            row_count = dp.count_table_rows()
            check.greater(
                row_count,
                0,
                f"Expected rows to return after clearing search on "
                f"{get_browser_name(dp.page)}, got {row_count}"
            )
            if row_count > 0:
                logger.info(
                    f"Verification Successful :: Clearing search restores "
                    f"{row_count} rows on {get_browser_name(dp.page)}"
                )

    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.search
    def test_devices_search_returns_matching_result(self, devices_page):
        """
        Verify that searching for a known device name returns at least one result.

        Complements test_devices_search_with_no_match_shows_empty_table by
        confirming the positive case: a valid search term actually filters the
        table down to matching rows rather than returning everything or nothing.

        The device name is defined as KNOWN_DEVICE_NAME at the top of this module.
        Update that constant if the device is renamed or replaced in the QA environment.

        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
        """
        logger.info("Starting test_devices_search_returns_matching_result")
        for dp in devices_page:
            dp.search_devices(KNOWN_DEVICE_NAME)

            row_count = dp.count_table_rows()
            check.greater(
                row_count,
                0,
                f"Expected at least 1 row when searching for '{KNOWN_DEVICE_NAME}' "
                f"on {get_browser_name(dp.page)}, got {row_count}"
            )
            if row_count > 0:
                logger.info(
                    f"Verification Successful :: Search for known device returned "
                    f"{row_count} row(s) on {get_browser_name(dp.page)}"
                )

    @pytest.mark.UI
    @pytest.mark.devices
    @pytest.mark.pagination
    def test_devices_pagination_elements(self, devices_page, verify_ui_elements):
        """
        Test that pagination elements are correctly displayed on the Devices page.
        
        When there are many devices, pagination becomes essential for usability.
        This test ensures that pagination controls are present and properly
        configured based on the number of devices and page size settings.
        
        Args:
            devices_page: The DevicesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.pagination_elements(devices_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing devices pagination elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Devices Pagination Elements found on {get_browser_name(page)}")
    
    