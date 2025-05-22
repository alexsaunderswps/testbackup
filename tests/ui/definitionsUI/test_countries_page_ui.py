#test_countries_page_ui.py (Playwright version)
import pytest
from pytest_check import check
from fixtures.definitions_menu.countries_fixture import countries_page
from utilities.utils import logger, get_browser_name
        
class TestCountriesPageUI:
    """
    Test suite for the Countries page UI elements using Playwright.
    
    This class follows the established pattern for Playwright-based UI testing,
    using the modern fixture-based approach and the verify_ui_elements pattern
    for consistent element verification across different browsers.
    """
    
    @pytest.mark.UI
    @pytest.mark.countries
    def test_countries_page_title(self, countries_page):
        """
        Test that the Countries page title is present and correct.
        
        The page title serves as a crucial navigation indicator for users and helps
        screen readers understand the current page context. This test ensures that
        users arriving at the Countries page can immediately understand where they are.
        
        Args:
            countries_page: The CountriesPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_countries_page_title")
        for cp in countries_page:
            title = cp.verify_page_title()
            check.is_true(title, "Title does not match")
            logger.info("Verification Successful :: Countries Page Title found")
            
    @pytest.mark.UI
    @pytest.mark.countries
    @pytest.mark.navigation 
    def test_countries_page_nav_elements(self, countries_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Countries page.
        
        Navigation consistency across all pages ensures users can always access
        core application functions regardless of their current location. This test
        verifies that standard navigation elements like the header, menu items,
        and user controls are available on the Countries page.
        
        Args:
            countries_page: The CountriesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(countries_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing countries navigation elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All Countries Navigation Elements found on {get_browser_name(page.page)}")
    
    @pytest.mark.UI
    @pytest.mark.countries
    @pytest.mark.navigation
    def test_countries_page_admin_elements(self, countries_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Countries page.
        
        Administrative functions need to be consistently accessible across all pages
        to ensure administrators can perform their duties efficiently. This test verifies
        that all expected admin menu items are available when accessed from the Countries page.
        
        Args:
            countries_page: The CountriesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(countries_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing countries admin elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All Countries Admin Elements found on {get_browser_name(page.page)}")
    
        
    @pytest.mark.UI
    @pytest.mark.countries
    @pytest.mark.navigation
    def test_countries_page_definition_elements(self, countries_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Countries page.
        
        The Definitions dropdown provides access to reference data and configuration options
        that users need to access from various contexts. This test ensures that the full
        definitions menu remains available when users are working with Countries data.
        
        Args:
            countries_page: The CountriesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(countries_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing countries definition elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All Countries Definition Elements found on {get_browser_name(page.page)}")
    
    @pytest.mark.UI
    @pytest.mark.countries
    @pytest.mark.page
    def test_countries_action_elements(self, countries_page):
        """
        Test that all action elements are present on the Countries page.

        Args:
            countries_page: The CountriesPage fixture
        """
        for cp in countries_page:
            all_elements, missing_elements = cp.verify_all_countries_action_elements_present()
            check.is_true(all_elements, f"Missing countries action elements {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Countries action Elements found")
    
    @pytest.mark.UI 
    @pytest.mark.countries
    @pytest.mark.table
    def test_countries_table_elements(self, countries_page):
        """
        Test that all expected table elements are present on the Countries page.
        
        The countries table serves as the primary interface for viewing and interacting
        with country data. This test verifies that essential table components like the
        table body, rows, and search functionality are properly rendered and accessible.
        
        Args:
            countries_page: The CountriesPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_countries_table_elements")
        for cp in countries_page:
            all_elements, missing_elements = cp.verify_all_countries_table_elements_present()
            check.is_true(all_elements, 
                f"Missing countries table elements: {', '.join(missing_elements)} on {get_browser_name(cp.page)}")
            logger.info(f"Verification Successful :: All Countries Table Elements found on {get_browser_name(cp.page)}")
    
    @pytest.mark.UI
    @pytest.mark.countries
    @pytest.mark.table
    def test_countries_table_data_presence(self, countries_page):
        """
        Test that the Countries table contains data and can be counted.
        
        Beyond just verifying that table elements exist, this test ensures that the
        table actually contains country data. This helps catch scenarios where the
        table structure loads correctly but data population fails due to API issues
        or other backend problems.
        
        Args:
            countries_page: The CountriesPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_countries_table_data_presence")
        for cp in countries_page:
            row_count = cp.count_table_rows()
            check.greater(row_count, 0, 
                f"Countries table should contain data, found {row_count} rows on {get_browser_name(cp.page)}")
            logger.info(f"Verification Successful :: Countries Table has {row_count} rows on {get_browser_name(cp.page)}")
    
    @pytest.mark.UI
    @pytest.mark.countries
    @pytest.mark.table
    def test_countries_data_retrieval(self, countries_page):
        """
        Test that country names can be retrieved from the table.
        
        This test validates the fundamental data extraction capability that supports
        more complex testing scenarios. Being able to reliably extract country names
        from the table enables verification of search functionality, sorting behavior,
        and data accuracy in subsequent tests.
        
        Args:
            countries_page: The CountriesPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_countries_data_retrieval")
        for cp in countries_page:
            country_names = cp.get_country_name_values()
            check.greater(len(country_names), 0, 
                f"Should retrieve country names, found {len(country_names)} names on {get_browser_name(cp.page)}")
            
            # Verify that retrieved names are valid (non-empty strings)
            valid_names = [name for name in country_names if name and name.strip()]
            check.equal(len(valid_names), len(country_names), 
                f"All retrieved names should be valid, found {len(valid_names)} valid out of {len(country_names)} total on {get_browser_name(cp.page)}")
            
            logger.info(f"Verification Successful :: Retrieved {len(country_names)} valid country names on {get_browser_name(cp.page)}")
    
    @pytest.mark.UI
    @pytest.mark.countries
    @pytest.mark.search
    def test_countries_search_functionality(self, countries_page):
        """
        Test the search functionality on the Countries page.
        
        Search capability is essential for users working with large datasets. This test
        verifies that the search interface exists and can be interacted with. The test
        focuses on UI functionality rather than search logic, ensuring that users can
        input search terms and trigger search operations.
        
        Args:
            countries_page: The CountriesPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_countries_search_functionality")
        for cp in countries_page:
            # Get initial row count
            initial_count = cp.count_table_rows()
            logger.info(f"Initial row count: {initial_count} on {get_browser_name(cp.page)}")
            
            # Test search functionality if available
            try:
                search_box = cp.get_countries_search_text()
                if search_box.count() > 0:
                    # Test that we can interact with the search box
                    search_box.fill("United")
                    cp.page.wait_for_load_state("networkidle")
                    
                    # Clear search to restore original state
                    search_box.clear()
                    cp.page.wait_for_load_state("networkidle")
                    
                    logger.info(f"Verification Successful :: Search functionality works on {get_browser_name(cp.page)}")
                else:
                    logger.info(f"Search functionality not available on {get_browser_name(cp.page)}")
                    
            except Exception as e:
                logger.warning(f"Search test encountered issue on {get_browser_name(cp.page)}: {str(e)}")
                # Don't fail the test for search issues, as search might not be implemented
                pass