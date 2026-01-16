#login_fixtures.py
import os
import pytest
from typing import List, Tuple
from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, Page
from page_objects.authentication.login_page import LoginPage
from utilities.utils import logger

# Load environmental variables
load_dotenv()
QA_LOGIN_URL = os.getenv("QA_LOGIN_URL").replace("\\x3a", ":") # type: ignore
SYS_ADMIN_USER = os.getenv("SYS_ADMIN_USERNAME")
SYS_ADMIN_PASS = os.getenv("SYS_ADMIN_PASSWORD")
ORG_WPS_USER = os.getenv("ORG_ADMIN_WPS_USERNAME")
ORG_WPS_PASS = os.getenv("ORG_ADMIN_WPS_PASSWORD")


@pytest.fixture
def login_page(browser_instances, request) -> List[LoginPage]: # type: ignore
    """
    Fixture that provides a fresh, unauthenticated Login page for each test.
    
    Each test gets a completely clean browser context with no cookies or 
    stored authentication, allowing tests to exercise the login flow itself.
    
    Args:
        browser_instances: Session-scoped browsers from conftest.py
        request: The pytest request object
        
    Yields:
        List[LoginPage]: A list of LoginPage objects (one per browser if running "all")
    """
    logger.debug("Starting login_page fixture")
    contexts_and_pages: List[Tuple[BrowserContext, Page]] = []
    login_pages: List[LoginPage] = []
    
    for browser_type, browser in browser_instances.items():
        logger.info(80 * "-")
        logger.info(f"Creating unauthenticated context for login page on {browser_type}")
        logger.info(80 * "-")

        # Create fresh context with NO auth state
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate to the login page
        page.goto(QA_LOGIN_URL)
        
        login_page_obj = LoginPage(page)
        
        # Verify that we're on the login page by checking for the login button
        try:
            login_button = login_page_obj.get_login_button()
            if login_button.count() > 0:
                logger.info(f"Successfully navigated to login page on {browser_type}")
                contexts_and_pages.append((context, page))
                login_pages.append(login_page_obj)
            else:
                logger.error(f"Failed to navigate to Login page on {browser_type}")
                context.close()
        except Exception as e:
            logger.error(f"Error verifying login page on {browser_type}: {str(e)}")
            context.close()
    
    logger.info(f"login_page fixture: yielding {len(login_pages)} login page(s)")
    yield login_pages
    
    # Teardown - close contexts (browsers stay alive, they're session-scoped)
    for context, page in contexts_and_pages:
        context.close()
    logger.debug("login_page fixture: finished")