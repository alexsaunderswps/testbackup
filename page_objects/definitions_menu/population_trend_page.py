# population_trend_page.py (Playwright version)
import os
from dotenv import load_dotenv
from typing import Tuple, List
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables
BASE_URL = os.getenv("QA_BASE_URL")

class PopulationTrendPage(BasePage):
    """
    Page object for the Population Trend page using Playwright.

    This class provides methods to interact with elements on the Population Trend page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger

    # Element locators - Using method-based approach for consistency
    def get_page_title(self):
        """Get the page title for the Population Trend page."""
        return self.page.locator("h1", has_text="Population Trend")

    def get_page_title_text(self):
        """Get the page title text for the Population Trend page."""
        return self.page.locator("h1").first().inner_text()

    # Population Trend Table elements
    def get_population_trend_table_body(self):
        """Get the Population Trend table body element."""
        return self.page.locator("table tbody")

    def get_population_trend_table_rows(self):
        """Get the Population Trend table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_decreasing_trend(self):
        """Get the Decreasing population trend element."""
        return self.page.get_by_role("cell", name="Decreasing")

    def get_increasing_trend(self):
        """Get the Increasing population trend element."""
        return self.page.get_by_role("cell", name="Increasing")

    def get_stable_trend(self):
        """Get the Stable population trend element."""
        return self.page.get_by_role("cell", name="Stable")

    def get_unknown_trend(self):
        """Get the Unknown population trend element."""
        return self.page.get_by_role("cell", name="Unknown")

    def get_various_trend(self):
        """Get the Various population trend element."""
        return self.page.get_by_role("cell", name="Various")

    def get_population_trend_by_name(self, name):
        """
        Find a population trend in the table by name.

        Args:
            name (str): The name of the population trend to find

        Returns:
            Locator: The row containing the population trend, or None if not found
        """
        rows = self.get_population_trend_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").first
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None
        
    # Check Page Element presence
    def verify_population_trend_page_title_present(self):
        """ Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying the page title is present")
        return super().verify_page_title("Population Trend")

    def verify_page_title(self) -> bool:
        """
        Verify that the page title is present and is the correct "Population Trend" title.
        
        Returns:
            bool: True if the page title correct, False otherwise.
        """
        return super().verify_page_title("Population Trend", tag="h1")

    def verify_all_population_trend_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected population trend table elements are present.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Checking Population Trend Table Elements")

        #Define elements with readable names
        table_elements = {
            "Population Trend Table Body": self.get_population_trend_table_body,
            "Population Trend Table Rows": self.get_population_trend_table_rows
        }
        return self.verify_page_elements_present(table_elements, "Population Trend Table Elements")
    
    def verify_all_population_trends_present_in_table(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected population trends are present in the table.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Checking Population Trend Table Elements")
        
        # Define expected population trends
        trend_elements = {
            "Decreasing": self.get_decreasing_trend,
            "Increasing": self.get_increasing_trend,
            "Stable": self.get_stable_trend,
            "Unknown": self.get_unknown_trend,
            "Various": self.get_various_trend
        }
        return self.verify_page_elements_present(trend_elements, "Population Trend Table Elements")
    
    def count_table_rows(self) -> int:
        """
        Count the number of rows in the Population Trend Table.

        Returns:
            int: The number of rows in the Population Trend Table.
        """
        self.logger.info("Counting the number of rows in the Population Trend Table")
        num_rows = 0
        try:
            rows = self.get_population_trend_table_rows()
            rows_count = rows.count()
            self.logger.info(f"Found {rows_count} rows in the Population Trend Table")
            return rows_count
        except Exception as e:
            self.logger.error(f"An error occurred while trying to count the number of rows in the Population Trend Table: {str(e)}")
            return 0

    def get_population_trend_name_values(self) -> List[str]:
        """
        Get the names of all population trends visible in the current page of the table.

        Returns:
            List[str]: A list of population trend names, or empty list if none found
        """
        self.logger.info("Getting the names of all population trends in the table on current page")
        population_trend_names = []
        try:
            rows = self.get_population_trend_table_rows()
            rows_count = rows.count()
            
            for i in range(rows_count):
                try:
                    # Get the first cell (population trend name) from each row
                    name_cell = rows.nth(i).locator("td").first
                    population_trend_name = name_cell.inner_text()
                    population_trend_names.append(population_trend_name)
                    self.logger.info(f"Found {len(population_trend_names)} population trend names")
                except Exception as row_error:
                    self.logger.error(f"An error occurred while trying to get the population trend name from row {i}: {str(row_error)}")
                    continue
            self.logger.info(f"Found a total of {len(population_trend_names)} population trend names")
            return population_trend_names
        except Exception as e:
            self.logger.error(f"An error occurred while trying to get the population trend names: {str(e)}")
            return []