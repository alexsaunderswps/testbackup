# species_page.py
import os
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
        SPECIES_NAME_HEADER = "//table/thead/tr/th[text()='Name']"
        SPECIES_COLLOQUIAL_HEADER = "//table/thead/tr/th[text()='Colloquial Name']"
        SPECIES_SCIENTIFIC_HEADER = "//table/thead/tr/th/div[text()='Scientific Name']"
        SPECIES_DESCRIPTION_HEADER = "//table/thead/tr/th/div[text()='Description']"
        SPECIES_IUCN_HEADER = "//table/thead/tr/th[text()='IUCN Status']"
        SPECIES_POPULATION_HEADER = "//table/thead/tr/th[text()='Population Trend']"
        SPECIES_CATEGORY_HEADER = "//table/thead/tr/th[text()='Species Category']"
            
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
    
    def verify_all_species_table_elements_present(self) -> Tuple[bool,list]:
        """_summary_

        Returns:
            Tuple[bool,list]: _description_
        """
        self.logger.info("Check if all Species Table elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        table_elements = {
            "Table Body": self.SpeciesTableElements.SPECIES_TABLE_BODY,
            "Table Rows": self.SpeciesTableElements.SPECIES_TABLE_ROWS,
            "Species Name": self.SpeciesTableElements.SPECIES_NAME_HEADER,
            "Colloquial Name": self.SpeciesTableElements.SPECIES_COLLOQUIAL_HEADER,
            "Scientific Name": self.SpeciesTableElements.SPECIES_SCIENTIFIC_HEADER,
            "Description": self.SpeciesTableElements.SPECIES_DESCRIPTION_HEADER,
            "IUCN Status": self.SpeciesTableElements.SPECIES_IUCN_HEADER,
            "Population Trend": self.SpeciesTableElements.SPECIES_POPULATION_HEADER,
            "Species Category": self.SpeciesTableElements.SPECIES_CATEGORY_HEADER,
        }
        for element_name, table_element in table_elements.items():
            try:
                if self.locator.is_element_present(table_element):
                    self.logger.info(f"Table element found: {element_name}")
                else:
                    raise NoSuchElementException(f"Table element not found: {element_name}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"species_table_elements_missing: {element_name}")
                self.logger.error(f"Element not found: {element_name}")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate element: {str(e)}")
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