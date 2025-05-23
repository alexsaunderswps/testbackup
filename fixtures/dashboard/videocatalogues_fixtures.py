#videocatalogues_fixtures.py (Fixture)
import os
import pytest
import requests
import uuid
from dotenv import load_dotenv
from typing import List, Dict, Any
from utilities.utils import logger, get_browser_name
from page_objects.dashboard.video_catalogues_page import VideoCataloguesPage

# Load environment variables from .env file
load_dotenv()

# Get API credentials and endpoints from environment variables
api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
api_token = os.getenv("API_TOKEN")
organization_id = os.getenv("TEST_ORGANIZATION_ID", "4ffbb8fe-d8b4-49d9-982d-5617856c9cce")

@pytest.fixture
def video_catalogue_page(logged_in_page):
    """
    Fixture that provides the Video Catalogues page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[VideoCataloguesPage]: A list of VideoCataloguesPage objects for each logged-in browser instance
    """
    logger.debug("Starting video_catalogue_page fixture")
    video_catalogue_pages = []
    for page in logged_in_page:
        logger.info(80 * "-")
        logger.info(f"Navigating to Video Catalogues page on {get_browser_name(page)}")
        logger.info(80 * "-")
    
    # Navigate to Video Catalogues page
        page.get_by_role("link", name="Video Catalogues").click()
        
    # Create the page object
        video_catalogue_page = VideoCataloguesPage(page)
        
    # Verify that we're on the Video Catalogues page
        if video_catalogue_page.verify_page_title_present():
            logger.info("Successfully navigated to Video Catalogues page")
            video_catalogue_pages.append(video_catalogue_page)
        else:
            logger.error(f"Failed to navigate to Video Catalogues page on {get_browser_name(page)}")
            
    logger.info(f"video_catalogue_page fixture: yielding {len(video_catalogue_pages)} video catalogue page(s)")
    yield video_catalogue_pages
    logger.debug("video_catalogue_page fixture: finished")