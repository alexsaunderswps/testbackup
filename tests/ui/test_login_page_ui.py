#test_login_page_ui.py
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

class TestLoginPageUI:
    
    @pytest.mark.UI 
    def test_login_page_elements(self, login_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        lp = login_page
        
        all_elements = lp.verify_all_elements_present()
        check.is_true(all_elements, "Elements missing from Login Page")
        logger.info("Verification Successful :: All Elements found on Login Page")
        
if __name__ == "__main__":
    TL = TestLoginPageUI()
    TL.test_valid_login()