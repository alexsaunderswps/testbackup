# countries_page.py
import os
from dotenv import load_dotenv
from typing import Tuple
from page_objects.common.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT
from utilities.utils import logger
from utilities.element_interactor import ElementInteractor
from utilities.element_locator import ElementLocator
from utilities.screenshot_manager import ScreenshotManager

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class CountriesPage(BasePage):
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
        
    class CountryPageElements:
        """_summary_

        Args:
            object (_type_): _description_
        """
        COUNTRIES_PAGE_TITLE = "//h1[contains(text(),'Countries')]"
        
    class CountryTableElemenets:
        COUNTRIES_TABLE_SEARCH = "//input[@placeholder='Search...']"
        COUNTRIES_TABLE_BODY = "//table//tbody"
        COUNTRIES_TABLE_ROWS = "//table//tbody/tr"
        # COUNTRIES_TABLE_COLUMNS = 
        # COUNTRIES_TABLE_HEADER = 
        # COUNTRIES_TABLE_FOOTER = 
        
    # Check Countries Title presence
    def verify_countries_page_title_present(self) -> bool:
        """_summary_

        Returns:
            _type_: _description_
        """
        return super().verify_page_title_present(self.CountryPageElements.COUNTRIES_PAGE_TITLE)
    
    # Check Countries Table contents
    
    def verify_all_countries_table_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
            Tuple[bool, list]: _description_
        """
        self.logger.info("Verifying all elements on the Countries Table")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        table_elements = {
        "Table Search": self.CountryTableElemenets.COUNTRIES_TABLE_SEARCH,
        "Table Body": self.CountryTableElemenets.COUNTRIES_TABLE_BODY,
        "Table Rows": self.CountryTableElemenets.COUNTRIES_TABLE_ROWS
        }
        for element_name, table_locator in table_elements.items():
            try:
                if self.locator.is_element_present(table_locator):
                    self.logger.info(f"{element_name} found in Countries Table")
                else:
                    raise NoSuchElementException(f"Unable to find {element_name} in Countries Table")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"countries_table_{element_name}_missing")
                self.logger.error(f"Could not find {element_name} in Countries Table")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"An error occurred while checking {element_name} in Countries Table: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
            
    def count_table_rows(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        self.logger.info("Counting the number of rows in the Countries Table")
        num_rows = 0
        try:
            table = self.locator.check_elements_present(self.CountryTableElemenets.COUNTRIES_TABLE_BODY)
            if table:
                table_rows = self.locator.get_elements(self.CountryTableElemenets.COUNTRIES_TABLE_ROWS)
                num_rows = len(table_rows)
                logger.info(f"Found {num_rows} rows in the Countries Table")
                return num_rows
            else:
                self.screenshot.take_screenshot(self.driver, "Countries_Table_Body_Not_Found")
                logger.error(f"Unable to find the country table on this page.")
        except Exception as e:
            self.logger.error(f"An error occurred while trying to count the number of rows in the Countries Table: {str(e)}")
            
    def get_country_name_values(self) -> list[str]:
        """_summary_

        Returns:
            list[str]: _description_
        """
        self.logger.info("Getting the names of all countries in the table on current page")
        country_names = []
        try:
            table = self.locator.check_elements_present(self.CountryTableElemenets.COUNTRIES_TABLE_BODY)
            if table:
                table_rows = self.locator.get_elements(self.CountryTableElemenets.COUNTRIES_TABLE_ROWS)
                for index, row in enumerate(table_rows, start=1):
                    text_container = self.locator.get_element(f"{self.CountryTableElemenets.COUNTRIES_TABLE_ROWS}[{index}]/td[1]")
                    country = text_container.text
                    country_names.append(country)
                    logger.debug(f"Here is the row: {country}")
                    logger.debug(f"Here is the list: {country_names}")
                return country_names
            else:
                logger.error(f"Unable to find the country table on this page with locator {table}.")
        except Exception as e:
            logger.error(f"An error occurred while trying to get the names of countries in the table: {str(e)}")
            
# TODO - check table elements if needed
# TODO - with table names can check sort order
# TODO - check search functionality