# installations_fixtures.py (Fixture)
import os
import pytest
import requests
import uuid
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Any
from utilities.config import PAGE_SIZE
from utilities.utils import logger, get_browser_name
from page_objects.admin_menu.installations_page import InstallationsPage

# Load environment variables from .env file
load_dotenv()

# Get API credentials and endpoints from environment variables
api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
api_token = os.getenv("API_TOKEN")
organization_id = os.getenv("TEST_ORGANIZATION_ID", "4ffbb8fe-d8b4-49d9-982d-5617856c9cce")
video_catalogue_id = os.getenv("TEST_VIDEO_CATALOGUE_ID", "b05980db-5833-43bd-23ca-08dc63b567ef")

@pytest.fixture
def installations_page(logged_in_page):
    """
    Fixture that provides the Installations page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[UsersPage]: A list of InstallationsPage objects for each logged-in browser instance
    """
    logger.debug("Staring installations_page fixture")
    installation_pages = []
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Installations page on {get_browser_name(page)}")
        logger.info("=" * 80)
        
        #Navigate to Installations page
        page.get_by_role("button", name="Admin").click()
        page.get_by_role("link", name="Installations").click()
        
        # Create the page object
        installations_page = InstallationsPage(page)
        
        # Verify that we're on the Installations page
        if installations_page.verify_page_title():
            logger.info("Successfully navigated to Installations page")
            installation_pages.append(installations_page)
        else:
            logger.error(f"Failed to navigate to Installations page on {get_browser_name(page)}")
            
    logger.info(f"installations_page fixture: yielding {len(installation_pages)} installations page(s)")
    yield installation_pages
    logger.debug("installations_page fixture: finished")

@pytest.fixture(scope="function")
def installations_pagination_test_data(request):
    """
    Fixture that creates enough installation records to test pagination on the Installations page.
    
    Returns:
        List[str]: List of installation IDs created for the test
    """
    # Determine how many records we need for pagination
    min_records_needed = PAGE_SIZE + 2  # At least enough to go to page 2
    
    # List to track created installation IDs for cleanup
    installation_ids = []
    
    # Headers for API calls
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Create test installations
    logger.info(f"\n=== Creating {min_records_needed} test installations ===")
    
    for i in range(min_records_needed):
        # Generate unique identifier
        installation_id = str(uuid.uuid4())
        test_run_id = installation_id[:8]
        username = os.getenv("USER", "unknown")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        test_installation_name = f"AUTOTEST_{username}_{timestamp}_{test_run_id}"
        
        # Create installation payload based on the captured data
        payload = {
            "installationId": installation_id,
            "name": test_installation_name,
            "videoCatalogueId": video_catalogue_id,
            "forceOfflineMode": False,
            "showGraphicDeath": True,
            "showGraphicSex": True,
            "controls": "Gaze",
            "demoMode": True,
            "globeStartLat": 0,
            "globeStartLong": -10,
            "appTimerLengthSeconds": 0,
            "idleTimerLengthSeconds": 0,
            "idleTimerDelaySeconds": 0,
            "startupVideoId": None,
            "resumeStartupVideoOnAwake": False,
            "startupVideoLoop": False,
            "showMenuTray": True,
            "tips": "Test installation for pagination testing",
            "favorites": [],
            "filterFavoritesByDefault": False,
            "tutorialMode": "None",
            "tutorialText": "<b>Test Installation</b>\n\nThis is an automated test installation.",
            "organizationId": organization_id
        }
        
        # Make API call to create installation
        try:
            installation_endpoint = f"{api_url}/Installations/create"
            logger.info(f"Creating installation: {test_installation_name}")
            
            # Use post instead of put (if needed)
            response = requests.put(installation_endpoint, json=payload, headers=headers)
            
            # Since we know our API returns empty responses on success,
            # we'll just use our generated ID if the status code indicates success
            if response.status_code in [200, 201]:
                installation_ids.append(installation_id)
                logger.info(f"Successfully created installation with ID: {installation_id}")
            else:
                logger.error(f"Failed to create installation: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")
                
    # Log summary
    logger.info(f"\nCreated {len(installation_ids)} test installations")
    
    # Yield the created installation IDs for test use
    yield installation_ids
    
    # Clean up - delete all created installations
    logger.info(f"\n=== Cleaning up {len(installation_ids)} test installations ===")
    for installation_id in installation_ids:
        try:
            delete_endpoint = f"{api_url}/Installations/delete?id={installation_id}"
            delete_response = requests.delete(delete_endpoint, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                logger.info(f"Deleted installation ID: {installation_id}")
            else:
                logger.error(f"Failed to delete installation ID {installation_id}: {delete_response.status_code}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")

@pytest.fixture(scope="function")
def conditional_pagination_data(installations_page):
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
    logger.info("=== Checking existing installation count for pagination test ===")
    
    # Caluculate the minimum records needed for pagination
    min_records_for_pagination = PAGE_SIZE + 2
    
    # Check current installation count using the first page object
    first_page = installations_page[0] if installations_page else None
    if not first_page:
        logger.error("No installations page object available for checking existing installations")
        return [], False
    
    # Get current pagination info
    try:
        first_page.page.reload()
        first_page.page.wait_for_load_state("networkidle")
        counts = first_page.get_pagination_counts()
        
        if counts:
            current_start, current_end, total_records = counts
            logger.info(f"Current installation count: {total_records}")
            logger.info(f"Minimum records needed for pagination: {min_records_for_pagination}")
            
            if total_records >= min_records_for_pagination:
                logger.info("Sufficient installations exist for pagination test, skipping data creation")
                return [], False
            else:
                logger.info(f"Insufficient installations ({total_records}) for pagination test, creating {min_records_for_pagination - total_records} more")            
        else:
            logger.warning("Failed to get pagination counts - will create test data")

    except Exception as e:
        logger.error(f"Error checking exisiting data count: {str(e)} - will create test data")
        
    # Create test data
    logger.info("Creating test data for pagination")
    
    # Calculate how many more records we need
    records_to_create = min_records_for_pagination + 1  # Ensure we create enough to go to at least page 2
    
    # Reuse the existing pagination test data creation logic
    installastions_ids = []
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    logger.info(f"Creating {records_to_create} test installations")
    
    for i in range(records_to_create):
        installation_id = str(uuid.uuid4())
        test_run_id = installation_id[:8]
        username = os.getenv("USER", "unknown")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        test_installation_name = f"AUTOTEST_{username}_{timestamp}_{test_run_id}"
        
        payload = {
            "installationId": installation_id,
            "name": test_installation_name,
            "videoCatalogueId": video_catalogue_id,
            "forceOfflineMode": False,
            "showGraphicDeath": True,
            "showGraphicSex": True,
            "controls": "Gaze",
            "demoMode": True,
            "globeStartLat": 0,
            "globeStartLong": -10,
            "appTimerLengthSeconds": 0,
            "idleTimerLengthSeconds": 0,
            "idleTimerDelaySeconds": 0,
            "startupVideoId": None,
            "resumeStartupVideoOnAwake": False,
            "startupVideoLoop": False,
            "showMenuTray": True,
            "tips": "Test installation for pagination testing",
            "favorites": [],
            "filterFavoritesByDefault": False,
            "tutorialMode": "None",
            "tutorialText": "<b>Test Installation</b>\n\nThis is an automated test installation.",
            "organizationId": organization_id
        }
        
        try:
            installation_endpoint = f"{api_url}/Installations/create"
            logger.info(f"Creating installation: {test_installation_name}")
            response = requests.put(installation_endpoint, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                installastions_ids.append(installation_id)
                logger.info(f"Successfully created installation with ID: {installation_id}")
            else:
                logger.error(f"Failed to create installation: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")
    
    logger.info(f"Created {len(installastions_ids)} test installations for pagination")
    
    # Yield the created installation IDs and indicate that data was created
    yield installastions_ids, True
    
    # Cleanup - delete all created installations
    logger.info(f"\n=== Cleaning up {len(installastions_ids)} test installations ===")
    for installation_id in installastions_ids:
        try:
            delete_endpoint = f"{api_url}/Installations/delete?id={installation_id}"
            delete_response = requests.delete(delete_endpoint, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                logger.info(f"Deleted installation ID: {installation_id}")
            else:
                logger.error(f"Failed to delete installation ID {installation_id}: {delete_response.status_code}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")