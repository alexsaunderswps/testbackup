# organizations_page.py
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
        ORGANIZATION_NAME_HEADER = "//table//th[text()='Name ']"
        
    # Check Page Element presence
    def verify_page_title_present(self):
        """_summary_
        """
        return super().verify_page_title_present(self.OrganizationsPageElements.ORGANIZATIONS_PAGE_TITLE)
    
    def verify_all_organization_search_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
            Tuple[bool, list]: _description_
        """
        self.logger.info("Verifying all expected organization search elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        search_elements = {
            "Search Text Box": self.OrganizationsSearchElements.SEARCH_TEXT,
            "Search Button": self.OrganizationsSearchElements.SEARCH_BUTTON,
            "Add Organization Link": self.OrganizationsSearchElements.ADD_ORGANIZATION_LINK
        }
        for element_name, element_locator in search_elements.items():
            try:
                if self.locator.is_element_present(element_locator):
                    self.logger.info(f"Search element found: {element_name}")
                else:
                    raise NoSuchElementException(f"Search element - {element_name} not found on Organizations page")
            except NoSuchElementException:    
                self.screenshot.take_screenshot(self.driver, f"Search element - {element_name} not found on Organizations page")
                self.logger.error(f"Search element - {element_name} not found on Organizations page")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexceptect error attempting to find search element - {element_name} on Organizations page: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
            return all_elements_present, missing_elements
        
    def verify_all_organization_table_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
            Tuple[bool, list]: _description_
        """
        self.logger.info("Verifying all expected Ogranization table elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        table_elements = {
            "Table Body": self.OrganizationsTableElements.ORGANIZATION_TABLE_BODY,
            "Table Rows": self.OrganizationsTableElements.ORGANIZATION_TABLE_ROWS,
            "Organization Name Header": self.OrganizationsTableElements.ORGANIZATION_NAME_HEADER,
        }
        for element_name, table_element in table_elements.items():
            try:
                if self.locator.is_element_present(table_element):
                    self.logger.info(f"Table element found: {element_name} on Organizations page")
                else:
                    raise NoSuchElementException(f"Table element - {element_name} not found on Organizations page")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Table element - {element_name} not found on Organizations page")
                self.logger.error(f"Table element - {element_name} not found on Organizations page")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to find table element: {str(e)} on Organizations page")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements