# users_page.py
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

class UsersPage(BasePage):
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
        
    class UsersPageElements:
        """_summary_
        """
        USERS_PAGE_TITLE = "//h1[text()='Users']"
        
    class UsersActionElements:
        """_summary_
        """
        ADD_USER_LINK = "//a[@href='/user/add']"
        
    class UsersTableElements:
        """_summary_
        """
        USERS_TABLE_BODY = "//table//tbody"
        USERS_TABLE_ROWS = "//table//tbody/tr"
        USERS_NAME_HEADER = "//table/thead/tr/th[text()='Name']"
        USERS_USERNAME_HEADER = "//table/thead/tr/th[text()='Username']"
        USERS_ROLES_HEADER = "//table/thead/tr/th[text()='Roles']"
        
    # Check Page Element presence
    def verify_page_title_present(self):
        """_summary_
        """
        return super().verify_page_title_present(self.UsersPageElements.USERS_PAGE_TITLE)
    
    def verify_add_user_link_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
        Tuple[bool,list]: _description_
        """
        self.logger.info("Verifying that all expected Users search elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        action_elements = {
            "Add Installation Button": self.UsersActionElements.ADD_USER_LINK,
        }
        for element_name, element_locator in action_elements.items():
            try:
                if self.locator.is_element_present(element_locator):
                    self.logger.info(f"Search element found: {element_name}")
                else:
                    raise NoSuchElementException(f"Search Element not found on Users page: {element_name}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Action element - {element_name}_Not_Found")
                self.logger.error(f"Action element not found: {element_name} on Users page")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to find action element: {str(e)} on Users page")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
    def verify_all_users_table_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
            Tuple[bool, list]: _description_
        """
        self.logger.info("Verifying all expected Users table elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        table_elements = {
            "Table Body": self.UsersTableElements.USERS_TABLE_BODY,
            "Table Rows": self.UsersTableElements.USERS_TABLE_ROWS,
            "Name Header": self.UsersTableElements.USERS_NAME_HEADER,
            "Username Header": self.UsersTableElements.USERS_USERNAME_HEADER,
            "Roles Header": self.UsersTableElements.USERS_ROLES_HEADER
        }
        for element_name, element_locator in table_elements.items():
            try:
                if self.locator.is_element_present(element_locator):
                    self.logger.info(f"Table element found: {element_name}")
                else:
                    raise NoSuchElementException(f"Table Element not found on Users page: {element_name}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Table element - {element_name}_Not_Found")
                self.logger.error(f"Table element not found: {element_name} on Users page")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to find table element: {str(e)} on Users page")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements