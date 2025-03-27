# installations_page.py
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

class InstallationsPage(BasePage):
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
        
    class InstallationPageElements:
        """_summary_
        """
        INSTALLATIONS_PAGE_TITLE = "//h1[text()='Installations']"
        
    class InstallationSearchElements:
        """_summary_
        """
        SEARCH_TEXT = "//input[@placeholder='Filter by name']"
        SEARCH_BUTTON = "//button[text()='Search']"
        ADD_INSTALLATION_LINK = "//a[@href='/installation/add']"
        
    class InstallationTableElements:
        """_summary_
        """
        INSTALLATION_TABLE_BODY = "//table//tbody"
        INSTALLATION_TABLE_ROWS = "//table//tbody/tr"
        INSTALLATION_NAME_HEADER = "//table/thead/tr/th[text()='Name']"
        INSTALLATION_START_LATLONG = "//table/thead/tr/th[text()='Global Start LatLong ']"
        INSTALLATION_STARTUP_VIDEO = "//table/thead/tr/th[text()='Startup Video']"
        INSTALLATION_VIDEO_CATALOGUE = "//table/thead/tr/th[text()='Video Catalogue']"
        INSTALLATION_ORGANIZATION_HEADER = "//table/thead/tr/th[text()='Organization']"
        
    # Check Page Element presence
    def verify_page_title_present(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return super().verify_page_title_present(self.InstallationPageElements.INSTALLATIONS_PAGE_TITLE)
    
    def verify_all_installations_search_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected installation search elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected installation search elements are present")
        
        # Define elements with readable names
        search_elements = {
            "Search Text Box": self.InstallationSearchElements.SEARCH_TEXT,
            "Search Button": self.InstallationSearchElements.SEARCH_BUTTON,
            "Add Installation Button": self.InstallationSearchElements.ADD_INSTALLATION_LINK,
        }
        return self.verify_page_elements_present(search_elements, "Installation Search Elements")
    
    def verify_all_installation_table_elements_present(self) -> Tuple[bool, list]:
        """
        Verify that all expected installation table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Check if all Installation Table elements are present")
    
        # Define elements with readable names
        table_elements = {
            "Table Body": self.InstallationTableElements.INSTALLATION_TABLE_BODY,
            "Table Rows": self.InstallationTableElements.INSTALLATION_TABLE_ROWS,
            "Installation Name": self.InstallationTableElements.INSTALLATION_NAME_HEADER,
            "Global Start LatLong": self.InstallationTableElements.INSTALLATION_START_LATLONG,
            "Startup Video": self.InstallationTableElements.INSTALLATION_STARTUP_VIDEO,
            "Video Catalogue": self.InstallationTableElements.INSTALLATION_VIDEO_CATALOGUE,
            "Installation Organization": self.InstallationTableElements.INSTALLATION_ORGANIZATION_HEADER,
        }
        return self.verify_page_elements_present(table_elements, "Installation Table Elements")