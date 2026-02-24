# devices_page.py (Playwright version)
import os
from dotenv import load_dotenv
from typing import Tuple, List
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class DevicesPage(BasePage):
    """
    Page object for the Devices page using Playwright.
    
    This class provides methods to interact with elements on the Devices page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators - Using method-based approach for consistency
    def get_page_title(self):
        """Get the page title for the Devices page/"""
        return self.page.get_by_role("heading", name="Devices")
    
    def get_page_title_text(self):
        """Get the page title text for the Devices page."""
        return self.page.get_by_role("heading", level=1).first().inner_text()
    
    def get_devices_search_text(self):
        """Get the devices search text element."""
        return self.page.get_by_role("textbox", name="Filter by name")
    
    def get_devices_search_button(self):
        """Get the devices search button element."""
        return self.page.get_by_role("button", name="Search")
    
    def get_devices_lookup_button(self):
        """Get the devices lookup button element."""
        return self.page.get_by_role("button", name="Device Lookup")
    
    # Device Lookup Modal elements
    
    def get_search_wildxr_number_label(self):
        """Get the search WildXR number label element."""
        return self.page.get_by_text("Search by WildXR Number")
    
    def get_search_wildxr_number_text(self):
        return self.page.locator("input[name='wildXRNumber\']")
    
    def get_wildxr_number_apply_button(self):
        """Get the WildXR number apply button element."""
        return self.page.get_by_role("button", name="Apply")
    
    def get_wildxr_number_close_button(self):
        """Get the WildXR number close button element."""
        return self.page.get_by_role("button", name="x")
    
    # This needs to be built out as possible for assigning devices organizations, installations, etc.
    
    # Device Table Elements
    def get_devices_table_body(self):
        """Get the devices table body element."""
        return self.page.locator("table tbody")
    
    def get_devices_table_rows(self):
        """Get the devices table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_devices_name_header(self):
        """Get the devices name header element."""
        return self.page.get_by_role("cell", name="Name", exact=True)
    
    def get_devices_wildxr_number_header(self):
        """Get the devices WildXR number header element."""
        return self.page.get_by_role("cell", name="WildXR Number", exact=True)
    
    def get_devices_installation_header(self):
        """Get the devices installation header element."""
        return self.page.get_by_role("cell", name="Installation", exact=True)
    
    def get_devices_organization_header(self):
        """Get the devices organization header element."""
        return self.page.get_by_role("cell", name="Organization", exact=True)
    
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
    
    def get_device_by_name(self, name):
        """ Find a device in the table by name. """
        rows = self.get_devices_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").first
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None

    # Check Page Element presence
    def verify_page_title_present(self):
        """ Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying page title is present")
        return super().verify_page_title("Devices")
    
    def verify_page_title(self):
        """
        Verify that the page title is present and is the correct "Devices" title.

        Returns:
            bool: True if the page title is present, False otherwise.
        """
        return super().verify_page_title("Devices", tag="h1")
    
    def count_table_rows(self) -> int:
        """
        Count the number of rows in the Devices table.

        Returns:
            int: The number of visible device rows, or 0 if an error occurs.
        """
        self.logger.info("Counting the number of rows in the Devices table")
        try:
            row_count = self.get_devices_table_rows().count()
            self.logger.info(f"Found {row_count} rows in the Devices table")
            return row_count
        except Exception as e:
            self.logger.error(f"Error counting Devices table rows: {str(e)}")
            return 0

    def search_devices(self, name: str) -> None:
        """
        Type a search term into the filter input, click Search, and wait for
        the API response before returning.

        Sets up the response listener before clicking to avoid a race condition
        where wait_for_load_state("networkidle") could resolve before the
        search request is even initiated.

        Args:
            name (str): The device name string to filter by.
        """
        self.logger.info(f"Searching devices with filter: '{name}'")
        self.get_devices_search_text().fill(name)
        with self.page.expect_response(
            lambda r: "/Device/search" in r.url and r.status == 200
        ):
            self.get_devices_search_button().click()
        # Wait for React to process the search results and re-render the table.
        # expect_response exits as soon as the HTTP response is received, but
        # the DOM update is async — without this wait the row count is stale.
        self.page.wait_for_timeout(500)

    def verify_all_devices_action_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected device action elements are present.
        This includes the search text box, search button, and add device button.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected device action elements are present")

        # Define elements with readable names
        action_elements = {
            "Search Text Box": self.get_devices_search_text,
            "Search Button": self.get_devices_search_button,
            "Lookup Device Button": self.get_devices_lookup_button,
        }

        return self.verify_page_elements_present(action_elements, "Device Action Elements")

    def verify_all_device_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected device table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Check if all Device Table elements are present")
        
        # Define elements with readable names
        table_elements = {
            "Table Body": self.get_devices_table_body,
            "Table Rows": self.get_devices_table_rows,
            "Device Name": self.get_devices_name_header,
            "Device Serial": self.get_devices_wildxr_number_header,
            "Device Installation": self.get_devices_installation_header,
            "Device Organization": self.get_devices_organization_header,
        }
        return self.verify_page_elements_present(table_elements, "Device Table Elements")