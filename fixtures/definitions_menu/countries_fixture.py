# countries_fixtures.py (Fixture)
import pytest
from utilities.utils import logger, get_browser_name
from page_objects.definitions_menu.countries_page import CountriesPage
from conftest import QA_WEB_BASE_URL

@pytest.fixture
def countries_page(logged_in_page):
    """
    Fixture that provides the Countries page for each test.
    
    This fixture handles the navigation to the Countries page through the Definitions
    dropdown menu and creates CountriesPage objects for each logged-in browser instance.
    It follows the established pattern for definitions menu page fixtures.

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py.
        
    Yields:
        List[CountriesPage]: A list of CountriesPage objects for each logged-in browser instance.
    """
    logger.debug("Starting countries_page fixture")
    country_pages = []
    
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Countries page on {get_browser_name(page)}")
        logger.info("=" * 80)
        
        # Navigate directly to Countries page
        page.goto(QA_WEB_BASE_URL + "/countries")
        
        # Create the page object
        countries_page = CountriesPage(page)
        
        # Verify that we're on the Countries page
        if countries_page.verify_page_title():
            logger.info(f"Successfully navigated to Countries page on {get_browser_name(page)}")
            country_pages.append(countries_page)
        else:
            logger.error(f"Failed to navigate to Countries page on {get_browser_name(page)}")
        
    logger.info(f"countries_page fixture: yielding {len(country_pages)} CountriesPage objects")
    yield country_pages
    logger.debug("countries_page fixture: finished")