# iucnstatus_fixtures.py (Fixture)
import pytest
from utilities.utils import logger, get_browser_name
from page_objects.definitions_menu.iucn_status_page import IUCNStatusPage

@pytest.fixture
def iucn_status_page(logged_in_page):
    """
    Fixture that provides the IUCN Status page for each test.
    
    This fixture handles the navigation to the IUCN Status page through the Definitions
    dropdown menu and creates IUCNStatusPage objects for each logged-in browser instance.
    It follows the established pattern for definitions menu page fixtures.

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py.
        
    Yields:
        List[IUCNStatusPage]: A list of IUCNStatusPage objects for each logged-in browser instance.
    """
    logger.debug("Starting iucn_status_page fixture")
    iucn_pages = []
    
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to IUCN Status page on {get_browser_name(page)}")
        logger.info("=" * 80)
        
        # Navigate to IUCN Status page through the Definitions menu
        page.get_by_role("button", name="Definitions").click()
        page.get_by_role("link", name="IUCN Status").click()
        
        # Create the page object
        iucn_status_page = IUCNStatusPage(page)
        
        # Verify that we're on the IUCN Status page
        if iucn_status_page.verify_page_title():
            logger.info(f"Successfully navigated to IUCN Status page on {get_browser_name(page)}")
            iucn_pages.append(iucn_status_page)
        else:
            logger.error(f"Failed to navigate to IUCN Status page on {get_browser_name(page)}")
        
    logger.info(f"iucn_status_page fixture: yielding {len(iucn_pages)} IUCNStatusPage objects")
    yield iucn_pages
    logger.debug("iucn_status_page fixture: finished")