# test_panel_collections_page_ui.py
# UI tests for the Panel Collections management page in the WildXR portal.
#
# SCOPE: Read-only structural and navigation tests. No panel collections are
# created or modified by this suite — no DELETE endpoint exists for panel
# collections, so any write operations would leave permanent test data in
# the QA environment.
#
# Covers (WILDXR-1864 / Panel Collections page):
#   - Page load and title
#   - Shared navigation elements (nav bar, admin dropdown, definitions dropdown)
#   - Panel Collections list page elements (search, + Add link, table)
#   - Table column headers
#   - Pagination elements
#   - Navigation to Add Panel Collection form (+ Add link)
#   - Add Panel Collection form elements
#   - Save button disabled state on form load
#   - Required field validation errors on empty submit
#   - Cancel returns to list
#   - Navigation to Edit Panel Collection form (row click)
#   - Search filter behaviour

import pytest
from pytest_check import check
from utilities.utils import get_browser_name, logger


class TestPanelCollectionsPageUI:
    """
    UI test suite for the Panel Collections management page.

    All tests are read-only — they navigate, inspect, and interact with the
    page without persisting any data. Each test iterates over all configured
    browser instances via the panel_collections_page fixture.
    """

    # =========================================================================
    # Page Load
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_panel_collections_page_title_present(self, panel_collections_page):
        """
        Verify that the 'Panel Collections' h1 heading is visible when the page loads.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(
                f"Verifying Panel Collections page title on {browser_name}"
            )

            result = pcp.verify_page_title_present()

            check.is_true(
                result,
                f"Expected 'Panel Collections' h1 heading to be visible on {browser_name}"
            )
            logger.info(
                f"Verification Successful :: 'Panel Collections' title is present "
                f"on {browser_name}"
            )

    # =========================================================================
    # Shared Navigation Elements
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_panel_collections_page_nav_elements_present(
        self, panel_collections_page, verify_ui_elements
    ):
        """
        Verify that all standard navigation elements are present on the
        Panel Collections page.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
            verify_ui_elements: Shared fixture providing nav/admin/definition checks.
        """
        logger.info("Verifying nav elements on the Panel Collections page")

        results = verify_ui_elements.nav_elements(panel_collections_page)

        for pcp, all_present, missing in results:
            browser_name = get_browser_name(pcp.page)
            check.is_true(
                all_present,
                f"Missing nav elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(
                    f"Verification Successful :: All nav elements present on {browser_name}"
                )

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_panel_collections_page_admin_elements_present(
        self, panel_collections_page, verify_ui_elements
    ):
        """
        Verify that all Admin dropdown links are present on the Panel Collections page.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
            verify_ui_elements: Shared fixture providing nav/admin/definition checks.
        """
        logger.info("Verifying Admin dropdown elements on the Panel Collections page")

        results = verify_ui_elements.admin_elements(panel_collections_page)

        for pcp, all_present, missing in results:
            browser_name = get_browser_name(pcp.page)
            check.is_true(
                all_present,
                f"Missing Admin dropdown elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(
                    f"Verification Successful :: All Admin elements present on {browser_name}"
                )

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_panel_collections_page_definition_elements_present(
        self, panel_collections_page, verify_ui_elements
    ):
        """
        Verify that all Definitions dropdown links are present on the
        Panel Collections page.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
            verify_ui_elements: Shared fixture providing nav/admin/definition checks.
        """
        logger.info(
            "Verifying Definitions dropdown elements on the Panel Collections page"
        )

        results = verify_ui_elements.definition_elements(panel_collections_page)

        for pcp, all_present, missing in results:
            browser_name = get_browser_name(pcp.page)
            check.is_true(
                all_present,
                f"Missing Definitions dropdown elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(
                    f"Verification Successful :: All Definitions elements present "
                    f"on {browser_name}"
                )

    # =========================================================================
    # Panel Collections List Page Elements
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_panel_collections_list_controls_present(self, panel_collections_page):
        """
        Verify that the search input, Search button, + Add link, and panel
        collections table are all present on the list page.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(
                f"Verifying Panel Collections list controls on {browser_name}"
            )

            all_present, missing = pcp.verify_all_list_elements_present()

            check.is_true(
                all_present,
                f"Missing Panel Collections list elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(
                    f"Verification Successful :: All Panel Collections list controls "
                    f"present on {browser_name}"
                )

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_panel_collections_table_columns_present(self, panel_collections_page):
        """
        Verify that all five expected column headers are present in the table.

        Expected columns (from PanelCollectionsList.tsx):
        Name, Organization, Description, Panels, Last Edited Date.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(
                f"Verifying Panel Collections table column headers on {browser_name}"
            )

            all_present, missing = pcp.verify_all_table_columns_present()

            check.is_true(
                all_present,
                f"Missing Panel Collections table column headers on "
                f"{browser_name}: {missing}"
            )
            if all_present:
                logger.info(
                    f"Verification Successful :: All 5 Panel Collections table "
                    f"columns present on {browser_name}"
                )

    @pytest.mark.UI
    @pytest.mark.panel_collections
    @pytest.mark.pagination
    def test_panel_collections_pagination_elements(
        self, panel_collections_page, verify_ui_elements
    ):
        """
        Verify that pagination elements are in the correct state on the
        Panel Collections page.

        Uses the shared pagination verification from BasePage which checks
        showing count, previous/next buttons, and ellipsis buttons against
        the actual pagination state of the current page.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
            verify_ui_elements: Shared fixture providing pagination checks.
        """
        logger.info("Verifying pagination elements on the Panel Collections page")

        results = verify_ui_elements.pagination_elements(panel_collections_page)

        for pcp, all_correct, issues in results:
            browser_name = get_browser_name(pcp.page)
            check.is_true(
                all_correct,
                f"Pagination element issues on {browser_name}: {issues}"
            )
            if all_correct:
                logger.info(
                    f"Verification Successful :: Pagination elements correct on {browser_name}"
                )

    # =========================================================================
    # Add Panel Collection Form Navigation and Structure
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_add_link_navigates_to_add_form(self, panel_collections_page):
        """
        Verify that clicking + Add navigates to the Add Panel Collection form
        with the correct 'Add Panel Collection' h1 heading.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(f"Testing + Add navigation on {browser_name}")

            pcp.navigate_to_add_panel_collection()

            heading = pcp.get_add_panel_collection_page_title()
            check.is_true(
                heading.is_visible(),
                f"Expected 'Add Panel Collection' heading after clicking + Add "
                f"on {browser_name}"
            )
            if heading.is_visible():
                logger.info(
                    f"Verification Successful :: 'Add Panel Collection' heading "
                    f"visible on {browser_name}"
                )

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_add_panel_collection_form_elements_present(self, panel_collections_page):
        """
        Verify that all expected fields and controls are present on the
        Add Panel Collection form.

        Navigates to /panelCollection/add and checks for: Name, Description,
        Panels label, + Add Panel button, Select Organization label, Cancel,
        and Save.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(
                f"Verifying Add Panel Collection form elements on {browser_name}"
            )

            pcp.navigate_to_add_panel_collection()

            all_present, missing = pcp.verify_all_add_form_elements_present()

            check.is_true(
                all_present,
                f"Missing Add Panel Collection form elements on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(
                    f"Verification Successful :: All Add Panel Collection form "
                    f"elements present on {browser_name}"
                )

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_save_button_disabled_on_add_form_load(self, panel_collections_page):
        """
        Verify that the Save button is disabled when the Add Panel Collection
        form first loads.

        The Save button is disabled until changesMade becomes true (i.e., the
        user modifies at least one field). This is enforced in
        ManageAddEditPanelCollection.tsx via 'disabled={isSaving || !changesMade}'
        on the submit button.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(
                f"Checking Save button disabled state on Add Panel Collection "
                f"form on {browser_name}"
            )

            pcp.navigate_to_add_panel_collection()

            save_button = pcp.get_save_button()

            check.is_true(
                save_button.is_visible(),
                f"Save button not visible on Add Panel Collection form on {browser_name}"
            )
            check.is_false(
                save_button.is_enabled(),
                f"Expected Save button to be disabled on initial form load on {browser_name}"
            )
            logger.info(
                f"Verification Successful :: Save button correctly disabled on "
                f"load on {browser_name}"
            )

    # =========================================================================
    # Required Field Validation
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_add_panel_collection_required_field_validation(
        self, panel_collections_page
    ):
        """
        Verify that submitting the Add Panel Collection form with no user-entered
        data shows all four required-field validation error messages.

        Triggering changesMade (by typing then clearing the Name field) is
        necessary to enable the Save button before submission.

        Expected errors (from ManageAddEditPanelCollection.tsx formIsValid()):
          - 'Panel collection name is required'
          - 'Description is required'
          - 'At least one panel is required'  (initial row has null selection)
          - 'Organization is required'  (system admin has multiple orgs; none is auto-selected)

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(
                f"Testing required field validation on Add Panel Collection "
                f"form on {browser_name}"
            )

            pcp.navigate_to_add_panel_collection()

            # Type a single character then clear it — this sets changesMade=True
            # so the Save button becomes enabled, allowing form submission.
            pcp.get_name_input().fill("x")
            pcp.get_name_input().fill("")

            pcp.click_save_button()

            all_present, missing = pcp.verify_required_field_errors_present()

            check.is_true(
                all_present,
                f"Missing required field validation errors on {browser_name}: {missing}"
            )
            if all_present:
                logger.info(
                    f"Verification Successful :: All required field errors present "
                    f"on {browser_name}"
                )

    # =========================================================================
    # Cancel Navigation
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_cancel_on_add_form_returns_to_list(self, panel_collections_page):
        """
        Verify that clicking Cancel on the Add Panel Collection form navigates
        back to the Panel Collections list page with the correct h1 heading.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(f"Testing Cancel navigation on {browser_name}")

            pcp.navigate_to_add_panel_collection()
            pcp.navigate_back_to_list()

            result = pcp.verify_page_title_present()

            check.is_true(
                result,
                f"Expected 'Panel Collections' heading after Cancel on {browser_name} "
                f"— page did not return to list"
            )
            if result:
                logger.info(
                    f"Verification Successful :: Cancel correctly returns to "
                    f"Panel Collections list on {browser_name}"
                )

    # =========================================================================
    # Edit Panel Collection Form Navigation
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_collection_row_click_navigates_to_edit_form(
        self, panel_collections_page
    ):
        """
        Verify that clicking an existing collection row opens the
        'Panel Collection Details' edit form with the correct h1 heading.

        If no collections exist in the QA environment this test is skipped
        rather than failed — that is a data condition, not a test failure.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(
                f"Testing collection row click navigation on {browser_name}"
            )

            if pcp.count_collection_rows() == 0:
                pytest.skip(
                    f"No panel collection rows in the QA environment on "
                    f"{browser_name} — cannot test edit form navigation."
                )

            pcp.navigate_to_first_collection_edit()

            heading = pcp.get_edit_panel_collection_page_title()
            check.is_true(
                heading.is_visible(),
                f"Expected 'Panel Collection Details' heading after clicking a "
                f"collection row on {browser_name}"
            )
            if heading.is_visible():
                logger.info(
                    f"Verification Successful :: 'Panel Collection Details' heading "
                    f"visible on {browser_name}"
                )

    # =========================================================================
    # Search / Filter
    # =========================================================================

    @pytest.mark.UI
    @pytest.mark.panel_collections
    def test_search_with_no_match_shows_empty_table(self, panel_collections_page):
        """
        Verify that searching for a name that matches no panel collections
        results in an empty table body rather than an error.

        Args:
            panel_collections_page: List of authenticated PanelCollectionsPage instances.
        """
        no_match_name = "ZZZZZ_WILDXR_TEST_NO_MATCH_ZZZZZ"

        for pcp in panel_collections_page:
            browser_name = get_browser_name(pcp.page)
            logger.info(f"Testing no-match search on {browser_name}")

            pcp.search_panel_collections(no_match_name)

            row_count = pcp.count_collection_rows()

            check.equal(
                row_count,
                0,
                f"Expected 0 rows for no-match search on {browser_name}, "
                f"got {row_count}"
            )
            if row_count == 0:
                logger.info(
                    f"Verification Successful :: No-match search returns empty "
                    f"table on {browser_name}"
                )
