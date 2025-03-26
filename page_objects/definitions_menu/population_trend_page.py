# population_trend_page.py
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

class PopulationTrendPage(BasePage):
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
        
    class PopulationTrendPageElements:
        """_summary_
        """
        POPULATION_TREND_PAGE_TITLE = "//h1[contains(text(),'Population Trend')]"
    
    class PopulationTrendTableElements:
        """_summary_
        """
        POPULATION_TREND_TABLE_BODY = "//table//tbody"
        POPULATION_TREND_TABLE_ROWS = "//table//tbody/tr"
        
    # Check Population Trend Page Title presence
    def verify_population_trend_page_title_present(self):
        """_summary_
        """
        return super().verify_page_title_present(self.PopulationTrendPageElements.POPULATION_TREND_PAGE_TITLE)
    
    # Check Population Trend Table presence
    def verify_population_trend_table_elements_present(self):
        """_summary_
        """
        self.logger.info("Checking Population Trend Table Elements")
        all_elements_present = True
        missing_elements = []
        #Define elements with readable names
        table_elements = {
            "Population Trend Table Body": self.PopulationTrendTableElements.POPULATION_TREND_TABLE_BODY,   
            "Population Trend Table Rows": self.PopulationTrendTableElements.POPULATION_TREND_TABLE_ROWS
        }
        for element_name, table_locator in table_elements.items():
            try:
                if self.locator.is_element_present(table_locator):
                    self.logger.info(f"Population Trends table {element_name} is present")
                else:
                    raise NoSuchElementException(f"Population Trends table {element_name} is missing")
            except NoSuchElementException:
                self.screenshot.take_screenshot(f"population_trend_table_{element_name}_missing")
                self.logger.error(f"Could not find {element_name} in Population Trends table")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"An error occurred while checking {element_name} in Population Trends table")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements