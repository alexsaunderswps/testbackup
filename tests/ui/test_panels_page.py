# test_panels_page.py
# UI tests for the Panels management page in the WildXR portal.
#
# SCOPE: Read-only structural and navigation tests. No panels are created
# or modified by this suite — no DELETE endpoint exists for panels, so any
# write operations would leave permanent test data in the QA environment.
#
# Covers (WILDXR-1870):
#   - Page load and title
#   - Shared navigation elements (nav bar, admin dropdown, definitions dropdown)
#   - Panels list page elements (search, + Add button, table)
#   - Table column headers
#   - Pagination elements
#   - Navigation to Add Panel form (+ Add button)
#   - Add Panel form elements
#   - Save button disabled state on load
#   - View Sample Panel modal open/close
#   - Required field validation errors on empty submit
#   - Cancel returns to list
#   - Navigation to Edit Panel form (row click)
#   - Search filter behaviour

import pytest
from pytest_check import check
from utilities.utils import get_browser_name, logger


class TestPanelsPageUI:
    """
    UI test suite for the Panels management page.

    All tests are read-only — they navigate, inspect, and interact with the
    page without persisting any data. Each test iterates over all configured
    browser instances via the panels_page fixture.
    """

    # =========================================================================
    # Page Load
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panels
    def test_panels_page_title_present(self, panels_page):
        """
        Verify that the 'Panels' h1 heading is visible when the page loads.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Verifying Panels page title on {browser_name}")

            result = pp.verify_page_title_present()

            check.is_true(
                result,
                f"Expected 'Panels' h1 heading to be visible on {browser_name}"
            )
            logger.info(f"Verification Successful :: 'Panels' title is present on {browser_name}")

    # =========================================================================
    # Shared Navigation Elements
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panels
    def test_panels_page_nav_elements_present(self, panels_page, verify_ui_elements):
        """
        Verify that all standard navigation elements are present on the Panels page.

        Uses the shared verify_ui_elements fixture so nav coverage is consistent
        with other page UI tests.

        Args:
            panels_page: List of authenticated PanelsPage instances.
            verify_ui_elements: Shared fixture providing nav/admin/definition checks.
        """
        logger.info("Verifying nav elements on the Panels page")

        results = verify_ui_elements.nav_elements(panels_page)

        for pp, all_present, missing in results:
            browser_name = get_browser_name(pp.page)
            check.is_true(
                all_present,
                f"Missing nav elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(f"Verification Successful :: All nav elements present on {browser_name}")

    @pytest.mark.UI
    @pytest.mark.panels
    def test_panels_page_admin_elements_present(self, panels_page, verify_ui_elements):
        """
        Verify that all Admin dropdown links are present on the Panels page.

        Args:
            panels_page: List of authenticated PanelsPage instances.
            verify_ui_elements: Shared fixture providing nav/admin/definition checks.
        """
        logger.info("Verifying Admin dropdown elements on the Panels page")

        results = verify_ui_elements.admin_elements(panels_page)

        for pp, all_present, missing in results:
            browser_name = get_browser_name(pp.page)
            check.is_true(
                all_present,
                f"Missing Admin dropdown elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(f"Verification Successful :: All Admin elements present on {browser_name}")

    @pytest.mark.UI
    @pytest.mark.panels
    def test_panels_page_definition_elements_present(self, panels_page, verify_ui_elements):
        """
        Verify that all Definitions dropdown links are present on the Panels page.

        Args:
            panels_page: List of authenticated PanelsPage instances.
            verify_ui_elements: Shared fixture providing nav/admin/definition checks.
        """
        logger.info("Verifying Definitions dropdown elements on the Panels page")

        results = verify_ui_elements.definition_elements(panels_page)

        for pp, all_present, missing in results:
            browser_name = get_browser_name(pp.page)
            check.is_true(
                all_present,
                f"Missing Definitions dropdown elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(f"Verification Successful :: All Definitions elements present on {browser_name}")

    # =========================================================================
    # Panels List Page Elements
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panels
    def test_panels_list_controls_present(self, panels_page):
        """
        Verify that the search input, Search button, + Add button, and panels
        table are all present on the Panels list page.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Verifying Panels list controls on {browser_name}")

            all_present, missing = pp.verify_all_panels_list_elements_present()

            check.is_true(
                all_present,
                f"Missing Panels list elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(f"Verification Successful :: All Panels list controls present on {browser_name}")

    @pytest.mark.UI
    @pytest.mark.panels
    def test_panels_table_columns_present(self, panels_page):
        """
        Verify that all seven expected column headers are present in the panels table.

        Expected columns (from PanelsList.tsx):
        Name, Description, Visual Type, Content Type, Video Catalogue, Header, Organization.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Verifying Panels table column headers on {browser_name}")

            all_present, missing = pp.verify_all_panels_table_columns_present()

            check.is_true(
                all_present,
                f"Missing Panels table column headers on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(f"Verification Successful :: All 7 Panels table columns present on {browser_name}")

    @pytest.mark.UI
    @pytest.mark.panels
    @pytest.mark.pagination
    def test_panels_page_pagination_elements(self, panels_page, verify_ui_elements):
        """
        Verify that pagination elements are in the correct state on the Panels page.

        Uses the shared pagination verification from BasePage which checks showing
        count, previous/next buttons, and ellipsis buttons against the actual
        pagination state of the current page.

        Args:
            panels_page: List of authenticated PanelsPage instances.
            verify_ui_elements: Shared fixture providing pagination checks.
        """
        logger.info("Verifying pagination elements on the Panels page")

        results = verify_ui_elements.pagination_elements(panels_page)

        for pp, all_correct, issues in results:
            browser_name = get_browser_name(pp.page)
            check.is_true(
                all_correct,
                f"Pagination element issues on {browser_name}: {issues}"
            )
            if all_correct:
                logger.info(f"Verification Successful :: Pagination elements correct on {browser_name}")

    # =========================================================================
    # Add Panel Form Navigation and Structure
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panels
    def test_add_button_navigates_to_add_form(self, panels_page):
        """
        Verify that clicking + Add navigates to the Add Panel form with the
        correct 'Add Panel' h1 heading.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Testing + Add navigation on {browser_name}")

            pp.navigate_to_add_panel()

            heading = pp.get_add_panel_page_title()
            check.is_true(
                heading.is_visible(),
                f"Expected 'Add Panel' heading after clicking + Add on {browser_name}"
            )
            if heading.is_visible():
                logger.info(f"Verification Successful :: 'Add Panel' heading visible on {browser_name}")

    @pytest.mark.UI
    @pytest.mark.panels
    def test_add_panel_form_elements_present(self, panels_page):
        """
        Verify that all expected fields and controls are present on the Add Panel form.

        Navigates to /panel/add and checks for: View Sample Panel button, Name,
        Description, Background Image label and file input, Visual Type, Content Type,
        Video Catalogue, Header, New checkbox, Cancel, and Save.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Verifying Add Panel form elements on {browser_name}")

            pp.navigate_to_add_panel()

            all_present, missing = pp.verify_all_add_panel_form_elements_present()

            check.is_true(
                all_present,
                f"Missing Add Panel form elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(f"Verification Successful :: All Add Panel form elements present on {browser_name}")

    @pytest.mark.UI
    @pytest.mark.panels
    def test_save_button_disabled_on_add_form_load(self, panels_page):
        """
        Verify that the Save button is disabled when the Add Panel form first loads.

        The Save button is disabled until changesMade becomes true (i.e., the user
        modifies at least one field). This is enforced in ManageAddEditPanel.tsx via
        the 'disabled={isSaving || !changesMade}' prop on the submit button.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Checking Save button disabled state on Add Panel form on {browser_name}")

            pp.navigate_to_add_panel()

            save_button = pp.get_save_button()

            check.is_true(
                save_button.is_visible(),
                f"Save button not visible on Add Panel form on {browser_name}"
            )
            check.is_false(
                save_button.is_enabled(),
                f"Expected Save button to be disabled on initial form load on {browser_name}"
            )
            logger.info(f"Verification Successful :: Save button correctly disabled on load on {browser_name}")

    # =========================================================================
    # View Sample Panel Modal
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panels
    def test_view_sample_panel_modal_opens_and_closes(self, panels_page):
        """
        Verify that the 'View Sample Panel' button opens a modal dialog and
        that the × close button dismisses it.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Testing View Sample Panel modal on {browser_name}")

            pp.navigate_to_add_panel()

            # Open modal
            pp.click_view_sample_panel_button()

            modal = pp.get_sample_panel_modal()
            check.is_true(
                modal.is_visible(),
                f"Expected sample panel modal to be visible after clicking View Sample Panel on {browser_name}"
            )

            # Close modal
            pp.close_sample_panel_modal()

            check.is_false(
                modal.is_visible(),
                f"Expected sample panel modal to be hidden after clicking close on {browser_name}"
            )
            logger.info(f"Verification Successful :: Sample panel modal opens and closes correctly on {browser_name}")

    # =========================================================================
    # Required Field Validation
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panels
    def test_add_panel_required_field_validation(self, panels_page):
        """
        Verify that submitting the Add Panel form with no user-entered data
        shows the expected required-field validation error messages.

        The six fields checked here are empty by default on form load. Video
        Catalogue and Organization are intentionally excluded because they are
        auto-populated (from 'All Videos' catalogue and the current user's
        default organisation) and do not trigger errors on a bare submit.

        Expected errors (from ManageAddEditPanel.tsx formIsValid()):
          - 'Panel name is required'
          - 'Panel description is required'
          - 'Visual type is required'
          - 'Content type is required'
          - 'Panel header is required'
          - 'Background image is required'

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Testing required field validation on Add Panel form on {browser_name}")

            pp.navigate_to_add_panel()

            # Type a single character into the Name field then clear it — this
            # sets changesMade to True so the Save button becomes enabled, which
            # is required to trigger form submission and validation.
            pp.get_name_input().fill("x")
            pp.get_name_input().fill("")

            pp.click_save_button()

            all_present, missing = pp.verify_required_field_errors_present()

            check.is_true(
                all_present,
                f"Missing required field validation errors on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(f"Verification Successful :: All required field errors present on {browser_name}")

    # =========================================================================
    # Cancel Navigation
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panels
    def test_cancel_on_add_form_returns_to_list(self, panels_page):
        """
        Verify that clicking Cancel on the Add Panel form navigates back to the
        Panels list page with the 'Panels' h1 heading visible.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Testing Cancel navigation on {browser_name}")

            pp.navigate_to_add_panel()
            pp.navigate_back_to_panels_list()

            result = pp.verify_page_title_present()

            check.is_true(
                result,
                f"Expected 'Panels' heading after Cancel on {browser_name} — page did not return to list"
            )
            if result:
                logger.info(f"Verification Successful :: Cancel correctly returns to Panels list on {browser_name}")

    # =========================================================================
    # Edit Panel Form Navigation
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panels
    def test_panel_row_click_navigates_to_edit_form(self, panels_page):
        """
        Verify that clicking an existing panel row opens the 'Panel Details'
        edit form with the correct h1 heading.

        If no panels exist in the QA environment this test is skipped rather than
        failed — that is a data condition, not a test failure.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Testing panel row click navigation on {browser_name}")

            if pp.count_panel_rows() == 0:
                pytest.skip(
                    f"No panel rows in the QA environment on {browser_name} — "
                    "cannot test edit form navigation."
                )

            pp.navigate_to_first_panel_edit()

            heading = pp.get_edit_panel_page_title()
            check.is_true(
                heading.is_visible(),
                f"Expected 'Panel Details' heading after clicking a panel row on {browser_name}"
            )
            if heading.is_visible():
                logger.info(f"Verification Successful :: 'Panel Details' heading visible on {browser_name}")

    # =========================================================================
    # Search / Filter
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panels
    def test_search_with_no_match_shows_empty_table(self, panels_page):
        """
        Verify that searching for a name that matches no panels results in
        an empty table body rather than an error.

        Args:
            panels_page: List of authenticated PanelsPage instances.
        """
        no_match_name = "ZZZZZ_WILDXR_TEST_NO_MATCH_ZZZZZ"

        for pp in panels_page:
            browser_name = get_browser_name(pp.page)
            logger.info(f"Testing no-match search on {browser_name}")

            pp.search_panels(no_match_name)

            row_count = pp.count_panel_rows()

            check.equal(
                row_count,
                0,
                f"Expected 0 rows for no-match search on {browser_name}, got {row_count}"
            )
            if row_count == 0:
                logger.info(f"Verification Successful :: No-match search returns empty table on {browser_name}")
