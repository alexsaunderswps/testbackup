#test_organizations_page.py
import pytest
from pytest_check import check
from page_objects.admin_menu.organizations_page import OrganizationsPage
from utilities.utils import logger

@pytest.fixture
def organizations_page(logged_in_page):
    """
    Fixture that provides the Organizations page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[OrganizationsPage]: A list of OrganizationsPage objects for each logged-in browser instance
    """
    logger.info("Starting organizations_page fixture")
    organization_pages = []
    
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Organizations page on {page.browser.browser_type.name}")
        logger.info("=" * 80)
        
        # Navigate to Organizations page
        page.get_by_role("button", name="Admin").click()
        page.get_by_role("link", name="Organizations").click()
        
        # Create the page object
        org_page = OrganizationsPage(page)
        
        # Verify that we're on the Organizations page
        if org_page.verify_page_title():
            logger.info("Successfully navigated to the Orgnizations Page")
            organization_pages.append(org_page)
        else:
            logger.error(f"Failed to navigate to the Organizations page on {page.browser.browser_type.name}")
            
    logger.info(f"organizations_page fixture: yielding {len(organization_pages)} organizations page(s)")
    yield organization_pages
    logger.debug("organizations_page fixture: finished")
        
    
class TestOrganizationsPageUI(TestBasePageUI):
    
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
            title = op.verify_page_title_present()
            check.is_true(title, "Organizations title does not match")
            logger.info("Verification Successful :: Organizations Page Title found")
    
    @pytest.mark.UI 
    @pytest.mark.organizations
    @pytest.mark.navigation
    def test_organizations_page_nav_elements(self, organizations_page):
        """
        Test that all navigation elements are present on the Organizations page.
        
        Args:
            organizations_page: The OrganizationsPage fixture
        """
        for op in organizations_page:
            all_elements, missing_elements = op.verify_all_nav_elements_present()
            check.is_true(all_elements, f"Missing navigation elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All navigation elements found")
    
    @pytest.mark.UI 
    @pytest.mark.navigation
    @pytest.mark.organizations
    def test_organizations_page_admin_elements(self, organizations_page):
        """_summary_

        Args:
            organizations_page (_type_): _description_
        """
        assert self._verify_page_admin_elements(organizations_page)
    
    @pytest.mark.UI 
    @pytest.mark.navigation
    @pytest.mark.organizations
    def test_organizations_page_definition_elements(self, organizations_page):
        """_summary_

        Args:
            organizations_page (_type_): _description_
        """
        assert self._verify_page_definition_elements(organizations_page)
    
    @pytest.mark.UI 
    @pytest.mark.organizations
    @pytest.mark.search
    def test_organizations_search_elements(self, organizations_page):
        """
        Test that all search elements are present on the Organizations page.
        
        Args:
            organizations_page: The OrganizationsPage fixture
        """
        for op in organizations_page:
            all_elements, missing_elements = op.verify_all_organization_page_elements_present()
            check.is_true(all_elements, f"Missing organizations search elements {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Organization Search Elements found")
            
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
    