# users_page.py
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
    
    def verify_add_user_link_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected user add elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected Users search elements are present")

        # Define elements with readable names
        action_elements = {
            "Add Installation Button": self.UsersActionElements.ADD_USER_LINK,
        }
        return self.verify_page_elements_present(action_elements, "Users Add Button")
    
    def verify_all_users_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected user table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying all expected Users table elements are present")
        # Define elements with readable names
        table_elements = {
            "Table Body": self.UsersTableElements.USERS_TABLE_BODY,
            "Table Rows": self.UsersTableElements.USERS_TABLE_ROWS,
            "Name Header": self.UsersTableElements.USERS_NAME_HEADER,
            "Username Header": self.UsersTableElements.USERS_USERNAME_HEADER,
            "Roles Header": self.UsersTableElements.USERS_ROLES_HEADER
        }
        return self.verify_page_elements_present(table_elements, "Users Table Elements")