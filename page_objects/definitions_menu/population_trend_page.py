# population_trend_page.py
import os
from dotenv import load_dotenv
from typing import Tuple, List
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
    def verify_population_trend_table_elements_present(self) -> Tuple[bool, List[str]]:
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
            "Population Trend Table Body": self.PopulationTrendTableElements.POPULATION_TREND_TABLE_BODY,   
            "Population Trend Table Rows": self.PopulationTrendTableElements.POPULATION_TREND_TABLE_ROWS
        }
        return self.verify_page_elements_present(table_elements, "Population Trend Table Elements")