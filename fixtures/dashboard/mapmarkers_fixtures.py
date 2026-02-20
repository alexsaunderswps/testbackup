#mapmarkers_fixtures.py (Fixture)
import os
import pytest
import requests
import uuid
from dotenv import load_dotenv
from typing import List, Dict, Any
from utilities.utils import logger, get_browser_name
from utilities.auth import get_auth_headers
from page_objects.dashboard.map_markers_page import MapMarkersPage
from conftest import QA_WEB_BASE_URL

# Load environment variables from .env file
load_dotenv()

# Get API credentials and endpoints from environment variables
api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
organization_id = os.getenv("TEST_ORGANIZATION_ID", "4ffbb8fe-d8b4-49d9-982d-5617856c9cce")

@pytest.fixture
def map_markers_page(logged_in_page):
    """
    Fixture that provides the Map Markers page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[MapMarkersPage]: A list of MapMarkersPage objects for each logged-in browser instance
    """
    logger.debug("Starting map_markers_page fixture")
    map_marker_pages = []
    for page in logged_in_page:
        logger.info(80 * "-")
        logger.info(f"Navigating to Map Markers page on {get_browser_name(page)}")
        logger.info(80 * "-")
    
    # Navigate directly to Map Markers page
        page.goto(QA_WEB_BASE_URL + "/mapMarkers")
        
    # Create the page object
        map_markers_page = MapMarkersPage(page)
        
    # Verify that we're on the Map Markers page
        if map_markers_page.verify_page_title_present():
            logger.info("Successfully navigated to Map Markers page")
            map_marker_pages.append(map_markers_page)
        else:
            logger.error(f"Failed to navigate to Map Markers page on {get_browser_name(page)}")
            
    logger.info(f"map_markers_page fixture: yielding {len(map_marker_pages)} map markers page(s)")
    yield map_marker_pages
    logger.debug("map_markers_page fixture: finished")