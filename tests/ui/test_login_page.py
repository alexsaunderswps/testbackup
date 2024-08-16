#test_login_page.py
import os
import pytest
import time
from faker import Faker
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium. webdriver.support import expected_conditions as EC
from page_objects.authentication.login_page import LoginPage
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger


# Initialize Faker
fake = Faker()
# Initialize helpers
screenshot = ScreenshotManager()

# Load environmental variables
load_dotenv()
BASE_URL = os.getenv("QA_BASE_URL")
LOGIN_URL = os.getenv("QA_LOGIN_URL")
ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")
FAKE_USER = fake.email()
FAKE_PASS = fake.password()
FAKE_USER_SHORT = fake.email()[:4]
FAKE_PASS_SHORT = fake.password()[:4]


class TestLogin:
    
    @pytest.mark.run(order=1)
    @pytest.mark.succeeds
    def test_valid_login(self, setup_isolated):
        driver, wait = setup_isolated
        logger.info(f"Attempting log from succeeding test on {driver.name}")
        driver.get(BASE_URL)
        
        lp = LoginPage(driver)
        lp.login(ADMIN_USER, ADMIN_PASS)
        time.sleep(2)
        login_succeeds = lp.verify_login_success()
        assert login_succeeds, "Login Failed which was not expected"
        
    @pytest.mark.run(order=0)
    @pytest.mark.fails
    def test_empty_creds(self, setup_isolated):
        driver, wait = setup_isolated
        logger.info(f"Attempting log from failing test on {driver.name}")
        driver.get(BASE_URL)
        
        lp = LoginPage(driver)
        lp.login()
        login_fails = lp.verify_both_missing()
        assert login_fails, "Login Succeed which was not expected"
        
    @pytest.mark.run(order=2)
    @pytest.mark.fails
    def test_empty_user(self, setup_isolated):
        driver, wait = setup_isolated
        logger.info(f"Attempting log from failing test on {driver.name}")
        driver.get(BASE_URL)
        
        lp = LoginPage(driver)
        lp.login("", FAKE_PASS)
        login_fails = lp.verify_user_missing()
        assert login_fails, "Login Succeed which was not expected"
        
    @pytest.mark.run(order=3)
    @pytest.mark.fails
    def test_empty_pass(self, setup_isolated):
        driver, wait = setup_isolated
        logger.info(f"Attempting log from failing test on {driver.name}")
        driver.get(BASE_URL)
        
        lp = LoginPage(driver)
        lp.login(FAKE_USER, "")
        login_fails = lp.verify_password_missing()
        assert login_fails, "Login Succeed which was not expected"
        
    @pytest.mark.run(order=4)
    @pytest.mark.fails
    def test_short_user(self, setup_isolated):
        driver, wait = setup_isolated
        logger.info(f"Attempting log from failing test on {driver.name}")
        driver.get(BASE_URL)
        
        lp = LoginPage(driver)
        lp.login(FAKE_USER_SHORT, FAKE_PASS)
        login_fails = lp.verify_user_short()
        assert login_fails, "Login Succeed which was not expected"
        
    @pytest.mark.run(order=5)
    @pytest.mark.fails
    def test_short_pass(self, setup_isolated):
        driver, wait = setup_isolated
        logger.info(f"Attempting log from failing test on {driver.name}")
        driver.get(BASE_URL)
        
        lp = LoginPage(driver)
        lp.login(FAKE_USER, FAKE_PASS_SHORT)
        login_fails = lp.verify_pass_short()
        assert login_fails, "Login Succeed which was not expected"     
        
if __name__ == "__main__":
    TL = TestLogin()
    TL.test_valid_login()