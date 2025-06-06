#organizations_fixtures.py (Fixture)
import os
import pytest
import requests
import uuid
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
    # Determine how many records we need for pagination
    min_records_needed = PAGE_SIZE + 2 # At least enough to go to page 2
    
    # List to track created organization data for cleanup
    organization_ids = []
    
    # Headers for API calls
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Create test organizations
    logger.info(f"\n=== Creating {min_records_needed} test organizations ===")
    
    for i in range(min_records_needed):
        # Generate unique identifier for the organization
        organization_id = str(uuid.uuid4())
        test_run_id = organization_id[:8]
        username = os.getenv("USER", "unknown")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        test_organization_name = f"AUTOTEST_{username}_{timestamp}_{test_run_id}"
        
        # Create organization payload
        payload ={
            "name": test_organization_name,
            "organizationId": organization_id,
        }
        
        # Make the API call to create organizations
        try:
            organization_endpoint = f"{api_url}/Organization/Create"
            logger.info(f"Creating organization: {test_organization_name}")

            # Use put method for creating organizations
            response = requests.put(organization_endpoint, json=payload, headers=headers)
            
            # Since we know our API returns empty responses on success,
            # we'll just use our generated ID if the status code indicates success
            if response.status_code in [200,201]:
                organization_ids.append(organization_id)
                logger.info(f"Successfully created organization with ID: {organization_id}")
            else:
                logger.error(f"Failed to create organization {test_organization_name}: {response.status_code} - {response.text}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"Exception during creation: {str(e)}")
            
    # Log summary
    logger.info(f"\nCreated {len(organization_ids)} test organizations for pagination testing")
    
    # Yield the created organization IDs for test use
    yield organization_ids
    
    # Clean up - delete all created organizations
    logger.info(f"\n=== Cleaning up {len(organization_ids)}created organizations ===")
    for organization_id in organization_ids:
        try:
            delete_endpoint = f"{api_url}/organization/delete?id={organization_id}"
            delete_response = requests.delete(delete_endpoint, headers=headers)

            if delete_response.status_code in [200, 204]:
                logger.info(f"Successfully deleted organization with ID: {organization_id}")
            else:
                logger.error(f"Failed to delete organization {organization_id}: {delete_response.status_code} - {delete_response.text}")
        except Exception as e:
            logger.error(f"Exception during deletion: {str(e)}")