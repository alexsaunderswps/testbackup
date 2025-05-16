# users_page.py (Playwright version)
import os
from dotenv import load_dotenv
from typing import Tuple, List
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class UsersPage(BasePage):
    """
    Page object for the Users page.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators
    def get_page_title(self):
        """ Get the page title for the Users page."""
        return self.page.get_by_role("heading", name="Users")
    
    def get_page_title_text(self):
        """ Get the page title text for the Users page."""
        return self.page.get_by_role("heading", level=1).first().inner_text()
        
    def get_user_add_button(self):
        """ Get the add user button element."""
        return self.page.get_by_role("link", name="Add")
    
    # Add User Modal Element Locators
    def get_save_button(self):
        """Get the save button element on the add user modal."""
        return self.page.get_by_role("button", name="Save")
    
    def get_cancel_button(self):
        """Get the cancel button element on the add user modal."""
        return self.page.get_by_role("button", name="Cancel")
    
    # Users Table Elements
    def get_users_table_body(self):
        """Get the Users table body element/"""
        return self.page.locator("table > tbody")
    
    def get_users_table_rows(self):
        """Get the Users table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_users_name_header(self):
        """Get the Users name header element."""
        return self.page.get_by_role("cell", name="Name", exact=True)
    
    def get_users_username_header(self):
        """Get the Users username header element."""
        return self.page.get_by_role("cell", name="Username", exact=True)
    
    def get_users_roles_header(self):
        """Get the Users roles header element."""
        return self.page.get_by_role("cell", name="Roles")
    
    def get_users_organization_header(self):
        """Get the Users organization header element."""
        return self.page.get_by_role("cell", name="Organization")
    
    # Verification methods
    def verify_page_title_present(self,) -> bool:
        """ Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying page title is present")
        return super().verify_page_title_present("Users")
    
    # Check Page Element presence
    def verify_page_title(self):
        """
        Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        return super().verify_page_title("Users", tag="h1")
    
    def verify_action_elements_present(self) -> bool:
        """
        Verify that all action elements are present.
        
        Returns:
            bool: True if all action elements are present, False otherwise.
        """
        self.logger.info("Verifying all action elements are present")

        # Define the elements with readable names
        action_elements = {
            "Add User Button": self.get_user_add_button,
        }
        return self.verify_page_elements_present(action_elements, "Add User Button")
    
    def verify_all_users_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected user table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying all expected Users table elements are present")
        # Define elements with readable names
        table_elements = {
            "Table Body": self.get_users_table_body,
            "Table Rows": self.get_users_table_rows,
            "Name Header": self.get_users_name_header,
            "Username Header": self.get_users_username_header,
            "Roles Header": self.get_users_roles_header,
            "Organization Header": self.get_users_organization_header
        }
        return self.verify_page_elements_present(table_elements, "Users Table Elements")