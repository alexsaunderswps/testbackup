# login_page.py (Playwright version)
import os
from dotenv import load_dotenv
from utilities.utils import logger

load_dotenv()

class LoginPage:
    """
    Page object for the login page using Playwright.
    """
    def __init__(self,page):
        self.page = page
        self.logger = logger
        
    # Element locators - Using playwright's role-based selectors.
    EMAIL_INPUT = lambda self: self.page.get_by_role("textbox", name="Email")
    PASSWORD_INPUT = lambda self: self.page.get_by_role("textbox", name="Password")
    LOGIN_BUTTON = lambda self: self.page.get_by_role("button", name="Log In")
    LOGOUT_BUTTON = lambda self: self.page.get_by_role("button", name="LOG OUT")
    
    # Error message selectors
    ERROR_BLANK_INPUT = lambda self: self.page.locator("div.alert-danger:has-text('UserName'):has-text('Password')")
    ERROR_NO_PASS = lambda self: self.page.locator("div.alert-danger:has-text('Password')")
    ERROR_NO_USER = lambda self: self.page.locator("div.alert-danger:has-text('UserName')")
    ERROR_INVALID = lambda self: self.page.locator("div.alert-danger:has-text('Failed')")
    ERROR_PASS_TOO_SHORT = lambda self: self.page.locator("div.alert-danger:has-text('Password'):has-text('4')")
    ERROR_PASS_TOO_LONG = lambda self: self.page.locator("div.alert-danger:has-text('Password'):has-text('20')")
    ERROR_USER_TOO_SHORT = lambda self: self.page.locator("div.alert-danger:has-text('UserName'):has-text('4')")

    # Action methods
    def navigate_to_login(self, login_url):
        """
        Navigate to the login page.
        
        Args:
            login_url (str): The URL of the login page.
        """
        cleaned_url = login_url.replace("\\x3a", ":") # Clean the URL
        self.logger.info(f"Navigating to login page: {cleaned_url}")
        self.page.goto(cleaned_url)
        
    def enter_username(self, username):
        """
        Enter the email address in the email input field.
        
        Args:
            username (str): The email address to enter.
        """
        self.logger.info(f"Entering username: {username}")
        self.EMAIL_INPUT().fill(username)
        
    def enter_password(self, password):
        """
        Enter the password in the password input field.
        
        Args:
            password (str): The password to enter.
        """
        self.logger.info(f"Entering password: {password}")
        self.PASSWORD_INPUT().fill(password)
    
    def click_login_button(self):
        """
        Click the login button.
        """
        self.logger.info("Clicking login button.")
        self.LOGIN_BUTTON().click()
        
    def login(self, username="", password=""):
        """
        Perform the login action with given credentials.
        
        Args:
            username (str): The email address to enter. Defaults to empty string.
            password (str): The password to enter. Defaults to empty string.
        """
        self.logger.info(f"Attempting login with username: {username} and password: {password}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
    # Verification methods
    def verify_login_success(self):
        """
        Verify that the login was successful by checking for the presence of the logout button.
        
        Returns:
            bool: True if login was successful, False otherwise.
        """
        self.logger.info("Verifying login success.")
        try:
            self.LOGOUT_BUTTON().wait_for(state="visible")
            self.logger.info("Login successful - logout button is visible.")
            return True
        except Exception as e:
            self.logger.error(f"Login failed - logout button is not visible. Error: {e}")
            self.page.screenshot(path="login_failure.png")
            return False
        
    def verify_both_missing(self):
        """    
        Verify the error message that both username and password fields are missing.
        
        Returns:
            bool: True if correct error message is shown, False otherwise.
        """
        self.logger.info("Verifying the error message when both username and password fields are missing.")
        try:
            self.ERROR_BLANK_INPUT().wait_for(state="visible")
            self.page.screenshot(path="No_Creds.png")
            self.logger.info("Correct error message shown for both Username and Password missing.")
            return True
        except Exception as e:
            self.page.screenshot(path="Error_No_Creds.png")
            self.logger.error(f"Error checking 'both missing' error message: {str(e)}")
            return False
        
    def verify_invalid_credentials(self):
        """
        Verify the error message for invalid credentials.
        
        Returns:
            bool: True if correct error message is shown, False otherwise
        """
        logger.info("Verifying the error message for invalid credentials.")
        try:
            self.ERROR_INVALID().wait_for(state='visible')
            self.page.screenshot(path="Invalid_Creds.png")
            self.logger.info("Correct error message shown for invalid credentials.")
            return True
        except Exception as e:
            self.page.screenshot(path="Error_Invalid_Creds.png")
            self.logger.error(f"Error checking 'invalid credentials' error message: {str(e)}")
            return False
        
    def verify_username_missing(self):
        """
        Verify the error message that the username field is missing.
        
        Returns:
            bool: True if correct error message is shown, False otherwise
        """
        self.logger.info("Verifying the error message when username field is missing.")
        try:
            self.ERROR_NO_USER().wait_for(state='visible')
            self.page.screenshot(path="No_User.png")
            self.logger.info("Correct error message shown for missing username.")
            return True
        except Exception as e:
            self.page.screenshot(path="Error_No_User.png")
            self.logger.error(f"Error checking 'username missing' error message: {str(e)}")
            return False
        
    def verify_password_missing(self):
        """
        Verify the error message that the password field is missing.
        Returns:
            bool: True if correct error message is shown, False otherwise
        """
        self.logger.info("Verifying the error message when password field is missing.")
        try:
            self.ERROR_NO_PASS().wait_for(state='visible')
            self.page.screenshot(path="No_Pass.png")
            self.logger.info("Correct error message shown for missing password.")
            return True
        except Exception as e:
            self.page.screenshot(path="Error_No_Pass.png")
            self.logger.error(f"Error checking 'password missing' error message: {str(e)}")
            return False
    
    def verify_username_too_short(self):
        """
        Verify the error message that the username is too short.
        Returns:
            bool: True if correct error message is shown, False otherwise
        """
        self.logger.info("Verifying the error message when username is too short.")
        try:
            self.ERROR_USER_TOO_SHORT().wait_for(state='visible')
            self.page.screenshot(path="User_Too_Short.png")
            self.logger.info("Correct error message shown for username too short.")
            return True
        except Exception as e:
            self.page.screenshot(path="Error_User_Too_Short.png")
            self.logger.error(f"Error checking 'username too short' error message: {str(e)}")
            return False
        
    def verify_password_too_short(self):
        """
        Verify the error message that the password is too short.
        Returns:
            bool: True if correct error message is shown, False otherwise
        """
        self.logger.info("Verifying the error message when password is too short.")
        try:
            self.ERROR_PASS_TOO_SHORT().wait_for(state='visible')
            self.page.screenshot(path="Pass_Too_Short.png")
            self.logger.info("Correct error message shown for password too short.")
            return True
        except Exception as e:
            self.page.screenshot(path="Error_Pass_Too_Short.png")
            self.logger.error(f"Error checking 'password too short' error message: {str(e)}")
            return False
        
    def verify_password_too_long(self):
        """
        Verify the error message that the password is too long.
        Returns:
            bool: True if correct error message is shown, False otherwise
        """
        self.logger.info("Verifying the error message when password is too long.")
        try:
            self.ERROR_PASS_TOO_LONG().wait_for(state='visible')
            self.page.screenshot(path="Pass_Too_Long.png")
            self.logger.info("Correct error message shown for password too long.")
            return True
        except Exception as e:
            self.page.screenshot(path="Error_Pass_Too_Long.png")
            self.logger.error(f"Error checking 'password too long' error message: {str(e)}")
            return False