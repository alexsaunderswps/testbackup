#test_base_page_ui.py
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

class TestBasePageUI:

    @pytest.mark.UI 
    @pytest.mark.debug
    def test_page_nav_elements(self, page_element):
        """_summary_

        Args:
            page_element (_type_): _description_
        """
        logger.debug(f"Starting test_base_page_nav_elements for {page_element[0].__class__.__name__}")
        all_browsers_passed = True
        for index, bp in enumerate(page_element):
            logger.info(f"Testing nav elements on brwoser {index + 1}: {bp.driver.name}")
            success, missing = bp.verify_all_nav_elements_present()

            if success:
                logger.info(f"Verification Successful :: All Nav Elements found on {bp.driver.name}")
            else:
                logger.error(f"Verification Failed :: Missing Nav Elements: {', '.join(missing)} for {bp.driver.name}")
                all_browsers_passed = False
        logger.info("test_page_nav_elements: finished")
        assert all_browsers_passed, "One or more browsers failed to find all nav elements"