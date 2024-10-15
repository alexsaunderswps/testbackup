# videos_page.py
import os
from dotenv import load_dotenv
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
        self.screenshot = ScreenshotManager(driver)
        self.logger = logger
        
    class CountryTableElements:
        """_summary_

        Args:
            object (_type_): _description_
        """
        COUNTRIES_PAGE_TITLE = "//h1[contains(text(),'Countries')]"
        COUNTRIES_TABLE_SEARCH = "//input[@placeholder='Search...']"
        COUNTRIES_TABLE_BODY = "//table//tbody"
        COUNTRIES_TABLE_ROWS = "//table//tbody/tr"
        # COUNTRIES_TABLE_COLUMNS = 
        # COUNTRIES_TABLE_HEADER = 
        # COUNTRIES_TABLE_FOOTER = 
        
