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
        USERS_PAGE_TITLE = "//hi[text()='Users']"
        
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
        