#test_login_functionality.py
import os
import pytest
import time
from faker import Faker
from dotenv import load_dotenv
from pytest_check import check
from page_objects.authentication.login_page import LoginPage
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger


# Initialize Faker and Screenshot
fake = Faker()
screenshot = ScreenshotManager()

# Load environmental variables
load_dotenv()
BASE_URL = os.getenv("QA_BASE_URL")
LOGIN_URL = os.getenv("QA_LOGIN_URL")
ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")
VALID_USER = os.getenv("VALID_USERNAME")
VALID_PASS = os.getenv("VALID_PASSWORD")

@pytest.fixture
def login_page(setup_isolated):
    driver, wait = setup_isolated
    logger.info(f"Navigating to login page on {driver.name}")
    driver.get(BASE_URL)
    return LoginPage(driver)

class TestLoginPageFunctionality:
    
    @pytest.mark.functionality
    @pytest.mark.succeeds
    def test_valid_admin_login(self, login_page):
        lp = login_page
        lp.login(ADMIN_USER, ADMIN_PASS)
        
        login_succeeds = lp.verify_login_success()
        check.is_true(login_succeeds, "Admin Login Failed")
        logger.info("Verifiction Successful :: Admin Login Succeeded" if login_succeeds else "Verification Failed :: Admin Login Failed")

        find_login_link = lp.find_login_link()
        check.is_false(find_login_link, "Login Link found after Admin login")
        logger.info("Verification Successful :: Login Link was not found after logging in as Admin." if not find_login_link else "Verification Failed :: Login link found after logging in as Admin")
        
        find_logout_link = lp.find_logout()
        check.is_true(find_logout_link, "Log Out Link not found after logging in as Admin")
        logger.info("Verification Successful :: Logout Link found after logging in as Admin." if find_logout_link else "Verification Failed :: Logout link was not found after logging in as Admin")

        lp.logout_site()


    @pytest.mark.functionality
    @pytest.mark.succeeds
    def test_valid_user_login(self, login_page):        
        lp = login_page
        lp.login(VALID_USER,VALID_PASS)
        
        login_succeeds = lp.verify_login_success()
        check.is_true(login_succeeds, "User Login Failed")
        logger.info("Verifiction Successful :: User Login Succeeded" if login_succeeds else "Verification Failed :: User Login Failed")

        find_login_link = lp.find_login_link()
        check.is_false(find_login_link, "Login Link found after User login")
        logger.info("Verification Successful :: Login Link was not found after logging in as User." if not find_login_link else "Verification Failed :: Login link found after logging in as User")
        
        find_logout_link = lp.find_logout()
        check.is_true(find_logout_link, "Log Out Link not found after logging in as User")
        logger.info("Verification Successful :: Logout Link found after logging in as User." if find_logout_link else "Verification Failed :: Logout link was not found after logging in as User")

        lp.logout_site()
        
        
    @pytest.mark.functionality 
    @pytest.mark.fails
    @pytest.mark.debug
    def test_login_failure(self, login_page):
        lp = login_page
        
        lp.login("","")
        login_fails = lp.verify_both_missing()
        check.is_true(login_fails, f"Logging in succeeded unexpectedly with empty user and password.")
        
        lp.login(fake.email(),fake.password())
        login_fails = lp.verify_invalid_creds()
        check.is_true(login_fails, f"Logging in succeeded unexpectedly with invalid user and password.")
        
        lp.login(fake.email(), "")
        login_fails = lp.verify_password_missing()
        check.is_true(login_fails, f"Logging in succeeded unexpectedly with empty password")
        
        lp.login("", fake.password())
        login_fails = lp.verify_user_missing()
        check.is_true(login_fails, f"Logging in succeeded unexpectedly with empty user name")
        
        lp.login(fake.email()[:3], fake.password())
        login_fails = lp.verify_user_short()
        check.is_true(login_fails, f"Logging in succeeded unexpectedly with a short username")
        
        lp.login(fake.email(), fake.password()[:3])
        login_fails = lp.verify_pass_short()
        check.is_true(login_fails, f"Logging in succeeded unexpectedly with a short password")
        
        
if __name__ == "__main__":
    TL = TestLoginPageFunctionality()
    TL.test_valid_login()