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
    
    # Navigation methods for pagination
    def navigate_to_next_page(self) -> bool:
        """
        Navigate to the next page by clicking the next page button.
        
        Returns:
            bool: True if the next page button was clicked successfully, False otherwise.
        """
        next_page_button = self.get_next_page_button()
        if next_page_button.count() > 0 and next_page_button.get_attribute("aria-disabled") != "true":
            self.logger.info("Navigating to the next page")
            next_page_button.click()
            return True
        else:
            self.logger.warning("Failed to navigate to the next page: Next page button is disabled or not found")
            return False
    
    def navigate_to_previous_page(self) -> bool:
        """
        Navigate to the previous page by clicking the previous page button.

        Returns:
            bool: True if the previous page button was clicked successfully, False otherwise.
        """
        previous_page_button = self.get_previous_page_button()
        if previous_page_button.count() > 0 and previous_page_button.get_attribute("aria-disabled") != "true":
            self.logger.info("Navigating to the previous page")
            previous_page_button.click()
            return True
        else:
            self.logger.warning("Failed to navigate to the previous page: Previous page button is disabled or not found")
            return False
        
    def navigate_foward_ellipsis(self) -> bool:
        """
        Naigate forward by click the foward ellipsis button.

        Returns:
            bool: True if the foward ellipsis button was clicked successfully, False otherwise.
        """
        forward_ellipsis_button = self.get_FW_break_ellipsis_button()
        if forward_ellipsis_button.count() > 0 and forward_ellipsis_button.get_attribute("aria-disabled") != "true":
            self.logger.info("Navigating to the next page using foward ellipsis")
            forward_ellipsis_button.click()
            return True
        else:
            self.logger.warning("Failed to navigate to the next page using foward ellipsis: Foward ellipsis button is disabled or not found")
            return False
        
    def navigate_backward_ellipsis(self) -> bool:
        """
        Navigate backward by clicking the backward ellipsis button.

        Returns:
            bool: True if the backward ellipsis button was clicked successfully, False otherwise.
        """
        backward_ellipsis_button = self.get_BW_break_ellipsis_button()
        if backward_ellipsis_button.count() > 0 and backward_ellipsis_button.get_attribute("aria-disabled") != "true":
            self.logger.info("Navigating to the previous page using backward ellipsis")
            backward_ellipsis_button.click()
            return True
        else:
            self.logger.warning("Failed to navigate to the previous page using backward ellipsis: Backward ellipsis button is disabled or not found")
            return False
        
    def get_current_page_number(self) -> int:
        """
        Get the current page number from the pagination element.

        Returns:
            int: The current page number, or None if not found.
        """
        try:
            # Try first using aria-current attribute
            current_page = self.page.locator("[aria-current='page']")
            if current_page.count() > 0:
                page_text = current_page.inner_text().strip()
                return int(page_text)
        except Exception as e:
            self.logger.debug(f"Could not get current page using aria-current: {str(e)}")
            
        try:
            # Try finding by role and name containing "is your current page"
            current_page = self.page.get_by_role("button", name=lambda n: "is your current page" in str(n) if n else False)
            if current_page.count() > 0:
                # Try to extract from name or inner text
                text = current_page.inner_text().strip()
                if text and text.isdigit():
                    return int(text)
        except Exception as e:
            self.logger.debug(f"Could not get current page using button role: {str(e)}")
            
        return None  # Return None if we couldn't determine the page number
    
    def get_pagination_counts(self) -> Tuple[int, int, int]:
        """
        Extract pagination counts from the 'Showing X to Y of Z' text.
        
        Returns:
            Tuple[int, int, int]: A tuple containing the start, end, and total record counts.
        """
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
                return current_start, current_end, total_records
            else:
                self.logger.warning(f"Could not parse showing text: {showing_text}")
                return None, None, None
        else:
            self.logger.warning("Showing count element not found")
            return None, None, None
        
    def verify_navigation_updates_page(self, action, expected_page=None) -> bool:
        """
        Verify that the navigation action updates the page correctly.

        Args:
            action (str): The action to perform (e.g., self.navigate_to_next_page).
            expected_page (str, optional): The expected page number after navigation, or None to calculate automatically.

        Returns:
            bool: True if the navigation was successful, False otherwise.
        """
        initial_page = self.get_current_page_number()
        if initial_page is None:
            self.logger.error("Could not determine the initial page number")
            return False

        if expected_page is None:
            if action.__name__ == "navigate_to_next_page":
                expected_page = initial_page + 1
            elif action.__name__ == "navigate_to_previous_page":
                expected_page = initial_page - 1
            else:
                self.logger.error(f"Cannot determine the expected page for action: {action.__name__}")
                return False
            
        # Perform the navigation action
        success = action()
        if not success:
            self.logger.error(f"Navigation action {action.__name__} failed")
            return False
        
        # Wait for the page to update
        self.page.wait_for_load_state("networkidle")
        
        # Check if the page number has updated
        new_page = self.get_current_page_number()
        if new_page == expected_page:
            self.logger.info(f"Navigation action {action.__name__} was successful: Page updated to {new_page}")
            return True
        else:
            self.logger.error(f"Navigation action {action.__name__} failed: Page number is still {new_page}, expected {expected_page}")
            return False    
        
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
    
    def verify_all_admin_elements_present(self, elements_to_check=None) -> Tuple[bool, list]:
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
    
    def verify_all_definition_elements_present(self, elements_to_check=None) -> Tuple[bool, list]:
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
            definition_element_getters = {key: value for key, value in definition_element_getters.items() if key in elements_to_check}
            
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
    def verify_all_pagination_elements_present(self) -> Tuple[bool, list]:
        """
        Verifies pagination elements based on functional availability rather than DOM presence.
        
        This method checks whether pagination elements are functionally available (visible and enabled)
        rather than just present in the DOM. This approach aligns with modern web development practices
        where elements are always rendered but their state is controlled through CSS and attributes.
        
        Returns:
            Tuple[bool, list]: A tuple containing a boolean (all expected elements are functional)
                            and a list of elements that don't match expectations
        """
        self.logger.info("Checking if pagination elements are functionally available on the page")
        all_elements_correct = True
        issues_found = []
        
        # Get the page size from utilities.config
        page_size = PAGE_SIZE
        
        # Extract information from the showing count to understand pagination state
        current_start = 1
        current_end = 0
        total_records = 0
        showing_element_exists = False
        
        try:
            self.page.wait_for_timeout(3000)
            showing_element = self.get_showing_count()
            if showing_element.count() > 0:
                showing_element_exists = True
                showing_text = showing_element.inner_text()
                
                # Parse "Showing x to y of z" format to understand current pagination state
                match = re.search(r'Showing\s+(\d+)\s+to\s+(\d+)\s+of\s+(\d+)', showing_text)
                if match:
                    current_start = int(match.group(1))
                    current_end = int(match.group(2))
                    total_records = int(match.group(3))
                    self.logger.info(f"Pagination state: {current_start} to {current_end} of {total_records}")
                else:
                    self.logger.warning(f"Could not parse showing text: {showing_text}")
            else:
                self.logger.info("No showing count element - likely no records to display")
        except Exception as e:
            self.logger.error(f"Error getting pagination info: {str(e)}")
        
        # Calculate pagination state based on your business rules
        is_first_page = (current_start == 1)
        has_multiple_pages = (total_records > page_size)
        is_last_page = (total_records <= current_start + page_size - 1)
        current_page_number = ((current_start - 1) // page_size) + 1 if current_start > 0 else 1
        total_pages = (total_records + page_size - 1) // page_size if total_records > 0 else 0
        
        # Log calculated state for debugging
        self.logger.info(f"Calculated pagination state:")
        self.logger.info(f"  - Current page: {current_page_number}")
        self.logger.info(f"  - Total pages: {total_pages}")
        self.logger.info(f"  - Is first page: {is_first_page}")
        self.logger.info(f"  - Is last page: {is_last_page}")
        self.logger.info(f"  - Has multiple pages: {has_multiple_pages}")
        
        # Define pagination element getters
        pagination_element_getters = {
            "Previous Page": self.get_previous_page_button,
            "Next Page": self.get_next_page_button,
            "Current Page": self.get_current_page_button,
            "Foward Ellipsis": self.get_FW_break_ellipsis_button,
            "Backward Ellipsis": self.get_BW_break_ellipsis_button,
            "Showing Count": self.get_showing_count
        }
        
        # Define when each element should be functionally available based on your business rules
        should_be_functional = {
            # Previous/Next buttons should be functional when there are multiple pages
            # and we're not at the boundary
            "Previous Page": has_multiple_pages and not is_first_page,
            "Next Page": has_multiple_pages and not is_last_page,
            
            # Current page and showing count should always be functional when there's data
            "Current Page": showing_element_exists,
            "Showing Count": showing_element_exists,
            
            # Forward ellipsis should be functional when there are more than 2 pages 
            # and we're not on the last 3 pages
            "Foward Ellipsis": (total_pages > 2 and current_page_number <= total_pages - 3),
            
            # Backward ellipsis should be functional when there are more than 3 pages
            # and we're on page 4 or higher
            "Backward Ellipsis": (total_pages > 3 and current_page_number >= 4)
        }
        
        # Check each pagination element
        for element_name, element_getter in pagination_element_getters.items():
            element_should_be_functional = should_be_functional[element_name]
            
            try:
                # Get the element locator
                locator = element_getter()
                is_present_in_dom = locator.count() > 0
                
                if not is_present_in_dom:
                    # Element not in DOM at all - this might be acceptable depending on implementation
                    if element_should_be_functional:
                        self.logger.error(f"Element {element_name} should be functional but is not present in DOM")
                        all_elements_correct = False
                        issues_found.append(element_name)
                        self.take_screenshot(f"{element_name}_missing_from_dom")
                    else:
                        self.logger.info(f"Element {element_name} correctly absent from DOM")
                    continue
                
                # Element is present in DOM, now check if it's functionally available
                is_functionally_available = self._is_element_functionally_available(
                    locator, element_name
                )
                
                # Compare expected vs actual functional state
                if is_functionally_available != element_should_be_functional:
                    expected_state = "functional" if element_should_be_functional else "disabled/hidden"
                    actual_state = "functional" if is_functionally_available else "disabled/hidden"
                    
                    self.logger.error(f"Element {element_name} should be {expected_state} but is {actual_state}")
                    all_elements_correct = False
                    issues_found.append(element_name)
                    self.take_screenshot(f"{element_name}_unexpected_functional_state")
                else:
                    correct_state = "functional" if is_functionally_available else "properly disabled/hidden"
                    self.logger.info(f"Element {element_name} is correctly {correct_state}")
                    
            except Exception as e:
                self.logger.error(f"Error checking pagination element {element_name}: {str(e)}")
                all_elements_correct = False
                issues_found.append(element_name)
        
        return all_elements_correct, issues_found

    def _is_element_functionally_available(self, locator, element_name: str) -> bool:
        """
        Helper method to determine if an element is functionally available to the user.
        
        An element is considered functionally available if it is:
        1. Visible on the page
        2. Not disabled through various disability mechanisms (aria-disabled, disabled attribute, CSS classes)
        3. Potentially clickable (for interactive elements)
        
        Args:
            locator: Playwright locator for the element
            element_name: Name of the element for logging purposes
            
        Returns:
            bool: True if element is functionally available, False otherwise
        """
        try:
            # Check if element is visible to the user
            is_visible = locator.is_visible()
            if not is_visible:
                self.logger.debug(f"Element {element_name} is not visible")
                return False
            
            # Check various disability indicators
            aria_disabled = locator.get_attribute("aria-disabled")
            is_aria_disabled = aria_disabled == "true"
            
            disabled_attribute = locator.get_attribute("disabled")
            is_disabled_attribute = disabled_attribute is not None
            
            css_classes = locator.get_attribute("class") or ""
            has_disabled_class = any(
                disabled_word in css_classes.lower() 
                for disabled_word in ["disabled", "inactive", "unavailable"]
            )
            
            # Element is functional if it's visible and not disabled by any mechanism
            is_functional = is_visible and not (is_aria_disabled or is_disabled_attribute or has_disabled_class)
            
            # Log detailed state for debugging purposes
            self.logger.debug(f"Element {element_name} functional analysis:")
            self.logger.debug(f"  - Visible: {is_visible}")
            self.logger.debug(f"  - aria-disabled: {aria_disabled}")
            self.logger.debug(f"  - disabled attribute: {disabled_attribute}")
            self.logger.debug(f"  - CSS classes: {css_classes}")
            self.logger.debug(f"  - Final functional state: {is_functional}")
            
            return is_functional
            
        except Exception as e:
            self.logger.error(f"Error checking functional availability of {element_name}: {str(e)}")
            # If we can't determine the state, assume it's not functional to be safe
            return False
    

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