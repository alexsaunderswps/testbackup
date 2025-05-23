#test_species_page_ui.py
import pytest
from pytest_check import check
from fixtures.dashboard.species_fixtures import species_page
from utilities.utils import logger, get_browser_name

class TestSpeciesPageUI:
    """
    Test suite for the Species page UI elements.

    This class follows the established pattern for Playwright-based UI testing,
    using the modern fixture-based approach and the verify_ui_elements pattern
    for consistent element verification across different browsers.
    """
    
    @pytest.mark.UI
    @pytest.mark.species
    def test_species_page_title(self, species_page):
        """
        Test that the Species page title is present and correct.

        This test verifies that when users navigate to the Species page,
        they see the correct page title, which is essential for user orientation
        and navigation feedback.
        
        Args:
            species_page: The SpeciesPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_species_page_title")
        for sp in species_page:
            title = sp.verify_page_title_present()
            check.is_true(title, "Species title does not match")
            logger.info("Verification Successful :: Species Page Title found")
    
    @pytest.mark.UI
    @pytest.mark.species
    @pytest.mark.navigation
    def test_species_page_nav_elements(self, species_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Species page.

        Navigation consistency is crucial for user experience. This test ensures
        that all standard navigation elements (logo, menu items, etc.) are present
        and accessible on the Species page, maintaining consistency across the application.

        Args:
            species_page: The SpeciesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(species_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing species navigation elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Species Navigation Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.species
    @pytest.mark.navigation
    def test_species_page_admin_elements(self, species_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Species page.

        The Admin dropdown provides access to administrative functions. This test
        ensures that all expected admin menu items are available when accessed
        from the Species page, maintaining administrative workflow consistency.

        Args:
            species_page: The SpeciesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(species_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing species admin elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Species Admin Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.species
    @pytest.mark.navigation
    def test_species_page_definition_elements(self, species_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Species page.

        The Definitions dropdown provides access to configuration and reference data.
        This test verifies that users can access all definition-related functions
        from the Species page, ensuring complete functionality is available.

        Args:
            species_page: The SpeciesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(species_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing species definition elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Species Definition Elements found on {get_browser_name(page)}")

    @pytest.mark.UI
    @pytest.mark.action
    @pytest.mark.species
    def test_species_page_search_elements(self, species_page):
        """
        Test that all species search elements are present and functional.

        This test ensures that the search input, search button, and Add Species button
        are all present and properly labeled for user interaction.

        Args:
            species_page: The SpeciesPage fixture providing page objects for each browser
        """
        for sp in species_page:
            all_elements, missing_elements = sp.verify_all_species_search_elements_present()
            check.is_true(all_elements, f"Search elements missing from Species Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Search elements found on Species Page")

    @pytest.mark.UI
    @pytest.mark.species
    @pytest.mark.table 
    def test_species_table_elements(self, species_page):
        """
        Test that all species table elements are present and properly structured.

        The species table is the primary interface for viewing species information.
        This test verifies that all expected columns (Name, Colloquial Name, Scientific Name,
        Description, IUCN Status, Population Trend, Species Category) are present, 
        ensuring users can access all relevant species data.

        Args:
            species_page: The SpeciesPage fixture providing page objects for each browser
        """
        logger.info("Starting test_species_table_elements")
        for sp in species_page:
            sp.page.wait_for_timeout(2000)
            all_elements, missing_elements = sp.verify_all_species_table_elements_present()
            check.is_true(all_elements, f"Table elements missing from Species Page: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Species Table Elements found on Species Page")

    @pytest.mark.UI
    @pytest.mark.species
    @pytest.mark.table
    def test_species_table_rows(self, species_page):
        """
        Test that species table rows can be counted and are accessible.

        Args:
            species_page: The SpeciesPage fixture providing page objects for each browser
        """
        for sp in species_page:
            sp.page.wait_for_timeout(2000)
            row_count = sp.count_table_rows()
            logger.info(f"Verification Successful :: Able to count all table rows. {row_count} Rows found")

    @pytest.mark.species
    @pytest.mark.table
    def test_species_name_retreval(self, species_page):
        """
        Test that species names can be retrieved from the table.

        Args:
            species_page: The SpeciesPage fixture providing page objects for each browser
        """
        for sp in species_page:
            sp.page.wait_for_timeout(2000)
            sp.get_species_name_values()
            
    @pytest.mark.UI
    @pytest.mark.species
    @pytest.mark.pagination
    def test_species_pagination_elements(self, species_page, verify_ui_elements):
        """
        Test that pagination elements are correctly displayed on the Species page.

        When there are many species, pagination becomes essential for usability.
        This test ensures that pagination controls are present and properly
        configured based on the number of species and page size settings.

        Args:
            species_page: The SpeciesPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        self.page.wait_for_timeout(2000)
        results = verify_ui_elements.pagination_elements(species_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing species pagination elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Species Pagination Elements found on {get_browser_name(page)}")