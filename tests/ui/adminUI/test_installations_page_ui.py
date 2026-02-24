#test_installations_page.py (Playwright version)
import math
import pytest
from datetime import datetime
from fixtures.admin_menu.installations_fixtures import installations_page, installations_conditional_pagination_data
from pytest_check import check
from utilities.utils import get_browser_name,logger
    
class TestInstallationsPageUI:
    """
    Test suite for the Installations page UI elements.

    This class follows the established pattern for Playwright-based UI testing,
    using the modern fixture-based approach and the verify_ui_elements pattern
    for consistent element verification across different browsers.
    """
    
    @pytest.mark.UI 
    @pytest.mark.installations
    def test_installations_page_title(self, installations_page):
        """
        Test that the Installations page title is present.
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        logger.debug("Starting test_installations_page_title")
        for ip in installations_page:
            title = ip.verify_page_title()
            check.is_true(title, "Installations title does not match")
            logger.info("Verification Successful :: Installations Page Title found")
            
    @pytest.mark.UI 
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_nav_elements(self, installations_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations navigation elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Navigation Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_admin_elements(self, installations_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations admin elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Admin Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_definition_elements(self, installations_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations definition elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Definition Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_action_elements(self, installations_page):
        """
        Test that the Add Installation button, Search textbox, and Serch button are present on the Users page.
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        logger.debug("Starting test_installations_action_elements")
        for ip in installations_page:
            all_elements, missing_elements = ip.verify_all_installation_action_elements_present()
            check.is_true(all_elements, f"Missing installations action elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Installations Action Elements found")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.table
    def test_installations_table_elements(self, installations_page):
        """
        Test that all table elements are present on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        for ip in installations_page:
            all_elements, missing_elements = ip.verify_all_installation_table_elements_present()
            check.is_true(all_elements, f"Missing installations table elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Installations Table Elements found")
            
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.pagination
    def test_installations_pagination_elements(self, installations_page, verify_ui_elements):
        """
        Test that pagination elements are correctly displayed on the Installations page.

        When there are many installations, pagination becomes essential for usability.
        This test ensures that pagination controls are present and properly
        configured based on the number of installations and page size settings.

        Args:
            installations_page: The InstallationsPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.pagination_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations pagination elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Pagination Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.pagination
    @pytest.mark.conditional_data
    def test_installations_pagination_elements_with_sufficient_data(self, installations_page, installations_conditional_pagination_data, verify_ui_elements):
        """
        Test pagination elements when we ensure sufficient data exists.
        
        This test:
        1. Checks if enough installations exist for pagination
        2. Creates test data only if needed
        3. Skips if sufficient data already exists (to avoid unnecessary data creation)
        
        Args:
            installations_page: The InstallationsPage fixture
            installations_conditional_pagination_data: Fixture that conditionally creates test data
            verify_ui_elements: The fixture providing UI element verification functions
        """
        installation_ids, data_was_created = installations_conditional_pagination_data

        if not data_was_created:
            logger.info("Test skipped - sufficient existing data for pagination testing")
            pytest.skip("Sufficient installations already exist for pagination testing")
        
        logger.info(f"Test executed with {len(installation_ids)} newly created installations")
        
        # Same verification logic as the original test
        for ip in installations_page:
            # Refresh to ensure our test data is loaded
            ip.page.reload()
            ip.page.wait_for_load_state("networkidle")
            
            # Verify pagination elements are present
            results = verify_ui_elements.pagination_elements([ip])
            for page, all_elements, missing_elements in results:
                check.is_true(all_elements, 
                            f"Missing pagination elements with test data: {', '.join(missing_elements)}")
            
            # Additional verification that our test data contributed to pagination
            counts = ip.get_pagination_counts()
            check.is_not_none(counts, "Should have pagination counts with sufficient test data")
            
            if counts:
                current_start, current_end, total_records = counts
                check.greater_equal(total_records, len(installation_ids),
                                "Total records should include our test installations")
                
                # Verify we actually have pagination (more than one page)
                page_size = current_end - current_start + 1
                total_pages = math.ceil(total_records / page_size)
                check.greater(total_pages, 1, "Should have multiple pages with sufficient data")
            
            logger.info(f"Verification Successful :: Pagination elements verified with test data on {get_browser_name(ip.page)}")

    # =========================================================================
    # WILDXR-1868 — Panel Collection Field on Installation Edit Form
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.installations
    def test_installation_edit_form_panel_collection_field_present(self, installations_page):
        """
        Verify that the Panel Collection label and dropdown are present on the
        Installation Details (edit) form — the frontend change introduced by
        WILDXR-1868.

        Navigates to the first installation row and checks that both the
        'Select Panel Collection' label and its React Select dropdown are
        visible. If no installations exist in the QA environment the test is
        skipped rather than failed, since that is a data condition.

        Args:
            installations_page: List of authenticated InstallationsPage instances.
        """
        for ip in installations_page:
            browser_name = get_browser_name(ip.page)
            logger.info(f"Verifying panel collection field on Installation edit form on {browser_name}")

            row_count = ip.get_installations_table_rows().count()
            if row_count == 0:
                pytest.skip(
                    f"No installation rows in the QA environment on {browser_name} — "
                    "cannot test Installation Details form."
                )

            ip.navigate_to_first_installation_edit()

            all_present, missing = ip.verify_panel_collection_field_present()

            check.is_true(
                all_present,
                f"Panel collection field missing on Installation edit form on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(
                    f"Verification Successful :: Panel collection field present on "
                    f"Installation edit form on {browser_name}"
                )

    @pytest.mark.UI
    @pytest.mark.installations
    def test_add_installation_form_panel_collection_defaults_to_wildxr_panels(self, installations_page):
        """
        Verify that the Add Installation form pre-selects 'WildXR Panels' as
        the default panel collection — the behavior introduced by WILDXR-1868.

        The default only applies to the Add form. Existing installations may
        have any collection (or none) depending on when they were created, so
        this check is intentionally scoped to the creation path.

        Args:
            installations_page: List of authenticated InstallationsPage instances.
        """
        for ip in installations_page:
            browser_name = get_browser_name(ip.page)
            logger.info(
                f"Verifying Add Installation form defaults panel collection to "
                f"'WildXR Panels' on {browser_name}"
            )

            ip.navigate_to_add_installation()

            selected_value = ip.get_panel_collection_selected_value_text()

            check.is_true(
                selected_value.is_visible(),
                f"Expected panel collection dropdown to show 'WildXR Panels' by default "
                f"on the Add Installation form on {browser_name} — field appears empty."
            )
            if selected_value.is_visible():
                value_text = selected_value.inner_text()
                check.equal(
                    value_text,
                    "WildXR Panels",
                    f"Expected default panel collection 'WildXR Panels' on {browser_name}, "
                    f"got '{value_text}'"
                )
                logger.info(
                    f"Verification Successful :: Add Installation form defaults panel "
                    f"collection to '{value_text}' on {browser_name}"
                )