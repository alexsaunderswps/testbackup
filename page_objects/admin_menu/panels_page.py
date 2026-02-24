# panels_page.py
import os
from typing import Tuple, List
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

BASE_URL = os.getenv("QA_BASE_URL")


class PanelsPage(BasePage):
    """
    Page object for the Panels management page using Playwright.

    The Panels page renders a searchable, paginated table of panel records.
    Administrators can add new panels and edit existing ones via a form
    accessible at /panel/add and /panel/{id}/edit respectively.

    This class covers:
      - The Panels list page (table, search, + Add button)
      - The Add/Edit Panel form (all fields, validation errors, sample modal)

    Source components:
      - ManagePanelsPage.tsx  — page load, data fetching
      - PanelsList.tsx        — list table structure and column headers
      - ManageAddEditPanel.tsx — form state management and validation logic
      - AddEditPanel.tsx       — form field rendering and labels
    """

    def __init__(self, page):
        """
        Initialize PanelsPage.

        Args:
            page: The Playwright page object.
        """
        super().__init__(page)
        self.page = page
        self.logger = logger

    # -------------------------------------------------------------------------
    # Panels List Page — Header & Controls
    # -------------------------------------------------------------------------

    def get_page_title(self):
        """Get the 'Panels' h1 heading on the list page."""
        return self.page.locator("h1", has_text="Panels")

    def get_search_input(self):
        """Get the name filter text input (placeholder: 'Filter by name')."""
        return self.page.get_by_placeholder("Filter by name")

    def get_search_button(self):
        """Get the Search button on the list page."""
        return self.page.get_by_role("button", name="Search")

    def get_add_button(self):
        """Get the '+ Add' button that navigates to the Add Panel form."""
        return self.page.get_by_role("button", name="+ Add")

    # -------------------------------------------------------------------------
    # Panels List Page — Table
    # -------------------------------------------------------------------------

    def get_panels_table(self):
        """Get the panels table element."""
        return self.page.locator("table")

    def get_panels_table_rows(self):
        """Get all panel row elements in the table body."""
        return self.page.locator("table tbody tr")

    def get_table_col_name(self):
        """Get the Name column header th element."""
        return self.page.locator("th", has_text="Name")

    def get_table_col_description(self):
        """Get the Description column header th element."""
        return self.page.locator("th", has_text="Description")

    def get_table_col_visual_type(self):
        """Get the Visual Type column header th element."""
        return self.page.locator("th", has_text="Visual Type")

    def get_table_col_content_type(self):
        """Get the Content Type column header th element."""
        return self.page.locator("th", has_text="Content Type")

    def get_table_col_video_catalogue(self):
        """Get the Video Catalogue column header th element."""
        return self.page.locator("th", has_text="Video Catalogue")

    def get_table_col_header(self):
        """Get the Header column header th element."""
        return self.page.locator("th", has_text="Header")

    def get_table_col_organization(self):
        """Get the Organization column header th element."""
        return self.page.locator("th", has_text="Organization")

    # -------------------------------------------------------------------------
    # Add / Edit Panel Form — Page Titles
    # -------------------------------------------------------------------------

    def get_add_panel_page_title(self):
        """Get the 'Add Panel' h1 heading rendered on the add form."""
        return self.page.locator("h1", has_text="Add Panel")

    def get_edit_panel_page_title(self):
        """Get the 'Panel Details' h1 heading rendered on the edit form."""
        return self.page.locator("h1", has_text="Panel Details")

    # -------------------------------------------------------------------------
    # Add / Edit Panel Form — Fields and Controls
    # -------------------------------------------------------------------------

    def get_view_sample_panel_button(self):
        """Get the 'View Sample Panel' button on the add/edit form."""
        return self.page.get_by_role("button", name="View Sample Panel")

    def get_name_input(self):
        """Get the Name text input field."""
        return self.page.locator("[name='name']")

    def get_description_input(self):
        """
        Get the Description input field.

        Rendered as a textarea (rows=3) by the TextInput component when the
        'rows' prop is provided in AddEditPanel.tsx.
        """
        return self.page.locator("[name='description']")

    def get_background_image_label(self):
        """Get the 'Background Image*' label above the file upload control."""
        return self.page.get_by_text("Background Image*")

    def get_choose_png_link(self):
        """Get the 'Choose a PNG file' label that triggers the file input."""
        return self.page.get_by_text("Choose a PNG file")

    def get_visual_type_label(self):
        """Get the Visual Type dropdown label."""
        return self.page.get_by_text("Visual Type", exact=True)

    def get_content_type_label(self):
        """Get the Content Type dropdown label."""
        return self.page.get_by_text("Content Type", exact=True)

    def get_video_catalogue_label(self):
        """Get the Video Catalogue dropdown label."""
        return self.page.get_by_text("Video Catalogue", exact=True)

    def get_header_input(self):
        """Get the Header text input field."""
        return self.page.locator("[name='header']")

    def get_new_flag_checkbox(self):
        """Get the 'New' checkbox input."""
        return self.page.locator("input[name='newFlag']")

    def get_new_flag_label(self):
        """Get the label element associated with the New checkbox."""
        return self.page.locator("label[for='newFlag']")

    def get_save_button(self):
        """Get the Save submit button on the add/edit form."""
        return self.page.get_by_role("button", name="Save")

    def get_cancel_button(self):
        """Get the Cancel button on the add/edit form."""
        return self.page.get_by_role("button", name="Cancel")

    # -------------------------------------------------------------------------
    # Sample Panel Preview Modal
    # -------------------------------------------------------------------------

    def get_sample_panel_modal(self):
        """Get the sample panel preview modal dialog element."""
        return self.page.get_by_role("dialog", name="Sample panel preview")

    def get_sample_panel_close_button(self):
        """Get the × close button inside the sample panel preview modal."""
        return self.page.get_by_label("Close sample preview")

    # -------------------------------------------------------------------------
    # Validation Error Messages
    #
    # These are the exact error strings set by formIsValid() in
    # ManageAddEditPanel.tsx when required fields are missing on save.
    # -------------------------------------------------------------------------

    def get_name_error(self):
        """Get the 'Panel name is required' validation error element."""
        return self.page.get_by_text("Panel name is required")

    def get_description_error(self):
        """Get the 'Panel description is required' validation error element."""
        return self.page.get_by_text("Panel description is required")

    def get_visual_type_error(self):
        """Get the 'Visual type is required' validation error element."""
        return self.page.get_by_text("Visual type is required")

    def get_content_type_error(self):
        """Get the 'Content type is required' validation error element."""
        return self.page.get_by_text("Content type is required")

    def get_video_catalogue_error(self):
        """Get the 'Video catalogue is required' validation error element."""
        return self.page.get_by_text("Video catalogue is required")

    def get_header_error(self):
        """Get the 'Panel header is required' validation error element."""
        return self.page.get_by_text("Panel header is required")

    def get_background_image_error(self):
        """Get the 'Background image is required' validation error element."""
        return self.page.get_by_text("Background image is required")

    def get_organization_error(self):
        """Get the 'Organization is required' validation error element."""
        return self.page.get_by_text("Organization is required")

    # -------------------------------------------------------------------------
    # Verification Methods
    # -------------------------------------------------------------------------

    def verify_page_title_present(self) -> bool:
        """
        Verify that the 'Panels' h1 heading is visible on the list page.

        Returns:
            bool: True if the heading is visible, False otherwise.
        """
        return super().verify_page_title("Panels")

    def verify_all_panels_list_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected controls on the Panels list page are present.

        Checks for the name filter input, Search button, + Add button, and
        the panels table.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise.
                - List[str]: List of missing element names (empty if all found).
        """
        self.logger.info("Verifying all expected Panels list page elements are present")

        list_elements = {
            "Search Input": self.get_search_input,
            "Search Button": self.get_search_button,
            "Add Button": self.get_add_button,
            "Panels Table": self.get_panels_table,
        }
        return self.verify_page_elements_present(list_elements, "Panels List Elements")

    def verify_all_panels_table_columns_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all seven expected column headers are present in the panels table.

        Column headers are defined in PanelsList.tsx:
        Name, Description, Visual Type, Content Type, Video Catalogue, Header, Organization.

        Returns:
            Tuple containing:
                - bool: True if all column headers were found, False otherwise.
                - List[str]: List of missing column header names (empty if all found).
        """
        self.logger.info("Verifying all expected Panels table column headers are present")

        column_elements = {
            "Name Column": self.get_table_col_name,
            "Description Column": self.get_table_col_description,
            "Visual Type Column": self.get_table_col_visual_type,
            "Content Type Column": self.get_table_col_content_type,
            "Video Catalogue Column": self.get_table_col_video_catalogue,
            "Header Column": self.get_table_col_header,
            "Organization Column": self.get_table_col_organization,
        }
        return self.verify_page_elements_present(column_elements, "Panels Table Columns")

    def verify_all_add_panel_form_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected elements on the Add/Edit Panel form are present.

        Checks all fields and controls rendered by AddEditPanel.tsx:
        View Sample Panel button, Name, Description, Background Image, Visual Type,
        Content Type, Video Catalogue, Header, New checkbox, Cancel, and Save.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise.
                - List[str]: List of missing element names (empty if all found).
        """
        self.logger.info("Verifying all expected Add/Edit Panel form elements are present")

        form_elements = {
            "View Sample Panel Button": self.get_view_sample_panel_button,
            "Name Input": self.get_name_input,
            "Description Input": self.get_description_input,
            "Background Image Label": self.get_background_image_label,
            "Choose PNG Link": self.get_choose_png_link,
            "Visual Type Label": self.get_visual_type_label,
            "Content Type Label": self.get_content_type_label,
            "Video Catalogue Label": self.get_video_catalogue_label,
            "Header Input": self.get_header_input,
            "New Flag Checkbox": self.get_new_flag_checkbox,
            "Cancel Button": self.get_cancel_button,
            "Save Button": self.get_save_button,
        }
        return self.verify_page_elements_present(form_elements, "Add Panel Form Elements")

    def verify_required_field_errors_present(self) -> Tuple[bool, List[str]]:
        """
        Verify the required-field validation errors that appear after submitting
        the Add Panel form with no user-entered data.

        This covers the six fields that are empty by default when the form loads.
        Video Catalogue and Organization are intentionally excluded because they
        are auto-populated on load (from the 'All Videos' catalogue and the
        current user's default organisation), so they do not produce errors on
        a bare form submit.

        Fields checked:
          - Name            → 'Panel name is required'
          - Description     → 'Panel description is required'
          - Visual Type     → 'Visual type is required'
          - Content Type    → 'Content type is required'
          - Header          → 'Panel header is required'
          - Background Image → 'Background image is required'

        Returns:
            Tuple containing:
                - bool: True if all six error messages are visible, False otherwise.
                - List[str]: List of missing error message names (empty if all found).
        """
        self.logger.info("Verifying required field validation errors are present on Add Panel form")

        error_elements = {
            "Name Error": self.get_name_error,
            "Description Error": self.get_description_error,
            "Visual Type Error": self.get_visual_type_error,
            "Content Type Error": self.get_content_type_error,
            "Header Error": self.get_header_error,
            "Background Image Error": self.get_background_image_error,
        }
        return self.verify_page_elements_present(error_elements, "Required Field Validation Errors")

    # -------------------------------------------------------------------------
    # Action Methods
    # -------------------------------------------------------------------------

    def click_add_button(self) -> None:
        """Click the '+ Add' button to navigate to the Add Panel form."""
        self.logger.info("Clicking + Add button on the Panels list page")
        self.get_add_button().click()

    def navigate_to_add_panel(self) -> None:
        """Click the '+ Add' button and wait for the Add Panel form heading to render.

        React Router navigation is client-side and does not trigger a network request,
        so wait_for_load_state("networkidle") fires before the component renders.
        This method waits for the h1 heading to become visible instead.
        """
        self.logger.info("Navigating to Add Panel form and waiting for heading")
        self.get_add_button().click()
        self.get_add_panel_page_title().wait_for(state="visible")

    def click_first_panel_row(self) -> None:
        """Click the first row in the panels table to open the edit form."""
        self.logger.info("Clicking the first panel row to navigate to Panel Details")
        self.get_panels_table_rows().first.click()

    def navigate_to_first_panel_edit(self) -> None:
        """Click the first panel row and wait for the Panel Details heading to render.

        React Router navigation is client-side, so this method waits for the h1
        heading rather than relying on wait_for_load_state("networkidle").
        """
        self.logger.info("Navigating to first panel edit form and waiting for heading")
        self.get_panels_table_rows().first.click()
        self.get_edit_panel_page_title().wait_for(state="visible")

    def click_save_button(self) -> None:
        """Click the Save submit button on the Add/Edit Panel form."""
        self.logger.info("Clicking the Save button on the Add/Edit Panel form")
        self.get_save_button().click()

    def click_cancel_button(self) -> None:
        """Click the Cancel button to discard changes and return to the list."""
        self.logger.info("Clicking Cancel on the Add/Edit Panel form")
        self.get_cancel_button().click()

    def navigate_back_to_panels_list(self) -> None:
        """Click Cancel on the Add/Edit form and wait for the Panels list heading to render.

        React Router navigation is client-side, so this method waits for the 'Panels'
        h1 heading to become visible rather than relying on wait_for_load_state.
        """
        self.logger.info("Clicking Cancel and waiting for Panels list heading")
        self.get_cancel_button().click()
        self.get_page_title().wait_for(state="visible")

    def click_view_sample_panel_button(self) -> None:
        """Click the 'View Sample Panel' button to open the preview modal."""
        self.logger.info("Clicking the View Sample Panel button")
        self.get_view_sample_panel_button().click()

    def close_sample_panel_modal(self) -> None:
        """Click the × close button to dismiss the sample panel preview modal."""
        self.logger.info("Closing the sample panel preview modal")
        self.get_sample_panel_close_button().click()

    def search_panels(self, name: str) -> None:
        """
        Type a search term into the filter input, click Search, and wait for
        the API response before returning.

        Sets up the response listener before clicking to avoid a race condition
        where wait_for_load_state("networkidle") could resolve before the
        search request is even initiated.

        Args:
            name (str): The panel name string to filter by.
        """
        self.logger.info(f"Searching panels with filter: '{name}'")
        self.get_search_input().fill(name)
        with self.page.expect_response(
            lambda r: "panel" in r.url.lower() and r.status == 200
        ):
            self.get_search_button().click()

    def count_panel_rows(self) -> int:
        """
        Count the number of panel rows currently rendered in the table body.

        Returns:
            int: The number of visible panel rows, or 0 if an error occurs.
        """
        try:
            row_count = self.get_panels_table_rows().count()
            self.logger.info(f"Found {row_count} panel rows in the table")
            return row_count
        except Exception as e:
            self.logger.error(f"Error counting panel rows: {str(e)}")
            return 0
