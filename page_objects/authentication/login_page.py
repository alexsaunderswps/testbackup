# login_page.py
import os
import time
from page_objects.common.base_page import BasePage
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.config import DEFAULT_TIMEOUT, SCREENSHOT_DIR
from utilities.utils import logger
from utilities.element_interactor import ElementInteractor
from utilities.element_locator import ElementLocator
from utilities.screenshot_manager import ScreenshotManager

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class LoginPage(BasePage):
    """_summary_
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.locator = ElementLocator(driver)
        self.interactor = ElementInteractor(driver)
        self.screenshot = ScreenshotManager()
        self.logger = logger
        
    class ElementLocators:
        LOGIN_LINK = "//section//button[text()='LOG IN']"
        USERNAME_INPUT = "//div//input[@name='Email']"
        PASSWORD_INPUT = "//div//input[@name='Password']"
        LOGIN_BUTTON = "//div//button[@id='SubmitButton']"
        LOGOUT_BUTTON = "//section//button[text()='LOG OUT']"
    
    class ErrorMessages:
        BASE_XPATH = "//div[contains(@class, 'alert-danger) and"
        ERROR_BLANK_INPUT = "//div[contains(@class, 'alert-danger') and contains(text(),'UserName') and contains(text(),'Password')]"
        ERROR_NO_PASS = "//div[contains(@class, 'alert-danger') and contains(text(),'Password')]"
        ERROR_NO_USER =  "//div[contains(@class, 'alert-danger') and contains(text(),'UserName')]"
        ERROR_INVALID = "//div[contains(@class, 'alert-danger') and contains(text(),'Failed')]"
        ERROR_PASS_TOO_SHORT = "//div[contains(@class,'alert-danger') and contains(text(),'Password') and contains(text(),'4')]"
        ERROR_USER_TOO_SHORT = "//div[contains(@class, 'alert-danger') and contains(text(),'UserName') and contains(text(),'4')]"

    
    def click_login_link(self):
        """_summary_
        """
        self.logger.info('Clicking login link')
        self.interactor.element_click(self.ElementLocators.LOGIN_LINK)
        
    def enter_username(self, user):
        """_summary_

        Args:
            user (_type_): _description_
        """
        self.logger.info("Entering user.")
        self.interactor.clear_element_input(self.ElementLocators.USERNAME_INPUT)
        self.interactor.element_send_input(user, self.ElementLocators.USERNAME_INPUT)
    
    def enter_password(self, password):
        """_summary_

        Args:
            password (_type_): _description_
        """
        self.logger.info("Entering password")
        self.interactor.clear_element_input(self.ElementLocators.PASSWORD_INPUT)
        self.interactor.element_send_input(password, self.ElementLocators.PASSWORD_INPUT)
        
    def click_login_button(self):
        """_summary_
        """
        self.logger.info("Clicking the Log In button")
        self.interactor.element_click(self.ElementLocators.LOGIN_BUTTON)
        
    def verify_all_elements_present(self) -> bool:
        """_summary_

        Returns:
            _type_: _description_
        """
        self.logger.info("Verifying that all expected elements are present")
        try:
            for page_element in [self.CommonLocators.HEADER_LOGO,
                            self.CommonLocators.LOGIN_LINK,
                            self.ElementLocators.PASSWORD_INPUT,
                            self.ElementLocators.USERNAME_INPUT,
                            self.ElementLocators.LOGIN_BUTTON
                            ]:
                self.locator.check_elements_present(page_element)
                self.logger.info(f"{page_element} was located successfully.")
            return True
        except NoSuchElementException:
            self.logger.error(f"Could not find {page_element} on page.")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while finding elements: {str(e)}")
            return False
        

    def verify_both_missing(self) -> bool:
        
        try:
            self.locator.is_element_present(self.ErrorMessages.ERROR_BLANK_INPUT)
            self.screenshot.take_screenshot(self.driver, "No_Creds")
            self.logger.info(f"Login was not successful, Missing credentials")
            return True
        except Exception as e:
            self.screenshot.take_screenshot(self.driver, "Error_No_Creds")
            self.logger.error(f"There was an Error with No Creds check: {str(e)}")
            return False

    def verify_user_missing(self) -> bool:
        """_summary_
        """
        try:
            self.locator.is_element_present(self.ErrorMessages.ERROR_NO_USER)
            self.screenshot.take_screenshot(self.driver, "Missing_User")
            self.logger.info(f"Login was not successful, Missing Username")
            return True
        except Exception as e:
            self.screenshot.take_screenshot(self.driver, "Error_Missing_User")
            self.logger.error(f"There was an Error with the User Missing check: {str(e)}")
            return False
            
    def verify_password_missing(self) -> bool:
        """_summary_
        """
        try:
            self.locator.is_element_present(self.ErrorMessages.ERROR_NO_PASS)
            self.screenshot.take_screenshot(self.driver, "Missing_Pass")
            self.logger.info(f"Login was not successful, Missing Password")
            return True
        except Exception as e:
            self.screenshot.take_screenshot("Error_Missing_Password")
            self.logger.error(f"There was an Error with the Password Missing check: {str(e)}")
            return False
            
    def verify_user_short(self) -> bool:
        """_summary_
        """
        try:
            self.locator.is_element_present(self.ErrorMessages.ERROR_USER_TOO_SHORT)
            self.screenshot.take_screenshot(self.driver, "Short_User")
            self.logger.info(f"Login was not successful, Username too short")
            return True
        except Exception as e:
            self.screenshot.take_screenshot(self.driver, "Error_User_Short")
            self.logger.error(f"There was an Error with the User too short check: {str(e)}")
            return False
    
    def verify_pass_short(self) -> bool:
        """_summary_
        """
        try:
            self.locator.is_element_present(self.ErrorMessages.ERROR_PASS_TOO_SHORT)
            self.screenshot.take_screenshot(self.driver, "Short_Pass")
            self.logger.info(f"Login was not successful, Password too short")
            return True
        except Exception as e:
            self.screenshot.take_screenshot(self.driver, "Error_Pass_Short")
            self.logger.error(f"There was an Error with the Password too short check: {str(e)}")
            return False
    
    def verify_login_success(self) -> bool:
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            element = self.locator.get_element(self.CommonLocators.LOGOUT_BUTTON)
            if element is not None:
                logger.info(f"Success in finding element: {element.text}")
                return True
            return False
        except TimeoutException:
            self.logger.error(f"Timeout Exception thrown")
            return False 
        except Exception as e:
            self.logger.error(f"Login does not appear to have been successful")
            return False
        
    def login(self, user: str = "", password: str = ""):
        
        try:
            self.logger.info(f"Attempting to login with username: {user}")
            self.enter_username(user)
            self.logger.info("Attempting to enter password")
            self.enter_password(password)
            self.logger.info("Attempting to click LogIn Button")
            self.click_login_button()
        except Exception as e:
            self.logger.error(f"There was a problem with the attempted login: {str(e)}")
            
    def find_logo(self):
        return super().find_logo()
    
    def find_login_link(self):
        return super().find_login_link()
    
