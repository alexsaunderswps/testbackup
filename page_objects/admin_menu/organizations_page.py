# organizations_page.py
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

class OrganizationsPage(BasePage):
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
        
    class OrganizationsPageElements:
        """_summary_
        """
        ORGANIZATIONS_PAGE_TITLE = "//h1[text()='Organizations']"
        
    class OrganizationsSearchElements:
        """_summary_
        """
        SEARCH_TEXT = "//input[@placeholder='Filter by name']"
        SEARCH_BUTTON = "//button[text()='Search']"
        ADD_ORGANIZATION_LINK ="//a[@href='/organization/add']"
        
    class OrganizationsTableElements:
        """_summary_
        """
        ORGANIZATION_TABLE_BODY = "//table//tbody"
        ORGANIZATION_TABLE_ROWS = "//table//tbody/tr"
        ORGANIZATION_NAME_HEADER = "//table/thead/tr/th[text()='Name ']"
        
    # Check Page Element presence
    def verify_page_title_present(self):
        """_summary_
        """
        return super().verify_page_title_present(self.OrganizationsPageElements.ORGANIZATIONS_PAGE_TITLE)
    
    def verify_all_organization_search_elements_present(self) -> Tuple[bool, list]:
        """
        Verify that all expected organization search elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying all expected organization search elements are present")
        
        # Define elements with readable names
        search_elements = {
            "Search Text Box": self.OrganizationsSearchElements.SEARCH_TEXT,
            "Search Button": self.OrganizationsSearchElements.SEARCH_BUTTON,
            "Add Organization Link": self.OrganizationsSearchElements.ADD_ORGANIZATION_LINK
        }
        return self.verify_page_elements_present(search_elements, "Organizations Search Elements")
        
    def verify_all_organization_table_elements_present(self) -> Tuple[bool, list]:
        """
        Verify that all expected organization table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying all expected Ogranization table elements are present")

        # Define elements with readable names
        table_elements = {
            "Table Body": self.OrganizationsTableElements.ORGANIZATION_TABLE_BODY,
            "Table Rows": self.OrganizationsTableElements.ORGANIZATION_TABLE_ROWS,
            "Organization Name Header": self.OrganizationsTableElements.ORGANIZATION_NAME_HEADER,
        }
        return self.verify_page_elements_present(table_elements, "Organization Table Elements")