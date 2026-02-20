# users_fixtures.py (Fixture)
import os
import pytest
import requests
import uuid
from dotenv import load_dotenv
from typing import List, Dict, Any
from utilities.config import PAGE_SIZE
from utilities.utils import logger, get_browser_name
from page_objects.admin_menu.users_page import UsersPage
from conftest import QA_WEB_BASE_URL

@pytest.fixture
def users_page(logged_in_page):
    """
    Fixture that provides the Users page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[UsersPage]: A list of UsersPage objects for each logged-in browser instance
    """
    logger.debug("Staring users_page fixture")
    user_pages = []
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Users page on {get_browser_name(page)}")
        logger.info("=" * 80)

        # Navigate directly to Users page
        page.goto(QA_WEB_BASE_URL + "/users")
        
        # Create the page object
        users_page = UsersPage(page)
        
        # Verify that we're on the Users page
        if users_page.verify_page_title():
            logger.info("Successfully navigated to Users page")
            user_pages.append(users_page)
        else:
            logger.error(f"Failed to navigate to Users page on {get_browser_name(page)}")

    logger.info(f"users_page fixture: yielding {len(user_pages)} users page(s)")
    yield user_pages
    logger.debug("users_page fixture: finished")
    
    
    
# User payload
# payload = {
#     "email": f"testuser{unique_suffix}@example.com", 
#     "firstName": f"Test user {unique_suffix}",
#     "isHeadSetAdmin": False,
#     "isSystemAdmin": False,
#     "lastName": "User",
#     "organizations": [
#         {
#             "name": f"Test Organization {unique_suffix}",
#             "organizationId": organization_id
            
#         }
#     ],
#     "roles": [
#         {
#             "id": "94e9113c-d7c6-4190-9338-dfb8a9434df9",
#             "name": "OrgAdmin"
#         }
#     ],
#     "userId": user_id,
#     "userName": f"ausername{unique_suffix}"
# }
