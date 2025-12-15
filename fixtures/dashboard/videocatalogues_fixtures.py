#videocatalogues_fixtures.py (Fixture)
import os
import pytest
import requests
import uuid
from conftest import (
    verify_delete_endpoint_works,
    create_test_record_payload,
    TEST_ENTITY_CONFIGURATIONS,
    api_token
)
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Any
from utilities.config import PAGE_SIZE
from utilities.utils import logger, get_browser_name
from utilities.auth import get_auth_headers
from page_objects.dashboard.video_catalogues_page import VideoCataloguesPage

# Load environment variables from .env file
load_dotenv()

# Get API credentials and endpoints from environment variables
api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
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
    
@pytest.fixture(scope="function")
def video_catalogue_pagination_test_data(request):
    """
    Fixture that creates enough video catalogue records to test pagination on the Video Catalogues page.

    Returns:
        List[str]: List of video catalogue IDs created for the test
    """
    logger.debug("Starting video_catalogue_pagination_test_data fixture")

    # Determine the number of records to create based on the PAGE_SIZE
    min_records_needed = PAGE_SIZE + 2
    
    # List to track created video catalogue IDs for cleanup
    video_catalogue_ids = []
    
    # Header for API calls with dynamic token
    headers = get_auth_headers()
    
    # Create test video catalogues
    logger.info(f"\n=== Creating {min_records_needed} test video catalogues ===")

    for i in range(min_records_needed):
        record_id, payload = create_test_record_payload("video_catalogues", f"_BULK_{i}")

        try:
            config = TEST_ENTITY_CONFIGURATIONS["video_catalogues"]
            response = requests.put(config["create_endpoint"], json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                video_catalogue_ids.append(record_id)
                logger.info(f"Successfully created video catalogue with ID: {record_id}")
            else:
                logger.error(f"Failed to create video catalogue: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")

    logger.info(f"\nCreated {len(video_catalogue_ids)} test video catalogues")

    yield video_catalogue_ids

    # Cleanup
    config = TEST_ENTITY_CONFIGURATIONS["video_catalogues"]
    logger.info(f"\n=== Cleaning up {len(video_catalogue_ids)} test video catalogues ===")
    for video_catalogue_id in video_catalogue_ids:
        try:
            delete_url = config["delete_endpoint_template"].format(id=video_catalogue_id)
            delete_response = requests.delete(delete_url, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                logger.info(f"Deleted video catalogue ID: {video_catalogue_id}")
            else:
                logger.error(f"Failed to delete video catalogue ID {video_catalogue_id}: {delete_response.status_code}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")

@pytest.fixture(scope="function")
def video_catalogue_conditional_pagination_data(video_catalogue_page):
    """
    Fixture that conditionally creates test data for pagination testing.
    
    Logic:
    1. Check how many video catalogues currently exist
    2. If insufficient for pagination, create test data
    3. If sufficient, return empty list and skip flag
    
    Returns:
        Tuple[List[str], bool]: (installation_ids, data_was_created)
            - installation_ids: List of created installation IDs (empty if none created)
            - data_was_created: Boolean indicating if test data was created
    """
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Always verify delete endpoint and cleanup first
    verify_delete_endpoint_works("video_catalogues", headers, logger)

    logger.info("=== Checking existing video catalogue count for pagination test ===")

    min_records_for_pagination = PAGE_SIZE + 2

    # Check current video catalogue count
    first_page = video_catalogue_page[0] if video_catalogue_page else None
    if not first_page:
        logger.error("No video catalogues page object available")
        return [], False
    
    try:
        first_page.page.reload()
        first_page.page.wait_for_load_state("networkidle")
        counts = first_page.get_pagination_counts()
        
        if counts:
            current_start, current_end, total_records = counts
            logger.info(f"Current video catalogue count: {total_records}")
            logger.info(f"Minimum records needed: {min_records_for_pagination}")
            
            if total_records >= min_records_for_pagination:
                logger.info("Sufficient video catalogues exist for pagination test")
                return [], False
        else:
            logger.warning("Failed to get pagination counts - will create test data")

    except Exception as e:
        logger.error(f"Error checking existing data count: {str(e)} - will create test data")
    
    # Create test data
    records_to_create = min_records_for_pagination + 1
    video_catalogue_ids = []
    headers = get_auth_headers()

    logger.info(f"Creating {records_to_create} test video catalogues")

    # DEBUG: Create first record with full debugging
    if records_to_create > 0:
        record_id, payload = create_test_record_payload("video_catalogues", f"_COND_0")
        logger.info(f"DEBUG: First bulk creation payload: {payload}")
        
        try:
            config = TEST_ENTITY_CONFIGURATIONS["video_catalogues"]
            response = requests.put(config["create_endpoint"], json=payload, headers=headers)
            
            logger.info(f"DEBUG: First bulk creation response status: {response.status_code}")
            logger.info(f"DEBUG: First bulk creation response text: {response.text}")
            
            if response.status_code in [200, 201]:
                video_catalogue_ids.append(record_id)
                logger.info(f"Successfully created video catalogue with ID: {record_id}")
            else:
                logger.error(f"Failed to create video catalogue: {response.status_code}")
                logger.error(f"Response: {response.text}")
                
                # STOP HERE - don't create more if first one fails
                logger.error("Stopping bulk creation due to first record failure")
                yield video_catalogue_ids, True
                return
                
        except Exception as e:
            logger.error(f"Exception during first creation: {str(e)}")
            yield video_catalogue_ids, True
            return
    
    # If first record succeeded, create the rest (abbreviated for brevity)
    for i in range(1, records_to_create):
        record_id, payload = create_test_record_payload("video_catalogues", f"_COND_{i}")
        
        try:
            config = TEST_ENTITY_CONFIGURATIONS["video_catalogues"]
            response = requests.put(config["create_endpoint"], json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                video_catalogue_ids.append(record_id)
                logger.info(f"Successfully created video catalogue with ID: {record_id}")
            else:
                logger.error(f"Failed to create video catalogue: {response.status_code}")
                break  # Stop on first failure
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")
            break

    logger.info(f"Created {len(video_catalogue_ids)} test video catalogues for pagination")

    yield video_catalogue_ids, True
    
    # Cleanup
    config = TEST_ENTITY_CONFIGURATIONS["video_catalogues"]
    logger.info(f"\n=== Cleaning up {len(video_catalogue_ids)} test video catalogues ===")
    for video_catalogue_id in video_catalogue_ids:
        try:
            delete_url = config["delete_endpoint_template"].format(id=video_catalogue_id)
            delete_response = requests.delete(delete_url, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                logger.info(f"Deleted video catalogue ID: {video_catalogue_id}")
            else:
                logger.error(f"Failed to delete video catalogue ID {video_catalogue_id}: {delete_response.status_code}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")