# confest.py (playwright)

import os
import pytest
import time
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from typing import Dict, List, Tuple, Generator, Any
from utilities.utils import logger, start_test_capture, end_test_capture, get_logs_for_test

# Load and define enviromnetal variables
load_dotenv()
SYS_ADMIN_USER = os.getenv("SYS_ADMIN_USERNAME")
SYS_ADMIN_PASS = os.getenv("SYS_ADMIN_PASSWORD")
ORG_WPS_USER = os.getenv("ORG_ADMIN_WPS_USERNAME")
ORG_WPS_PASS = os.getenv("ORG_ADMIN_WPS_PASSWORD")
ORG_BP_USER = os.getenv("ORG_ADMIN_BP_USERNAME")
ORG_BP_PASS = os.getenv("ORG_ADMIN_BP_PASSWORD")
ORG_DTA_USER = os.getenv("ORG_ADMIN_DTA_USERNAME")
ORG_DTA_PASS = os.getenv("ORG_ADMIN_DTA_PASSWORD")
QA_LOGIN_URL = os.getenv("QA_LOGIN_URL").replace("\\x3a", ":")

# Define pytest addoption for Command Line runnig of Pytest with options
def pytest_addoption(parser):
    """
    Add custom command line options to pytest.
    
    This function is called by pytest to add custom options to the command line parser.
    It defines options for browser selection, headless mode, and login credentials.
    
    Args:
        parser (argparse.Parser): The pytest command line parser.
        
    Example:
        pytest --browser fireforx --headless False
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Specify the browser to use: chromium, firefox, webkit, or all. Default is chromium."        
    )
    parser.addoption(
        "--headless",
        action="store",
        default=True,
        help="Run tests in headsless mode (True or False). Default is True." 
    )
    parser.addoption(
        "--username",
        action="store",
        default=SYS_ADMIN_USER,
        help="Username for login. Default is the ADMIN_USER value from .env file."
    )
    parser.addoption(
        "--password",
        action="store",
        default=SYS_ADMIN_PASS,
        help="Password for login. Default is the ADMIN_PASS value from .env file."
    )
    
@pytest.fixture(scope="session")
def playwright():
    """
    Fixture providing the Playwright instance.
    """
    with sync_playwright() as playwright:
        yield playwright
        
def get_browser_instance(playwright, browser_name: str, headless: bool) -> Browser:
    """
    Get a browser instance based on the specified browser name and options.
    
    Args:
        playwright (sync_playwright): The Playwright instance.
        browser_name (str): The name of the browser to use (chromium, firefox, webkit).
        headless (bool): Whether to run the browser in headless mode.
        
    Returns:
        Browser: The browser instance.
    """
    logger.info(f"Launching {browser_name} browser in {'headless' if headless else 'non-headless'} mode.")
    
    # Convert headless to boolean
    if isinstance(headless, str):
        headless = headless.lower() == "true"
    
    if browser_name.lower() == "chromium":
        return playwright.chromium.launch(headless=headless)
    elif browser_name.lower() == "firefox":
        return playwright.firefox.launch(headless=headless)
    elif browser_name.lower() == "webkit":
        return playwright.webkit.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser {browser_name}. Supported browsers are: chromium, firefox, webkit.")

@pytest.fixture(scope="function")
def browser_context_and_page(playwright, request):
    """
    Fixture that provides a browser, context, and page for each test.
    
    Args:
        playwright: The Playwright instance.
        request: The pytest request object.
    
    Yields:
    tuple: A tuple containing the browser, context, and page.
    """
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    # Handle 'all' browser option
    if browser_name.lower() == "all":
        browser_contexts =[]
        for browser_type in ["chromium", "firefox", "webkit"]:
            browser = get_browser_instance(playwright, browser_type, headless)
            context = browser.new_context()
            page = context.new_page()
            start_test_capture(f"{page.browser.browser_type.name}_{request.node.name}")
            browser_contexts.append((browser, context, page))
            
        yield browser_contexts
        
        # Teardown
        
        for browser, context, page in browser_contexts:
            end_test_capture(f"{page.browser.browser_type.name}_{request.node.name}")
            context.close()
            browser.close()
    
    else:
        # Single browser setup
        browser = get_browser_instance(playwright, browser_name, headless)
        context = browser.new_context()
        page = context.new_page()
        
        start_test_capture(f"{browser_name}_{request.node.name}")
        yield [(browser, context, page)]
        
        # Teardown
        end_test_capture(f"{browser_name}_{request.node.name}")
        context.close()
        browser.close()

@pytest.fixture
def logged_in_page(browser_context_and_page, request):
    """
    Fixture that provides a logged-in page(s) for tests that require pre-authentication.

    Args:
        browser_context_and_page: A fixture providing brower, context, and page.
        request: The pytest request object.
        
    Yields:
    List[Page]: A list of logged-in pages.
    """
    logger.info("Starting logged_in_page fixture.")
    logged_in_pages = []
    
    username = request.config.getoption("--username", default=SYS_ADMIN_USER)
    password = request.config.getoption("--password", default=SYS_ADMIN_PASS)
    
    for browser, context, page in browser_context_and_page:
        logger.info("="* 80)
        logger.info(f"Logging in on {browser.browser_type.name}")
        logger.info("=" * 80)
        
        # Navigate to the login page
        page.goto(QA_LOGIN_URL)
        
        # Login process
        page.get_by_role("textbox", name="Email").fill(username)
        page.get_by_role("textbox", name="Password").fill(password)
        page.get_by_role("button", name="Log In").click()
        
        # Wait for login to complete - adjust the selector as needed
        page.get_by_role("button", name="LOG OUT").wait_for(state="visible")
        
        logged_in_pages.append(page)
        
    logger.debug(f"logged_in_page fixture: yielding {len(logged_in_pages)} logged-in page(s).")
    yield logged_in_pages
    logger.debug("logged_in_page fixture: finshed.")
    