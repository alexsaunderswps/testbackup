#test_countries_page_ui.py
import pytest
import time
from pytest_check import check
from page_objects.dashboard.countries_page import CountriesPage
from page_objects.common.base_page import BasePage
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def countries_page(logged_in_browser):
    """_summary_

    Args:
        logged_in_browser (_type_): _description_
    """
    logger.debug("Starting countries_page fixture")
    country_pages = []
    for login_page in logged_in_browser:
        driver = login_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Countries page on {driver.name}")
        logger.info("=" * 80)
        
        # Navigate to Countries page
        base_page.click_definitions_button()
        base_page.go_countries_page()
        # Verify that we're on the Countries page
        countries_page = CountriesPage(driver)
        if countries_page.verify_page_title_present():
            logger.info("Successfully navigated to Countries page")
            country_pages.append(countries_page)
        else:
            logger.error(f"Failed to navigate to Countries page on {driver.name}")
    
    logger.info(f"countries_page fixture: yielding {len(country_pages)} country page(s)")
    yield country_pages
    logger.debug("countries_page fixture: finished")
        
class TestCountriesPageUI:
    
    @pytest.mark.UI
    @pytest.mark.countries
    #@pytest.mark.debug
    def test_countries_page_title(self, countries_page):
        """_summary_

        Args:
            countries_page (_type_): _description_
        """
        logger.debug("Starting test_countries_page_title")
        for cp in countries_page:
            title = cp.verify_page_title_present()
            check.is_true(title, "Title does not match")
            logger.info("Verification Successful :: Countries Page Title found")
            
    @pytest.mark.UI
    @pytest.mark.countries
    #@pytest.mark.debug
    def test_countries_page_nav_elements(self, countries_page):
        """_summary_

        Args:
            countries_page (_type_): _description_
        """
        logger.info("Starting test_countries_page_nav_elements")
        all_browsers_passed = True
        for index, cp in enumerate(countries_page):
            logger.info(f"Testing countries page nav elements on browser {index + 1}: {cp.driver.name}")
            all_elements = cp.verify_all_nav_elements_present()
            if all_elements:
                logger.info(f"Verification Successful :: All Navigation elements found on Countries Page for {cp.driver.name}")
            else:
                logger.error(f"Verification failed :: Some elements missing from Countries Page for {cp.driver.name}")
                all_browsers_passed = False
        logger.info("Finished test_countries_page_nav_elements")
        assert all_browsers_passed, "One or more browsers failed the navigation elements check"
        
    @pytest.mark.UI
    @pytest.mark.countries
    #@pytest.mark.debug 
    def test_countries_page_definition_elements(self, countries_page):
        """_summary_

        Args:
            countries_page (_type_): _description_
        """
        for cp in countries_page:
            logger.debug("Starting test_countries_page_definition_elements")
            all_elements = cp.verify_all_definition_links_present()
            check.is_true(all_elements, "Definition elements not found")
            logger.info("Verification Successful :: All Definition elements found on Countries Page")
            logger.debug("Finished test_countries_page_definition_elements")
            
    @pytest.mark.UI
    @pytest.mark.countries
    @pytest.mark.table
    #@pytest.mark.debug
    def test_countries_table_rows(self, countries_page):
        """_summary_

        Args:
            countries_page (_type_): _description_
        """
        for cp in countries_page:
            logger.debug("Starting test_countries_table_rows")
            row_count = cp.count_table_rows()
            check.is_true(row_count > 0, "No rows found in table")
            logger.info(f"Verification Successful :: Countries Table has {row_count} rows")
            logger.debug("Finished test_countries_table_rows")
            
    @pytest.mark.UI
    @pytest.mark.countries
    @pytest.mark.table
    #@pytest.mark.debug
    def test_country_name_retreval(self, countries_page):
        """_summary_

        Args:
            countries_page (_type_): _description_
        """
        for cp in countries_page:
            logger.debug("Starting test_country_name_retreval")
            country_names = cp.get_country_name_values()
            check.is_true(len(country_names) > 0, "No country names found")
            logger.info(f"Verification Successful :: Found {len(country_names)} country names")
            logger.debug("Finished test_country_name_retreval")
            
# TODO - check countries page for starting Todos prior to writing tests here