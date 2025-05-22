# test_population_trend_page_ui.py (Playwright version)
import pytest
from pytest_check import check
from fixtures.definitions_menu.populationtrends_fixture import population_trend_page
from utilities.utils import get_browser_name, logger
    
class TestPopulationTrendPageUI:
    """
    Test suite for the Population Trend page UI elements using Playwright.
    
    This class follows the established pattern for Playwright-based UI testing,
    demonstrating comprehensive verification strategies for reference data pages.
    Population Trend information provides essential context for wildlife conservation
    efforts, making reliable access to this data critical for effective decision-making.
    """

    @pytest.mark.UI
    @pytest.mark.population_trend
    def test_population_trend_page_title(self, population_trend_page):
        """
        Test that the Population Trend page title is present and correct.
        
        Population Trend data helps wildlife managers understand whether species
        populations are increasing, decreasing, or stable over time. A clear title
        immediately communicates to users that they're accessing this important
        temporal analysis information.
        
        Args:
            population_trend_page: The PopulationTrendPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_population_trend_page_title")
        for ptp in population_trend_page:
            title_present = ptp.verify_page_title()
            check.is_true(title_present, f"Population Trend page title not found on {get_browser_name(ptp.page)}")
            logger.info(f"Verification Successful :: Population Trend Page Title found on {get_browser_name(ptp.page)}")
    
    @pytest.mark.UI
    @pytest.mark.population_trend
    @pytest.mark.navigation
    def test_population_trend_page_nav_elements(self, population_trend_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Population Trend page.
        
        Wildlife researchers and conservationists often move between Population Trend
        data and other reference information when conducting analyses. Consistent
        navigation ensures they can efficiently access related data sources without
        losing their analytical workflow context.
        
        Args:
            population_trend_page: The PopulationTrendPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(population_trend_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing Population Trend navigation elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All Population Trend Navigation Elements found on {get_browser_name(page.page)}")
    
    
    @pytest.mark.UI
    @pytest.mark.population_trend
    @pytest.mark.navigation
    def test_population_trend_page_admin_elements(self, population_trend_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Population Trend page.
        
        Population trend definitions may require updates as scientific understanding
        evolves and new trend categories are established. Administrative access from
        the trend page enables timely maintenance of these scientific classifications.
        
        Args:
            population_trend_page: The PopulationTrendPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(population_trend_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing Population Trend admin elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All Population Trend Admin Elements found on {get_browser_name(page.page)}")
    
    
    @pytest.mark.UI
    @pytest.mark.population_trend
    @pytest.mark.navigation
    def test_population_trend_page_definition_elements(self, population_trend_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Population Trend page.
        
        Population trends work in conjunction with IUCN status, country information,
        and species classifications to provide comprehensive conservation context.
        The definitions menu enables users to quickly access these complementary
        reference datasets during their research and analysis activities.
        
        Args:
            population_trend_page: The PopulationTrendPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(population_trend_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing Population Trend definition elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All Population Trend Definition Elements found on {get_browser_name(page.page)}")
    
    @pytest.mark.UI
    @pytest.mark.population_trend
    @pytest.mark.table
    def test_population_trend_table_elements(self, population_trend_page):
        """
        Test that all expected table elements are present on the Population Trend page.
        
        The Population Trend table presents scientific classifications that researchers
        use to categorize and communicate population dynamics. This test ensures the
        table infrastructure properly supports the display and accessibility of this
        specialized scientific vocabulary.
        
        Args:
            population_trend_page: The PopulationTrendPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_population_trend_table_elements")
        for ptp in population_trend_page:
            all_elements, missing_elements = ptp.verify_all_population_trend_table_elements_present()
            check.is_true(all_elements, 
                f"Missing Population Trend table elements: {', '.join(missing_elements)} on {get_browser_name(ptp.page)}")
            logger.info(f"Verification Successful :: All Population Trend Table Elements found on {get_browser_name(ptp.page)}")
    
    @pytest.mark.UI
    @pytest.mark.population_trend
    @pytest.mark.table
    def test_population_trend_data_presence(self, population_trend_page):
        """
        Test that the Population Trend table contains the expected trend classification data.
        
        Population trend categories represent standardized scientific terminology for
        describing demographic changes in wildlife populations. The presence of this
        reference data is essential for consistent classification and reporting across
        different research projects and conservation initiatives.
        
        Args:
            population_trend_page: The PopulationTrendPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_population_trend_data_presence")
        for ptp in population_trend_page:
            row_count = ptp.count_table_rows()
            check.greater(row_count, 0, 
                f"Population Trend table should contain classification data, found {row_count} rows on {get_browser_name(ptp.page)}")
            logger.info(f"Verification Successful :: Population Trend Table has {row_count} rows on {get_browser_name(ptp.page)}")
    
    @pytest.mark.UI
    @pytest.mark.population_trend
    @pytest.mark.table
    def test_population_trend_data_retrieval(self, population_trend_page):
        """
        Test that Population Trend names and comprehensive data can be retrieved from the table.
        
        Automated data extraction capabilities enable integration testing scenarios
        where population trend classifications need to be validated for consistency
        with scientific standards and cross-referenced with species population data
        from monitoring systems.
        
        Args:
            population_trend_page: The PopulationTrendPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_population_trend_data_retrieval")
        for ptp in population_trend_page:
            # Test basic name retrieval functionality
            trend_names = ptp.get_population_trend_name_values()
            check.greater(len(trend_names), 0, 
                f"Should retrieve Population Trend names, found {len(trend_names)} names on {get_browser_name(ptp.page)}")
            
            # Verify data quality of retrieved names
            valid_names = [name for name in trend_names if name and name.strip()]
            check.equal(len(valid_names), len(trend_names), 
                f"All retrieved names should be valid, found {len(valid_names)} valid out of {len(trend_names)} total on {get_browser_name(ptp.page)}")
            logger.info(f"Verification Successful :: Retrieved {len(trend_names)} Population Trend names on {get_browser_name(ptp.page)}")