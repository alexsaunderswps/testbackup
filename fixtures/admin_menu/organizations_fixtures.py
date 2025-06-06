#organizations_fixtures.py (Fixture)
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
from page_objects.admin_menu.organizations_page import OrganizationsPage

# Load environment variables from .env file
load_dotenv()

# Get API credentials and endpoints from environment variables
api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
api_token = os.getenv("API_TOKEN")
organization_id = os.getenv("TEST_ORGANIZATION_ID", "4ffbb8fe-d8b4-49d9-982d-5617856c9cce")
video_catalogue_id = os.getenv("TEST_VIDEO_CATALOGUE_ID", "b05980db-5833-43bd-23ca-08dc63b567ef")


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
        
@pytest.fixture(scope="function")
def organizations_pagination_test_data(request):
    """
    Fixture that creates enough organization records to test pagination on the Organizations page.

    This fixture generates a specified number of organization records and returns them
    as a list of dictionaries, each containing the organization name and ID.

    Args:
        request: The pytest request object

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing organization data
    """
    # Headers for API calls
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Verify delete endpoint works and cleanup orphaned records
    verify_delete_endpoint_works("organizations", headers, logger)
    
    # Proceed with bulk creation
    min_records_needed = PAGE_SIZE + 2
    organization_ids = []

    logger.info(f"\n=== Creating {min_records_needed} test organizations ===")

    for i in range(min_records_needed):
        record_id, payload = create_test_record_payload("organizations", f"_BULK_{i}")

        try:
            config = TEST_ENTITY_CONFIGURATIONS["organizations"]
            response = requests.put(config["create_endpoint"], json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                organization_ids.append(record_id)
                logger.info(f"Successfully created organization with ID: {record_id}")
            else:
                logger.error(f"Failed to create organization: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")

    logger.info(f"\nCreated {len(organization_ids)} test organizations")

    yield organization_ids

    # Cleanup
    config = TEST_ENTITY_CONFIGURATIONS["organizations"]
    logger.info(f"\n=== Cleaning up {len(organization_ids)} test organizations ===")
    for organization_id in organization_ids:
        try:
            delete_url = config["delete_endpoint_template"].format(id=organization_id)
            delete_response = requests.delete(delete_url, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                logger.info(f"Deleted organization ID: {organization_id}")
            else:
                logger.error(f"Failed to delete organization ID {organization_id}: {delete_response.status_code}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")

            
@pytest.fixture(scope="function")
def organizations_conditional_pagination_data(organizations_page):
    """
    Enhanced conditional organizations fixture with delete verification and debugging.
    """
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Always verify delete endpoint and cleanup first
    verify_delete_endpoint_works("organizations", headers, logger)

    logger.info("=== Checking existing organization count for pagination test ===")

    min_records_for_pagination = PAGE_SIZE + 2

    # Check current organization count
    first_page = organizations_page[0] if organizations_page else None
    if not first_page:
        logger.error("No organizations page object available")
        return [], False

    try:
        first_page.page.reload()
        first_page.page.wait_for_load_state("networkidle")
        counts = first_page.get_pagination_counts()
        
        if counts:
            current_start, current_end, total_records = counts
            logger.info(f"Current organization count: {total_records}")
            logger.info(f"Minimum records needed: {min_records_for_pagination}")
            
            if total_records >= min_records_for_pagination:
                logger.info("Sufficient organizations exist for pagination test")
                return [], False
        else:
            logger.warning("Failed to get pagination counts - will create test data")

    except Exception as e:
        logger.error(f"Error checking existing data count: {str(e)} - will create test data")
    
    # Create test data
    records_to_create = min_records_for_pagination + 1
    organization_ids = []

    logger.info(f"Creating {records_to_create} test organizations")

    # DEBUG: Create first record with full debugging
    if records_to_create > 0:
        record_id, payload = create_test_record_payload("organizations", f"_COND_0")
        logger.info(f"DEBUG: First bulk creation payload: {payload}")
        
        try:
            config = TEST_ENTITY_CONFIGURATIONS["organizations"]
            response = requests.put(config["create_endpoint"], json=payload, headers=headers)
            
            logger.info(f"DEBUG: First bulk creation response status: {response.status_code}")
            logger.info(f"DEBUG: First bulk creation response text: {response.text}")
            
            if response.status_code in [200, 201]:
                organization_ids.append(record_id)
                logger.info(f"Successfully created organization with ID: {record_id}")
            else:
                logger.error(f"Failed to create organization: {response.status_code}")
                logger.error(f"Response: {response.text}")
                
                # STOP HERE - don't create more if first one fails
                logger.error("Stopping bulk creation due to first record failure")
                yield organization_ids, True
                return
                
        except Exception as e:
            logger.error(f"Exception during first creation: {str(e)}")
            yield organization_ids, True
            return
    
    # If first record succeeded, create the rest (abbreviated for brevity)
    for i in range(1, records_to_create):
        record_id, payload = create_test_record_payload("organizations", f"_COND_{i}")
        
        try:
            config = TEST_ENTITY_CONFIGURATIONS["organizations"]
            response = requests.put(config["create_endpoint"], json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                organization_ids.append(record_id)
                logger.info(f"Successfully created organization with ID: {record_id}")
            else:
                logger.error(f"Failed to create organization: {response.status_code}")
                break  # Stop on first failure
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")
            break

    logger.info(f"Created {len(organization_ids)} test organizations for pagination")

    yield organization_ids, True
    
    # Cleanup
    config = TEST_ENTITY_CONFIGURATIONS["organizations"]
    logger.info(f"\n=== Cleaning up {len(organization_ids)} test organizations ===")
    for organization_id in organization_ids:
        try:
            delete_url = config["delete_endpoint_template"].format(id=organization_id)
            delete_response = requests.delete(delete_url, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                logger.info(f"Deleted organization ID: {organization_id}")
            else:
                logger.error(f"Failed to delete organization ID {organization_id}: {delete_response.status_code}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")