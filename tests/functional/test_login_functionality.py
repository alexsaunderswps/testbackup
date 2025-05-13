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
    def test_login_failure(self, login_page):
        """
        Test login failure functionality.
        
        This test verifies that a user cannot log in with invalid credentials.
        """
        for lp in login_page:
            # Test empty credentials
            lp.login("", "")
            login_fails = lp.verify_both_missing()
            assert login_fails, "Login should fail with empty credentials"
            logger.info("Verification Successful :: Login Failed with empty credentials")
        
            # Test invalid credentials
            lp.login(fake.user_name(), fake.password())
            login_fails = lp.verify_invalid_credentials()
            assert login_fails, "Login should fail with invalid credentials"
            logger.info("Verification Successful :: Login Failed with invalid credentials") 
            
            # Testing missing username
            lp.login("", fake.password())
            login_fails = lp.verify_username_missing()
            assert login_fails, "Login should fail with missing username"
            logger.info("Verification Successful :: Login Failed with missing username")
            
            # Test missing password
            lp.login(fake.user_name(), "")
            login_fails = lp.verify_password_missing()
            assert login_fails, "Login should fail with missing password"
            logger.info("Verification Successful :: Login Failed with missing password")    
            
            # Test short username
            lp.login(fake.user_name()[:3], fake.password())
            login_fails = lp.verify_username_too_short()
            assert login_fails, "Login should fail with short username"
            logger.info("Verification Successful :: Login Failed with short username")
            
            # Test short password
            lp.login(fake.user_name(), fake.password()[:3])
            login_fails = lp.verify_password_too_short()
            assert login_fails, "Login should fail with short password" 
            logger.info("Verification Successful :: Login Failed with short password")
            
            # Test long password
            lp.login(fake.user_name(), fake.password(length=21))
            login_fails = lp.verify_password_too_long()
            assert login_fails, "Login should fail with long password"
            logger.info("Verification Successful :: Login Failed with long password")
            
        