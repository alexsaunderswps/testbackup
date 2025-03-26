import pytest
from pytest_check import check 
from page_objects.definitions_menu.population_trend_page import PopulationTrendPage
from page_objects.common.base_page import BasePage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def population_trend_page(logged_in_browser):
    """_summary_

    Args:
        logged_in_browser (_type_): _description_
    """
    logger.debug("Starting population_trend_page fixture")
    population_trend_pages = []
    for login_page in logged_in_browser:
        driver = login_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Population Trend page on {driver.name}")
        logger.info("=" * 80)
        
        # Navigate to Population Trend page
        base_page.click_definitions_button()
        base_page.go_pop_trend_page()
        # Verfify that we're on the Population Trend page
        population_trend_page = PopulationTrendPage(driver)
        if population_trend_page.verify_population_trend_page_title_present():
            logger.info("Successfully navigated to Population Trend page")
            population_trend_pages.append(population_trend_page)
        else:
            logger.error(f"Failed to navigate to Population Trend page on {driver.name}")
            
    logger.info(f"population_trend_page fixture: yielding {len(population_trend_pages)} population_trend page(s)")
    yield population_trend_pages
    logger.debug("population_trend_page fixture: finished")
    
class TestPopulationTrendPageUI(TestBasePageUI):

    @pytest.mark.UI 
    @pytest.mark.population_trend
    def test_population_trend_page_title(self, population_trend_page):
        """_summary_

        Args:
            population_trend_page (_type_): _description_
        """
        logger.debug("Starting test_population_trend_page_title")
        for pp in population_trend_page:
            title = pp.verify_population_trend_page_title_present()
            check.is_true(title, "Population Trend title does not match")
            logger.info("Verification Successful :: Population Trend Page Title found")
    
    @pytest.mark.UI 
    @pytest.mark.navigation
    @pytest.mark.population_trend
    def test_population_trend_page_nav_elements(self, population_trend_page):
        """_summary_

        Args:
            population_trend_page (_type_): _description_
        """
        return super().test_page_nav_elements(population_trend_page)
    
    @pytest.mark.UI
    @pytest.mark.navigation
    @pytest.mark.population_trend
    def test_population_trend_page_admin_elements(self, population_trend_page):
        """_summary_

        Args:
            population_trend_page (_type_): _description_
        """
        return super().test_page_admin_elements(population_trend_page)
    
    @pytest.mark.UI 
    @pytest.mark.navigation
    @pytest.mark.population_trend
    def test_population_trend_page_definitions_elements(self, population_trend_page):
        """_summary_

        Args:
            population_trend_page (_type_): _description_
        """
        return super().test_page_definition_elements(population_trend_page)