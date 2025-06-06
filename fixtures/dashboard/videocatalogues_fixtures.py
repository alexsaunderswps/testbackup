#videocatalogues_fixtures.py (Fixture)
import os
import pytest
import requests
import uuid
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Any
from utilities.config import PAGE_SIZE
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
    
    # List to tracj created video catalogue IDs for cleanup
    video_catalogue_ids = []
    
    # Header for API calls
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Create test video catalogues
    logger.info(f"\n=== Creating {min_records_needed} test video catalogues ===")
    
    for i in range(min_records_needed):
        # Generate a unique ID for the video catalogue
        video_catalogue_id = str(uuid.uuid4())
        test_run_id = video_catalogue_id[:8]
        username = os.getenv("USER", "unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        test_video_catalogue_name = f"AUTOTEST_{username}_{timestamp}_{test_run_id}"
        
        # Create video catalogue payload
        payload = {
            "description": f"Test Video Catalogue {i + 1} created by {username}",
            "lastEditedDate": datetime.now(datetime.timezone.utc).isoformat() + 'Z',
            "mapMarkers": [],
            "name": test_video_catalogue_name,
            "organizationId": organization_id,
            "videoCatalogueId": video_catalogue_id,
            "videos": []
        }

        # Make API call to create the video catalogue
        try:
            video_catalogue_endpoint = f"{api_url}/videoCatalogue/create"
            logger.info(f"Creating video catalogue: {test_video_catalogue_name} with ID: {video_catalogue_id}")
            
            # Use put (we don't use post)
            response = requests.put(video_catalogue_endpoint, json=payload, headers=headers)
            
            # Since we know our API returns empty responses on success,
            # We'll just use our generated ID if the status code indicates success
            if response.status_code in [200, 201]:
                video_catalogue_ids.append(video_catalogue_id)
                logger.info(f"Successfully created video catalogue: {test_video_catalogue_name} with ID: {video_catalogue_id}")
            else:
                logger.error(f"Failed to create video catalogue: {test_video_catalogue_name} with ID: {video_catalogue_id}. Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")
            
    # Log summary
    logger.info(f"\n=== Created {len(video_catalogue_ids)} test video catalogues ===")
    
    # Yield the created video catalogue IDs for the test
    yield video_catalogue_ids
    
    # Cleanup - delete all created installations
    logger.info(f"\n=== Cleaning up {len(video_catalogue_ids)} test video catalogues ===")
    for video_catalogue_id in video_catalogue_ids:
        try:
            delete_endpoint = f"{api_url}/videoCatalogue/delete?id={video_catalogue_id}"
            delete_response = requests.delete(delete_endpoint, headers=headers)

            if delete_response.status_code in [200, 201]:
                logger.info(f"Successfully deleted video catalogue with ID: {video_catalogue_id}")
            else:
                logger.error(f"Failed to delete video catalogue with ID: {video_catalogue_id}. Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")

@pytest.fixture(scope="function")
def video_catalogue_conditional_pagination_data(video_catalogue_page):
    """
    Fixture that conditionally creates test data for pagination testing.
    
    Logic:
    1. Check how many installations currently exist
    2. If insufficient for pagination, create test data
    3. If sufficient, return empty list and skip flag
    
    Returns:
        Tuple[List[str], bool]: (installation_ids, data_was_created)
            - installation_ids: List of created installation IDs (empty if none created)
            - data_was_created: Boolean indicating if test data was created
    """
    logger.info("=== Starting video_catalogue_conditional_pagination_data fixture ===")
    
    # Calculate the minimum records needed for pagination
    min_records_needed_for_pagination = PAGE_SIZE + 2
    
    # Check the current video catalogue count
    first_page = video_catalogue_page[0] if video_catalogue_page else None
    if not first_page:
        logger.error("No video catalogue page available to check current count")
        return [], False
    
    # Get current pagination info
    try:
        first_page.page.reload()
        first_page.page.wait_for_load_state("networkidle")
        counts = first_page.get_pagination_counts()
        
        if counts:
            current_start, current_end, total_records = counts
            logger.info(f"Current video catalogue count: {total_records}")
            logger.info(f"Minimum records needed for pagination: {min_records_needed_for_pagination}")

            if total_records >= min_records_needed_for_pagination:
                logger.info("Sufficient video catalogues already exist for pagination testing")
                return [], False
            else:
                logger.info(f"Insufficient video catalogues for pagination testing. Current count: {total_records}")
        else:
            logger.warning("Could not retrieve pagination counts. Assuming insufficient data.")
        
    except Exception as e:
        logger.error(f"Error checking current video catalogue count: {str(e)} - creating test data")
        
    # Create test data
    logger.info("Creating test video catalogues for pagination testing")
    
    # Calculate how many more records we need to create
    records_to_create = min_records_needed_for_pagination + 1 # +1 to ensure we exceed the minimum
    
    # Reuse the exisiting pagination test data creation logic
    video_catalogue_ids = []
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    logger.info(f"Creating {records_to_create} test video catalogues")
    for i in range(records_to_create):
        video_catalogue_id = str(uuid.uuid4())
        test_run_id = video_catalogue_id[:8]
        username = os.getenv("USER", "unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        editedDate = f"{datetime.now().isoformat() + 'Z'}"
        
        test_video_catalogue_name = f"AUTOTEST_{username}_{timestamp}_{test_run_id}"
        
        payload = {
            "description": f"Test Video Catalogue {video_catalogue_id}",
            "lastEditedDate": editedDate,
            "mapMarkers": [],
            "name": test_video_catalogue_name,
            "organizationId": organization_id,
            "videoCatalogueId": video_catalogue_id,
            "videos": []
        }

        try:
            video_catalogue_endpoint = f"{api_url}/videoCatalogue/create"
            logger.info(f"Creating video catalogue: {test_video_catalogue_name} with ID: {video_catalogue_id}")
            response = requests.put(video_catalogue_endpoint, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                video_catalogue_ids.append(video_catalogue_id)
                logger.info(f"Successfully created video catalogue: {test_video_catalogue_name} with ID: {video_catalogue_id}")
            else:
                logger.error(f"Failed to create video catalogue: {test_video_catalogue_name} with ID: {video_catalogue_id}. Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")
    
    logger.info(f"Created {len(video_catalogue_ids)} test video catalogues for pagination testing")
    
    # Yield the created video catalogue IDs and indicate that data was created
    yield video_catalogue_ids, True
    
    # Cleanup - delete all created video catalogues
    logger.info(f"\n=== Cleaning up {len(video_catalogue_ids)} test video catalogues ===")
    for video_catalogue_id in video_catalogue_ids:
        try:
            delete_endpoint = f"{api_url}/videoCatalogue/delete?id={video_catalogue_id}"
            delete_response = requests.delete(delete_endpoint, headers=headers)

            if delete_response.status_code in [200, 204]:
                logger.info(f"Successfully deleted video catalogue with ID: {video_catalogue_id}")
            else:
                logger.error(f"Failed to delete video catalogue with ID: {video_catalogue_id}. Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")