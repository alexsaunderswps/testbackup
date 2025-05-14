#base_page.py (Playwright version)
import os
import re
from datetime import datetime
from typing import List, Dict as DICT, Tuple, Optional
from utilities.config import DEFAULT_TIMEOUT, SCREENSHOT_DIR, PAGE_SIZE
from utilities.utils import logger


class BasePage:
    """Base class for all page objects using Playwright"""
    def __init__(self, page):
        """
        Initialize BasePage

        Args:
            page: The Playwright page object.
        """
        self.page = page
        self.logger = logger
        
    # Common element locators
    def get_header_logo(self):
        """Get the header logo element"""
        return self.page.get_by_role("img", name="logo")
    
    def get_login_button(self):
        """ Get the login button element. """
        return self.page.get_by_role("button", name="Log In")
    
    def get_logout_button(self):
        """ Get the logout button element. """
        return self.page.get_by_role("button", name="LOG OUT")
    
    # Navigation menu element getters
    def get_videos_link(self):
        """Get the Videos link element"""
        return self.page.get_by_role("link", name="Videos")
    
    def get_video_catalogues_link(self):
        """Get the Video Catalogues link element"""
        return self.page.get_by_role("link", name="Video Catalogues")
    
    def get_map_markers_link(self):
        """Get the Map Markers link element"""
        return self.page.get_by_role("link", name="Map Markers")
    
    def get_species_link(self):
        """Get the Species link element"""
        return self.page.get_by_role("link", name="Species")
    
    def get_admin_button(self):
        """Get the Admin button element"""
        return self.page.get_by_role("button", name="Admin")
    
    def get_definitions_button(self):
        """Get the Definitions button element"""
        return self.page.get_by_role("button", name="Definitions")
    
    # Admin dropdown element getters
    def get_installations_link(self):
        """Get the Installations link element"""
        return self.page.get_by_role("link", name="Installations")
    
    def get_devices_link(self):
        """Get the Devices link element""" 
        return self.page.get_by_role("link", name="Devices")
    
    def get_users_link(self):
        """Get the Users link element"""
        return self.page.get_by_role("link", name="Users")
    
    def get_organizations_link(self):
        """Get the Organizations link element"""
        return self.page.get_by_role("link", name="Organizations")
    
    # Definitions dropdown element getters
    def get_countries_link(self):
        """Get the Countries link element"""
        return self.page.get_by_role("link", name="Countries")
    
    def get_iucnstatus_link(self):
        """Get the IUCN Status link element"""
        return self.page.get_by_role("link", name="IUCN Status")
    
    def get_pop_trend_link(self):
        """Get the Population Trend link element"""
        return self.page.get_by_role("link", name="Population Trend")
    
    def get_tags_link(self):
        """Get the Tags link element"""
        return self.page.get_by_role("link", name="Tags")
    
    # Pagination element getters
    def get_previous_page_button(self):
        """Get the Previous Page button element"""
        return self.page.get_by_role("button", name="Previous page")
        
    def get_next_page_button(self):
        """Get the Next Page button element"""
        return self.page.get_by_role("button", name="Next page")
    
    def get_current_page_button(self):
        """Get the Current Page button element"""
        return self.page.locator("[aria-current='page']")
    
    def get_FW_break_ellipsis_button(self):
        """Get the Forward Break Ellipsis button element"""
        return self.page.get_by_role("button", name="Jump forward")
    
    def get_BW_break_ellipsis_button(self):
        """Get the Backward Break Ellipsis button element"""
        return self.page.get_by_role("button", name="Jump backward")
    
    def get_showing_count(self):
        """Get the Showing Count element"""
        return self.page.get_by_text("Showing")
        
    # Not Currently working
    # PREVIOUS_PAGE_DISABLED = "//ul//a[@aria-label='Previous page']"
    # CURRENT_PAGE = "//ul//a[@aria-current='page']"
    
        
    # Check for page title (as h1) on each page
    def verify_page_title(self, expected_title: str, tag="h1") -> bool:
        """
        Verify that the page has the epected title in an h1 tag.

        Args:
        expected_title (str): The expected title text.
        tag (str): The HTML tag to search for (default is "h1").

        Returns:
            bool: True if correct title is present as h1, False otherwise
        """
        self.logger.info(f"Checking if {expected_title} in {tag} is present")
        try:
            heading = self.page.locator(f"{tag}:has-text('{expected_title}')")
            heading.wait_for(state="visible")
            self.logger.info(f"Page title '{expected_title}' as {tag} is present")
            return True
        except Exception as e:
            self.logger.error(f"Page title '{expected_title}' is not present: {str(e)}")
            self.take_screenshot(f"{expected_title}_Page_Title_Not_Present")
            return False

    
    # Check for common Navigation elements across pages
    def verify_all_nav_elements_present(self, elements_to_check=None) -> Tuple[bool, list]:
        """
        Verify that all expected navigation elements are present on the page.

        Args:
            elements_to_check (list, optional): List of specific elements to check. Defaults to None.
        
        Returns:
            bool: True if all elements were found, False otherwise.
            List[str]: list of missing element names (empty if all found)
        """
        page_class = self.__class__.__name__
        self.logger.info(f"Verifying all expected navigation elements are present on page: {page_class}")
        
        # Define elements with reable names
        nav_element_getters = {
            "Header Logo": self.get_header_logo,
            # "Logout Button": self.CommonLocators.LOGOUT_BUTTON,
            "Videos Link": self.get_videos_link,
            "Video Catalogues Link": self.get_video_catalogues_link,
            "Map Markers Link": self.get_map_markers_link,
            "Species Link": self.get_species_link,
            "Admin Button": self.get_admin_button,
            "Definitions Button": self.get_definitions_button,
        }
        
        # if specific elements are passed, use those instead
        if elements_to_check:
            nav_element_getters = {key: value for key, value in nav_element_getters.items() if key in elements_to_check}
            
        return self._verify_elements_present(nav_element_getters)
    
    def verify_all_admin_links_present(self, elements_to_check=None) -> Tuple[bool, list]:
        """
        Verify that all expected admin navigation elements are present in the Admin dropdown.

        Args:
            elements_to_check (list, optional): Optional list of specific element names to check.

        Returns:
            Tuple containing:
            bool: True if all expected elements are present, False otherwise.
            List[str]: List of missing element names (empty if all found).
        """
        page_class = self.__class__.__name__
        self.logger.info(f"Verifying that all expected navigation elements are present in: Admin Dropdown on {page_class}")
        
        # Click the admin button to open the dropdown
        self.get_admin_button().click()
        
        # Define elements with reable names
        admin_element_getters = {
            "Installations Link": self.get_installations_link,
            "Devices Link": self.get_devices_link,
            "Users Link": self.get_users_link,
            "Organizations Link": self.get_organizations_link,
        }
        
        # if specific elements are passed, use those instead
        if elements_to_check:
            admin_element_getters = {key: value for key, value in admin_element_getters.items() if key in elements_to_check}
            
        return self._verify_elements_present(admin_element_getters)
    
    def verify_all_definition_links_present(self, elements_to_check=None) -> Tuple[bool, list]:
        """
        Verify that all expected navigation elements are present in the Definitions dropdown.

        Args:
            elements_to_check (list, optional): Optional list of specific element names to check.

        Returns:
            Tuple containing:
            bool: True if all expected elements are present, False otherwise.
            List[str]: List of missing element names (empty if all found).
        """
        page_class = self.__class__.__name__
        self.logger.info(f"Verifying that all expected navigation elements are present in: Definintions Dropdown page: {page_class}")
        
        # Click the definitions button to open the dropdown
        self.get_definitions_button().click()
        
        # Define elements with reable names
        definition_element_getters = {
            "Countries Link": self.get_countries_link,
            "IUCN Status Link": self.get_iucnstatus_link,
            "Population Trend Link": self.get_pop_trend_link,
            "Tags Link": self.get_tags_link,
        }
        
        # if specific elements are passed, use those instead
        if elements_to_check:
            definition_element_getter = {key: value for key, value in definition_element_getter.items() if key in elements_to_check}
            
        return self._verify_elements_present(definition_element_getters)
    
    # Method for verifying page elements
    def verify_page_elements_present(self, elements_dict: DICT[str, str], context: str = "") -> Tuple[bool, List[str]]:
        """
        Verify that multiple elements exist on the page

        Args:
            elements_dict: Dictionary mapping element names to locators
            context: Optional conext string for logging (e.g., "Serch", "Table")

        Returns:
            Tuple containing:
            - bool: True if all elements are present, False otherwise
            - List[str]: List of missing elementsd names (empty if all found)
        """
        return self._verify_elements_present(elements_dict, context)
    
    def _verify_elements_present(self, elements_dict: DICT[str, str], context: str = "") -> Tuple[bool, List[str]]:
        """
        Internal helper to verify elements are present using method-based locators

        Args:
            elements_dict (DICT[str, str]): Dictionary mapping element names to getter methods
            context (str, optional): Optional conext string for logging

        Returns:
            Tuple containing:
            bool: True if all elements are present, False otherwise
            List[str]: List of missing element names (empty if all found)
        """
        all_elements_present = True
        missing_elements = []
        context_str = f" in {context}" if context else ""
        self.logger.info(f"Verifying all expected elements (for a total of {len(elements_dict)} elements) are present{context_str}")
        
        for element_name, element_getter in elements_dict.items():
            try:
                locator = element_getter()
                if locator.count() > 0:
                    self.logger.info(f"Element '{element_name}{context_str}' is present")
                else:
                    raise Exception(f"Element '{element_name}{context_str}' not found")
            except Exception as e:
                self.take_screenshot(f"{context}_{element_name}_missing".replace(" ", "_"))
                self.logger.error(f"Element '{element_name}{context_str}' is missing: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
                
        return all_elements_present, missing_elements

    # Check for pagination elements
    def verify_pagination_elements_present(self) -> Tuple[bool, list]:
        """
        Verifies pagination elements based on page size and current record count.
    
        Returns:
            Tuple[bool, list]: A tuple containing a boolean (all expected elements present)
                        and a list of missing expected elements
        """
        self.logger.info("Checking if the correct Pagination elements are present on Species Page")
        all_elements_correct = True
        issues_found = []
        
        # Get the page size from utilities.config
        page_size = PAGE_SIZE
        
        # Extract information from the showing count
        current_start = 1
        total_records = 0
        
        try:
            showing_element = self.get_showing_count()
            if showing_element.count() > 0:
                showing_text = showing_element.inner_text()
                
                # Parse "Showing x to y of z" format
                match = re.search(r'Showing\s+(\d+)\s+to\s+(\d+)\s+of\s+(\d+)', showing_text)
                if match:
                    current_start = int(match.group(1))
                    current_end = int(match.group(2))
                    total_records = int(match.group(3))
                    self.logger.info(f"Showing count parsed: {current_start} to {current_end} of {total_records}")
                else:
                    self.logger.warning(f"Could not parse showing text: {showing_text}")
            else:
                self.logger.warning("Showing count element not found")
        except Exception as e:
            self.logger.error(f"Error getting pagination info: {str(e)}")
        
        # Determine which pagination elements should be present based on extracted information
        is_first_page = (current_start == 1)
        has_multiple_pages = (total_records > page_size)
        is_last_page = (total_records <= current_start + page_size - 1)
        
        # Deine a helper function to check if an element is disbaled
        def is_element_disabled(element_getter):
            try:
                locator = element_getter()
                if locator.count() > 0:
                    return locator.get_attribute("aria-disabled") == "true" or locator.get_attribute("disabled") == "true"
                return False
            except Exception as e:
                self.logger.error(f"Error checking if element is disabled: {str(e)}")
                return False
            
        # Define elements with getter methods
        pagination_element_getters = {
            "Previous Page": self.get_previous_page_button,
            "Next Page": self.get_next_page_button,
            "Current Page": self.get_current_page_button,
            "Foward Ellipsis": self.get_FW_break_ellipsis_button,
            "Backward Ellipsis": self.get_BW_break_ellipsis_button,
            "Showing Count": self.get_showing_count
        }
        
        # Define expected state of each element
        should_be_present = {
            "Previous Page": True,
            "Next Page": True,
            "Current Page": True,
            "Foward Ellipsis": total_records > (page_size * 2), # Need at least 3 pages for ellipsis
            "Backward Ellipsis": current_start > (page_size * 2), # Need to be at least on page 3
            "Showing Count": True
        }
        
        # Define enabled/disabled state of each element
        should_be_enabled ={
            "Previous Page": has_multiple_pages and not is_first_page,
            "Next Page": has_multiple_pages and not is_last_page,
            "Current Page": True,
            "Foward Ellipsis": total_records > (page_size * 2), # Need at least 3 pages for ellipsis
            "Backward Ellipsis": current_start > (page_size * 2), # Need to be at least on page 3
            "Showing Count": True
        }
        
        for element_name, element_getter in pagination_element_getters.items():
            element_should_be_present = should_be_present[element_name]
            element_should_be_enabled = should_be_enabled[element_name]
            expected_presence = "present" if element_should_be_present else "absent"
            expected_state = "enabled" if element_should_be_enabled else "disabled"
        
            try:
                is_present = element_getter().count() > 0
                
                # Check if the element is enabled/disabled  
                is_disabled = is_element_disabled(element_getter) if is_present else False
                is_enabled = not is_disabled
                
                # Check is presence matches expectation
                if is_present != element_should_be_present:
                    self.logger.error(f"Element {element_name} should be {expected_presence} but is {'present' if is_present else 'absent'}")
                    all_elements_correct = False
                    issues_found.append(element_name)
                    self.take_screenshot(f"{element_name}_unexpected_state")
                # If element should be present, check if enabled/disabled state matches expectation
                elif is_present and element_should_be_present:
                    if is_enabled != element_should_be_enabled:
                        self.logger.error(f"Element {element_name} should be {expected_state} but is {'enabled' if is_enabled else 'disabled'}")
                        all_elements_correct = False
                        issues_found.append(element_name)
                        self.take_screenshot(f"{element_name}_unexpected_state")
                    else:
                        self.logger.info(f"Element {element_name} correctly {expected_state}")
                else:
                    self.logger.info(f"Element {element_name} correctly {expected_presence}")
            except Exception as e:
                self.logger.error(f"Error checking pagination element {element_name}: {str(e)}")
                all_elements_correct = False
                issues_found.append(element_name)
                
        return all_elements_correct,issues_found
    

    # Basic methods
    def find_logo(self) -> bool:
        """
        Check if the header logo is present on the page.

        Returns:
            bool: True if the logo is present, False otherwise.
        """
        return self.get_header_logo().count() > 0
    
    def find_login_link(self) -> bool:
        """
        Check if the login link is present on the page.

        Returns:
            bool: True if the login link is present, False otherwise.
        """
        return self.get_login_button().count() > 0
    
    def find_logout(self) -> bool:
        """
        Check if the logout button is present on the page.

        Returns:
            bool: True if the logout button is present, False otherwise.
        """
        return self.get_logout_button().count() > 0
    
    def logout_site(self) -> None:
        """
        Click the logout button to log out of the site.
        """
        self.get_logout_button().click()
        
    def get_page_title(self) -> str:
        """
        Get the title of the current page.

        Returns:
            str: The title of the current page.
        """
        return self.page.title
    
    def get_current_url(self) -> str:
        """
        Get the URL of the current page.

        Returns:
            str: The URL of the current page.
        """
        return self.page.url
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.page.goto(url)
    
    def refresh_page(self) -> None:
        """
        Refresh the current page.
        """
        self.page.reload()
        
    def go_back(self) -> None:
        """
        Navigate to the previous page in the browser history.
        """
        self.page.go_back()
        
    def go_forward(self) -> None:
        """
        Navigate to the next page in the browser history.
        """
        self.page.go_forward()
    
    # Navigation methods
    def find_videos_link(self) -> bool:
        """
        Check if the Videos link is present on the page.

        Returns:
            bool: True if the Videos link is present, False otherwise.
        """
        return self.get_videos_link().count() > 0
    
    def go_videos_page(self) -> None:
        """ 
        Click the Videos link to navigate to the Videos page.
        """
        self.get_videos_link().click()
        
    def find_video_catalogues_link(self) -> bool:
        """
        Check if the Video Catalogues link is present on the page.

        Returns:
            bool: True if the Video Catalogues link is present, False otherwise.
        """
        return self.get_video_catalogues_link().count() > 0
    
    def go_video_catalogues_page(self) -> None:
        """
        Click the Video Catalogues link to navigate to the Video Catalogues page.
        """
        self.get_video_catalogues_link().click()
        
    def find_map_markers_link(self) -> bool:
        """
        Check if the Map Markers link is present on the page.

        Returns:
            bool: True if the Map Markers link is present, False otherwise.
        """
        return self.get_map_markers_link().count() > 0
    
    def go_map_markers_page(self) -> None:
        """
        Click the Map Markers link to navigate to the Map Markers page.
        """
        self.get_map_markers_link().click()
        
    def find_species_link(self) -> bool:
        """
        Check if the Species link is present in the Definitions dropdown.

        Returns:
            bool: True if the Species link is present, False otherwise.
        """
        return self.get_species_link().count() > 0
    
    def go_species_page(self) -> None:
        """
        Click the Species link in the Definitions dropdown to navigate to the Species page.
        """
        self.get_species_link().click()
    
    # Handle Admin as it is a dropdown list
    def find_admin_button(self) -> bool:
        """
        Check if the Admin button is present on the page.

        Returns:
            bool: True if the Admin button is present, False otherwise.
        """
        return self.get_admin_button().count() > 0
    
    def click_admin_button(self) -> None:
        """
        Click the Admin Button to open the Admin dropdown.
        """
        self.get_admin_button().click()
        
    # Navigate the Admin dropdown elements
    # May need to add function to click admin button to expose admin links
    def find_installations_link(self) -> bool:
        """
        Check if the Installations link is present in the Admin dropdown.

        Returns:
            bool: True if the Installations link is present, False otherwise.
        """
        return self.get_installations_link().count() > 0
    
    def go_installations_page(self) -> None:
        """
        Click the Installations link to navigate to the Installations page.
        """
        self.get_installations_link().click()
        
    def find_devices_link(self) -> bool:
        """
        Check if the Devices link is present in the Admin dropdown.

        Returns:
            bool: True if the Devices link is present, False otherwise.
        """
        return self.get_devices_link().count() > 0
    
    def go_devices_page(self) -> None:
        """
        Click the Devices link to navigate to the Devices page.
        """
        self.get_devices_link().click()
        
    def find_users_link(self) -> bool:
        """
        Check if the Users link is present in the Admin dropdown.

        Returns:
            bool: True if the Users link is present, False otherwise.
        """
        return self.get_users_link().count() > 0
    
    def go_users_page(self) -> None:
        """
        Click the Users link to navigate to the Users page.
        """
        self.get_users_link().click()
        
    def find_organizations_link(self) -> bool:
        """
        Check if the Organizations link is present in the Admin dropdown.

        Returns:
            bool: True if the Organizations link is present, False otherwise.
        """
        return self.get_organizations_link().count() > 0
    
    def go_organizations_page(self) -> None:
        """
        Click the Organizations link to navigate to the Organizations page.
        """
        self.get_organizations_link().click()
        
    # Handle Definitions as it is a dropdown list
    def find_definitions_button(self) -> bool:
        """
        Check if the Definitions button is present on the page.

        Returns:
            bool: True if the Definitions button is present, False otherwise.
        """
        return self.get_definitions_button().count() > 0
        
    def click_definitions_button(self) -> None:
        """
        Click the Definitions button to open the Definitions dropdown.
        """
        self.get_definitions_button().click()
        
    # Navigate the Definitions dropdown elements
        
    def find_countries_link(self) -> bool:
        """
        Check if the Countries link is present in the Definitions dropdown.

        Returns:
            bool: True if the Countries link is present, False otherwise.
        """
        return self.get_countries_link().count() > 0
    
    def go_countries_page(self) -> None:
        """
        Click the Countries link in the Definitions dropdown to navigate to the Countries page.
        """
        self.get_countries_link().click()
    
    def find_iucnstatus_link(self) -> bool:
        """
        Check if the IUCN Status link is present in the Definitions dropdown.

        Returns:
            bool: True if the IUCN Status link is present, False otherwise.
        """
        return self.get_iucnstatus_link().count() > 0

    def go_iucnstatus_page(self) -> None:
        """
        Click the IUCN Status link in the Definitions dropdown to navigate to the IUCN Status page.
        """
        self.get_iucnstatus_link().click()
    
    def find_pop_trend_link(self) -> bool:
        """
        Check if the Population Trend link is present in the Definitions dropdown.

        Returns:
            bool: True if the Population Trend link is present, False otherwise.
        """
        return self.get_pop_trend_link().count() > 0

    def go_pop_trend_page(self) -> None:
        """
        Click the Population Trend link in the Definitions dropdown to navigate to the Population Trend page.
        """
        self.get_pop_trend_link().click()
    
    def find_tags_link(self) -> bool:
        """
        Check if the Tags link is present in the Definitions dropdown.

        Returns:
            bool: True if the Tags link is present, False otherwise.
        """
        return self.get_tages_link().count() > 0

    def go_tags_page(self) -> None:
        """
        Click the Tags link in the Definitions dropdown to navigate to the Tags page.
        """
        self.get_tags_link().click()
        
            
    def take_screenshot(self, name: str) -> str:
        """
        Take a screenshot with a consistent naming pattern.
        
        Args:
            name (str): Base name for the screenshot file.
            
        Returns:
            str: The filename of the saved screenshot.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        self.page.screenshot(path=path)
        self.logger.info(f"Screenshot saved: {filename}")
        return filename