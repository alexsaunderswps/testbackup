# species_page.py
import os
import re
from typing import Tuple, List
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class SpeciesPage(BasePage):
    """
    Page object for the Species page using Playwright.

    This class provides methods to interact with elements on the Species page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators
    def get_page_title(self):
        """Get the page title for the Species page."""
        return self.page.get_by_role("heading", name="Species")
    
    def get_page_title_text(self):
        """Get the text of the page title for the Species page."""
        return self.get_by_role("heading", level=1).inner_text()
    
    def get_species_search_input(self):
        """Get the species search input element."""
        return self.page.get_by_placeholder("Filter by name")
    
    def get_species_search_button(self):
        """Get the search button element."""
        return self.page.get_by_role("button", name="Search")
    
    def get_add_species_button(self):
        """Get the add species button element."""
        return self.page.get_by_role("link", name="Add")
    
    # Species Table Elements
    def get_species_table_body(self):
        """Get the species table body element."""
        return self.page.locator("table tbody")
    
    def get_species_table_rows(self):
        """Get the species table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_species_table_name_header(self):
        """Get the species table name header element."""
        return self.page.get_by_role("cell", name="Name")
    
    def get_species_table_colloquial_header(self):
        """Get the species table colloquial name header element."""
        return self.page.get_by_role("cell", name="Colloquial Name")
    
    def get_species_table_scientific_header(self):
        """Get the species table scientific name header element."""
        return self.page.get_by_role("cell", name="Scientific Name")
    
    def get_species_table_description_header(self):
        """Get the species table description header element."""
        return self.page.get_by_role("cell", name="Description")
    
    def get_species_table_iucn_header(self):
        """Get the species table IUCN status header element."""
        return self.page.get_by_role("cell", name="IUCN Status")
    
    def get_species_table_population_header(self):
        """Get the species table population trend header element."""
        return self.page.get_by_role("cell", name="Population Trend")
    
    def get_species_table_category_header(self):
        """Get the species table species category header element."""
        return self.page.get_by_role("cell", name="Species Category")
    
    def get_species_by_name(self, name):
        """ Find a species in the table by name. """
        rows = self.get_species_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").nth(0)
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None
    
    # Species Pagination Elements
    def get_species_count_text(self):
        """ Get the species count text element."""
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
    def verify_page_title_present(self) -> bool:
        r""" Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying page title is present")
        return super().verify_page_title("Species")
    
    def verify_page_title(self) -> bool:
        """
        Verify that the page title is present and is the correct "Species" title.

        Returns:
            bool: True if the page title is correct, False otherwise.
        """
        return super().verify_page_title("Species", tag="h1")

    def verify_all_species_search_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected species search elements are present.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected species search elements are present")

        # Define elements with readable names
        search_elements = {
            "Search Input": self.get_species_search_input,
            "Search Button": self.get_species_search_button,
            "Add Species Button": self.get_add_species_button,
        }
        return self.verify_page_elements_present(search_elements, "Species Search Elements")
    
    def verify_all_species_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected species table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected species table elements are present")

        # Define elements with readable names
        table_elements = {
            "Table Body": self.get_species_table_body,
            "Table Rows": self.get_species_table_rows,
            "Name Header": self.get_species_table_name_header,
            "Colloquial Name Header": self.get_species_table_colloquial_header,
            "Scientific Name Header": self.get_species_table_scientific_header,
            "Description Header": self.get_species_table_description_header,
            "IUCN Status Header": self.get_species_table_iucn_header,
            "Population Trend Header": self.get_species_table_population_header,
            "Species Category Header": self.get_species_table_category_header,
        }
        return self.verify_page_elements_present(table_elements, "Species Table Elements")

    def count_table_rows(self) -> int:
        """
        Count the number of rows in the Species Table.

        Returns:
            int: The number of rows in the Species Table.
        """
        self.logger.info("Counting the number of rows in the Species Table")
        num_rows = 0
        try:
            rows = self.get_species_table_rows()
            rows_count = rows.count()
            self.logger.info(f"Found {rows_count} rows in the Species Table")
            return rows_count
        except Exception as e:
            self.logger.error(f"An error occurred while trying to count the number of rows in the Species Table: {str(e)}")
            return 0

    def get_species_name_values(self) -> List[str]:
        """
        Get the names of all species visible in the current page of the table.

        Returns:
            List[str]: A list of species names, or empty list if none found
        """
        self.logger.info("Getting the names of all species in the table on current page")
        species_names = []
        try:
            rows = self.get_species_table_rows()
            rows_count = rows.count()
            
            for i in range(rows_count):
                try:
                    # Get the first cell (species name) from each row
                    name_cell = rows.nth(i).locator("td").first
                    species_name = name_cell.inner_text()
                    species_names.append(species_name)
                    self.logger.info(f"Found {len(species_names)} species names")
                except Exception as row_error:
                    self.logger.error(f"An error occurred while trying to get the species name from row {i}: {str(row_error)}")
                    continue
            self.logger.info(f"Found a total of {len(species_names)} species names")
            return species_names
        except Exception as e:
            self.logger.error(f"An error occurred while trying to get the species names: {str(e)}")
            return []