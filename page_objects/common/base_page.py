#base_page.py
import re
from typing import List, Dict as DICT
from utilities.config import DEFAULT_TIMEOUT, SCREENSHOT_DIR, PAGE_SIZE
from utilities.element_interactor import ElementInteractor
from utilities.element_locator import ElementLocator
from utilities.screenshot_manager import ScreenshotManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
from utilities.utils import logger
from datetime import datetime
from utilities.config import SCREENSHOT_DIR
import os

class BasePage:
    """Base class for all page objects"""
    def __init__(self, page):
        """
        Initialize BasePage

        Args:
            driver (WebDriver): The Selenium WebDriver instance
        """
        self.page = page
        self.logger = logger
        
    class CommonLocators:
        HEADER_LOGO = "//section//img[@alt='logo']"
        # FOOTER = # Add footer locator if needed
        LOGIN_LINK = "//section//button[text()='LOG IN']"
        LOGOUT_BUTTON = "//section//button[text()='LOG OUT']"
    
    class NavigationLocators:
        # Updated navigation locators
        VIDEOS_LINK = "//li//a[contains(@href,'/') and contains(text(), 'Videos')]"
        VIDEO_CATALOGUES_LINK = "//li//a[@href='/videoCatalogues']"
        MAP_MARKERS_LINK = "//li//a[@href='/mapMarkers']"
        SPECIES_LINK = "//a[@href='/species']"
        ADMIN_BUTTON = "//li//button[text()='Admin']"
        DEFINITIONS_BUTTON = "//li//button[text()='Definitions']"
        
        #Dropdown choices from Admin button
        INSTALLATIONS_LINK = "//a[@href='/installations']"
        DEVICES_LINK = "//a[@href='/devices']"
        USERS_LINK = "//a[@href='/users']"
        ORGANIZATIONS_LINK = "//a[@href='/organizations']"

        # Dropdown choices from Definitions button
        COUNTRIES_LINK = "//a[@href='/countries']"
        IUCNSTATUS_LINK = "//a[@href='/iucnStatus']"
        POP_TREND_LINK = "//a[@href='/populationTrend']"
        TAGS_LINK = "//a[text()='Tags']"
        
    class PaginationElements:
        PREVIOUS_PAGE = "//ul//a[@aria-label='Previous page']"
        PREVIOUS_PAGE_DISABLED = "//ul//a[@aria-label='Previous page']"
        NEXT_PAGE= "//ul//a[@aria-label='Next page']"
        CURRENT_PAGE = "//ul//a[@aria-current='page']"
        FW_BREAK_ELLIPSIS = "//ul//a[@aria-label='Jump forward']"
        BW_BREAK_ELLIPSIS = "//ul//a[@aria-label='Jump backward']"
        SHOWING_COUNT = "//span[contains(text(),'Showing')]"
        
    # Check for page title (as h1) on each page
    def verify_page_title_present(self, page_title) -> bool:
        """_summary_

        Raises:
            NoSuchElementException: _description_
            NoSuchElementException: _description_
            NoSuchElementException: _description_

        Returns:
            bool: _description_
        """
        self.logger.info(f"Checking if {page_title} Page Title is present")
        try:
            if self.locator.is_element_present(page_title):
                logger.info(f"{page_title} Page Title was located successfully")
                return True
            else:
                raise NoSuchElementException(f"{page_title} Page Title not found")
        except NoSuchElementException:
            self.screenshot.take_screenshot(self.driver, f"{page_title}_Page_Title_Not_Found")
            self.logger.error(f"Could not find {page_title} Page title on page")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while trying to locate {page_title} Page Title: {str(e)}")
            return False

    
    # Check for common Navigation elements across pages
    def verify_all_nav_elements_present(self, elements_to_check=None) -> Tuple[bool, list]:
        """_summary_

        Args:
            list (_type_): _description_
        """
        page_class = self.__class__.__name__
        self.logger.info(f"Verifying all expected navigation elements are present on page: {page_class}")
        # Define elements with reable names
        nav_elements = {
            "Header Logo": self.CommonLocators.HEADER_LOGO,
            # "Logout Button": self.CommonLocators.LOGOUT_BUTTON,
            "Videos Link": self.NavigationLocators.VIDEOS_LINK,
            "Video Catalogues Link": self.NavigationLocators.VIDEO_CATALOGUES_LINK,
            "Map Markers Link": self.NavigationLocators.MAP_MARKERS_LINK,
            "Species Link": self.NavigationLocators.SPECIES_LINK,
            "Admin Button": self.NavigationLocators.ADMIN_BUTTON,
            "Definitions Button": self.NavigationLocators.DEFINITIONS_BUTTON,
        }
        # if specific elements are passed, use those instead
        if elements_to_check:
            nav_elements = {key: value for key, value in nav_elements.items() if key in elements_to_check}
            
        all_elements_present = True
        missing_elements = []
        for element_name, element_locator in nav_elements.items():
            try:
                if self.locator.is_element_present(element_locator):
                    self.logger.info(f"Element {element_name} was located successfully")
                else:
                    raise NoSuchElementException(f"Element {element_name} not found")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{element_name}_Not_Found")
                self.logger.error(f"Could not find {element_name} on page")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        if not all_elements_present:
            self.logger.error(f"Missing elements: {', '.join(missing_elements)}")
        return all_elements_present, missing_elements
    
    def verify_all_admin_links_present(self, elements_to_check=None) -> Tuple[bool, list]:
        """_summary_

        Args:
            elements_to_check (_type_, optional): _description_. Defaults to None.

        Raises:
            NoSuchElementException: _description_

        Returns:
            Tuple[bool, list]: _description_
        """
        page_class = self.__class__.__name__
        self.logger.info(f"Verifying that all expected navigation elements are present in: Admin Dropdown on {page_class}")
        # Define elements with reable names
        admin_elements = {
            "Installations Link": self.NavigationLocators.INSTALLATIONS_LINK,
            "Devices Link": self.NavigationLocators.DEVICES_LINK,
            "Users Link": self.NavigationLocators.USERS_LINK,
            "Organizations Link": self.NavigationLocators.ORGANIZATIONS_LINK,
        }
        # if specific elements are passed, use those instead
        if elements_to_check:
            admin_elements = {key: value for key, value in admin_elements.items() if key in elements_to_check}
            
        all_elements_present = True
        missing_elements = []
        self.interactor.element_click(self.NavigationLocators.ADMIN_BUTTON)
    
        for element_name, element_locator in admin_elements.items():
            try:
                if self.locator.is_element_present(element_locator):
                    self.logger.info(f"{element_name} was located successfully.")
                else:
                    raise NoSuchElementException(f"Element {element_name} Not Found")
                # self.interactor.element_click(self.NavigationLocators.DEFINITIONS_BUTTON)
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{element_name}_Not_Found")
                self.logger.error(f"Could not find {element_name} on page.")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
    def verify_all_definition_links_present(self, elements_to_check=None) -> Tuple[bool, list]:
        """_summary_

        Args:
            elements_to_check (_type_, optional): _description_. Defaults to None.

        Raises:
            NoSuchElementException: _description_

        Returns:
            Tuple[bool, list]: _description_
        """
        page_class = self.__class__.__name__
        self.logger.info(f"Verifying that all expected navigation elements are present in: Definintions Dropdown page: {page_class}")
        # Define elements with reable names
        definition_elements = {
            "Countries Link": self.NavigationLocators.COUNTRIES_LINK,
            "IUCN Status Link": self.NavigationLocators.IUCNSTATUS_LINK,
            "Population Trend Link": self.NavigationLocators.POP_TREND_LINK,
            "Tags Link": self.NavigationLocators.TAGS_LINK,
        }
        # if specific elements are passed, use those instead
        if elements_to_check:
            definition_elements = {key: value for key, value in definition_elements.items() if key in elements_to_check}
        
        all_elements_present = True
        missing_elements = []
        self.interactor.element_click(self.NavigationLocators.DEFINITIONS_BUTTON)
    
        for element_name, element_locator in definition_elements.items():
            try:
                if self.locator.is_element_present(element_locator):
                    self.logger.info(f"{element_name} was located successfully.")
                else:
                    raise NoSuchElementException(f"Element {element_name} Not Found")
                # self.interactor.element_click(self.NavigationLocators.DEFINITIONS_BUTTON)
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{element_name}_Not_Found")
                self.logger.error(f"Could not find {element_name} on page.")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
    # Common checks for page elements
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
        all_elements_present = True
        missing_elements = []
        context_str = f" in {context}" if context else ""
        self.logger.info(f"Verifying {len(elements_dict)} elements {context_str}")
        
        for element_name, element_locator in elements_dict.items():
            try:
                if self.locator.is_element_present(element_locator):
                    self.logger.info(f"Element found: {element_name}{context_str}")
                else:
                    raise NoSuchElementException(f"Element {element_name} not found{context_str}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{context}_{element_name}_missing".replace(" ", "_"))
                self.logger.error(f"Element not found: {element_name}{context_str}")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while finding {element_name}{context_str}: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements

    # Check for pagination elements as needed with conditional checks based on record size
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
            if self.locator.is_element_present(self.PaginationElements.SHOWING_COUNT):
                showing_element = self.locator.get_element(self.PaginationElements.SHOWING_COUNT)
                showing_text = showing_element.text
                
                # Parse "Showing 1 to 25 of 171"
                match = re.search(r'Showing\s+(\d+)\s+to\s+(\d+)\s+of\s+(\d+)', showing_text)
                if match:
                    current_start = int(match.group(1))
                    current_end = int(match.group(2))
                    total_records = int(match.group(3))
                    self.logger.info(f"Showing {current_start} to {current_end} of {total_records}")
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
        
        # Define a helper function to check if an element is disbaled
        def is_element_disabled(element_locator):
            try:
                if self.locator.is_element_present(element_locator):
                    element = self.locator.get_element(element_locator)
                    return element.get_attribute("aria-disabled") == "true" or element.get_attribute("disabled") == "true"
                return False
            except Exception as e:
                self.logger.error(f"Error checking if element is disabled: {str(e)}")
                return False
            
        # Define elements with readable names
        pagination_element_locators = {
            "Previous Page": self.PaginationElements.PREVIOUS_PAGE,
            "Next Page": self.PaginationElements.NEXT_PAGE,
            "Current Page": self.PaginationElements.CURRENT_PAGE,
            "Foward Ellipsis": self.PaginationElements.FW_BREAK_ELLIPSIS,
            "Backward Ellipsis": self.PaginationElements.BW_BREAK_ELLIPSIS,
            "Showing Count": self.PaginationElements.SHOWING_COUNT
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
        
        for element_name, element_locator in pagination_element_locators.items():
            element_should_be_present = should_be_present[element_name]
            element_should_be_enabled = should_be_enabled[element_name]
            expected_presence = "present" if element_should_be_present else "absent"
            expected_state = "enabled" if element_should_be_enabled else "disabled"
        
            try:
                is_present = self.locator.is_element_present(element_locator)
                is_disabled = is_element_disabled(element_locator) if is_present else False
                is_enabled = not is_disabled
                
                # Check is presence matches expectation
                
                if is_present != element_should_be_present:
                    self.logger.error(f"Element {element_name} should be {expected_presence} but is {'present' if is_present else 'absent'}")
                    all_elements_correct = False
                    issues_found.append(element_name)
                    self.screenshot.take_screenshot(self.driver, f"{element_name}_unexpected_state")
                # If element should be present, check if enabled/disabled state matches expectation
                elif is_present and element_should_be_present:
                    if is_enabled != element_should_be_enabled:
                        self.logger.error(f"Element {element_name} should be {expected_state} but is {'enabled' if is_enabled else 'disabled'}")
                        all_elements_correct = False
                        issues_found.append(element_name)
                        self.screenshot.take_screenshot(self.driver, f"{element_name}_unexpected_state")
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
    def find_logo(self):
        """
        Check if the header logo is present on the page.

        Returns:
            bool: True if the logo is present, False otherwise.
        """
        return self.locator.is_element_present(self.CommonLocators.HEADER_LOGO)
    
    def find_login_link(self):
        """
        Check if the login link is present on the page.

        Returns:
            bool: True if the login link is present, False otherwise.
        """
        return self.locator.is_element_present(self.CommonLocators.LOGIN_LINK)
    
    def find_logout(self):
        """
        Check if the logout button is present on the page.

        Returns:
            bool: True if the logout button is present, False otherwise.
        """
        return self.locator.is_element_present(self.CommonLocators.LOGOUT_BUTTON)
    
    def logout_site(self):
        """
        Click the logout button to log out of the site.
        """
        self.interactor.element_click(self.CommonLocators.LOGOUT_BUTTON)
        
    def get_page_title(self):
        """
        Get the title of the current page.

        Returns:
            str: The title of the current page.
        """
        return self.driver.title
    
    def get_current_url(self):
        """
        Get the URL of the current page.

        Returns:
            str: The URL of the current page.
        """
        return self.driver.current_url
    
    def navigate_to(self, url: str):
        """
        Navigate to a specific URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.driver.get(url)
    
    def refresh_page(self):
        """
        Refresh the current page.
        """
        self.driver.refresh()
        
    def go_back(self):
        """
        Navigate to the previous page in the browser history.
        """
        self.driver.back()
        
    def go_forward(self):
        """
        Navigate to the next page in the browser history.
        """
        self.driver.forward()
        
    def switch_to_frame(self, frame_reference: str):
        """
        Switch to a specified frame.

        Args:
            frame_reference (str): The reference to the frame (name, id, or index).
        """
        self.driver.switch_to.frame(frame_reference)
    
    def switch_to_default_content(self):
        """
        Switch back to the default content (main frame).
        """
        self.driver.switch_to.default_content()
        
    def accept_alert(self):
        """
        Accept the currently displayed alert.
        """
        self.driver.switch_to.alert.accept()
    
    def dismiss_alert(self):
        """
        Dismiss the currently displayed alert.
        """
        self.driver.switch_to.alert.dismiss()
    
    def get_alert_text(self) -> str:
        """
        Get the text of the currently displayed alert.

        Returns:
            str: The text of the alert.
        """
        return self.driver.switch_to.alert.text
    
    # Navigation methods
    
    def find_videos_link(self):
        """
        Check if the Videos link is present on the page.

        Returns:
            bool: True if the Videos link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.VIDEOS_LINK)
    
    def go_videos_page(self):
        """
        Click the Videos link to navigate to the Videos page.
        """
        self.interactor.element_click(self.NavigationLocators.VIDEOS_LINK)
        
    def find_video_catalogues_link(self):
        """
        Check if the Video Catalogues link is present on the page.

        Returns:
            bool: True if the Video Catalogues link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.VIDEO_CATALOGUES_LINK)
    
    def go_video_catalogues_page(self):
        """
        Click the Video Catalogues link to navigate to the Video Catalogues page.
        """
        self.interactor.element_click(self.NavigationLocators.VIDEO_CATALOGUES_LINK)
        
    def find_map_markers_link(self):
        """
        Check if the Map Markers link is present on the page.

        Returns:
            bool: True if the Map Markers link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.MAP_MARKERS_LINK)
    
    def go_map_markers_page(self):
        """
        Click the Map Markers link to navigate to the Map Markers page.
        """
        self.interactor.element_click(self.NavigationLocators.MAP_MARKERS_LINK)
        
    def find_species_link(self):
        """
        Check if the Species link is present in the Definitions dropdown.

        Returns:
            bool: True if the Species link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.SPECIES_LINK)

    def go_species_page(self):
        """
        Click the Species link in the Definitions dropdown to navigate to the Species page.
        """
        self.interactor.element_click(self.NavigationLocators.SPECIES_LINK)
    
    # Handle Admin as it is a dropdown list
    
    def find_admin_button(self):
        """
        Check if the Admin button is present on the page.

        Returns:
            bool: True if the Admin button is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.ADMIN_BUTTON)
    
    def click_admin_button(self):
        """
        Click the Admin Button to open the Admin dropdown.
        """
        self.interactor.element_click(self.NavigationLocators.ADMIN_BUTTON)
        
    # Navigate the Admin dropdown elements
    
    def find_installations_link(self):
        """
        Check if the Installations link is present in the Admin dropdown.

        Returns:
            bool: True if the Installations link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.INSTALLATIONS_LINK)
    
    def go_installations_page(self):
        """
        Click the Installations link to navigate to the Installations page.
        """
        self.interactor.element_click(self.NavigationLocators.INSTALLATIONS_LINK)
        
    def find_devices_link(self):
        """
        Check if the Devices link is present in the Admin dropdown.

        Returns:
            bool: True if the Devices link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.DEVICES_LINK)
    
    def go_devices_page(self):
        """
        Click the Devices link to navigate to the Devices page.
        """
        self.interactor.element_click(self.NavigationLocators.DEVICES_LINK)
        
    def find_users_link(self):
        """
        Check if the Users link is present in the Admin dropdown.

        Returns:
            bool: True if the Users link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.USERS_LINK)
    
    def go_users_page(self):
        """
        Click the Users link to navigate to the Users page.
        """
        self.interactor.element_click(self.NavigationLocators.USERS_LINK)

    def find_organizations_link(self):
        """
        Check if the Organizations link is present in the Admin dropdown.

        Returns:
            bool: True if the Organizations link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.ORGANIZATIONS_LINK)
    
    def go_organizations_page(self):
        """
        Click the Organizations link to navigate to the Organizations page.
        """
        self.interactor.element_click(self.NavigationLocators.ORGANIZATIONS_LINK)
        
    # Handle Definitions as it is a dropdown list
    
    def find_definitions_button(self):
        """
        Check if the Definitions button is present on the page.

        Returns:
            bool: True if the Definitions button is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.DEFINITIONS_BUTTON)
        
    def click_definitions_button(self):
        """
        Click the Definitions button to open the Definitions dropdown.
        """
        self.interactor.element_click(self.NavigationLocators.DEFINITIONS_BUTTON)
        
    # Navigate the Definitions dropdown elements
        
    def find_countries_link(self):
        """
        Check if the Countries link is present in the Definitions dropdown.

        Returns:
            bool: True if the Countries link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.COUNTRIES_LINK)

    def go_countries_page(self):
        """
        Click the Countries link in the Definitions dropdown to navigate to the Countries page.
        """
        self.interactor.element_click(self.NavigationLocators.COUNTRIES_LINK)
    
    def find_iucnstatus_link(self):
        """
        Check if the IUCN Status link is present in the Definitions dropdown.

        Returns:
            bool: True if the IUCN Status link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.IUCNSTATUS_LINK)

    def go_iucnstatus_page(self):
        """
        Click the IUCN Status link in the Definitions dropdown to navigate to the IUCN Status page.
        """
        self.interactor.element_click(self.NavigationLocators.IUCNSTATUS_LINK)
    
    def find_pop_trend_link(self):
        """
        Check if the Population Trend link is present in the Definitions dropdown.

        Returns:
            bool: True if the Population Trend link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.POP_TREND_LINK)

    def go_pop_trend_page(self):
        """
        Click the Population Trend link in the Definitions dropdown to navigate to the Population Trend page.
        """
        self.interactor.element_click(self.NavigationLocators.POP_TREND_LINK)
    
    def find_tags_link(self):
        """
        Check if the Tags link is present in the Definitions dropdown.

        Returns:
            bool: True if the Tags link is present, False otherwise.
        """
        return self.locator.is_element_present(self.NavigationLocators.TAGS_LINK)

    def go_tags_page(self):
        """
        Click the Tags link in the Definitions dropdown to navigate to the Tags page.
        """
        self.interactor.element_click(self.NavigationLocators.TAGS_LINK)
        
            
    def take_screenshot(self, name):
        """Take a screenshot with a consistent naming pattern."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        browser_name = self.page.browser.browser_type.name
        filename = f"{browser_name}_{name}_{timestamp}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        self.page.screenshot(path=path)
        self.logger.info(f"Screenshot saved: {filename}")
        return filename