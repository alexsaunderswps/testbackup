#videos_fixtures.py (Fixture)
import os
import pytest
import requests
import uuid
from dotenv import load_dotenv
from typing import List, Dict, Any
from utilities.utils import logger, get_browser_name
from utilities.auth import get_auth_headers
from page_objects.dashboard.videos_page import VideosPage
from conftest import QA_WEB_BASE_URL

# Load environment variables from .env file
load_dotenv()

# Get API credentials and endpoints from environment variables
api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
organization_id = os.getenv("TEST_ORGANIZATION_ID", "4ffbb8fe-d8b4-49d9-982d-5617856c9cce")

@pytest.fixture
def videos_page(logged_in_page):
    """
    Fixture that provides the Videos page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[VideosPage]: A list of VideosPage objects for each logged-in browser instance
    """
    logger.debug("Starting videos_page fixture")
    video_pages = []
    for page in logged_in_page:
        logger.info(80 * "-")
        logger.info(f"Navigating to Videos page on {get_browser_name(page)}")
        logger.info(80 * "-")
    
    # Navigate to the Videos page, then explicitly wait for network idle.
    # VideoManagementPage.tsx renders a MoonLoader spinner (hiding the entire UI,
    # including the h1 "Videos") until pageLoaded is true, which only flips after
    # searchVideos() resolves. The React useEffect that fires searchVideos() runs
    # AFTER the JS bundle loads, so wait_until="networkidle" on goto() exits too
    # early (it only catches the bundle load). Calling wait_for_load_state() as a
    # separate step after goto() catches the second wave of network activity — the
    # actual searchVideos() API call initiated by useEffect. A longer timeout (60s)
    # accounts for QA environment slowness when concurrent API tests are running.
        page.goto(QA_WEB_BASE_URL + "/videos")
        page.wait_for_load_state("networkidle", timeout=60000)

    # Create the page object
        videos_page = VideosPage(page)

    # Verify that we're on the Videos page
        if videos_page.verify_page_title_present():
            logger.info("Successfully navigated to Videos page")
            video_pages.append(videos_page)
        else:
            logger.error(f"Failed to navigate to Videos page on {get_browser_name(page)}")
            
    logger.info(f"videos_page fixture: yielding {len(video_pages)} video page(s)")
    yield video_pages
    logger.debug("videos_page fixture: finished")