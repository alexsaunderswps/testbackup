#populationtrends_fixture.py (Fixture)
import pytest
from utilities.utils import logger, get_browser_name
from page_objects.definitions_menu.population_trend_page import PopulationTrendPage
from conftest import QA_WEB_BASE_URL

@pytest.fixture
def population_trend_page(logged_in_page):
    """
    Fixture that provides the Population Trend page for each test.
    
    This fixture handles the navigation to the Population Trend page through the Definitions
    dropdown menu and creates PopulationTrendPage objects for each logged-in browser instance.
    It follows the established pattern for definitions menu page fixtures.

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py.
        
    Yields:
        List[PopulationTrendPage]: A list of PopulationTrendPage objects for each logged-in browser instance.
    """
    logger.debug("Starting population_trend_page fixture")
    trend_pages = []
    
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Population Trend page on {get_browser_name(page)}")
        logger.info("=" * 80)
        
        # Navigate directly to Population Trend page
        page.goto(QA_WEB_BASE_URL + "/populationTrend")
        
        # Create the page object
        population_trend_page = PopulationTrendPage(page)
        
        # Verify that we're on the Population Trend page
        if population_trend_page.verify_page_title():
            logger.info(f"Successfully navigated to Population Trend page on {get_browser_name(page)}")
            trend_pages.append(population_trend_page)
        else:
            logger.error(f"Failed to navigate to Population Trend page on {get_browser_name(page)}")
        
    logger.info(f"population_trend_page fixture: yielding {len(trend_pages)} PopulationTrendPage objects")
    yield trend_pages
    logger.debug("population_trend_page fixture: finished")