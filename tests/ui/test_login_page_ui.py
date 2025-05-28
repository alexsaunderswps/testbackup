#test_login_page_ui.py
import os
import pytest
from faker import Faker
from dotenv import load_dotenv
from pytest_check import check
from page_objects.authentication.login_page import LoginPage
from utilities.utils import get_browser_name, logger

# Initialize Faker
fake = Faker()

# Load environmental variables
load_dotenv()
QA_LOGIN_URL = os.getenv("QA_LOGIN_URL").replace("\\x3a", ":")
SYS_ADMIN_USER = os.getenv("SYS_ADMIN_USERNAME")
SYS_ADMIN_PASS = os.getenv("SYS_ADMIN_PASSWORD")
ORG_WPS_USER = os.getenv("ORG_ADMIN_WPS_USERNAME")
ORG_WPS_PASS = os.getenv("ORG_ADMIN_WPS_PASSWORD")

class TestLoginPageUI:
    
    @pytest.mark.UI 
    def test_login_page_elements(self, login_page):
        """_summary_

        Args:
            login_page (_type_): _description_
        """
        for lp in login_page:
        
            all_elements = lp.verify_all_elements_present()
            check.is_true(all_elements, "Elements missing from Login Page")
            logger.info("Verification Successful :: All Elements found on Login Page")
        
if __name__ == "__main__":
    TL = TestLoginPageUI()
    TL.test_valid_login()