# map_markers_page.py
import os
import re
from typing import Tuple, List
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables
BASE_URL = os.getenv("QA_BASE_URL")

class MapMarkersPage(BasePage):
    """
    Page object for the Map Markers page using Playwright.

    This class provides methods to interact with elements on the Map Markers page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators
    def get_page_title(self):
        """Get the page title for the Map Markers page."""
        return self.page.locator("h1", has_text="Map Marker Admin")

    def get_page_title_text(self):
        """Get the text of the page title for the Map Markers page."""
        return self.page.locator("h1").inner_text()
    
    # Tab Elements
    def get_map_markers_core_tab(self):
        """Get the core map markers tab element."""
        return self.page.get_by_role("button", name="Map Markers", exact=True)
    
    def get_map_markers_custom_tab(self):
        """Get the custom map markers tab element."""
        return self.page.get_by_role("button", name="Custom Map Markers", exact=True)
    
    def get_add_map_marker_button(self):
        """Get the add map marker button element."""
        return self.page.get_by_role("link", name="Add Map Marker")
    
    # Map Markers Table Elements
    def get_map_markers_table_body(self):
        """Get the map markers table body element."""
        return self.page.locator("table tbody")
    
    def get_map_markers_table_rows(self):
        """Get the map markers table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_map_markers_table_icon_header(self):
        """Get the map markers table icon header element."""
        return self.page.get_by_role("cell", name="Icon")
    
    def get_map_markers_table_name_header(self):
        """Get the map markers table name header element."""
        return self.page.get_by_role("cell", name="Name")
    
    def get_map_markers_table_description_header(self):
        """Get the map markers table description header element."""
        return self.page.get_by_role("cell", name="Description")
    
    def get_map_markers_table_videos_header(self):
        """Get the map markers table videos header element."""
        return self.page.get_by_role("cell", name="Videos")
    
    def get_map_markers_table_location_header(self):
        """Get the map markers table location header element."""
        return self.page.get_by_role("cell", name="Location")
    
    def get_map_markers_table_organization_header(self):
        """Get the map markers table organization header element (Custom tab only)."""
        return self.page.get_by_role("cell", name="Organization")
    
    def get_map_marker_by_name(self, name):
        """Find a map marker in the table by name."""
        rows = self.get_map_markers_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").nth(1)  # Name is usually the second column
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None
    
    # Map Markers Pagination Elements
    def get_map_markers_count_text(self):
        """Get the map markers count text element."""
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
        """Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying page title is present")
        return super().verify_page_title("Map Marker Admin")
    
    def verify_page_title(self) -> bool:
        """
        Verify that the page title is present and is the correct "Map Marker Admin" title.

        Returns:
            bool: True if the page title is correct, False otherwise.
        """
        return super().verify_page_title("Map Marker Admin", tag="h1")

    def verify_all_map_markers_action_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected map markers action elements are present.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected map markers action elements are present")

        # Define elements with readable names
        action_elements = {
            "Core Tab": self.get_map_markers_core_tab,
            "Custom Tab": self.get_map_markers_custom_tab,
            "Add Map Marker Button": self.get_add_map_marker_button,
        }
        return self.verify_page_elements_present(action_elements, "Map Markers Action Elements")
    
    def verify_all_core_map_markers_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected core map markers table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected core map markers table elements are present")

        # Make sure we're on the core tab
        core_tab = self.get_map_markers_core_tab()
        if core_tab.count() > 0 and not core_tab.get_attribute("aria-selected") == "true":
            core_tab.click()
            self.page.wait_for_timeout(1000)

        # Define elements with readable names
        table_elements = {
            "Table Body": self.get_map_markers_table_body,
            "Table Rows": self.get_map_markers_table_rows,
            "Icon Header": self.get_map_markers_table_icon_header,
            "Name Header": self.get_map_markers_table_name_header,
            "Description Header": self.get_map_markers_table_description_header,
            "Videos Header": self.get_map_markers_table_videos_header,
            "Location Header": self.get_map_markers_table_location_header,
        }
        return self.verify_page_elements_present(table_elements, "Core Map Markers Table Elements")

    def verify_all_custom_map_markers_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected custom map markers table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected custom map markers table elements are present")

        # Click on custom tab
        custom_tab = self.get_map_markers_custom_tab()
        if custom_tab.count() > 0:
            custom_tab.click()
            self.page.wait_for_timeout(1000)

        # Define elements with readable names
        table_elements = {
            "Table Body": self.get_map_markers_table_body,
            "Table Rows": self.get_map_markers_table_rows,
            "Icon Header": self.get_map_markers_table_icon_header,
            "Name Header": self.get_map_markers_table_name_header,
            "Description Header": self.get_map_markers_table_description_header,
            "Videos Header": self.get_map_markers_table_videos_header,
            "Organization Header": self.get_map_markers_table_organization_header,
            "Location Header": self.get_map_markers_table_location_header,
        }
        return self.verify_page_elements_present(table_elements, "Custom Map Markers Table Elements")

    def count_table_rows(self) -> int:
        """
        Count the number of rows in the Map Markers Table.

        Returns:
            int: The number of rows in the Map Markers Table.
        """
        self.logger.info("Counting the number of rows in the Map Markers Table")
        num_rows = 0
        try:
            rows = self.get_map_markers_table_rows()
            rows_count = rows.count()
            self.logger.info(f"Found {rows_count} rows in the Map Markers Table")
            return rows_count
        except Exception as e:
            self.logger.error(f"An error occurred while trying to count the number of rows in the Map Markers Table: {str(e)}")
            return 0

    def get_map_marker_name_values(self) -> List[str]:
        """
        Get the names of all map markers visible in the current page of the table.

        Returns:
            List[str]: A list of map marker names, or empty list if none found
        """
        self.logger.info("Getting the names of all map markers in the table on current page")
        marker_names = []
        try:
            rows = self.get_map_markers_table_rows()
            rows_count = rows.count()
            
            for i in range(rows_count):
                try:
                    # Get the name cell (usually second column) from each row
                    name_cell = rows.nth(i).locator("td").nth(1)
                    marker_name = name_cell.inner_text()
                    marker_names.append(marker_name)
                    self.logger.info(f"Found {len(marker_names)} map marker names")
                except Exception as row_error:
                    self.logger.error(f"An error occurred while trying to get the map marker name from row {i}: {str(row_error)}")
                    continue
            self.logger.info(f"Found a total of {len(marker_names)} map marker names")
            return marker_names
        except Exception as e:
            self.logger.error(f"An error occurred while trying to get the map marker names: {str(e)}")
            return []