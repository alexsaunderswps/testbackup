# test_iucn_status_page_ui.py (Playwright version)
import pytest
from pytest_check import check
from fixtures.definitions_menu.iucnstatus_fixture import iucn_status_page
from utilities.utils import get_browser_name, logger

class TestIUCNStatusPageUI:
    """
    Test suite for the IUCN Status page UI elements using Playwright.
    
    This class follows the established pattern for Playwright-based UI testing,
    using the modern fixture-based approach and comprehensive element verification
    strategies.
    """
    
    @pytest.mark.UI
    @pytest.mark.iucn_status
    def test_iucn_status_page_title(self, iucn_status_page):
        """
        Test that the IUCN Status page title is present and correct.
        
        Args:
            iucn_status_page: The IUCNStatusPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_iucn_status_page_title")
        for isp in iucn_status_page:
            title_present = isp.verify_page_title()
            check.is_true(title_present, f"IUCN Status page title not found on {get_browser_name(isp.page)}")
            logger.info(f"Verification Successful :: IUCN Status Page Title found on {get_browser_name(isp.page)}")
    
    @pytest.mark.UI
    @pytest.mark.iucn_status
    @pytest.mark.navigation
    def test_iucn_status_page_nav_elements(self, iucn_status_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the IUCN Status page.
        
        Args:
            iucn_status_page: The IUCNStatusPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(iucn_status_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing IUCN Status navigation elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All IUCN Status Navigation Elements found on {get_browser_name(page.page)}")
    
    @pytest.mark.UI
    @pytest.mark.iucn_status
    @pytest.mark.navigation
    def test_iucn_status_page_admin_elements(self, iucn_status_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the IUCN Status page.
        
        Args:
            iucn_status_page: The IUCNStatusPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(iucn_status_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing IUCN Status admin elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All IUCN Status Admin Elements found on {get_browser_name(page.page)}")
    
    @pytest.mark.UI
    @pytest.mark.iucn_status
    @pytest.mark.navigation
    def test_iucn_status_page_definition_elements(self, iucn_status_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the IUCN Status page.
        
        Args:
            iucn_status_page: The IUCNStatusPage fixture providing page objects for each browser
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(iucn_status_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, 
                f"Missing IUCN Status definition elements: {', '.join(missing_elements)} on {get_browser_name(page.page)}")
            logger.info(f"Verification Successful :: All IUCN Status Definition Elements found on {get_browser_name(page.page)}")
    
    @pytest.mark.UI
    @pytest.mark.iucn_status
    @pytest.mark.table
    def test_iucn_status_table_elements(self, iucn_status_page):
        """
        Test that all expected table elements are present on the IUCN Status page.
        
        The IUCN Status table presents standardized conservation classifications
        that must be consistently accessible and readable. This test ensures the
        table structure properly supports the display of this reference information.
        
        Args:
            iucn_status_page: The IUCNStatusPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_iucn_status_table_elements")
        for isp in iucn_status_page:
            isp.page.wait_for_timeout(1000)
            all_elements, missing_elements = isp.verify_all_iucn_status_table_elements_present()
            check.is_true(all_elements, 
                f"Missing IUCN Status table elements: {', '.join(missing_elements)} on {get_browser_name(isp.page)}")
            logger.info(f"Verification Successful :: All IUCN Status Table Elements found on {get_browser_name(isp.page)}")
    
    @pytest.mark.UI
    @pytest.mark.iucn_status
    @pytest.mark.table
    def test_iucn_status_data_presence(self, iucn_status_page):
        """
        Test that the IUCN Status table contains the expected conservation status data.
        
        IUCN Status definitions are standardized globally, so the table should contain
        the established set of conservation status categories. This test verifies that
        the reference data has been properly loaded and is available to users.
        
        Args:
            iucn_status_page: The IUCNStatusPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_iucn_status_data_presence")
        for isp in iucn_status_page:
            isp.page.wait_for_timeout(1000)
            row_count = isp.count_table_rows()
            check.greater(row_count, 0, 
                f"IUCN Status table should contain reference data, found {row_count} rows on {get_browser_name(isp.page)}")
            logger.info(f"Verification Successful :: IUCN Status Table has {row_count} rows on {get_browser_name(isp.page)}")
    
    @pytest.mark.UI
    @pytest.mark.iucn_status
    @pytest.mark.table
    def test_iucn_status_data_retrieval(self, iucn_status_page):
        """
        Test that IUCN Status names and data can be retrieved from the table.
        
        The ability to programmatically extract status information enables automated
        verification of data consistency and supports integration testing scenarios
        where status definitions need to be validated against external standards.
        
        Args:
            iucn_status_page: The IUCNStatusPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_iucn_status_data_retrieval")
        for isp in iucn_status_page:
            isp.page.wait_for_timeout(1000)
            # Test basic name retrieval
            status_names = isp.get_iucn_status_name_values()
            check.greater(len(status_names), 0, 
                f"Should retrieve IUCN Status names, found {len(status_names)} names on {get_browser_name(isp.page)}")
            
            # Verify that retrieved names are valid (non-empty strings)
            valid_names = [name for name in status_names if name and name.strip()]
            check.equal(len(valid_names), len(status_names), 
                f"All retrieved names should be valid, found {len(valid_names)} valid out of {len(status_names)} total on {get_browser_name(isp.page)}")
            
            # Verify that all expected status names are present
            for isp in iucn_status_page:
                isp.page.wait_for_timeout(1000)
                all_elements, missing_elements = isp.verify_all_iucn_status_present_in_table()
                check.is_true(all_elements, 
                    f"Missing IUCN Status names: {', '.join(missing_elements)} on {get_browser_name(isp.page)}")
                logger.info(f"Verification Successful :: All IUCN Status Names found on {get_browser_name(isp.page)}")