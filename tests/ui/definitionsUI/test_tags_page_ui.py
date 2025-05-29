# test_tags_page_ui.py (Playwright version)
import pytest
from pytest_check import check
from fixtures.definitions_menu.tags_fixture import tags_page
from utilities.utils import get_browser_name, logger

class TestTagsPageUI:
    """
    Test suite for the Tags page UI elements using Playwright.
    
    This class follows the established pattern for Playwright-based UI testing,
    showcasing comprehensive verification strategies for interactive reference data pages.
    Tags provide flexible categorization capabilities for wildlife data, enabling
    researchers to organize and retrieve information using customizable classification systems.
    """
    
    @pytest.mark.UI
    @pytest.mark.tags
    def test_tags_development_notice(self, tags_page):
        """
        Test that the Tags page development notice is present and correct.

        Tags represent user-defined categories that provide flexible organization
        beyond standard taxonomic and conservation classifications. A clear title
        helps users understand they're working with customizable organizational
        tools rather than fixed scientific classifications.
        
        Args:
            tags_page: The TagsPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_tags_development_notice")
        for tp in tags_page:
            notice_present = tp.verify_development_notice()
            check.is_true(notice_present, f"Tags page development notice not found on {get_browser_name(tp.page)}")
            logger.info(f"Verification Successful :: Tags Page Development Notice found on {get_browser_name(tp.page)}")
            
    @pytest.mark.UI
    @pytest.mark.tags
    @pytest.mark.navigation
    def test_tags_page_nav_elements(self, tags_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Tags page.
        
        Users typically access tags while organizing data or setting up categorization
        schemes for their research projects. Consistent navigation ensures they can
        move seamlessly between tag management and their primary data organization
        workflows without losing context or productivity.
        
        Args:
            tags_page: The TagsPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(tags_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing Tags navigation elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All Tags Navigation Elements found on {get_browser_name(page.page)}")
    
    @pytest.mark.UI
    @pytest.mark.tags
    @pytest.mark.navigation
    def test_tags_page_admin_elements(self, tags_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Tags page.
        
        Tag management often requires administrative oversight to maintain consistency
        across research teams and prevent proliferation of duplicate or conflicting
        categories. Administrative access from the tags page enables efficient
        governance of organizational taxonomy systems.
        
        Args:
            tags_page: The TagsPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(tags_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing Tags admin elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All Tags Admin Elements found on {get_browser_name(page.page)}")
    
    @pytest.mark.UI
    @pytest.mark.tags
    @pytest.mark.navigation
    def test_tags_page_definition_elements(self, tags_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Tags page.
        
        Tags work alongside other definition categories to create comprehensive
        classification systems. Users often need to reference countries, IUCN status,
        and population trends while creating or managing tags to ensure their
        custom categories complement rather than duplicate existing classifications.
        
        Args:
            tags_page: The TagsPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(tags_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing Tags definition elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All Tags Definition Elements found on {get_browser_name(page.page)}")
    