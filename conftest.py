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
from utilities.config import PAGE_SIZE

# Load and define environmental variables
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
QA_WEB_BASE_URL = QA_LOGIN_URL.replace("/login", "")  # e.g. https://wildxr-web-qa.azurewebsites.net

api_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
api_token = os.getenv("API_TOKEN")
organization_id = os.getenv("TEST_ORGANIZATION_ID", "4ffbb8fe-d8b4-49d9-982d-5617856c9cce")
video_catalogue_id = os.getenv("TEST_VIDEO_CATALOGUE_ID", "b05980db-5833-43bd-23ca-08dc63b567ef")

# Define pytest addoption for Command Line running of Pytest with options
def pytest_addoption(parser):
    """
    Add custom command line options to pytest.
    
    This function is called by pytest to add custom options to the command line parser.
    It defines options for browser selection, headless mode, and login credentials.
    
    Args:
        parser (argparse.Parser): The pytest command line parser.
        
    Example:
        pytest --browser firefox --headless False
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
        help="Run tests in headless mode (True or False). Default is True." 
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

@pytest.fixture(scope="session")
def browser_instances(playwright, request) -> Dict[str, Browser]: # type: ignore
    """
    Fixture that provides browser instances based on command line options.
    
    Args:
        playwright: The Playwright instance.
        request: The pytest request object.
        
    Returns:
        Dict[str, Browser]: A dictionary of browser instances.
    """
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    #Convert headless to boolean if needed
    if isinstance(headless, str):
        headless = headless.lower() == "true"
    
    browsers = {}
    
    if browser_name.lower() == "all":
        browser_types = ["chromium", "firefox", "webkit"]
    else:
        browser_types = [browser_name.lower()]
    
    # Launch each browser once
    for browser_type in browser_types:
        logger.info(f"Launching {browser_type} browser in {'headless' if headless else 'headed'} mode (session scope)")
        
        if browser_type == "chromium":
            browsers[browser_type] = playwright.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            browsers[browser_type] = playwright.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            browsers[browser_type] = playwright.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser {browser_type}. Supported browsers are: chromium, firefox, webkit.")
    
    logger.info(f"Launched {len(browsers)} browses(s) for test session/")
    
    yield browsers
    
    # Teardown - close all browsers at end of session
    for browser_type, browser in browsers.items():
        logger.info(f"Closing {browser_type} browser (session scope)")
        browser.close()
        
@pytest.fixture(scope="session")
def auth_states(browser_instances, request) -> Dict[str, str]: # type: ignore
    """
    Fixture that provides authentication states for each browser.
    
    Args:
        browser_instances: A dictionary of browser instances.
        request: The pytest request object.
    """
    username = request.config.getoption("--username", default=SYS_ADMIN_USER)
    password = request.config.getoption("--password", default=SYS_ADMIN_PASS)
    
    auth_states = {}
    
    for browser_type, browser in browser_instances.items():
        logger.info("="* 80)
        logger.info(f"Performing one-time login on {browser_type} to capture auth state")
        logger.info("=" * 80)
        
        # Create temporary context just for login
        context = browser.new_context()
        page = context.new_page()
        
        # Perform actual login
        page.goto(QA_LOGIN_URL)
        page.get_by_role("textbox", name="Username").fill(username)
        page.get_by_role("textbox", name="Password").fill(password)
        page.get_by_role("button", name="Log In").click()
        page.get_by_role("button", name="LOG OUT").wait_for(state="visible")
        
        # Capture the authentication state (cookies, local storage)
        storage_state = context.storage_state()
        auth_states[browser_type] = storage_state

        logger.info(f"Captured auth state for {browser_type} browser")

        # Close this temporary context immediately — we only needed it to capture
        # the auth state. Previously this close() call was outside the loop, so
        # only the last browser's context was ever closed when running --browser all.
        context.close()

    yield auth_states

# @pytest.fixture(scope="function")
# def browser_context_and_page(playwright, request):
#     """
#     Fixture that provides a browser, context, and page for each test.
    
#     Args:
#         playwright: The Playwright instance.
#         request: The pytest request object.
    
#     Yields:
#     tuple: A tuple containing the browser, context, and page.
#     """
#     browser_name = request.config.getoption("--browser")
#     headless = request.config.getoption("--headless")
    
#     # Handle 'all' browser option
#     if browser_name.lower() == "all":
#         browser_contexts =[]
#         for browser_type in ["chromium", "firefox", "webkit"]:
#             browser = get_browser_instance(playwright, browser_type, headless)
#             context = browser.new_context()
#             page = context.new_page()
#             start_test_capture(f"{page.browser.browser_type.name}_{request.node.name}")
#             browser_contexts.append((browser, context, page))
            
#         yield browser_contexts
        
#         # Teardown
        
#         for browser, context, page in browser_contexts:
#             end_test_capture(f"{page.browser.browser_type.name}_{request.node.name}")
#             context.close()
#             browser.close()
    
#     else:
#         # Single browser setup
#         browser = get_browser_instance(playwright, browser_name, headless)
#         context = browser.new_context()
#         page = context.new_page()
        
#         start_test_capture(f"{browser_name}_{request.node.name}")
#         yield [(browser, context, page)]
        
#         # Teardown
#         end_test_capture(f"{browser_name}_{request.node.name}")
#         context.close()
#         browser.close()

@pytest.fixture(scope="function")
def logged_in_page(browser_instances, auth_states, request) -> List[Page]: # type: ignore
    """
    Function-scoped fixture that provides fresh, isolated, pre-authenticated pages.

    Each test gets:
    - A NEW context (isolation — clean cookies, cache, etc.)
    - Pre-loaded auth state (no login flow needed)
    - The same long-lived browser (no launch overhead)
    - A blank page ready for the page fixture to navigate to its target

    No navigation happens here. Each page fixture is responsible for navigating
    to its own target page. This means every test makes exactly ONE network
    round-trip before the test body starts, rather than two (previously this
    fixture navigated to QA_LOGIN_URL and waited for LOG OUT, then the page
    fixture navigated again to the actual target page).

    Auth failure is still detected: if the stored auth state is expired, the
    app will redirect to the login page when the page fixture navigates, and
    the fixture's page-title verification will fail with a clear error.

    Args:
        browser_instances: Session-scoped browsers
        auth_states: Session-scoped authentication states
        request: The pytest request object

    Yields:
        List[Page]: List of authenticated pages (one per browser if running "all")
    """
    logger.info("Starting logged_in_page fixture.")
    contexts_and_pages : List[Tuple[BrowserContext, Page]] = []
    pages: List[Page] = []

    for browser_type, browser in browser_instances.items():
        logger.info("=" * 80)
        logger.info(f"Creating new context and page in {browser_type} browser for test: {request.node.name} with saved auth state")
        logger.info("=" * 80)

        # Create new context with stored auth state
        storage_state = auth_states[browser_type]
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()

        start_test_capture(f"{browser_type}_{request.node.name}")

        contexts_and_pages.append((context, page))
        pages.append(page)
        
    logger.info(f"Prepared logged-in page in {browser_type} browser for test: {request.node.name}")
        
    yield pages

    # Teardown - close contexts (but NOT browsers - they are session-scoped)
    for context, page in contexts_and_pages:
        logger.info(f"Tearing down context in {browser.browser_type.name} browser for test: {request.node.name}")
        browser_type = page.context.browser.browser_type.name
        end_test_capture(f"{browser_type}_{request.node.name}")
        context.close()
        logger.debug(f"Closed context in {browser_type} browser for test: {request.node.name}")
    logger.debug("Completed logged_in_page fixture teardown.")
        

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

@pytest.fixture(scope="function")
def panels_page(logged_in_page):
    """
    Function-scoped fixture that provides an authenticated PanelsPage for each browser.

    Navigates directly to /panels and wraps each Playwright page in a PanelsPage
    object. Navigation is done via URL rather than clicking a nav link so the
    fixture works regardless of whether a 'Panels' nav entry is present.

    Args:
        logged_in_page: List of authenticated Playwright pages from the base fixture.

    Yields:
        List[PanelsPage]: One PanelsPage instance per configured browser.
    """
    from page_objects.admin_menu.panels_page import PanelsPage

    panels_pages = []
    for page in logged_in_page:
        page.goto(f"{QA_WEB_BASE_URL}/panels")
        page.wait_for_load_state("networkidle")
        panels_pages.append(PanelsPage(page))

    yield panels_pages


@pytest.fixture(scope="function")
def panel_collections_page(logged_in_page):
    """
    Function-scoped fixture that provides an authenticated PanelCollectionsPage
    for each browser.

    Navigates directly to /panelCollections and wraps each Playwright page in a
    PanelCollectionsPage object. Navigation is done via URL rather than clicking
    a nav link so the fixture works regardless of nav structure.

    Args:
        logged_in_page: List of authenticated Playwright pages from the base fixture.

    Yields:
        List[PanelCollectionsPage]: One PanelCollectionsPage instance per configured browser.
    """
    from page_objects.admin_menu.panel_collections_page import PanelCollectionsPage

    panel_collection_pages = []
    for page in logged_in_page:
        page.goto(f"{QA_WEB_BASE_URL}/panelCollections")
        page.wait_for_load_state("networkidle")
        panel_collection_pages.append(PanelCollectionsPage(page))

    yield panel_collection_pages


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
        "list_endpoint": f"{api_url}/Organization",  # For cleanup search (/Organizations returns 404)
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
        # pageNumber and pageSize are required — without them the API returns only 1 record.
        # 500 is large enough to catch all test records without multiple requests.
        list_response = requests.get(
            config["list_endpoint"],
            params={"pageNumber": 1, "pageSize": 500},
            headers=headers,
        )
        
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
    
    # Generate test record with SHORTER name
    test_id = str(uuid.uuid4())
    test_run_id = test_id[:8]
    username = get_current_username()
    # Shorter timestamp format
    timestamp = datetime.now().strftime('%m%d_%H%M')  # Shortened from '%Y%m%d_%H%M%S'
    
    # Create name for test record here
    base_name = f"DEL_{username}_{timestamp}_{test_run_id}"
    # Truncate to fit within 35 characters
    base_name = base_name[:35]

    # Create payload for test record
    payload = config["payload_template"].copy()
    
    # Fill in test-specific values based on entity type
    if entity_type == "installations":
        payload["installationId"] = test_id
        payload["name"] = base_name
        payload["tips"] = "Test record for delete endpoint verification"
        payload["tutorialText"] = "<b>Delete Test</b>\n\nThis record verifies delete endpoint works."
    elif entity_type == "video_catalogues":
        payload["videoCatalogueId"] = test_id
        payload["name"] = base_name
        payload["description"] = f"Test {entity_name} for delete endpoint verification"
        payload["lastEditedDate"] = datetime.now().isoformat() + 'Z'
    elif entity_type == "organizations":
        payload["organizationId"] = test_id
        payload["name"] = base_name

    # DEBUG: Log the working payload and its length
    logger.info(f"DEBUG: Delete verification payload name: '{payload['name']}' (Length: {len(payload['name'])})")
    
    test_record_created = False
    
    try:
        # Create test record
        logger.info(f"Creating test {entity_name} for delete verification: {test_id}")
        
        create_response = requests.put(
            config["create_endpoint"], 
            json=payload, 
            headers=headers
        )
        logger.info("Pausing 5 seconds - check UI now if you want to see the test record")
        
        if create_response.status_code not in [200, 201]:
            pytest.fail(
                f"Cannot verify delete endpoint - failed to create test {entity_name}: "
                f"{create_response.status_code} - {create_response.text}"
            )
        
        test_record_created = True
        logger.info(f"SUCCESS: Test {entity_name} created successfully: {test_id}")
        
        # Test delete endpoint
        delete_url = config["delete_endpoint_template"].format(id=test_id)
        logger.info(f"Testing delete endpoint: {delete_url}")
        
        delete_response = requests.delete(delete_url, headers=headers)
        
        if delete_response.status_code not in [200, 204]:
            # Delete failed - we have an orphaned record
            logger.error(f"FAILED: Delete endpoint failed for {entity_name}")
            logger.error(f"ORPHANED RECORD ALERT: {entity_name} ID {test_id} created but could not be deleted")
            logger.error(f"Manual cleanup required for: {payload.get('name', test_id)}")
            
            pytest.fail(
                f"Delete endpoint verification failed for {entity_name}. "
                f"Status: {delete_response.status_code} - {delete_response.text}. "
                f"ORPHANED RECORD: {test_id} requires manual cleanup. "
                f"Cannot proceed with bulk data creation."
            )
        
        logger.info(f"SUCCESS: Delete endpoint verification successful for {entity_name}")
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
    Uses shortened names to fit database constraints (50 char limit).
    """
    if entity_type not in TEST_ENTITY_CONFIGURATIONS:
        raise ValueError(f"Unknown entity type: {entity_type}")
    
    config = TEST_ENTITY_CONFIGURATIONS[entity_type]
    
    # Generate unique identifier
    record_id = str(uuid.uuid4())
    test_run_id = record_id[:6]  # Shortened from 8 to 6 characters
    username = get_current_username()
    # Much shorter timestamp
    timestamp = datetime.now().strftime('%m%d_%H%M')  # Just month/day and hour/minute
    
    # Name format: AUTOTEST_username_mmdd_hhmm_id_suffix
    # AUTOTEST_ matches the prefix checked by cleanup_orphaned_test_records.
    # Target: Keep under 45 characters to be safe.
    base_name = f"AUTOTEST_{username}_{timestamp}_{test_run_id}"
    
    # Add suffix but truncate if too long
    if suffix:
        test_name = f"{base_name}{suffix}"
    else:
        test_name = base_name
    
    # Ensure we don't exceed 45 characters (5 char buffer from 50 limit)
    if len(test_name) > 45:
        # Truncate suffix or base name to fit
        available_suffix_chars = 45 - len(base_name)
        if available_suffix_chars > 0 and suffix:
            test_name = f"{base_name}{suffix[:available_suffix_chars]}"
        else:
            test_name = base_name[:45]
    
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
    
    # DEBUG: Log the name length
    logger.info(f"DEBUG: Created test record name: '{test_name}' (Length: {len(test_name)})")
    
    return record_id, payload