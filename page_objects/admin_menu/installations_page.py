# installations_page.py
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
        INSTALLATION_NAME_HEADER = "//table//th[text()='Name']"
        INSTALLATION_START_LATLONG = "//table//th[text()='Global Start LatLong ']"
        INSTALLATION_STARTUP_VIDEO = "//table//th[text()='Startup Video']"
        INSTALLATION_VIDEO_CATALOGUE = "//table//th[text()='Video Catalogue']"
        INSTALLATION_ORGANIZATION_HEADER = "//table//th[text()='Organization']"
        
    # Check Page Element presence
    def verify_page_title_present(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return super().verify_page_title_present(self.InstallationPageElements.INSTALLATIONS_PAGE_TITLE)
    
    def verify_all_installations_search_elements_present(self) -> Tuple[bool,list]:
        """_summary_

        Returns:
            Tuple[bool,list]: _description_
        """
        self.logger.info("Verifying that all expected installation search elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        search_elements = {
            "Search Text Box": self.InstallationSearchElements.SEARCH_TEXT,
            "Search Button": self.InstallationSearchElements.SEARCH_BUTTON,
            "Add Installation Button": self.InstallationSearchElements.ADD_INSTALLATION_LINK,
        }
        for element_name, element_locator in search_elements.items():
            try:
                if self.locator.is_element_present(element_locator):
                    self.logger.info(f"Element found: {element_name}")
                else:
                    raise NoSuchElementException(f"Search Element not found on Installations page: {element_name}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Search element - {element_name}_Not_Found")
                self.logger.error(f"Search element not found: {element_name} on Installations page")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to find search element: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
    def verify_all_installation_table_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
            Tuple[bool, list]: _description_
        """
        self.logger.info("Check if all Installation Table elements are present")
        all_elements_present = True
        missing_elements = []
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
        for element_name, table_element in table_elements.items():
            try:
                if self.locator.is_element_present(table_element):
                    self.logger.info(f"Table element found: {element_name} on Installations page")
                else:
                    raise NoSuchElementException(f"Table Element not found: {element_name} on Installations page")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"installation_table_elements_not_found: {element_name}")
                self.logger.error(f"Table Element not found: {element_name}")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to find table element: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements