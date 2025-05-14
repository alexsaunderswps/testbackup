#test_login_functionality.py (Playwright version)

import os
import pytest
from faker import Faker
from dotenv import load_dotenv
from page_objects.authentication.login_page import LoginPage
from utilities.utils import logger

# Initialize Faker
fake = Faker()

# Load environment variables
load_dotenv()
QA_LOGIN_URL = os.getenv("QA_LOGIN_URL").replace("\\x3a", ":")
SYS_ADMIN_USER = os.getenv("SYS_ADMIN_USERNAME")
SYS_ADMIN_PASS = os.getenv("SYS_ADMIN_PASSWORD")
VALID_USER = os.getenv("ORG_ADMIN_WPS_USERNAME")
VALID_PASS = os.getenv("ORG_ADMIN_WPS_PASSWORD")

@pytest.fixture
def login_page(browser_context_and_page):
    login_pages = []
    for browser, conext, page in browser_context_and_page:
        logger.info(f"Setting up login page on {browser.browser_type.name}")
        page.goto(QA_LOGIN_URL)
        login_pages.append(LoginPage(page))
        
    yield login_pages
    
class TestLoginPageFunctionality:
    
    @pytest.mark.login
    @pytest.mark.functionality
    @pytest.mark.valid_credentials
    def test_valid_admin_login(self, login_page):
        """
        Test valid login functionality.
        
        This test verifies that a user can successfully log in with valid credentials.
        """
        for lp in login_page:
            lp.login(SYS_ADMIN_USER, SYS_ADMIN_PASS)
            
            login_succeeds = lp.verify_login_success()
            assert login_succeeds, "Admin Login Failed"
            logger.info("Verification Successful :: Admin Login Succeeded")
    
    @pytest.mark.login
    @pytest.mark.functionality
    @pytest.mark.valid_credentials
    def test_valid_org_login(self, login_page):
        """
        Test valid organization login functionality.
        
        This test verifies that a user can successfully log in with valid credentials.
        """
        for lp in login_page:
            lp.login(VALID_USER, VALID_PASS)
            
            login_succeeds = lp.verify_login_success()
            assert login_succeeds, "Organization Login Failed"
            logger.info("Verification Successful :: Organization Login Succeeded")
            
    @pytest.mark.login
    @pytest.mark.functionality
    @pytest.mark.invalid_credentials
    @pytest.mark.parametrize("username, password, verification_method, expected_message",[
        ("", "", "verify_both_missing", "Login should fail with empty credentials"),
        (fake.user_name(), fake.password(), "verify_invalid_credentials", "Login should fail with invalid credentials"),
        ("", fake.password(), "verify_username_missing", "Login should fail with missing username"),
        (fake.user_name(), "", "verify_password_missing", "Login should fail with missing password"),
        (fake.user_name()[:3], fake.password(), "verify_username_too_short", "Login should fail with short username"),
        (fake.user_name(), fake.password()[:3], "verify_password_too_short", "Login should fail with short password"),
        (fake.user_name(), fake.password(length=21), "verify_password_too_long", "Login should fail with long password")
    ])
    def test_login_failure(self, login_page, username, password, verification_method, expected_message):
        """
        Test login failure functionality.
        
        This test verifies that a user cannot log in with invalid credentials.
        """
        for lp in login_page:
            # Test various login failure scenarios
            for lp in login_page:
                lp.login(username, password)
                verifcation_func = getattr(lp, verification_method)
                login_fails = verifcation_func()
                assert login_fails, expected_message
                logger.info(f"Verification Successful :: {expected_message}")
    