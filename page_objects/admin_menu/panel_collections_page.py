# panel_collections_page.py
import os
from typing import Tuple, List
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

BASE_URL = os.getenv("QA_BASE_URL")


class PanelCollectionsPage(BasePage):
    """
    Page object for the Panel Collections management page using Playwright.

    The Panel Collections page renders a searchable, paginated table of
    collection records. Administrators can add new collections and edit
    existing ones via a form accessible at /panelCollection/add and
    /panelCollection/{id}/edit respectively.

    This class covers:
      - The Panel Collections list page (table, search, + Add link)
      - The Add/Edit Panel Collection form (all fields, validation errors)

    Source components:
      - ManagePanelCollectionsPage.tsx  — page load, data fetching
      - PanelCollectionsList.tsx        — list table structure and column headers
      - ManageAddEditPanelCollection.tsx — form state management and validation
      - AddEditPanelCollection.tsx       — form field rendering and labels
    """

    def __init__(self, page):
        """
        Initialize PanelCollectionsPage.

        Args:
            page: The Playwright page object.
        """
        super().__init__(page)
        self.page = page
        self.logger = logger

    # -------------------------------------------------------------------------
    # Panel Collections List Page — Header & Controls
    # -------------------------------------------------------------------------

    def get_page_title(self):
        """Get the 'Panel Collections' h1 heading on the list page."""
        return self.page.locator("h1", has_text="Panel Collections")

    def get_search_input(self):
        """Get the name filter text input (placeholder: 'Filter by name')."""
        return self.page.get_by_placeholder("Filter by name")

    def get_search_button(self):
        """Get the Search button on the list page."""
        return self.page.get_by_role("button", name="Search")

    def get_add_button(self):
        """
        Get the '+ Add' link that navigates to the Add Panel Collection form.

        PanelCollectionsList.tsx renders this as a React Router <Link> element,
        which becomes an <a> tag in the DOM with role='link', not role='button'.
        """
        return self.page.get_by_role("link", name="+ Add")

    # -------------------------------------------------------------------------
    # Panel Collections List Page — Table
    # -------------------------------------------------------------------------

    def get_panel_collections_table(self):
        """Get the panel collections table element."""
        return self.page.locator("table")

    def get_panel_collections_table_rows(self):
        """Get all collection row elements in the table body."""
        return self.page.locator("table tbody tr")

    def get_table_col_name(self):
        """Get the Name column header th element."""
        return self.page.locator("th", has_text="Name")

    def get_table_col_organization(self):
        """Get the Organization column header th element."""
        return self.page.locator("th", has_text="Organization")

    def get_table_col_description(self):
        """Get the Description column header th element."""
        return self.page.locator("th", has_text="Description")

    def get_table_col_panels(self):
        """Get the Panels column header th element."""
        return self.page.locator("th", has_text="Panels")

    def get_table_col_last_edited_date(self):
        """Get the Last Edited Date column header th element."""
        return self.page.locator("th", has_text="Last Edited Date")

    # -------------------------------------------------------------------------
    # Add / Edit Panel Collection Form — Page Titles
    # -------------------------------------------------------------------------

    def get_add_panel_collection_page_title(self):
        """Get the 'Add Panel Collection' h1 heading on the add form."""
        return self.page.locator("h1", has_text="Add Panel Collection")

    def get_edit_panel_collection_page_title(self):
        """Get the 'Panel Collection Details' h1 heading on the edit form."""
        return self.page.locator("h1", has_text="Panel Collection Details")

    # -------------------------------------------------------------------------
    # Add / Edit Panel Collection Form — Fields and Controls
    # -------------------------------------------------------------------------

    def get_name_input(self):
        """Get the Name text input field."""
        return self.page.locator("[name='name']")

    def get_description_input(self):
        """
        Get the Description input field.

        Rendered as a textarea (rows=3) by the TextInput component when the
        'rows' prop is provided in AddEditPanelCollection.tsx.
        """
        return self.page.locator("[name='description']")

    def get_panels_section_label(self):
        """
        Get the 'Panels' label above the panel selection rows on the form.

        Rendered as a <label> wrapping a <span>Panels</span> and an info
        tooltip icon in AddEditPanelCollection.tsx.
        """
        return self.page.get_by_text("Panels", exact=True)

    def get_add_panel_row_button(self):
        """
        Get the '+ Add Panel' button that appends a new panel selection row.

        This is a type='button' element (not a submit), rendered inside the
        Panels section of the form in AddEditPanelCollection.tsx.
        """
        return self.page.get_by_role("button", name="+ Add Panel")

    def get_select_organization_label(self):
        """
        Get the 'Select Organization' label for the organization dropdown.

        Visible only for system admin users or users belonging to more than
        one organization, as conditional logic in AddEditPanelCollection.tsx
        hides this dropdown for single-org users.
        """
        return self.page.get_by_text("Select Organization", exact=True)

    def get_save_button(self):
        """Get the Save submit button on the add/edit form."""
        return self.page.get_by_role("button", name="Save")

    def get_cancel_button(self):
        """Get the Cancel button on the add/edit form."""
        return self.page.get_by_role("button", name="Cancel")

    # -------------------------------------------------------------------------
    # Validation Error Messages
    #
    # These are the exact error strings set by formIsValid() in
    # ManageAddEditPanelCollection.tsx when required fields are missing on save.
    # -------------------------------------------------------------------------

    def get_name_error(self):
        """Get the 'Panel collection name is required' validation error element."""
        return self.page.get_by_text("Panel collection name is required")

    def get_description_error(self):
        """Get the 'Description is required' validation error element."""
        return self.page.get_by_text("Description is required")

    def get_panels_error(self):
        """Get the 'At least one panel is required' validation error element."""
        return self.page.get_by_text("At least one panel is required")

    def get_organization_error(self):
        """Get the 'Organization is required' validation error element."""
        return self.page.get_by_text("Organization is required")

    # -------------------------------------------------------------------------
    # Verification Methods
    # -------------------------------------------------------------------------

    def verify_page_title_present(self) -> bool:
        """
        Verify that the 'Panel Collections' h1 heading is visible on the list page.

        Returns:
            bool: True if the heading is visible, False otherwise.
        """
        return super().verify_page_title("Panel Collections")

    def verify_all_list_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected controls on the Panel Collections list page are present.

        Checks for the name filter input, Search button, + Add link, and the table.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise.
                - List[str]: List of missing element names (empty if all found).
        """
        self.logger.info(
            "Verifying all expected Panel Collections list page elements are present"
        )
        list_elements = {
            "Search Input": self.get_search_input,
            "Search Button": self.get_search_button,
            "Add Link": self.get_add_button,
            "Panel Collections Table": self.get_panel_collections_table,
        }
        return self.verify_page_elements_present(
            list_elements, "Panel Collections List Elements"
        )

    def verify_all_table_columns_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all five expected column headers are present in the table.

        Column headers are defined in PanelCollectionsList.tsx:
        Name, Organization, Description, Panels, Last Edited Date.

        Returns:
            Tuple containing:
                - bool: True if all column headers were found, False otherwise.
                - List[str]: List of missing column header names (empty if all found).
        """
        self.logger.info(
            "Verifying all expected Panel Collections table column headers are present"
        )
        column_elements = {
            "Name Column": self.get_table_col_name,
            "Organization Column": self.get_table_col_organization,
            "Description Column": self.get_table_col_description,
            "Panels Column": self.get_table_col_panels,
            "Last Edited Date Column": self.get_table_col_last_edited_date,
        }
        return self.verify_page_elements_present(
            column_elements, "Panel Collections Table Columns"
        )

    def verify_all_add_form_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected elements on the Add/Edit Panel Collection form are present.

        Checks fields and controls rendered by AddEditPanelCollection.tsx:
        Name, Description, Panels label, + Add Panel button, Select Organization label,
        Cancel, and Save.

        The organization dropdown is conditionally rendered only for system admins
        or multi-org users. Since the test suite runs as system admin, this element
        is expected to be visible.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise.
                - List[str]: List of missing element names (empty if all found).
        """
        self.logger.info(
            "Verifying all expected Add/Edit Panel Collection form elements are present"
        )
        form_elements = {
            "Name Input": self.get_name_input,
            "Description Input": self.get_description_input,
            "Panels Label": self.get_panels_section_label,
            "Add Panel Row Button": self.get_add_panel_row_button,
            "Select Organization Label": self.get_select_organization_label,
            "Cancel Button": self.get_cancel_button,
            "Save Button": self.get_save_button,
        }
        return self.verify_page_elements_present(
            form_elements, "Add Panel Collection Form Elements"
        )

    def verify_required_field_errors_present(self) -> Tuple[bool, List[str]]:
        """
        Verify the required-field validation errors that appear after submitting
        the Add Panel Collection form with no user-entered data.

        All four fields are empty by default when the form loads as system admin:
          - Name is empty by default
          - Description is empty by default
          - Panels — the initial row has no panel selected (null), so panels list is empty
          - Organization — system admin sees multiple orgs, none is auto-selected

        Validation errors from ManageAddEditPanelCollection.tsx formIsValid():
          - 'Panel collection name is required'
          - 'Description is required'
          - 'At least one panel is required'
          - 'Organization is required'

        Returns:
            Tuple containing:
                - bool: True if all four error messages are visible, False otherwise.
                - List[str]: List of missing error message names (empty if all found).
        """
        self.logger.info(
            "Verifying required field validation errors are present on "
            "Add Panel Collection form"
        )
        error_elements = {
            "Name Error": self.get_name_error,
            "Description Error": self.get_description_error,
            "Panels Error": self.get_panels_error,
            "Organization Error": self.get_organization_error,
        }
        return self.verify_page_elements_present(
            error_elements, "Required Field Validation Errors"
        )

    # -------------------------------------------------------------------------
    # Action Methods
    # -------------------------------------------------------------------------

    def navigate_to_add_panel_collection(self) -> None:
        """
        Click the '+ Add' link and wait for the Add Panel Collection form heading.

        React Router navigation is client-side and does not trigger a network
        request, so wait_for_load_state("networkidle") fires before the component
        renders. This method waits for the h1 heading to become visible instead.
        """
        self.logger.info(
            "Navigating to Add Panel Collection form and waiting for heading"
        )
        self.get_add_button().click()
        self.get_add_panel_collection_page_title().wait_for(state="visible")

    def navigate_to_first_collection_edit(self) -> None:
        """
        Click the first collection row and wait for the Panel Collection Details
        heading to render.

        React Router navigation is client-side, so this method waits for the h1
        heading rather than relying on wait_for_load_state("networkidle").
        """
        self.logger.info(
            "Navigating to first panel collection edit form and waiting for heading"
        )
        self.get_panel_collections_table_rows().first.click()
        self.get_edit_panel_collection_page_title().wait_for(state="visible")

    def navigate_back_to_list(self) -> None:
        """
        Click Cancel on the Add/Edit form and wait for the Panel Collections
        list heading to render.

        React Router navigation is client-side, so this method waits for the
        'Panel Collections' h1 heading to become visible.
        """
        self.logger.info(
            "Clicking Cancel and waiting for Panel Collections list heading"
        )
        self.get_cancel_button().click()
        self.get_page_title().wait_for(state="visible")

    def click_save_button(self) -> None:
        """Click the Save submit button on the Add/Edit Panel Collection form."""
        self.logger.info("Clicking the Save button on the Add/Edit Panel Collection form")
        self.get_save_button().click()

    def search_panel_collections(self, name: str) -> None:
        """
        Type a search term into the filter input, click Search, and wait for
        the API response before returning.

        Sets up the response listener before clicking to avoid a race condition
        where wait_for_load_state("networkidle") could resolve before the
        search request is even initiated.

        Args:
            name (str): The panel collection name string to filter by.
        """
        self.logger.info(f"Searching panel collections with filter: '{name}'")
        self.get_search_input().fill(name)
        with self.page.expect_response(
            lambda r: "panelcollection" in r.url.lower() and r.status == 200
        ):
            self.get_search_button().click()

    def count_collection_rows(self) -> int:
        """
        Count the number of collection rows currently rendered in the table body.

        Returns:
            int: The number of visible collection rows, or 0 if an error occurs.
        """
        try:
            row_count = self.get_panel_collections_table_rows().count()
            self.logger.info(f"Found {row_count} panel collection rows in the table")
            return row_count
        except Exception as e:
            self.logger.error(f"Error counting panel collection rows: {str(e)}")
            return 0
