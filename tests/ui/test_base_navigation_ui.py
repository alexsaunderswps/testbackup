#test_base_navigation_ui.py
import pytest
from pytest_check import check
from page_objects.common.base_page import BasePage
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def base_page(logged_in_browser):
    logger.debug("Starting base_page fixture")
    base_pages = []
    for login_page in logged_in_browser:
        driver = login_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Base page on {driver.name}")
        logger.info("=" * 80)
        base_pages.append(base_page)
    logger.info(f"base_page fixture: yielding {len(base_pages)} base page(s)")
    yield base_pages
    logger.debug("base_page fixture: finished")

        