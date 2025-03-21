# species_page.py
import os
import re
from dotenv import load_dotenv
from typing import Tuple
from page_objects.common.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT, PAGE_SIZE
from utilities.utils import logger
from utilities.element_interactor import ElementInteractor
from utilities.element_locator import ElementLocator
from utilities.screenshot_manager import ScreenshotManager

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class SpeciesPage(BasePage):
    """_summary_

    Args:
        BasePage (_type_): _description_
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.locator = ElementLocator(driver)
        self.interactor = ElementInteractor(driver)
        self.screenshot = ScreenshotManager()
        self.logger = logger
        
    class SpeciesPageElements:
        """_summary_
        """
        SPECIES_PAGE_TITLE = "//h1[text()='Species']"
        
    class SpeciesSearchElements:
        """_summary_
        """
        SEARCH_TEXT = '//input[@placeholder="Filter by name"]'
        SEARCH_BUTTON = "//button[text()='Search']"
        ADD_SPECIES_LINK = "//a[@href='/species/add']"

    class SpeciesTableElements:
        """_summary_
        """
        SPECIES_TABLE_BODY = "//table//tbody"
        SPECIES_TABLE_ROWS = "//table//tbody/tr"
        SPECIES_NAME_HEADER = "//table//th[text()='Name']"
        SPECIES_COLLOQUIAL_HEADER = "//table//th[text()='Colloquial Name']"
        SPECIES_SCIENTIFIC_HEADER = "//table//div[text()='Scientific Name']"
        SPECIES_DESCRIPTION_HEADER = "//table//div[text()='Description']"
        SPECIES_IUCN_HEADER = "//table//th[text()='IUCN Status']"
        SPECIES_POPULATION_HEADER = "//table//th[text()='Population Trend']"
        SPECIES_CATEGORY_HEADER = "//table//th[text()='Species Category']"
        
    class PaginationElements:
        PREVIOUS_PAGE = "//ul//a[@aria-label='Previous page']"
        PREVIOUS_PAGE_DISABLED = "//ul//a[@aria-label='Previous page']"
        NEXT_PAGE= "//ul//a[@aria-label='Next page']"
        CURRENT_PAGE = "//ul//a[@aria-current='page']"
        FW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump forward']"
        BW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump backward']"
        SHOWING_COUNT = "//span[contains(text(),'Showing')]"
            
    # Check Page Element presence
    def verify_page_title_present(self):
        return super().verify_page_title_present(self.SpeciesPageElements.SPECIES_PAGE_TITLE)
    
    def verify_all_species_search_elements_present(self) -> Tuple[bool, list]:
        """_summary_
        
        Returns:
            _type_: _description_
        """
        self.logger.info("Verifying that all expected species search elements are present in: Species Page")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        search_elements = {
            "Search Text Box": self.SpeciesSearchElements.SEARCH_TEXT,
            "Search Button": self.SpeciesSearchElements.SEARCH_BUTTON,
            "Add Species Button": self.SpeciesSearchElements.ADD_SPECIES_LINK,
        }
        for element_name, search_element in search_elements.items():
            try:
                if self.locator.is_element_present(search_element):
                    self.logger.info(f"Element found: {element_name}")
                else:
                    raise NoSuchElementException(f"Element not found: {element_name}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"species_search_elements_missing: {element_name}")
                self.logger.error(f"Element not found: {element_name}")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate element: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
    def verify_all_species_table_elements_present(self) -> bool:
        """_summary_
        
        Returns:
            _type_: _description_
        """
        self.logger.info("Checking if all Species Table elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        table_elements = {
            "Name Header": self.SpeciesTableElements.SPECIES_NAME_HEADER,
            "Colloquial Header": self.SpeciesTableElements.SPECIES_COLLOQUIAL_HEADER,
            "Scientific Header": self.SpeciesTableElements.SPECIES_SCIENTIFIC_HEADER,
            "Description Header": self.SpeciesTableElements.SPECIES_DESCRIPTION_HEADER,
            "IUCN Header": self.SpeciesTableElements.SPECIES_IUCN_HEADER,
            "Population Header": self.SpeciesTableElements.SPECIES_POPULATION_HEADER,
            "Catagory Header": self.SpeciesTableElements.SPECIES_CATEGORY_HEADER
        }
        for element_name, table_element in table_elements.items():
            try:
                if self.locator.is_element_present(table_element):
                    self.logger.info(f"Element found: {element_name}")
                else:
                    raise NoSuchElementException(f"Element not found: {element_name}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"species_table_elements_missing_{element_name}")
                self.logger.error(f"Element not found: {element_name} in species table")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate element: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
    def verify_pagination_elements_present(self) -> Tuple[bool, list]:
        """
        Verifies pagination elements based on page size and current record count.
    
        Returns:
            Tuple[bool, list]: A tuple containing a boolean (all expected elements present)
                        and a list of missing expected elements
        """
        self.logger.info("Checking if the correct Pagination elements are present on Species Page")
        all_elements_present = True
        missing_elements = []
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

        # Define elements with readable names
        pagination_element_locators = {
            "Previous Page": self.PaginationElements.PREVIOUS_PAGE,
            "Next Page": self.PaginationElements.NEXT_PAGE,
            "Current Page": self.PaginationElements.CURRENT_PAGE,
            "Foward Elipsis": self.PaginationElements.FW_BREAK_ELIPSIS,
            "Backward Elipsis": self.PaginationElements.BW_BREAK_ELIPSIS,
            "Showing Count": self.PaginationElements.SHOWING_COUNT
        }
        
        # Define expected state of each element
        should_be_present = {
            "Previous Page": True,
            "Next Page": has_multiple_pages and not is_last_page,
            "Current Page": True,
            "Foward Elipsis": total_records > (page_size * 2), # Need at least 3 pages for ellipsis
            "Backward Elipsis": current_start > (page_size * 2), # Need to be at least on page 3
            "Showing Count": True
        }
        
        for element_name, element_locator in pagination_element_locators.items():
            element_should_be_present = should_be_present[element_name]
            expected_state = "present" if element_should_be_present else "absent"
        
            try:
                is_present = self.locator.is_element_present(element_locator)
                if is_present == element_should_be_present:
                    self.logger.info(f"Element {element_name} correctly {expected_state}")
                else:
                    self.logger.error(f"Element {element_name} should be {expected_state} but is {'present' if is_present else 'absent'}")
                    all_elements_present = False
                    missing_elements.append(element_name)
                    self.screenshot.take_screenshot(self.driver, f"{element_name}_unexpected_state")
            except Exception as e:
                self.logger.error(f"Error checking pagination element {element_name}: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
    def get_page_locator(page_number):
        return f"//ul//a[@aria-label='Page {page_number}']"
            
    def check_current_page(page_number):
        return f"//ul//a[@aria-label='Page {page_number} is your current page']"
    
    def move_next_page_arrow(self):
        self.interactor.element_click(self.PaginationElements.NEXT_PAGE)
    
    def move_prev_page_arrow(self):
        self.interactor.element_click(self.PaginationElements.PREVIOUS_PAGE)
        
    def move_next_page_jump(self):
        self.interactor.element_click(self.PaginationElements.FW_BREAK_ELIPSIS)
    
    def move_prev_page_jump(self):
        self.interactor.element_click(self.PaginationElements.BW_BREAK_ELIPSIS)