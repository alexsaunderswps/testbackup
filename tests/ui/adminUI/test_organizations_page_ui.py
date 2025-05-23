#test_organizations_page.py (Playwright version)
import pytest
from pytest_check import check
from fixtures.admin_menu.organizations_fixtures import organizations_page
from utilities.utils import get_browser_name, logger

class TestOrganizationsPageUI:
    """
    Test suite for the Organizations page UI elements.

    This class follows the established pattern for Playwright-based UI testing,
    using the modern fixture-based approach and the verify_ui_elements pattern
    for consistent element verification across different browsers.
    """
    
    @pytest.mark.UI 
    @pytest.mark.organizations
    def test_organizations_page_title(self, organizations_page):
        """
        Test that the Organizations page title is present.
        
        Args:
            organizations_page: The OrganizationsPage fixture
        """
        logger.debug("Starting test_organizations_page_title")
        for op in organizations_page:
            title = op.verify_page_title()
            check.is_true(title, "Organizations title does not match")
            logger.info("Verification Successful :: Organizations Page Title found")
    
    @pytest.mark.UI 
    @pytest.mark.organizations
    @pytest.mark.navigation
    def test_organizations_page_nav_elements(self, organizations_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Organizations page.
        
        Args:
            organizations_page: The OrganizationsPage fixture
            verify_ui_elements: The UI element verification fixture
        """
        results = verify_ui_elements.nav_elements(organizations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing navigation elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All navigation elements found")
    
    @pytest.mark.UI 
    @pytest.mark.navigation
    @pytest.mark.organizations
    def test_organizations_page_admin_elements(self, organizations_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Organizations page.

        Args:
            organizations_page: The OrganizationsPage fixture
            verify_ui_elements: The UI element verification fixture
        """
        results = verify_ui_elements.admin_elements(organizations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing admin elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All admin elements found")
    
    @pytest.mark.UI 
    @pytest.mark.navigation
    @pytest.mark.organizations
    def test_organizations_page_definition_elements(self, organizations_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Users page.
        
        Args:
            organizations_page: The OrganizationsPage fixture
            verify_ui_elements: The UI element verification fixture
        """
        results = verify_ui_elements.definition_elements(organizations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing definition elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All definition elements found")

    @pytest.mark.UI
    @pytest.mark.organizations
    @pytest.mark.page
    def test_organizations_action_elements(self, organizations_page):
        """
        Test that all action elements are present on the Organizations page.

        Args:
            organizations_page: The OrganizationsPage fixture
        """
        for op in organizations_page:
            all_elements, missing_elements = op.verify_all_organization_action_elements_present()
            check.is_true(all_elements, f"Missing organizations action elements {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Organization action Elements found")

    @pytest.mark.UI
    @pytest.mark.organizations
    @pytest.mark.table
    def test_organization_table_elements(self, organizations_page):
        """
        Test that all table elements are present on the Organizations page.
        
        Args:
            organizations_page: The OrganizationsPage fixture
        """
        for op in organizations_page:
            all_elements, missing_elements = op.verify_all_organization_table_elements_present()
            check.is_true(all_elements, f"Missing organization table elements {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Organization table elements found")
    