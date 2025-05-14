# login_page.py (Playwright version)
import os
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

class LoginPage(BasePage):
    """
    Page object for the login page using Playwright.
    """
    def __init__(self,page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators - Using method-based approach for consistency across pages
    def get_email_input(self):
        """ Get the email input field element. """
        return self.page.get_by_role("textbox", name="Email")
    
    def get_password_input(self):
        """ Get the password input field element. """
        return self.page.get_by_role("textbox", name="Password")
    
    def get_login_button(self):
        """ Get the login button element. """
        return self.page.get_by_role("button", name="Log In")
    
    def get_logout_button(self):
        """ Get the logout button element. """
        return self.page.get_by_role("button", name="LOG OUT")
    
    # Error message locators
    def get_error_blank_input(self):
        """ Get the error message for blank input fields. """
        return self.page.locator("div.alert-danger:has-text('UserName'):has-text('Password')")
    
    def get_error_no_pass(self):
        """ Get the error message for missing password. """
        return self.page.locator("div.alert-danger:has-text('Password')")
    
    def get_error_no_user(self):
        """ Get the error message for missing username. """
        return self.page.locator("div.alert-danger:has-text('UserName')")
    
    def get_error_invalid(self):
        """ Get the error message for invalid credentials. """
        return self.page.locator("div.alert-danger:has-text('Failed')")
    
    def get_error_pass_too_short(self):
        """ Get the error message for password too short. """
        return self.page.locator("div.alert-danger:has-text('Password'):has-text('4')")
    
    def get_error_pass_too_long(self):
        """ Get the error message for password too long. """
        return self.page.locator("div.alert-danger:has-text('Password'):has-text('20')")
    
    def get_error_user_too_short(self):
        """ Get the error message for username too short. """
        return self.page.locator("div.alert-danger:has-text('UserName'):has-text('4')")

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
        self.get_email_input().fill(username)
        
    def enter_password(self, password):
        """
        Enter the password in the password input field.
        
        Args:
            password (str): The password to enter.
        """
        self.logger.info(f"Entering password: {password}")
        self.get_password_input().fill(password)
    
    def click_login_button(self):
        """
        Click the login button.
        """
        self.logger.info("Clicking login button.")
        self.get_login_button().click()
        
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
            self.get_logout_button().wait_for(state="visible")
            self.logger.info("Login successful - logout button is visible.")
            return True
        except Exception as e:
            self.logger.error(f"Login failed - logout button is not visible. Error: {e}")
            self.take_screenshot("login_failure")
            return False
        
    def verify_both_missing(self):
        """    
        Verify the error message that both username and password fields are missing.
        
        Returns:
            bool: True if correct error message is shown, False otherwise.
        """
        self.logger.info("Verifying the error message when both username and password fields are missing.")
        try:
            self.get_error_blank_input().wait_for(state="visible")
            self.take_screenshot("No_Creds")
            self.logger.info("Correct error message shown for both Username and Password missing.")
            return True
        except Exception as e:
            self.take_screenshot("Error_No_Creds")
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
            self.get_error_invalid().wait_for(state='visible')
            self.take_screenshot("Invalid_Creds")
            self.logger.info("Correct error message shown for invalid credentials.")
            return True
        except Exception as e:
            self.take_screenshot("Error_Invalid_Creds")
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
            self.get_error_no_user().wait_for(state='visible')
            self.take_screenshot("No_User")
            self.logger.info("Correct error message shown for missing username.")
            return True
        except Exception as e:
            self.take_screenshot("Error_No_User")
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
            self.get_error_no_pass().wait_for(state='visible')
            self.take_screenshot("No_Pass")
            self.logger.info("Correct error message shown for missing password.")
            return True
        except Exception as e:
            self.take_screenshot("Error_No_Pass")
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
            self.get_error_user_too_short().wait_for(state='visible')
            self.take_screenshot("User_Too_Short")
            self.logger.info("Correct error message shown for username too short.")
            return True
        except Exception as e:
            self.take_screenshot("Error_User_Too_Short")
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
            self.get_error_pass_too_short().wait_for(state='visible')
            self.take_screenshot("Pass_Too_Short")
            self.logger.info("Correct error message shown for password too short.")
            return True
        except Exception as e:
            self.take_screenshot("Error_Pass_Too_Short")
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
            self.get_error_pass_too_long().wait_for(state='visible')
            self.take_screenshot("Pass_Too_Long")
            self.logger.info("Correct error message shown for password too long.")
            return True
        except Exception as e:
            self.take_screenshot("Error_Pass_Too_Long")
            self.logger.error(f"Error checking 'password too long' error message: {str(e)}")
            return False