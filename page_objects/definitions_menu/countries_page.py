# countries_page.py (Playwright version)
import os
from dotenv import load_dotenv
from typing import Tuple, List
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class CountriesPage(BasePage):
    """
    Page object for the Countries page using Playwright.

    This class provides methods to interact with elements on the Countries page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators
    def get_page_title(self):
        """Get the page title for the Countries page."""
        return self.page.get_by_role("heading", name="Countries")
    
    def get_page_title_text(self):
        """Get the page title text for the Countries page."""
        return self.page.get_by_role("heading", level=1).first().inner_text()
    
    def get_countries_search_text(self):
        """Get the countries search text element."""
        return self.page.get_by_role("textbox", name="Search...")
    
    # Countries Table elements
    def get_countries_table_body(self):
        """Get the countries table body element."""
        return self.page.locator("table tbody")
    
    def get_countries_table_rows(self):
        """Get the countries table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_country_by_name(self, name):
        """
        Find a country in the table by name.
        
        Args:
            name (str): The name of the country to find
            
        Returns:
            Locator: The row containing the country, or None if not found
        """
        rows = self.get_countries_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").first
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None
        
    # Check Page Element presence
    def verify_page_title_present(self) -> bool:
        """ Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying the page title is present")
        return super().verify_page_title("Countries")

    def verify_page_title(self) -> bool:
        """
        Verify that the page title is present and is the correct "Countries" title.
        
        Returns:
            bool: True if the page title correct, False otherwise.
        """
        return super().verify_page_title("Countries", tag="h1")
    
    def verify_all_action_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected country action elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying all expected country action elements are present")
        # Define the elements with readable names
        action_elements = {
            "Search Text Box": self.get_countries_search_text,
        }
        return self.verify_page_elements_present(action_elements, "Country Action Elements")

    def verify_all_countries_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected countries table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying all elements on the Countries Table")

        # Define elements with readable names
        table_elements = {
            "Countries Table Body": self.get_countries_table_body,
            "Countries Table Rows": self.get_countries_table_rows
        }
        return self.verify_page_elements_present(table_elements, "Countries Table Elements")
            
    def count_table_rows(self) -> int:
        """
        Count the number of rows in the Countries Table.
        
        Returns:
            int: The number of rows in the Countries Table.
        """
        self.logger.info("Counting the number of rows in the Countries Table")
        num_rows = 0
        try:
            rows = self.get_countries_table_rows()
            rows_count = rows.count()
            self.logger.info(f"Found {rows_count} rows in the Countries Table")
            return rows_count
        except Exception as e:
            self.logger.error(f"An error occurred while trying to count the number of rows in the Countries Table: {str(e)}")
            return 0

    def get_country_name_values(self) -> List[str]:
        """
        Get the names of all countries visible in the current page of the table.
        
        Returns:
            List[str]: A list of country names, or empty list if none found
        """
        self.logger.info("Getting the names of all countries in the table on current page")
        country_names = []
        try:
            rows = self.get_countries_table_rows()
            rows_count = rows.count()
            
            for i in range(rows_count):
                try:
                    # Get the first cell (country name) from each row
                    name_cell = rows.nth(i).locator("td").first
                    country_name = name_cell.inner_text()
                    country_names.append(country_name)
                    self.logger.info(f"Found {len(country_names)} country names")
                except Exception as row_error:
                    self.logger.error(f"An error occurred while trying to get the country name from row {i}: {str(row_error)}")
                    continue
            self.logger.info(f"Found a total of {len(country_names)} country names")
            return country_names
        except Exception as e:
            self.logger.error(f"An error occurred while trying to get the country names: {str(e)}")
            return []
    
    def search_countries(self, search_term: str):
        """
        Search for countries using the search box.
        
        Args:
            search_term (str): The term to search for
        """
        self.logger.info(f"Searching for countries with term: {search_term}")
        search_box = self.get_countries_search_text()
        search_box.clear()
        search_box.fill(search_term)
        # Wait for the search to take effect
        self.page.wait_for_load_state("networkidle")
            
# TODO - with table names can check sort order
