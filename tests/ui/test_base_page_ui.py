#test_base_page_ui.py
import pytest
from pytest_check import check
from page_objects.common.base_page import BasePage
from utilities.screenshot_manager import ScreenshotManager
from utilities.utils import logger

# Initialize Screenshot
screenshot = ScreenshotManager()

class TestBasePageUI:

    def _verify_page_nav_elements(self, base_page):
        """_summary_

        Args:
            page_element (_type_): _description_
        """
        logger.debug(f"Starting test_base_page_nav_elements for {base_page[0].__class__.__name__}")
        all_browsers_passed = True
        for index, bp in enumerate(base_page):
            logger.info(f"Testing nav elements on browser {index + 1}: {bp.driver.name}")
            success, missing = bp.verify_all_nav_elements_present()

            if success:
                logger.info(f"Verification Successful :: All Nav Elements found on {bp.driver.name}")
            else:
                logger.error(f"Verification Failed :: Missing Nav Elements: {', '.join(missing)} for {bp.driver.name}")
                all_browsers_passed = False
        logger.info("test_page_nav_elements: finished")
        return all_browsers_passed, "One or more browsers failed to find all nav elements"
        
    def _verify_page_admin_elements(self, base_page):
        """_summary_

        Args:
            page_element (_type_): _description_
        """
        logger.debug(f"Starting test_base_page_admin_elements for {base_page[0].__class__.__name__}")
        all_browsers_passed = True
        for index, bp in enumerate(base_page):
            logger.info(f"Testing admin elements on browser {index + 1}: {bp.driver.name}")
            success, missing = bp.verify_all_admin_links_present()

            if success:
                logger.info(f"Verification Successful :: All Admin Elements found on {bp.driver.name}")
            else:
                logger.error(f"Verification Failed :: Missing Admin Elements: {', '.join(missing)} for {bp.driver.name}")
                all_browsers_passed = False
        logger.info("test_page_admin_elements: finished")
        return all_browsers_passed, "One or more browsers failed to find all admin elements"

    def _verify_page_definition_elements(self, base_page):
        """_summary_

        Args:
            page_element (_type_): _description_
        """
        logger.debug(f"Starting test_base_page_definitions_elements for {base_page[0].__class__.__name__}")
        all_browsers_passed = True
        for index, bp in enumerate(base_page):
            logger.info(f"Testing admin elements on browser {index + 1}: {bp.driver.name}")
            success, missing = bp.verify_all_definition_links_present()

            if success:
                logger.info(f"Verification Successful :: All Admin Elements found on {bp.driver.name}")
            else:
                logger.error(f"Verification Failed :: Missing Admin Elements: {', '.join(missing)} for {bp.driver.name}")
                all_browsers_passed = False
        logger.info("test_page_admin_elements: finished")
        return all_browsers_passed, "One or more browsers failed to find all admin elements"
        
    def _verify_page_pagination_elements(self,base_page):
        """_summary_

        Args:
            base_page (_type_): _description_
        """
        logger.debug(f"Starting test_base_page_pagination_elements for {base_page[0].__class__.__name__}")
        all_browsers_passed = True
        for index, bp in enumerate(base_page):
            logger.info(f"Testing pagination elements on browser {index + 1}: {bp.driver.name}")
            success, missing = bp.verify_pagination_elements_present()

            if success:
                logger.info(f"Verification Successful :: All Pagination Elements found on {bp.driver.name}")
            else:
                logger.error(f"Verification Failed :: Missing Pagination Elements: {', '.join(missing)} for {bp.driver.name}")
                all_browsers_passed = False
        logger.info("test_page_pagination_elements: finished")
        return all_browsers_passed, "One or more browsers failed to find all pagination elements"
    
    @pytest.mark.base 
    def test_base_page_nav_elements(self, base_page):
        """_summary_

        Args:
            base_page (_type_): _description_
        """
        assert self._verify_page_nav_elements(base_page), "One or more browser failed to find all elements"
        
    @pytest.mark.base  
    def test_base_page_admin_elements(self, base_page):
        """_summary_

        Args:
            base_page (_type_): _description_
        """
        assert self._verify_page_admin_elements(base_page), "One or more browser failed to find all elements"
        
    @pytest.mark.base  
    def test_base_page_definition_elements(self, base_page):
        """_summary_

        Args:
            base_page (_type_): _description_
        """
        assert self._verify_page_definition_elements(base_page), "One or more browser failed to find all elements"
        
    @pytest.mark.base  
    def test_base_page_pagination_elements(self, base_page):
        """_summary_

        Args:
            base_page (_type_): _description_
        """
        assert self._verify_page_pagination_elements(base_page), "One or more browser failed to find all elements"