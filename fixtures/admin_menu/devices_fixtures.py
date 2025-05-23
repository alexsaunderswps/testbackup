#devices_fixtures.py (Fixture)
import pytest
from utilities.utils import logger, get_browser_name
from page_objects.admin_menu.devices_page import DevicesPage

@pytest.fixture
def devices_page(logged_in_page):
    """
    Fxiture that provides the Devices page for each test.
    
    This fixture handles the navigation to the Devices page and creates
    DevicesPage objects for each logged-in browser instance. It follows
    the established pattern for admin menu page fixtures.

    Args:
        logged_in_page: A fixture providing a logged-in browser instace from conftest.py.
        
    Yields:
        List[DevicesPage]: A list of DevicesPage objects for each logged0in browser instance.
    """
    logger.debug("Starting devices_page fixture")
    device_pages = []
    
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Devices page on {get_browser_name(page)}")
        logger.info("=" * 80)
        
        # Navigate to Devices page through the Admin menu
        page.get_by_role("button", name="Admin").click()
        page.get_by_role("link", name="Devices").click()
        
        # Create the page object
        devices_page = DevicesPage(page)
        
        # Verify that we're on the Devices page
        if devices_page.verify_page_title():
            logger.info(f"Successfully navigated to Devices page on {get_browser_name(page)}")
            device_pages.append(devices_page)
        else:
            logger.error(f"Failed to navigate to Devices page on {get_browser_name(page)}")
        
    logger.info(f"devices_page fixture: yielding {len(device_pages)} DevicesPage objects")
    yield device_pages
    logger.debug("devices_page fixture: finished")