# login_page.py

import os
import time
from dotenv import load_dotenv
from utilities.utils import logger
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.config import DEFAULT_TIMEOUT, SCREENSHOT_DIR
from utilities.element_interactor import ElementInteractor
from utilities.element_locator import ElementLocator
from utilities.screenshot_manager import ScreenshotManager

class LoginPage:
    """_summary_
    """
    
    def __init__(self, driver):
        """_summary_

        Args:
            driver (_type_): _description_
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.locator = ElementLocator(driver)
        self.interactor = ElementInteractor(driver)
        self.screenshot = ScreenshotManager()
        
    # Element Locators
    _login_link = "//section//button[text()='LOG IN']"
    _username_input = "//div//input[@name='Email']"
    _password_input = "//div//input[@name='Password']"
    _login_button = "//div//button[@id='SubmitButton']"
    _error_blank_input = "//div//div[contains(@class, 'alert-danger') and contains(text(), 'Password field is required') and contains(text(), 'UserName field is required')]"
    _error_no_pass = "//div//div[contains(@class, 'alert-danger') and contains(text(), 'Password field is required')]"
    _error_no_user =  "//div//div[contains(@class, 'alert-danger') and contains(text(), 'UserName field is required')]"
    _invalid_creds = "//div//div[contains(@class, 'alert-danger') and contains(text(),'Failed')]"
    _pass_too_short = "//div//div[contains(@class, 'alert-danger') and contains(text(), 'Password must be a string or array type with a minimum length of '4')]"
    _user_too_short = "//div//div[contains(@class, 'alert-danger') and contains(text(), 'UserName must be a string or array type with a minimum length of '4')]"
    
    def click_login_link(self):
        """_summary_
        """
        logger.info('Clicking login link')
        self.interactor.element_click(self._login_link)
        
    def enter_username(self, user):
        """_summary_

        Args:
            user (_type_): _description_
        """
        logger.info("Entering user: {user}")
        self.interactor.clear_element_input(self._username_input)
        self.interactor.element_send_input(user, self._username_input)
    
    def enter_password(self, password):
        """_summary_

        Args:
            password (_type_): _description_
        """
        logger.info("Entering password")
        self.interactor.clear_element_input(self._password_input)
        self.interactor.element_send_input(password, self._password_input)
    
    