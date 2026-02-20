#tags_fixture.py (Fixture)
import pytest
from utilities.utils import logger, get_browser_name
from page_objects.definitions_menu.tags_page import TagsPage
from conftest import QA_WEB_BASE_URL

@pytest.fixture
def tags_page(logged_in_page):
    """
    Fixture that provides the Tags page for each test.
    
    This fixture handles the navigation to the Tags page through the Definitions
    dropdown menu and creates TagsPage objects for each logged-in browser instance.
    It follows the established pattern for definitions menu page fixtures.

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py.
        
    Yields:
        List[TagsPage]: A list of TagsPage objects for each logged-in browser instance.
    """
    logger.debug("Starting tags_page fixture")
    tag_pages = []
    
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Tags page on {get_browser_name(page)}")
        logger.info("=" * 80)
        
        # Navigate directly to Tags (development notice) page
        page.goto(QA_WEB_BASE_URL + "/developmentNotice")
        
        # Create the page object
        tags_page = TagsPage(page)
        
        # Verify that we're on the Tags page
        if tags_page.verify_development_notice():
            logger.info(f"Successfully navigated to Tags page on {get_browser_name(page)}")
            tag_pages.append(tags_page)
        else:
            logger.error(f"Failed to navigate to Tags page on {get_browser_name(page)}")
        
    logger.info(f"tags_page fixture: yielding {len(tag_pages)} TagsPage objects")
    yield tag_pages
    logger.debug("tags_page fixture: finished")