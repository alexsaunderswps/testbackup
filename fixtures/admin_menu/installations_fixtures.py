# installations_fixtures.py (Fixture)
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
    Enhanced fixture that creates enough installation records to test pagination on the Installations page.
    Includes delete endpoint verification and orphaned record cleanup.
    
    Returns:
        List[str]: List of installation IDs created for the test
    """
    # Headers for API calls
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Verify delete endpoint works and cleanup orphaned records
    verify_delete_endpoint_works("installations", headers, logger)
    
    # Proceed with bulk creation
    min_records_needed = PAGE_SIZE + 2
    installation_ids = []
    
    logger.info(f"\n=== Creating {min_records_needed} test installations ===")
    
    for i in range(min_records_needed):
        record_id, payload = create_test_record_payload("installations", f"_BULK_{i}")
        
        try:
            config = TEST_ENTITY_CONFIGURATIONS["installations"]
            response = requests.put(config["create_endpoint"], json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                installation_ids.append(record_id)
                logger.info(f"Successfully created installation with ID: {record_id}")
            else:
                logger.error(f"Failed to create installation: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")
    
    logger.info(f"\nCreated {len(installation_ids)} test installations")
    
    yield installation_ids
    
    # Cleanup
    config = TEST_ENTITY_CONFIGURATIONS["installations"]
    logger.info(f"\n=== Cleaning up {len(installation_ids)} test installations ===")
    for installation_id in installation_ids:
        try:
            delete_url = config["delete_endpoint_template"].format(id=installation_id)
            delete_response = requests.delete(delete_url, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                logger.info(f"Deleted installation ID: {installation_id}")
            else:
                logger.error(f"Failed to delete installation ID {installation_id}: {delete_response.status_code}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")
            
@pytest.fixture(scope="function")
def installations_conditional_pagination_data(installations_page):
    """
    Enhanced conditional installations fixture with delete verification and debugging.
    """
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Always verify delete endpoint and cleanup first
    verify_delete_endpoint_works("installations", headers, logger)
    
    logger.info("=== Checking existing installation count for pagination test ===")
    
    min_records_for_pagination = PAGE_SIZE + 2
    
    # Check current installation count
    first_page = installations_page[0] if installations_page else None
    if not first_page:
        logger.error("No installations page object available")
        return [], False
    
    try:
        first_page.page.reload()
        first_page.page.wait_for_load_state("networkidle")
        counts = first_page.get_pagination_counts()
        
        if counts:
            current_start, current_end, total_records = counts
            logger.info(f"Current installation count: {total_records}")
            logger.info(f"Minimum records needed: {min_records_for_pagination}")
            
            if total_records >= min_records_for_pagination:
                logger.info("Sufficient installations exist for pagination test")
                return [], False
        else:
            logger.warning("Failed to get pagination counts - will create test data")

    except Exception as e:
        logger.error(f"Error checking existing data count: {str(e)} - will create test data")
    
    # Create test data
    records_to_create = min_records_for_pagination + 1
    installation_ids = []
    
    logger.info(f"Creating {records_to_create} test installations")
    
    # DEBUG: Create first record with full debugging
    if records_to_create > 0:
        record_id, payload = create_test_record_payload("installations", f"_COND_0")
        logger.info(f"DEBUG: First bulk creation payload: {payload}")
        
        try:
            config = TEST_ENTITY_CONFIGURATIONS["installations"]
            response = requests.put(config["create_endpoint"], json=payload, headers=headers)
            
            logger.info(f"DEBUG: First bulk creation response status: {response.status_code}")
            logger.info(f"DEBUG: First bulk creation response text: {response.text}")
            
            if response.status_code in [200, 201]:
                installation_ids.append(record_id)
                logger.info(f"Successfully created installation with ID: {record_id}")
            else:
                logger.error(f"Failed to create installation: {response.status_code}")
                logger.error(f"Response: {response.text}")
                
                # STOP HERE - don't create more if first one fails
                logger.error("Stopping bulk creation due to first record failure")
                yield installation_ids, True
                return
                
        except Exception as e:
            logger.error(f"Exception during first creation: {str(e)}")
            yield installation_ids, True
            return
    
    # If first record succeeded, create the rest (abbreviated for brevity)
    for i in range(1, records_to_create):
        record_id, payload = create_test_record_payload("installations", f"_COND_{i}")
        
        try:
            config = TEST_ENTITY_CONFIGURATIONS["installations"]
            response = requests.put(config["create_endpoint"], json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                installation_ids.append(record_id)
                logger.info(f"Successfully created installation with ID: {record_id}")
            else:
                logger.error(f"Failed to create installation: {response.status_code}")
                break  # Stop on first failure
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")
            break
    
    logger.info(f"Created {len(installation_ids)} test installations for pagination")
    
    yield installation_ids, True
    
    # Cleanup
    config = TEST_ENTITY_CONFIGURATIONS["installations"]
    logger.info(f"\n=== Cleaning up {len(installation_ids)} test installations ===")
    for installation_id in installation_ids:
        try:
            delete_url = config["delete_endpoint_template"].format(id=installation_id)
            delete_response = requests.delete(delete_url, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                logger.info(f"Deleted installation ID: {installation_id}")
            else:
                logger.error(f"Failed to delete installation ID {installation_id}: {delete_response.status_code}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")