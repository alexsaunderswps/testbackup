# iucn_status_page.py (Playwright version)
import os
from typing import Tuple, List
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class IUCNStatusPage(BasePage):
    """
    Page object for the IUCN Status page using Playwright.
    
    This class provides methods to interact with elements on the IUCN Status page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
    
    # Element locators - Using method-based approach for consistency
    def get_page_title(self):
        """Get the page title for the IUCN Status page."""
        return self.page.locator("h1", has_text="IUCN Status")

    # IUCN Status Table elements
    def get_iucn_status_table_body(self):
        """Get the IUCN Status table body element."""
        return self.page.locator("table tbody")
    
    def get_iucn_status_table_rows(self):
        """Get the IUCN Status table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_critically_endangered_status(self):
        """Get the Critically Endangered status element."""
        return self.page.get_by_role("cell", name="Critically Endangered (CR)")
    
    def get_endangered_status(self):
        """Get the Endangered status element."""
        return self.page.get_by_role("cell", name="Endangered (EN)")
    
    def get_least_concern_status(self):
        """Get the Least Concern status element."""
        return self.page.get_by_role("cell", name="Least Concern (LC)")
    
    def get_near_threatened_status(self):
        """Get the Near Threatened status element."""
        return self.page.get_by_role("cell", name="Near Threatened (NT)")
    
    def get_not_evaluated_status(self):
        """Get the Not Evaluated status element."""
        return self.page.get_by_role("cell", name="Not Evaluated (NE)")
    
    def get_various_status(self):
        """Get the Various status element."""
        return self.page.get_by_role("cell", name="Various")
    
    def get_vulnerable_status(self):
        """Get the Vulnerable status element."""
        return self.page.get_by_role("cell", name="Vulnerable (VU)")
    
    def get_iucn_status_by_name(self, name):
        """
        Find a iucn status in the table by name.
        
        Args:
            name (str): The name of the iucn status to find

        Returns:
            Locator: The row containing the iucn status, or None if not found
        """
        rows = self.get_iucn_status_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").first
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None
        
    # Check Page Element Presence
    
    def verify_iucn_page_title_present(self) -> bool:
        """ Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying the page title is present")
        return super().verify_page_title("IUCN Status")

    def verify_page_title(self) -> bool:
        """
        Verify that the page title is present and is the correct "IUCN Status" title.
        
        Returns:
            bool: True if the page title correct, False otherwise.
        """
        return super().verify_page_title("IUCN Status", tag="h1")

    def verify_all_iucn_status_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected iucn status table elements are present.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Checking IUCN Status Table Elements")

        #Define elements with readable names
        table_elements = {
            "IUCN Table Body": self.get_iucn_status_table_body,
            "IUCN Table Rows": self.get_iucn_status_table_rows
        }
        return self.verify_page_elements_present(table_elements, "IUCN Table Elements")
    
    def verify_all_iucn_status_present_in_table(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected iucn status are present in the table.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Checking IUCN Status Table Elements")
        
        # Define elements with readable names
        status_elements = {
            "Critically Endangered": self.get_critically_endangered_status,
            "Endangered": self.get_endangered_status,
            "Least Concern": self.get_least_concern_status,
            "Near Threatened": self.get_near_threatened_status,
            "Not Evaluated": self.get_not_evaluated_status,
            "Various": self.get_various_status,
            "Vulnerable": self.get_vulnerable_status,
        }
        return self.verify_page_elements_present(status_elements, "IUCN Status Elements")

    def count_table_rows(self) -> int:
        """
        Count the number of rows in the IUCN Status Table.

        Returns:
            int: The number of rows in the IUCN Status Table.
        """
        self.logger.info("Counting the number of rows in the IUCN Status Table")
        num_rows = 0
        try:
            rows = self.get_iucn_status_table_rows()
            rows_count = rows.count()
            self.logger.info(f"Found {rows_count} rows in the IUCN Status Table")
            return rows_count
        except Exception as e:
            self.logger.error(f"An error occurred while trying to count the number of rows in the Countries Table: {str(e)}")
            return 0
        
    def get_iucn_status_name_values(self) -> List[str]:
        """
        Get the names of all IUCN statuses visible in the current page of the table.

        Returns:
            List[str]: A list of IUCN status names, or empty list if none found
        """
        self.logger.info("Getting the names of all IUCN statuses in the table on current page")
        iucn_status_names = []
        try:
            rows = self.get_iucn_status_table_rows()
            rows_count = rows.count()
            
            for i in range(rows_count):
                try:
                    # Get the first cell (IUCN status name) from each row
                    name_cell = rows.nth(i).locator("td").first
                    iucn_status_name = name_cell.inner_text()
                    iucn_status_names.append(iucn_status_name)
                    self.logger.info(f"Found {len(iucn_status_names)} IUCN status names")
                except Exception as row_error:
                    self.logger.error(f"An error occurred while trying to get the IUCN status name from row {i}: {str(row_error)}")
                    continue
            self.logger.info(f"Found a total of {len(iucn_status_names)} IUCN status names")
            return iucn_status_names
        except Exception as e:
            self.logger.error(f"An error occurred while trying to get the IUCN status names: {str(e)}")
            return []