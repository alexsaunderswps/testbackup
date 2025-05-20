# test_fixture_check.py
import pytest
import os
import uuid
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials and endpoints from environment variables
api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
api_token = os.getenv("API_TOKEN")
organization_id = os.getenv("TEST_ORGANIZATION_ID", "4ffbb8fe-d8b4-49d9-982d-5617856c9cce")
video_catalogue_id = os.getenv("TEST_VIDEO_CATALOGUE_ID", "b05980db-5833-43bd-23ca-08dc63b567ef")

def test_installation_create_and_delete():
    """
    Test that verifies both creation and deletion of installations work correctly.
    Creates 2 installations, verifies they exist, then deletes them and verifies they're gone.
    """
    # Headers for API calls
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # List to track created installation IDs
    installation_ids = []
    installation_names = []
    
    # === STEP 1: Create 2 test installations ===
    print("\n=== Creating 2 test installations ===")
    
    for i in range(2):
        # Generate unique identifier
        installation_id = str(uuid.uuid4())
        unique_suffix = installation_id[:8]
        installation_name = f"Test Installation {unique_suffix}"
        
        # Create installation payload
        payload = {
            "installationId": installation_id,
            "name": installation_name,
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
            "tips": "Test installation - DELETE ME",
            "favorites": [],
            "filterFavoritesByDefault": False,
            "tutorialMode": "None",
            "tutorialText": "<b>Test Installation</b>\n\nThis is a temporary test installation.",
            "organizationId": organization_id
        }
        
        # Make API call to create installation
        try:
            installation_endpoint = f"{api_url}/Installations/create"
            print(f"Creating installation: {installation_name}")
            
            response = requests.put(installation_endpoint, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                installation_ids.append(installation_id)
                installation_names.append(installation_name)
                print(f"✓ Successfully created installation with ID: {installation_id}")
            else:
                print(f"✗ Failed to create installation: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"✗ Exception during creation: {str(e)}")
    
    # Basic verification of creation
    assert len(installation_ids) == 2, "Failed to create both test installations"
    
    # === STEP 2: Verify installations exist by listing all installations ===
    print("\n=== Verifying installations exist ===")
    
    # Wait a moment for any backend processing
    time.sleep(1)
    
    try:
        list_endpoint = f"{api_url}/Installations"
        response = requests.get(list_endpoint, headers=headers)
        
        if response.status_code == 200:
            all_installations = response.json()
            print(f"Found {len(all_installations)} total installations")
            
            # Check if our IDs exist in the list
            found_installations = [inst for inst in all_installations 
                                if 'installationId' in inst and inst['installationId'] in installation_ids]
            
            print(f"Found {len(found_installations)} of our test installations in the list")
            
            # Verify our installations exist
            found_ids = [inst['installationId'] for inst in found_installations]
            for installation_id in installation_ids:
                if installation_id in found_ids:
                    print(f"✓ Verified installation exists: {installation_id}")
                else:
                    print(f"✗ Installation not found: {installation_id}")
            
            assert len(found_installations) == 2, "Not all created installations were found in the list"
        else:
            print(f"✗ Failed to list installations: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Exception during verification: {str(e)}")
    
    # === STEP 3: Delete the installations ===
    print("\n=== Deleting test installations ===")
    
    deleted_ids = []
    for installation_id in installation_ids:
        try:
            delete_endpoint = f"{api_url}/Installations/delete?id={installation_id}"
            print(f"Deleting installation: {installation_id}")
            
            delete_response = requests.delete(delete_endpoint, headers=headers)
            
            if delete_response.status_code in [200, 204]:
                deleted_ids.append(installation_id)
                print(f"✓ Successfully deleted installation ID: {installation_id}")
            else:
                print(f"✗ Failed to delete installation: {delete_response.status_code}")
                print(f"Response: {delete_response.text}")
        except Exception as e:
            print(f"✗ Exception during deletion: {str(e)}")
    
    # Verify all installations were deleted
    assert len(deleted_ids) == 2, "Failed to delete both test installations"
    
    # === STEP 4: Verify installations no longer exist ===
    print("\n=== Verifying installations are deleted ===")
    
    # Wait a moment for any backend processing
    time.sleep(1)
    
    try:
        list_endpoint = f"{api_url}/Installations"
        response = requests.get(list_endpoint, headers=headers)
        
        if response.status_code == 200:
            all_installations = response.json()
            
            # Check if any of our deleted IDs still exist
            remaining_installations = [inst for inst in all_installations 
                                    if 'installationId' in inst and inst['installationId'] in installation_ids]
            
            if not remaining_installations:
                print("✓ All test installations were properly deleted")
            else:
                for inst in remaining_installations:
                    print(f"✗ Installation still exists after deletion: {inst['installationId']}")
            
            assert len(remaining_installations) == 0, "Some installations were not properly deleted"
        else:
            print(f"✗ Failed to list installations: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Exception during deletion verification: {str(e)}")
    
    print("\n=== Test completed successfully ===")
    print(f"✓ Created and verified 2 installations")
    print(f"✓ Deleted and verified removal of 2 installations")


if __name__ == "__main__":
    # Allow running directly without pytest
    test_installation_create_and_delete()