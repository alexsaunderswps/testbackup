#test_species_page_ui.py
import pytest
from pytest_check import check
from page_objects.dashboard.species_page import SpeciesPage
from page_objects.common.base_page import BasePage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def species_page(logged_in_browser):
    logger.debug("Starting species_page fixture")
    species_pages = []
    for login_page in logged_in_browser:
        driver = login_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Species page on {driver.name}")
        logger.info("=" * 80)
        
        # Navigate to Species page
        base_page.go_species_page()
        # Verify that we're on the Species page
        species_page = SpeciesPage(driver)
        if species_page.verify_page_title_present():
            logger.info("Successfully navigated to Species page")
            species_pages.append(species_page)
        else:
            logger.error(f"Failed to navigate to Species page on {driver.name}")
        
    logger.info(f"species_page fixture: yielding {len(species_pages)} species page(s)")
    yield species_pages
    logger.debug("species_page fixture: finished")
    
class TestSpeciesPageUI(TestBasePageUI):
        
    @pytest.mark.UI 
    @pytest.mark.debug
    def test_species_page_title(self, species_page):
        """_summary_

        Args:
            species_page (_type_): _description_
        """
        logger.debug("Starting test_species_page_title")
        for sp in species_page:
            title = sp.verify_page_title_present()
            check.equal(title, True, "Title does not match")
            logger.info("Verificaiton Successful :: Species Page Title found")

    @pytest.mark.UI 
    @pytest.mark.debug
    def test_species_page_nav_elements(self, species_page):
        """_summary_

        Args:
            species_page (_type_): _description_
        """
        return super().test_page_nav_elements(species_page)