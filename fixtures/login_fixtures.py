#login_fixtures.py
import os
import pytest
from faker import Faker
from dotenv import load_dotenv
from pytest_check import check
from page_objects.authentication.login_page import LoginPage
from utilities.utils import get_browser_name, logger

# Load environmental variables
load_dotenv()
QA_LOGIN_URL = os.getenv("QA_LOGIN_URL").replace("\\x3a", ":")
SYS_ADMIN_USER = os.getenv("SYS_ADMIN_USERNAME")
SYS_ADMIN_PASS = os.getenv("SYS_ADMIN_PASSWORD")
ORG_WPS_USER = os.getenv("ORG_ADMIN_WPS_USERNAME")
ORG_WPS_PASS = os.getenv("ORG_ADMIN_WPS_PASSWORD")

@pytest.fixture
def login_page(logged_in_page):
    """
    Fixture that provides the Map Markers page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[MapMarkersPage]: A list of MapMarkersPage objects for each logged-in browser instance
    """
    logger.debug("Starting login_page fixture")
    login_pages = []
    for page in logged_in_page:
        logger.info(80 * "-")
        logger.info(f"Navigating to login page on {get_browser_name(page)}")
        logger.info(80 * "-")
        
        
        login_page = LoginPage(page)
        login_pages.append(login_page)
        
    yield login_pages