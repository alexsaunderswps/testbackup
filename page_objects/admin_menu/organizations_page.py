# organizations_page.py (Playwright version)
import os
from dotenv import load_dotenv
from typing import Tuple, List
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class OrganizationsPage(BasePage):
    """
    Page object for the Organizations page using Playwright.

    This class provides methods to interact with elements on the Organizations page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
    
    # Element locators    
    def get_page_title(self):
        """ Get the page title for the Organizations page."""
        return self.page.locator("h1", has_text="Organizations")

    def get_page_title_text(self):
        """ Get the page title text for the Organizations page."""
        return self.page.locator("h1").first().inner_text()
    
    def get_search_text_box(self):
        """ Get the search text box element."""
        return self.page.get_by_role("textbox", name="Filter by name")
    
    def get_search_button(self):
        """ Get the search button element."""
        return self.page.get_by_role("button", name="Search")
    
    def get_add_organization_button(self):
        """ Get the add organization button element."""
        return self.page.get_by_role("link", name="Add")
    
    # Organizations Add Modal Elements locators
    def get_save_button(self):
        """ Get the save button element."""
        return self.page.get_by_role("button", name="Save")
    
    def get_cancel_button(self):
        """ Get the cancel button element."""
        return self.page.get_by_role("button", name="Cancel")
    
    def get_add_organization_textbox(self):
        """ Get the add organization textbox element."""
        return self.page.get_by_role("textbox")

    # Organization Table Elements
    def get_organization_table_body(self):
        """ Get the organization table body element."""
        return self.page.locator("table > tbody")
    
    def get_organization_table_name_header(self):
        """ Get the organization table header element."""
        return self.page.get_by_role("cell", name="Name")
    
    def get_organization_table_rows(self):
        """ Get the organization table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_organization_by_name(self, name):
        """ Find an organization in the table by name. """
        rows = self.get_organization_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").first
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None
    
    # Organizations Pagination Elements
    def get_organizations_count_text(self):
        """ Get the organizations count text element."""
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

    # Check Page Element presence
    def verify_page_title_present(self,) -> bool:
        """ Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying page title is present")
        return super().verify_page_title_present("Organizations")
    
    def verify_page_title(self):
        """
        Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        return super().verify_page_title("Organizations", tag="h1")
    
    def verify_all_organization_action_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected organization action elements are present.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying all expected organization action elements are present")

        # Define elements with readable names
        action_elements = {
            "Search Text Box": self.get_search_text_box,
            "Search Button": self.get_search_button,
            "Add Organization Link": self.get_add_organization_button
        }
        return self.verify_page_elements_present(action_elements, "Organizations page Elements")
        
    def verify_all_organization_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected organization table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying all expected Ogranization table elements are present")

        # Define elements with readable names
        table_elements = {
            "Table Body": self.get_organization_table_body,
            "Organization Name Header": self.get_organization_table_name_header,
        }
        success, missing_elements = self.verify_page_elements_present(table_elements, "Organization Table Elements")
        
        rows = self.get_organization_table_rows()
        rows_count = rows.count()
        if rows_count > 0:
            self.logger.info(f"Found {rows_count} rows in the organization table")
        else:
            self.logger.info("No rows found in the organization table")
            
        return success, missing_elements