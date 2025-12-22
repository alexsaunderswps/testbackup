#login_fixtures.py
import os
import pytest
from faker import Faker
from dotenv import load_dotenv
from pytest_check import check # type: ignore
from page_objects.authentication.login_page import LoginPage
from utilities.utils import get_browser_name, logger

# Load environmental variables
load_dotenv()
QA_LOGIN_URL = os.getenv("QA_LOGIN_URL").replace("\\x3a", ":") # type: ignore
SYS_ADMIN_USER = os.getenv("SYS_ADMIN_USERNAME")
SYS_ADMIN_PASS = os.getenv("SYS_ADMIN_PASSWORD")
ORG_WPS_USER = os.getenv("ORG_ADMIN_WPS_USERNAME")
ORG_WPS_PASS = os.getenv("ORG_ADMIN_WPS_PASSWORD")

@pytest.fixture
def login_page(browser_context_and_page):
    """
    Fixture that provides the Login page for each test.
    
    This fixture creates fresh LoginPage objects for testing the login process itself.
    Unlike other page fixtures, this uses browser_context_and_page instead of 
    logged_in_page since we need to test the authentication process.
    
    Args:
        browser_context_and_page: A fixture providing fresh browser instances from conftest.py
        
    Yields:
        List[LoginPage]: A list of LoginPage objects for each browser instance
    """
    logger.debug("Starting login_page fixture")
    login_pages = []
    
    for browser, context, page in browser_context_and_page:
        logger.info(80 * "-")
        logger.info(f"Navigating to login page on {get_browser_name(page)}")
        logger.info(80 * "-")

        # Navigate to the login page
        page.goto(QA_LOGIN_URL)
        
        login_page = LoginPage(page)
        
        # Verify that we're on the login page by checking for the login button
        try:
            login_button = login_page.get_login_button()
            if login_button.count() > 0:
                logger.info(f"Successfully navigate to login page on {get_browser_name(page)}")
                login_pages.append(login_page)
            else:
                logger.error(f"Failed to navigate to Login page on {get_browser_name(page)}")
        except Exception as e:
            logger.error(f"Error verifying login page on {get_browser_name(page)}: {str(e)}")
    
    logger.info(f"login_page fixture: yielding {len(login_pages)} login page(s)")
    yield login_pages
    logger.debug("login_page fixture: finished")
    
@pytest.fixture
def fresh_login_page(browser_context_and_page):
    """
    Alternative fixture for tests that need a completely fresh login page.
    
    This is useful for tests that might need to clear browser state or
    test specific scenarios with clean browser sessions.
    
    Args:
        browser_context_and_page: A fixture providing fresh browser instances from conftest.py
        
    Yields:
        List[LoginPage]: A list of fresh LoginPage objects for each browser instance
    """
    logger.debug("Starting fresh_login_page fixture")
    fresh_login_pages = []
    
    for browser, context, page in browser_context_and_page:
        logger.info(80 * "-")
        logger.info(f"Navigating to fresh login page on {get_browser_name(page)}")
        logger.info(80 * "-")
        
        # Clear existing session data if needed
        context.clear_cookies()

        # Navigate to the login page
        page.goto(QA_LOGIN_URL)
        
        fresh_login_page = LoginPage(page)
        
        
        # Verify that we're on the login page by checking for the login button
        try:
            login_button = fresh_login_page.get_login_button
            if login_button.count() > 0: # type: ignore
                fresh_login_pages.append(fresh_login_page)
                logger.info(f"Successfully navigated to fresh login page on {get_browser_name(page)}")
            else:
                logger.error(f"Failed to navigate to fresh Login page on {get_browser_name(page)}")
        except Exception as e:
            logger.error(f"Error verifying fresh login page on {get_browser_name(page)}: {str(e)}")
    
    logger.info(f"fresh_login_page fixture: yielding {len(fresh_login_pages)} fresh login page(s)")
    yield fresh_login_pages
    logger.debug("fresh_login_page fixture: finished")