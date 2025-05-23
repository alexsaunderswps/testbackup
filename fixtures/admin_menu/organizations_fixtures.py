#organizations_fixtures.py (Fixture)
import os
import pytest
import requests
import uuid
from dotenv import load_dotenv
from typing import List, Dict, Any
from utilities.config import PAGE_SIZE
from utilities.utils import logger, get_browser_name
from page_objects.admin_menu.organizations_page import OrganizationsPage

@pytest.fixture
def organizations_page(logged_in_page):
    """
    Fixture that provides the Organizations page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[OrganizationsPage]: A list of OrganizationsPage objects for each logged-in browser instance
    """
    logger.info("Starting organizations_page fixture")
    organization_pages = []
    
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Organizations page on {get_browser_name(page)}")
        logger.info("=" * 80)
        
        # Navigate to Organizations page
        page.get_by_role("button", name="Admin").click()
        page.get_by_role("link", name="Organizations").click()
        
        # Create the page object
        org_page = OrganizationsPage(page)
        
        # Verify that we're on the Organizations page
        if org_page.verify_page_title():
            logger.info("Successfully navigated to the Orgnizations Page")
            organization_pages.append(org_page)
        else:
            logger.error(f"Failed to navigate to the Organizations page on {get_browser_name(page)}")
            
    logger.info(f"organizations_page fixture: yielding {len(organization_pages)} organizations page(s)")
    yield organization_pages
    logger.debug("organizations_page fixture: finished")
        
    