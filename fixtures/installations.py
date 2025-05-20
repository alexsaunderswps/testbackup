# installations.py
import os
import pytest
import requests
import uuid
from dotenv import load_dotenv
from typing import List, Dict, Any
from utilities.config import PAGE_SIZE  

# Load environment variables from .env file
load_dotenv()

# Get API credentials and endpoints from environment variables
api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
api_token = os.getenv("API_TOKEN")
organization_id = os.getenv("TEST_ORGANIZATION_ID", "4ffbb8fe-d8b4-49d9-982d-5617856c9cce")
video_catalogue_id = os.getenv("TEST_VIDEO_CATALOGUE_ID", "b05980db-5833-43bd-23ca-08dc63b567ef")

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
    print(f"\n=== Creating {min_records_needed} test installations ===")
    
    for i in range(min_records_needed):
        # Generate unique identifier
        installation_id = str(uuid.uuid4())
        unique_suffix = installation_id[:8]
        
        # Create installation payload based on the captured data
        payload = {
            "installationId": installation_id,
            "name": f"Test Installation {unique_suffix}",
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
            print(f"Creating installation: {unique_suffix}")
            
            # Use post instead of put (if needed)
            response = requests.put(installation_endpoint, json=payload, headers=headers)
            
            # Since we know our API returns empty responses on success,
            # we'll just use our generated ID if the status code indicates success
            if response.status_code in [200, 201]:
                installation_ids.append(installation_id)
                print(f"Successfully created installation with ID: {installation_id}")
            else:
                print(f"Failed to create installation: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Exception during creation: {str(e)}")
                
    # Print summary
    print(f"\nCreated {len(installation_ids)} test installations")
    
    # Yield the created installation IDs for test use
    yield installation_ids
    
    # Clean up - delete all created installations
    print(f"\n=== Cleaning up {len(installation_ids)} test installations ===")
    for installation_id in installation_ids:
        try:
            delete_endpoint = f"{api_url}/Installations/delete?id={installation_id}"
            delete_response = requests.delete(delete_endpoint, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                print(f"Deleted installation ID: {installation_id}")
            else:
                print(f"Failed to delete installation ID {installation_id}: {delete_response.status_code}")
        except Exception as e:
            print(f"Exception during deletion: {str(e)}")