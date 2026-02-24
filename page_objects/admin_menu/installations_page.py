# installations_page.py (Playwright version)
import os
from dotenv import load_dotenv
from typing import Tuple, List
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class InstallationsPage(BasePage):
    """
    Page object for the Installations page using Playwright.

    This class provides methods to interact with elements on the Installations page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators
    def get_page_title(self):
        """ Get the page title for the Installations page."""
        return self.page.locator("h1", has_text="Installations")

    def get_installation_search_text(self):
        """ Get the installation search text element."""
        return self.page.get_by_role("textbox", name="Filter by name")
    
    def get_installation_search_button(self):
        """ Get the search button element."""
        return self.page.get_by_role("button", name="Search")
    
    def get_installation_add_button(self):
        """ Get the add installation button element."""
        return self.page.get_by_role("link", name="Add")
    
    # Installation Table Elements
    def get_installations_table_body(self):
        """ Get the installations table body element."""
        return self.page.locator("table tbody")
    
    def get_installations_table_rows(self):
        """ Get the installations table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_installations_name_header(self):
        """ Get the installations name header element."""
        return self.page.get_by_role("cell", name="Name", exact=True)
    
    def get_installations_start_latlong_header(self):
        """ Get the installations start latitude and longitude header element."""
        return self.page.get_by_role("cell", name="Global Start LatLong ", exact=True)
    
    def get_installations_startup_video_header(self):
        """ Get the installations startup video header element."""
        return self.page.get_by_role("cell", name="Startup Video", exact=True)
    
    def get_installations_video_catalogue_header(self):
        """ Get the installations video catalogue header element."""
        return self.page.get_by_role("cell", name="Video Catalogue", exact=True)
    
    def get_installations_organization_header(self):
        """ Get the installations organization header element."""
        return self.page.get_by_role("cell", name="Organization", exact=True)
    
    def get_installation_by_name(self, name):
        """ Find an installation in the table by name. """
        rows = self.get_installations_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").first
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None
    
    # Installations Pagination Elements
    def get_installations_count_text(self):
        """ Get the installations count text element."""
        showing_element = self.get_showing_count()
        if showing_element.count() > 0:
            return showing_element.inner_text()
        return None
    
    def get_pagination_counts(self):
        """
        Extract the pagination counts from the "Showing X to Y of Z" text.

        Returns:
            Tuple[int, int, int]: A tuple containing:
                - start_count (int): The starting index of the current page.
                - end_count (int): The ending index of the current page.
                - total_count (int): The total number of items.
        """
        return super().get_pagination_counts()
    
    # Installations Add Modal Elements locators
    def get_save_button(self):
        """ Get the save button element."""
        return self.page.get_by_role("button", name="Save")
    
    def get_cancel_button(self):
        """ Get the cancel button element."""
        return self.page.get_by_role("button", name="Cancel")
    
    def get_installation_name_label(self):
        """ Get the installation name label element."""
        return self.page.get_by_text("Name")
    
    def get_installation_name_textbox(self):
        """ Get the installation name textbox element."""
        return self.page.locator("input[name=\"name\"]")
    
    def get_installation_select_organization_label(self):
        """ Get the installation select organization label element."""
        return self.page.get_by_text("Select Organization")
    
    def get_installation_select_organization_dropdown(self):
        """ Get the installation select organization dropdown element."""
        return self.page.locator(".css-19bb58m").first
    
    def get_installations_tips_label(self):
        """ Get the installations tips label element."""
        return self.page.get_by_text("Tips")
    
    def get_installations_tips_textbox(self):
        """ Get the installations tips textbox element."""
        return self.page.locator("textarea[name=\"tips\"]")
    
    def get_installations_select_tutorial_label(self):
        """ Get the installations select tutorial label element."""
        return self.page.get_by_text("Select Tutorial")
    
    def get_installations_select_tutorial_dropdown(self):
        """ Get the installations select tutorial dropdown element."""
        return self.page.locator(".css-19bb58m").nth(1)
    
    def get_installations_tutorial_textbox(self):
        """ Get the installations tutorial textbox element."""
        return self.page.locator("textarea[name=\"tutorialText\"]")

    def get_installations_apptimerlengthseconds_label(self):
        """ Get the installations app timer length label element."""
        return self.page.get_by_text("App Timer Length Seconds")
    
    def get_installations_apptimerlengthseconds_textbox(self):
        """ Get the installations app timer length textbox element."""
        return self.page.locator("input[name=\"appTimerLengthSeconds\"]")
    
    def get_installations_idletimerlengthseconds_label(self):
        """ Get the installations idle timer length label element."""
        return self.page.get_by_text("Idle Timer Length Seconds")
    
    def get_installations_idletimerlengthseconds_textbox(self):
        """ Get the installations idle timer length textbox element."""
        return self.page.locator("input[name=\"idleTimerLengthSeconds\"]")
    
    def get_installations_idletimerdelayseconds_label(self):
        """ Get the installations idle timer delay label element."""
        return self.page.get_by_text("Idle Timer Delay Seconds")
    
    def get_installations_idletimerdelayseconds_textbox(self):
        """ Get the installations idle timer delay textbox element."""
        return self.page.locator("input[name=\"idleTimerDelaySeconds\"]")
    
    def get_installations_globestartlatitude_label(self):
        """ Get the installations globe start latitude label element."""
        return self.page.get_by_text("Globe Start Latitude")
    
    def get_installations_globestartlatitude_textbox(self):
        """ Get the installations globe start latitude textbox element."""
        return self.page.locator("input[name=\"globeStartLat\"]")
    
    def get_installations_globestartlongitude_label(self):
        """ Get the installations globe start longitude label element."""
        return self.page.get_by_text("Globe Start Longitude")
    
    def get_installations_globestartlongitude_textbox(self):
        """ Get the installations globe start longitude textbox element."""
        return self.page.locator("input[name=\"globeStartLong\"]")
    
    def get_installations_select_panel_collection_label(self):
        """Get the installations select panel collection label element."""
        return self.page.get_by_text("Select Panel Collection")

    def get_installations_select_panel_collection_dropdown(self):
        """Get the installations select panel collection dropdown element."""
        return self.page.locator(
            "div:has(> input[name='panelCollectionId']) .css-19bb58m"
        )

    def get_installations_select_video_catalogue_label(self):
        """ Get the installations select video catalogue label element."""
        return self.page.get_by_text("Select Video Catalogue")

    def get_installations_select_video_catalogue_dropdown(self):
        """Get the installations select video catalogue dropdown element.

        Previously used .nth(2) which broke when panelCollectionId was added to
        the form between tutorialMode and videoCatalogueId, shifting the index.
        Now anchored to the hidden input name so index changes cannot affect it.
        """
        return self.page.locator(
            "div:has(> input[name='videoCatalogueId']) .css-19bb58m"
        )
    
    def get_installations_show_graphic_death_checkbox(self):
        """ Get the installations show graphic death checkbox element."""
        return self.page.get_by_role("checkbox", name="Show Graphic Death")
    
    def get_installations_show_graphic_death_label(self):
        """ Get the installations show graphic death label element."""
        return self.page.get_by_text("Show Graphic Death")
    
    def get_installations_show_graphic_sex_checkbox(self):
        """ Get the installations show graphic sex checkbox element."""
        return self.page.get_by_role("checkbox", name="Show Graphic Sex")

    def get_installations_show_graphic_sex_label(self):
        """ Get the installations show graphic sex label element."""
        return self.page.get_by_text("Show Graphic Sex")

    def get_installations_select_startup_video_label(self):
        """ Get the installations select startup video label element."""
        return self.page.get_by_text("Select Startup Video")

    def get_installations_select_automatic_download_mode_label(self):
        """Get the installations select automatic download mode label element.

        This label is rendered as a <span> element outside the SelectInput component
        (alongside a tooltip), so it is located by its visible text content.
        """
        return self.page.get_by_text("Select Automatic Download Mode")

    def get_installations_select_automatic_download_mode_dropdown(self):
        """Get the installations select automatic download mode dropdown element.

        Uses the hidden input's name attribute to scope the locator to the correct
        React Select container. This avoids the fragile nth() positional approach used
        by other dropdowns on this form, which breaks when conditional elements
        (e.g. startup video, favorites) appear or disappear and shift the index.
        """
        return self.page.locator(
            "div:has(> input[name='automaticDownloadModeID']) .css-19bb58m"
        )

    # -------------------------------------------------------------------------
    # Add / Edit Installation Form — Page Titles & Navigation
    # -------------------------------------------------------------------------

    def get_add_installation_page_title(self):
        """Get the 'Add Installation' h1 heading on the add form."""
        return self.page.locator("h1", has_text="Add Installation")

    def get_edit_installation_page_title(self):
        """Get the 'Installation Details' h1 heading on the edit form."""
        return self.page.locator("h1", has_text="Installation Details")

    def navigate_to_first_installation_edit(self) -> None:
        """Click the first installation row and wait for the Installation Details heading.

        React Router navigation is client-side, so this waits for the h1 heading
        to become visible rather than relying on wait_for_load_state("networkidle").
        """
        self.logger.info("Navigating to first installation edit form and waiting for heading")
        self.get_installations_table_rows().first.click()
        self.get_edit_installation_page_title().wait_for(state="visible")

    # -------------------------------------------------------------------------
    # Panel Collection Field — Display Value
    # -------------------------------------------------------------------------

    def get_panel_collection_selected_value_text(self):
        """Get the visible displayed text of the currently selected panel collection.

        React Select renders the chosen option in a child element whose class
        contains 'singleValue'. Using a partial class match avoids breakage if
        React Select's generated class names change between library versions.
        """
        return self.page.locator(
            "div:has(> input[name='panelCollectionId'])"
        ).locator("[class*='singleValue']")

    # -------------------------------------------------------------------------
    # Verification Methods
    # -------------------------------------------------------------------------

    def verify_panel_collection_field_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that the Panel Collection label and dropdown are both present
        on the Add/Edit Installation form.

        This check supports WILDXR-1868 — the panel collection selector was
        added to the installation form as the frontend counterpart to the
        API changes in WILDXR-1867.

        Returns:
            Tuple containing:
                - bool: True if both elements were found, False otherwise.
                - List[str]: List of missing element names (empty if all found).
        """
        self.logger.info("Verifying panel collection field is present on Installation form")

        field_elements = {
            "Panel Collection Label": self.get_installations_select_panel_collection_label,
            "Panel Collection Dropdown": self.get_installations_select_panel_collection_dropdown,
        }
        return self.verify_page_elements_present(field_elements, "Panel Collection Field")

    # Check Page Element presence
    def verify_page_title_present(self) -> bool:
        """ Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying page title is present")
        return super().verify_page_title("Installations")

    def verify_page_title(self) -> bool:
        """
        Verify that the page title is present and is the correct "Installations" title.
        
        Returns:
            bool: True if the page title is correct, False otherwise.
        """
        return super().verify_page_title("Installations", tag="h1")
    
    def verify_all_installation_action_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected installation action elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected installation search elements are present")
        
        # Define elements with readable names
        action_elements = {
            "Search Text Box": self.get_installation_search_text,
            "Search Button": self.get_installation_search_button,
            "Add Installation Button": self.get_installation_add_button,
        }
        return self.verify_page_elements_present(action_elements, "Installation Action Elements")
    
    def verify_all_installation_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected installation table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Check if all Installation Table elements are present")
    
        # Define elements with readable names
        table_elements = {
            "Table Body": self.get_installations_table_body,
            "Table Rows": self.get_installations_table_rows,
            "Installation Name": self.get_installations_name_header,
            "Global Start LatLong": self.get_installations_start_latlong_header,
            "Startup Video": self.get_installations_startup_video_header,
            "Video Catalogue": self.get_installations_video_catalogue_header,
            "Installation Organization": self.get_installations_organization_header
        }
        return self.verify_page_elements_present(table_elements, "Installation Table Elements")