#test_organizations_page.py
import pytest
from pytest_check import check
from page_objects.admin_menu.organizations_page import OrganizationsPage
from page_objects.common.base_page import BasePage
from tests.ui.test_base_page_ui import TestBasePageUI
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

@pytest.fixture
def organizations_page(logged_in_browser):
    logger.debug("Starting organizations_page fixture")
    organization_pages = []
    for organization_page in logged_in_browser:
        driver = organization_page.driver
        base_page = BasePage(driver)
        logger.info("=" * 80)
        logger.info(f"Navigating to Organizations page on {driver.name}")
        logger.info("=" * 80)
        
        # Navigate to Organizations page
        base_page.click_admin_button()
        base_page.go_organizations_page()
        # Verify that we're on the Organizations page
        organizations_page = OrganizationsPage(driver)
        if organizations_page.verify_page_title_present():
            logger.info("Successfully navigated to the Orgnizations Page")
            organization_pages.append(organizations_page)
        else:
            logger.error(f"Failed to navigate to the Organizations page on {driver.name}")
    logger.info(f"organizations_page fixture: yielding {len(organization_pages)} organizations page(s)")
    yield organization_pages
    logger.debug("organizations_page fixture: finished")
    
class TestOrganizationsPageUI(TestBasePageUI):
    
    @pytest.mark.UI 
    @pytest.mark.organizations
    def test_organizations_page_title(self, organizations_page):
        """_summary_

        Args:
            organizations_page (_type_): _description_
        """
        logger.debug("Starting test_organizations_page_title")
        for op in organizations_page:
            title = op.verify_page_title_present()
            check.equal(title, True, "Organizations title does not match")
            logger.info("Verifcation Successful :: Organizations Page Title found")
    
    @pytest.mark.UI 
    @pytest.mark.navigation
    @pytest.mark.organizations
    def test_organizations_page_nav_elements(self, organizations_page):
        """_summary_

        Args:
            organizations_page (_type_): _description_
        """
        return super().test_page_nav_elements(organizations_page)
    
    @pytest.mark.UI 
    @pytest.mark.navigation
    @pytest.mark.organizations
    def test_organizations_page_admin_elements(self, organizations_page):
        """_summary_

        Args:
            organizations_page (_type_): _description_
        """
        return super().test_page_admin_elements(organizations_page)
    
    @pytest.mark.UI 
    @pytest.mark.navigation
    @pytest.mark.organizations
    def test_organizations_page_definition_elements(self, organizations_page):
        """_summary_

        Args:
            organizations_page (_type_): _description_
        """
        return super().test_page_definition_elements(organizations_page)
    
    @pytest.mark.UI 
    @pytest.mark.organizations
    @pytest.mark.search
    def test_organizations_search_elements(self, organizations_page):
        """_summary_

        Args:
            organizations_page (_type_): _description_
        """
        for op in organizations_page:
            all_elements, missing_elements = op.verify_all_organization_search_elements_present()
            check.is_true(all_elements, f"Missing organizations search elements {', '.join(missing_elements)}")
            logger.info("Verifcation Successful :: All Organization Search Elements found")
            
    @pytest.mark.UI 
    @pytest.mark.organizations
    @pytest.mark.table
    def test_organization_table_elements(self, organizations_page):
        """_summary_

        Args:
            organizations_page (_type_): _description_
        """
        for op in organizations_page:
            all_elements, missing_elements = op.verify_all_organization_table_elements_present()
            check.is_true(all_elements, f"Missing organization table elements {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Organization table elements found")
    