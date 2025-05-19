#test_installations_page.py (Playwright version)
import pytest
from pytest_check import check
from page_objects.admin_menu.installations_page import InstallationsPage
from page_objects.common.base_page import BasePage
from utilities.utils import get_browser_name,logger

@pytest.fixture
def installations_page(logged_in_page):
    """
    Fixture that provides the Installations page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[UsersPage]: A list of InstallationsPage objects for each logged-in browser instance
    """
    logger.debug("Staring installations_page fixture")
    installation_pages = []
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Installations page on {get_browser_name(page)}")
        logger.info("=" * 80)
        
        #Navigate to Installations page
        page.get_by_role("button", name="Admin").click()
        page.get_by_role("link", name="Installations").click()
        
        # Create the page object
        installations_page = InstallationsPage(page)
        
        # Verify that we're on the Installations page
        if installations_page.verify_page_title():
            logger.info("Successfully navigated to Installations page")
            installation_pages.append(installations_page)
        else:
            logger.error(f"Failed to navigate to Installations page on {get_browser_name(page)}")
            
    logger.info(f"installations_page fixture: yielding {len(installation_pages)} installations page(s)")
    yield installation_pages
    logger.debug("installations_page fixture: finished")
    
class TestInstallationsPageUI:
    
    @pytest.mark.UI 
    @pytest.mark.installations
    def test_installations_page_title(self, installations_page):
        """
        Test that the Installations page title is present.
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        logger.debug("Starting test_installations_page_title")
        for ip in installations_page:
            title = ip.verify_page_title()
            check.is_true(title, "Installations title does not match")
            logger.info("Verification Successful :: Installations Page Title found")
            
    @pytest.mark.UI 
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_nav_elements(self, installations_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations navigation elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Navigation Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_admin_elements(self, installations_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations admin elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Admin Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_definition_elements(self, installations_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations definition elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Definition Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_action_elements(self, installations_page):
        """
        Test that the Add Installation button, Search textbox, and Serch button are present on the Users page.
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        logger.debug("Starting test_installations_action_elements")
        for ip in installations_page:
            all_elements, missing_elements = ip.verify_action_elements_present()
            check.is_true(all_elements, f"Missing installations action elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Installations Action Elements found")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.table
    def test_installations_table_elements(self, installations_page):
        """
        Test that all table elements are present on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        for ip in installations_page:
            all_elements, missing_elements = ip.verify_all_installation_table_elements_present()
            check.is_true(all_elements, f"Missing installations table elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Installations Table Elements found")
            
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.pagination
    def test_installations_pagination_elements(self, installations_page, verify_ui_elements):
        """
        Test that pagination elements are correctly displayed on the Installations page.
    
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
    """
        results = verify_ui_elements.pagination_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations pagination elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Pagination Elements found on {get_browser_name(page)}")