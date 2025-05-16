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
    Page object for the Installations page.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators
    def get_page_title(self):
        """ Get the page title for the Installations page."""
        return self.page.get_by_role("heading", name="Installations")
    
    def get_page_title_text(self):
        """ Get the page title text for the Installations page."""
        return self.page.get_by_role("heading", level=1).first().inner_text()
    
    def get_installation_search_text(self):
        """ Get the installation search text element."""
        return self.page.get_by_role("textbox", name="Filter by name")
    
    def get_search_button(self):
        """ Get the search button element."""
        return self.page.get_by_role("button", name="Search")
    
    def get_installation_add_button(self):
        """ Get the add installation button element."""
        return self.page.get_by_role("link", name="Add")
    
    # Add Modal Element locators
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
    
    def get_installations_select_video_catalogue_label(self):
        """ Get the installations select video catalogue label element."""
        return self.page.get_by_text("Select Video Catalogue")  
    
    def get_installations_select_video_catalogue_dropdown(self):
        """ Get the installations select video catalogue dropdown element."""
        return self.page.locator(".css-19bb58m").nth(2)
    
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
    
   # Start back here with modal elements
   # there are some issues regarding select dropdowns because
   # of the way they are hidden and then appear at some points
   # so that nth() selectors change depending on what is visible 
    
    class InstallationPageElements:
        """Locators for the Installations page elements."""
        INSTALLATIONS_PAGE_TITLE = "//h1[text()='Installations']"
        
    class InstallationSearchElements:
        """_summary_
        """
        SEARCH_TEXT = "//input[@placeholder='Filter by name']"
        SEARCH_BUTTON = "//button[text()='Search']"
        ADD_INSTALLATION_LINK = "//a[@href='/installation/add']"
        
    class InstallationTableElements:
        """_summary_
        """
        INSTALLATION_TABLE_BODY = "//table//tbody"
        INSTALLATION_TABLE_ROWS = "//table//tbody/tr"
        INSTALLATION_NAME_HEADER = "//table/thead/tr/th[text()='Name']"
        INSTALLATION_START_LATLONG = "//table/thead/tr/th[text()='Global Start LatLong ']"
        INSTALLATION_STARTUP_VIDEO = "//table/thead/tr/th[text()='Startup Video']"
        INSTALLATION_VIDEO_CATALOGUE = "//table/thead/tr/th[text()='Video Catalogue']"
        INSTALLATION_ORGANIZATION_HEADER = "//table/thead/tr/th[text()='Organization']"
        
    # Check Page Element presence
    def verify_page_title_present(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return super().verify_page_title_present(self.InstallationPageElements.INSTALLATIONS_PAGE_TITLE)
    
    def verify_all_installations_search_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected installation search elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected installation search elements are present")
        
        # Define elements with readable names
        search_elements = {
            "Search Text Box": self.InstallationSearchElements.SEARCH_TEXT,
            "Search Button": self.InstallationSearchElements.SEARCH_BUTTON,
            "Add Installation Button": self.InstallationSearchElements.ADD_INSTALLATION_LINK,
        }
        return self.verify_page_elements_present(search_elements, "Installation Search Elements")
    
    def verify_all_installation_table_elements_present(self) -> Tuple[bool, list]:
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
            "Table Body": self.InstallationTableElements.INSTALLATION_TABLE_BODY,
            "Table Rows": self.InstallationTableElements.INSTALLATION_TABLE_ROWS,
            "Installation Name": self.InstallationTableElements.INSTALLATION_NAME_HEADER,
            "Global Start LatLong": self.InstallationTableElements.INSTALLATION_START_LATLONG,
            "Startup Video": self.InstallationTableElements.INSTALLATION_STARTUP_VIDEO,
            "Video Catalogue": self.InstallationTableElements.INSTALLATION_VIDEO_CATALOGUE,
            "Installation Organization": self.InstallationTableElements.INSTALLATION_ORGANIZATION_HEADER,
        }
        return self.verify_page_elements_present(table_elements, "Installation Table Elements")