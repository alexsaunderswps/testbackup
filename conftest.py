# conftest.py (Playwright version)
import os
import pytest
import requests
import time
import uuid
import platform
import pytest
from datetime import datetime
from dotenv import load_dotenv
# from fixtures.admin_menu.installations_fixtures import installations_pagination_test_data
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from typing import Dict, List, Tuple, Generator, Any
from utilities.utils import logger, start_test_capture, end_test_capture, get_browser_name

# Load and define enviromnetal variables
load_dotenv()
SYS_ADMIN_USER = os.getenv("SYS_ADMIN_USERNAME")
SYS_ADMIN_PASS = os.getenv("SYS_ADMIN_PASSWORD")
ORG_WPS_USER = os.getenv("ORG_ADMIN_WPS_USERNAME")
ORG_WPS_PASS = os.getenv("ORG_ADMIN_WPS_PASSWORD")
ORG_BP_USER = os.getenv("ORG_ADMIN_BP_USERNAME")
ORG_BP_PASS = os.getenv("ORG_ADMIN_BP_PASSWORD")
ORG_DTA_USER = os.getenv("ORG_ADMIN_DTA_USERNAME")
ORG_DTA_PASS = os.getenv("ORG_ADMIN_DTA_PASSWORD")
QA_LOGIN_URL = os.getenv("QA_LOGIN_URL").replace("\\x3a", ":")

api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
api_token = os.getenv("API_TOKEN")
organization_id = os.getenv("TEST_ORGANIZATION_ID", "4ffbb8fe-d8b4-49d9-982d-5617856c9cce")
video_catalogue_id = os.getenv("TEST_VIDEO_CATALOGUE_ID", "b05980db-5833-43bd-23ca-08dc63b567ef")

# Define pytest addoption for Command Line runnig of Pytest with options
def pytest_addoption(parser):
    """
    Add custom command line options to pytest.
    
    This function is called by pytest to add custom options to the command line parser.
    It defines options for browser selection, headless mode, and login credentials.
    
    Args:
        parser (argparse.Parser): The pytest command line parser.
        
    Example:
        pytest --browser fireforx --headless False
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Specify the browser to use: chromium, firefox, webkit, or all. Default is chromium."        
    )
    parser.addoption(
        "--headless",
        action="store",
        default=True,
        help="Run tests in headsless mode (True or False). Default is True." 
    )
    parser.addoption(
        "--username",
        action="store",
        default=SYS_ADMIN_USER,
        help="Username for login. Default is the ADMIN_USER value from .env file."
    )
    parser.addoption(
        "--password",
        action="store",
        default=SYS_ADMIN_PASS,
        help="Password for login. Default is the ADMIN_PASS value from .env file."
    )
    
@pytest.fixture(scope="session")
def playwright():
    """
    Fixture providing the Playwright instance.
    """
    with sync_playwright() as playwright:
        yield playwright
        
def get_browser_instance(playwright, browser_name: str, headless: bool) -> Browser:
    """
    Get a browser instance based on the specified browser name and options.
    
    Args:
        playwright (sync_playwright): The Playwright instance.
        browser_name (str): The name of the browser to use (chromium, firefox, webkit).
        headless (bool): Whether to run the browser in headless mode.
        
    Returns:
        Browser: The browser instance.
    """
    logger.info(f"Launching {browser_name} browser in {'headless' if headless else 'non-headless'} mode.")
    
    # Convert headless to boolean
    if isinstance(headless, str):
        headless = headless.lower() == "true"
    
    if browser_name.lower() == "chromium":
        return playwright.chromium.launch(headless=headless)
    elif browser_name.lower() == "firefox":
        return playwright.firefox.launch(headless=headless)
    elif browser_name.lower() == "webkit":
        return playwright.webkit.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser {browser_name}. Supported browsers are: chromium, firefox, webkit.")

@pytest.fixture(scope="function")
def browser_context_and_page(playwright, request):
    """
    Fixture that provides a browser, context, and page for each test.
    
    Args:
        playwright: The Playwright instance.
        request: The pytest request object.
    
    Yields:
    tuple: A tuple containing the browser, context, and page.
    """
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    # Handle 'all' browser option
    if browser_name.lower() == "all":
        browser_contexts =[]
        for browser_type in ["chromium", "firefox", "webkit"]:
            browser = get_browser_instance(playwright, browser_type, headless)
            context = browser.new_context()
            page = context.new_page()
            start_test_capture(f"{page.browser.browser_type.name}_{request.node.name}")
            browser_contexts.append((browser, context, page))
            
        yield browser_contexts
        
        # Teardown
        
        for browser, context, page in browser_contexts:
            end_test_capture(f"{page.browser.browser_type.name}_{request.node.name}")
            context.close()
            browser.close()
    
    else:
        # Single browser setup
        browser = get_browser_instance(playwright, browser_name, headless)
        context = browser.new_context()
        page = context.new_page()
        
        start_test_capture(f"{browser_name}_{request.node.name}")
        yield [(browser, context, page)]
        
        # Teardown
        end_test_capture(f"{browser_name}_{request.node.name}")
        context.close()
        browser.close()

@pytest.fixture
def logged_in_page(browser_context_and_page, request):
    """
    Fixture that provides a logged-in page(s) for tests that require pre-authentication.

    Args:
        browser_context_and_page: A fixture providing brower, context, and page.
        request: The pytest request object.
        
    Yields:
    List[Page]: A list of logged-in pages.
    """
    logger.info("Starting logged_in_page fixture.")
    logged_in_pages = []
    
    username = request.config.getoption("--username", default=SYS_ADMIN_USER)
    password = request.config.getoption("--password", default=SYS_ADMIN_PASS)
    
    for browser, context, page in browser_context_and_page:
        logger.info("="* 80)
        logger.info(f"Logging in on {browser.browser_type.name}")
        logger.info("=" * 80)
        
        # Navigate to the login page
        page.goto(QA_LOGIN_URL)
        
        # Login process
        page.get_by_role("textbox", name="Username").fill(username)
        page.get_by_role("textbox", name="Password").fill(password)
        page.get_by_role("button", name="Log In").click()
        
        # Wait for login to complete - adjust the selector as needed
        page.get_by_role("button", name="LOG OUT").wait_for(state="visible")
        
        logged_in_pages.append(page)
        
    logger.debug(f"logged_in_page fixture: yielding {len(logged_in_pages)} logged-in page(s).")
    yield logged_in_pages
    logger.debug("logged_in_page fixture: finished.")

@pytest.fixture
def verify_ui_elements():
    """ 
    Fixture providing UI element verification functions.
    
    This fixture returns a namespace object with various verification methods
    that can be used to test UI elements across different pages.
    """
    def verify_nav_elements(pages):
        """
        Verify navigation elements on all provided pages.
        
        Args:
            pages (List[Page]): A list of Playwright Page objects.
            
        Returns:
            List of tuples (page, all_elements_present, missing_elements)
        """
        results = []
        for page in pages:
            logger.info(f"Verifying navigation elements on {get_browser_name(page)}")
            all_elements, missing = page.verify_all_nav_elements_present()
            results.append((page, all_elements, missing))
        return results
    
    def verify_admin_elements(pages):
        """
        Verify admin elements on all provided pages.
        
        Args:
            pages (List[Page]): A list of Playwright Page objects.
            
        Returns:
            List of tuples (page, all_elements_present, missing_elements)
        """
        results = []
        for page in pages:
            logger.info(f"Verifying admin elements on {get_browser_name(page)}")
            all_elements, missing = page.verify_all_admin_elements_present()
            results.append((page, all_elements, missing))
        return results
    
    def verify_definition_elements(pages):
        """
        Verify definition elements on all provided pages.
        
        Args:
            pages (List[Page]): A list of Playwright Page objects.
            
        Returns:
            List of tuples (page, all_elements_present, missing_elements)
        """
        results = []
        for page in pages:
            logger.info(f"Verifying definition elements on {get_browser_name(page)}")
            all_elements, missing = page.verify_all_definition_elements_present()
            results.append((page, all_elements, missing))
        return results
    
    def verify_pagination_elements(pages):
        """
        Verify pagination elements on all provided pages.
        
        Args:
            pages (List[Page]): A list of Playwright Page objects.
            
        Returns:
            List of tuples (page, all_elements_present, missing_elements)
        """
        results = []
        for page in pages:
            logger.info(f"Verifying pagination elements on {get_browser_name(page)}")
            all_elements, missing = page.verify_all_pagination_elements_present()
            results.append((page, all_elements, missing))
        return results
    
    # Return a namespace object with the verification methods
    return type('UI_Verification', (), {
        'nav_elements': verify_nav_elements,
        'admin_elements': verify_admin_elements,
        'definition_elements': verify_definition_elements,
        'pagination_elements': verify_pagination_elements
    })

# =========================================================    
# ENDPOINT CONFIGURATIONS FOR DELETE VERIFICATION
# =========================================================

def get_current_username():
    """
    Get the current username for test record naming.
    Uses SYS_ADMIN_USER from environment variables for consistency.
    """
    # Use the same username that's used for login to maintain consistency
    username = SYS_ADMIN_USER
    if username:
        # Clean up email format if needed (remove @domain.com part)
        if '@' in username:
            username = username.split('@')[0]
        return username
    
    # Fallback if SYS_ADMIN_USER is not set
    return "autotest_user"


TEST_ENTITY_CONFIGURATIONS = {
    "installations": {
        "create_endpoint": f"{api_url}/Installations/create",
        "delete_endpoint_template": f"{api_url}/Installations/delete?id={{id}}",
        "list_endpoint": f"{api_url}/Installations",  # For cleanup search
        "entity_name": "installation",
        "id_field": "installationId",
        "name_field": "name",
        "payload_template": {
            "installationId": "",  # Will be filled
            "name": "",  # Will be filled
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
            "tips": "",  # Will be filled
            "favorites": [],
            "filterFavoritesByDefault": False,
            "tutorialMode": "None",
            "tutorialText": "",  # Will be filled
            "organizationId": organization_id
        }
    },
    "video_catalogues": {
        "create_endpoint": f"{api_url}/videoCatalogue/create",
        "delete_endpoint_template": f"{api_url}/videoCatalogue/delete?id={{id}}",
        "list_endpoint": f"{api_url}/videoCatalogue",  # For cleanup search
        "entity_name": "video catalogue",
        "id_field": "videoCatalogueId",
        "name_field": "name",
        "payload_template": {
            "description": "",  # Will be filled
            "lastEditedDate": "",  # Will be filled
            "mapMarkers": [],
            "name": "",  # Will be filled
            "organizationId": organization_id,
            "videoCatalogueId": "",  # Will be filled
            "videos": []
        }
    },
    "organizations": {
        "create_endpoint": f"{api_url}/Organization/Create",
        "delete_endpoint_template": f"{api_url}/Organization/Delete?id={{id}}",
        "list_endpoint": f"{api_url}/Organizations",  # For cleanup search
        "entity_name": "organization",
        "id_field": "organizationId",
        "name_field": "name",
        "payload_template": {
            "name": "",  # Will be filled
            "organizationId": "",  # Will be filled
        }
    }
    # Add more entity types as needed
}

# =========================================================
# ORPHANED RECORD CLEANUP FUNCTION
# =========================================================

def cleanup_orphaned_test_records(entity_type, headers, logger):
    """
    Search for and delete orphaned test records with AUTOTEST prefix.
    
    Args:
        entity_type (str): Key from TEST_ENTITY_CONFIGURATIONS
        headers (dict): Headers for API requests
        logger: Logger instance
    """
    if entity_type not in TEST_ENTITY_CONFIGURATIONS:
        logger.warning(f"Unknown entity type for cleanup: {entity_type}")
        return
    
    config = TEST_ENTITY_CONFIGURATIONS[entity_type]
    entity_name = config["entity_name"]
    
    logger.info(f"\n=== Cleaning up orphaned AUTOTEST {entity_name} records ===")
    
    try:
        # Get list of existing records
        list_response = requests.get(config["list_endpoint"], headers=headers)
        
        if list_response.status_code != 200:
            logger.warning(f"Could not fetch {entity_name} list for cleanup: {list_response.status_code}")
            return
        
        records = list_response.json()
        if not records:
            logger.info(f"No {entity_name} records found for cleanup")
            return
        
        # Filter for AUTOTEST records
        orphaned_records = []
        name_field = config["name_field"]
        id_field = config["id_field"]
        
        for record in records:
            if isinstance(record, dict) and name_field in record:
                if record[name_field] and record[name_field].startswith("AUTOTEST_"):
                    orphaned_records.append({
                        "id": record.get(id_field),
                        "name": record.get(name_field)
                    })
        
        if not orphaned_records:
            logger.info(f"No orphaned AUTOTEST {entity_name} records found")
            return
        
        logger.info(f"Found {len(orphaned_records)} orphaned AUTOTEST {entity_name} records")
        
        # Delete orphaned records
        deleted_count = 0
        for record in orphaned_records:
            try:
                delete_url = config["delete_endpoint_template"].format(id=record["id"])
                delete_response = requests.delete(delete_url, headers=headers)
                
                if delete_response.status_code in [200, 204]:
                    logger.info(f"Cleaned up orphaned {entity_name}: {record['name']} (ID: {record['id']})")
                    deleted_count += 1
                else:
                    logger.warning(f"Failed to cleanup {entity_name} {record['id']}: {delete_response.status_code}")
            except Exception as e:
                logger.error(f"Exception cleaning up {entity_name} {record['id']}: {str(e)}")
        
        logger.info(f"Successfully cleaned up {deleted_count}/{len(orphaned_records)} orphaned {entity_name} records")
        
    except Exception as e:
        logger.error(f"Error during orphaned {entity_name} cleanup: {str(e)}")


# =============================================================================
# ENHANCED DELETE ENDPOINT VERIFICATION
# =============================================================================

def verify_delete_endpoint_works(entity_type, headers, logger, cleanup_orphaned=True):
    """
    Enhanced function to verify delete endpoint works and optionally cleanup orphaned records.
    
    Args:
        entity_type (str): Key from TEST_ENTITY_CONFIGURATIONS
        headers (dict): Headers for API requests  
        logger: Logger instance
        cleanup_orphaned (bool): Whether to cleanup orphaned records first
        
    Raises:
        pytest.fail: If delete endpoint verification fails
    """
    if entity_type not in TEST_ENTITY_CONFIGURATIONS:
        pytest.fail(f"Unknown entity type: {entity_type}")
    
    config = TEST_ENTITY_CONFIGURATIONS[entity_type]
    entity_name = config["entity_name"]
    
    # Step 1: Cleanup orphaned records from previous failed runs
    if cleanup_orphaned:
        cleanup_orphaned_test_records(entity_type, headers, logger)
    
    # Step 2: Verify delete endpoint works
    logger.info(f"\n=== Verifying delete endpoint for {entity_name} ===")
    
    # Generate test record
    test_id = str(uuid.uuid4())
    test_run_id = test_id[:8]
    username = get_current_username()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create payload for test record
    payload = config["payload_template"].copy()
    
    # Fill in test-specific values based on entity type
    if entity_type == "installations":
        payload["installationId"] = test_id
        payload["name"] = f"DELETE_TEST_{username}_{timestamp}_{test_run_id}"
        payload["tips"] = "Test record for delete endpoint verification"
        payload["tutorialText"] = "<b>Delete Test</b>\n\nThis record verifies delete endpoint works."
    elif entity_type == "video_catalogues":
        payload["videoCatalogueId"] = test_id
        payload["name"] = f"DELETE_TEST_{username}_{timestamp}_{test_run_id}"
        payload["description"] = f"Test {entity_name} for delete endpoint verification"
        payload["lastEditedDate"] = datetime.now().isoformat() + 'Z'
    elif entity_type == "organizations":
        payload["organizationId"] = test_id
        payload["name"] = f"DELETE_TEST_{username}_{timestamp}_{test_run_id}"
    
    test_record_created = False
    
    try:
        # Create test record
        logger.info(f"Creating test {entity_name} for delete verification: {test_id}")
        
        create_response = requests.put(
            config["create_endpoint"], 
            json=payload, 
            headers=headers
        )
        
        if create_response.status_code not in [200, 201]:
            pytest.fail(
                f"Cannot verify delete endpoint - failed to create test {entity_name}: "
                f"{create_response.status_code} - {create_response.text}"
            )
        
        test_record_created = True
        logger.info(f"✓ Test {entity_name} created successfully: {test_id}")
        
        # Test delete endpoint
        delete_url = config["delete_endpoint_template"].format(id=test_id)
        logger.info(f"Testing delete endpoint: {delete_url}")
        
        delete_response = requests.delete(delete_url, headers=headers)
        
        if delete_response.status_code not in [200, 204]:
            # Delete failed - we have an orphaned record
            logger.error(f"❌ Delete endpoint failed for {entity_name}")
            logger.error(f"ORPHANED RECORD ALERT: {entity_name} ID {test_id} created but could not be deleted")
            logger.error(f"Manual cleanup required for: {payload.get('name', test_id)}")
            
            pytest.fail(
                f"Delete endpoint verification failed for {entity_name}. "
                f"Status: {delete_response.status_code} - {delete_response.text}. "
                f"ORPHANED RECORD: {test_id} requires manual cleanup. "
                f"Cannot proceed with bulk data creation."
            )
        
        logger.info(f"✓ Delete endpoint verification successful for {entity_name}")
        test_record_created = False  # Successfully cleaned up
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error during delete endpoint verification for {entity_name}: {str(e)}"
        if test_record_created:
            error_msg += f" ORPHANED RECORD: {test_id} may require manual cleanup."
        logger.error(error_msg)
        pytest.fail(error_msg)
        
    except Exception as e:
        error_msg = f"Unexpected error during delete endpoint verification for {entity_name}: {str(e)}"
        if test_record_created:
            error_msg += f" ORPHANED RECORD: {test_id} may require manual cleanup."
        logger.error(error_msg)
        pytest.fail(error_msg)


# =============================================================================
# HELPER FUNCTION FOR CONSISTENT TEST RECORD CREATION
# =============================================================================

def create_test_record_payload(entity_type, suffix=""):
    """
    Create a standardized test record payload for any entity type.
    
    Args:
        entity_type (str): Key from TEST_ENTITY_CONFIGURATIONS
        suffix (str): Optional suffix for the test name
        
    Returns:
        tuple: (record_id, payload_dict)
    """
    if entity_type not in TEST_ENTITY_CONFIGURATIONS:
        raise ValueError(f"Unknown entity type: {entity_type}")
    
    config = TEST_ENTITY_CONFIGURATIONS[entity_type]
    
    # Generate unique identifier
    record_id = str(uuid.uuid4())
    test_run_id = record_id[:8]
    username = get_current_username()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    test_name = f"AUTOTEST_{username}_{timestamp}_{test_run_id}{suffix}"
    
    # Create payload
    payload = config["payload_template"].copy()
    
    if entity_type == "installations":
        payload["installationId"] = record_id
        payload["name"] = test_name
        payload["tips"] = "Test installation for pagination testing"
        payload["tutorialText"] = "<b>Test Installation</b>\n\nThis is an automated test installation."
    elif entity_type == "video_catalogues":
        payload["videoCatalogueId"] = record_id
        payload["name"] = test_name
        payload["description"] = f"Test video catalogue {record_id}"
        payload["lastEditedDate"] = datetime.now().isoformat() + 'Z'
    elif entity_type == "organizations":
        payload["organizationId"] = record_id
        payload["name"] = test_name
    
    return record_id, payload
