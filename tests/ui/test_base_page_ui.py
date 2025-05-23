#test_base_page_ui.py (Playwright version)

import pytest
from pytest_check import check
from page_objects.common.base_page import BasePage
from utilities.utils import get_browser_name, logger

class TestBasePageUI:
    """
    Base class for UI tests that provides common verification methods.
    
    This class is designed to be inherited by specific page test classes
    to provide reusable verification methods for common UI elements.
    """

    def _verify_page_nav_elements(self, base_page) -> bool:
        """
        Verify that all navigation elements are present on each page.
        
        Args:
            base_pages (List[BasePage]): A list of page objects to check
            
        Returns:
            bool: True if all elements were found on all pages, False otherwise
        """
        logger.debug(f"Starting test_base_page_nav_elements for {base_page[0].__class__.__name__}")
        all_browsers_passed = True
        
        for index, bp in enumerate(base_page):

            logger.info(f"Testing nav elements on browser: {get_browser_name(bp.page)}")
            success, missing = bp.verify_all_nav_elements_present()

            if success:
                logger.info(f"Verification Successful :: All Nav Elements found on {get_browser_name(bp.page)}")
            else:
                logger.error(f"Verification Failed :: Missing Nav Elements: {', '.join(missing)} for {get_browser_name(bp.page)}")
                all_browsers_passed = False
                
        logger.info("test_page_nav_elements: finished")
        return all_browsers_passed
        
    def _verify_page_admin_elements(self, base_page) -> bool:
        """
        Verify that all admin dropdown elements are present on each page.
        
        Args:
            base_pages (List[BasePage]): A list of page objects to check
            
        Returns:
            bool: True if all elements were found on all pages, False otherwise
        """
        logger.debug(f"Starting test_base_page_admin_elements for {base_page[0].__class__.__name__}")
        all_browsers_passed = True
        
        for index, bp in enumerate(base_page):

            logger.info(f"Testing admin elements on browser: {get_browser_name(bp.page)}")
            success, missing = bp.verify_all_admin_elements_present()

            if success:
                logger.info(f"Verification Successful :: All Admin Elements found on {get_browser_name(bp.page)}")
            else:
                logger.error(f"Verification Failed :: Missing Admin Elements: {', '.join(missing)} for {get_browser_name(bp.page)}")
                all_browsers_passed = False
                
        logger.info("test_page_admin_elements: finished")
        return all_browsers_passed

    def _verify_page_definition_elements(self, base_page) -> bool:
        """
        Verify that all definition dropdown elements are present on each page.
        
        Args:
            base_pages (List[BasePage]): A list of page objects to check
            
        Returns:
            bool: True if all elements were found on all pages, False otherwise
        """
        logger.debug(f"Starting test_base_page_definitions_elements for {base_page[0].__class__.__name__}")
        all_browsers_passed = True
        
        for index, bp in enumerate(base_page):

            logger.info(f"Testing admin elements on browser: {get_browser_name(bp.page)}")
            success, missing = bp.verify_all_definition_elements_present()

            if success:
                logger.info(f"Verification Successful :: All Admin Elements found on {get_browser_name(bp.page)}")
            else:
                logger.error(f"Verification Failed :: Missing Admin Elements: {', '.join(missing)} for {get_browser_name(bp.page)}")
                all_browsers_passed = False
                
        logger.info("test_page_admin_elements: finished")
        return all_browsers_passed

    def _verify_page_pagination_elements(self, base_page) -> bool:
        """
        Verify that all pagination elements are present on each page.
        
        Args:
            base_pages (List[BasePage]): A list of page objects to check
            
        Returns:
            bool: True if all elements were found on all pages, False otherwise
        """
        logger.debug(f"Starting test_base_page_pagination_elements for {base_page[0].__class__.__name__}")
        all_browsers_passed = True
        
        for index, bp in enumerate(base_page):

            logger.info(f"Testing pagination elements on browser: {get_browser_name(bp.page)}")
            success, missing = bp.verify_all_pagination_elements_present()

            if success:
                logger.info(f"Verification Successful :: All Pagination Elements found on {get_browser_name(bp.page)}")
            else:
                logger.error(f"Verification Failed :: Missing Pagination Elements: {', '.join(missing)} for {get_browser_name(bp.page)}")
                all_browsers_passed = False
                
        logger.info("test_page_pagination_elements: finished")
        return all_browsers_passed
    
    @pytest.mark.base
    def test_base_page_nav_elements(self, base_page):
        """
        Test that all navigation elements are present on the base page.
        
        Args:
            base_page (List[BasePage]): A list of base page objects to check
        """
        assert self._verify_page_nav_elements(base_page), "One or more browser failed to find all elements"
        
    @pytest.mark.base  
    def test_base_page_admin_elements(self, base_page):
        """
        Test that all admin elements are present on the base page.
        
        Args:
            base_page (List[BasePage]): A list of base page objects to check
        """
        assert self._verify_page_admin_elements(base_page), "One or more browser failed to find all elements"
        
    @pytest.mark.base  
    def test_base_page_definition_elements(self, base_page):
        """
        Test that all definition elements are present on the base page.
        
        Args:
            base_page (List[BasePage]): A list of base page objects to check
        """
        assert self._verify_page_definition_elements(base_page), "One or more browser failed to find all elements"
        
    @pytest.mark.base  
    def test_base_page_pagination_elements(self, base_page):
        """
        Test that all pagination elements are present on the base page.
        
        Args:
            base_page (List[BasePage]): A list of base page objects to check
        """
        assert self._verify_page_pagination_elements(base_page), "One or more browser failed to find all elements"