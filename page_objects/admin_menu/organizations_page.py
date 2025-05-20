# organizations_page.py
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
    Page object for the Organizations page.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
    
    # Element locators    
    def get_page_title(self):
        """ Get the page title for the Organizations page."""
        return self.page.get_by_role("heading", name="Organizations")
    
    def get_page_title_text(self):
        """ Get the page title text for the Organizations page."""
        return self.page.get_by_role("heading", level=1).first().inner_text()
    
    def get_search_text_box(self):
        """ Get the search text box element."""
        return self.page.get_by_role("textbox", name="Filter by name")
    
    def get_search_button(self):
        """ Get the search button element."""
        return self.page.get_by_role("button", name="Search")
    
    def get_add_organization_button(self):
        """ Get the add organization button element."""
        return self.page.get_by_role("link", name="Add")
    
    # Add Modal Element locators
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
    
    # Verification methods
    def verify_page_title_present(self,) -> bool:
        """ Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying page title is present")
        return super().verify_page_title_present("Organizations")
    
    # Check Page Element presence
    def verify_page_title(self):
        """
        Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        return super().verify_page_title("Organizations", tag="h1")
    
    def verify_all_organization_page_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected organization page elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying all expected organization page elements are present")
        
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