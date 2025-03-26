# video_catalogues_page.py
import os
from dotenv import load_dotenv
from typing import Tuple
from page_objects.common.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT
from utilities.utils import logger
from utilities.element_interactor import ElementInteractor
from utilities.element_locator import ElementLocator
from utilities.screenshot_manager import ScreenshotManager

load_dotenv()

# Environmental Variables
BASE_URL = os.getenv("QA_BASE_URL")

class VideoCataloguesPage(BasePage):
    """_summary_

    Args:
        BasePage (_type_): _description_
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.locator = ElementLocator(driver)
        self.interactor = ElementInteractor(driver)
        self.screenshot = ScreenshotManager()
        self.logger = logger
        
    class VideoCataloguesPageElements:
        """_summary_
        """
        VIDEO_CATALOGUES_PAGE_TITLE = "//h1[contains(text(),'Video Catalogues')]"

    class VideoCataloguesSearchElements:
        """_summary_
        """
        SEARCH_TEXT = "//input[@placeholder='Filter by name']"
        SEARCH_BUTTON = "//button[text()='Search']"
        ADD_VIDEO_CATALOGUE_LINK = "//a[@href='/videoCatalogue/add']"
        

    class VideoCataloguesTableElements:
        """_summary_
        """
        CATALOGUE_TABLE_BODY = "//table/tbody"
        CATAGLOUE_TABLE_ROWS = "//table//tbody/tr"
        CATALOGUE_NAME_HEADER = "//table/thead/tr/th/div[text()='Name']"
        CATALOGUE_ORGANIZATION_HEADER = "//table/thead/tr/th[text()='Organization']"
        CATALGOUE_DESCRIPTION_HEADER = "//table/thead/tr/th/div[text()='Description']"
        CATALOGUE_LAST_EDITED_BY_HEADER = "//table/thead/tr/th[text()='Last Edited By']"
        CATALOGUE_LAST_EDITED_DATE_HEADER = "//table/thead/tr/th[text()='Last Edited Date']"
    
    class VideoCataloguesSortingElements:
        """_summary_
        """
        NAME_SORT = "//table//div[text()='Name']//button//i"
        
    # Check Title Element presence

    def verify_page_title_present(self):
        """_summary_
        """
        return super().verify_page_title_present(self.VideoCataloguesPageElements.VIDEO_CATALOGUES_PAGE_TITLE)
    
    # Check Search Elements
    
    def verify_all_catalgoue_search_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
            Tuple[bool, list]: _description_
        """
        self.logger.info("Verifying that all expected video catalogue search elements are present in: Video Catalogues Page")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        search_elements ={
            "Search Text": self.VideoCataloguesSearchElements.SEARCH_TEXT,
            "Search Button": self.VideoCataloguesSearchElements.SEARCH_BUTTON,
            "Add Video Catalogue Link": self.VideoCataloguesSearchElements.ADD_VIDEO_CATALOGUE_LINK
        }
        for element_name, search_locator in search_elements.items():
            try:
                if self.locator.is_element_present(search_locator):
                    self.logger.info(f"Search element found: {element_name} on Video Catalogues Page")
                else:
                    raise NoSuchElementException(f"Search element not found: {element_name} on Video Catalogues Page")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Video_Catalogue_Search_{element_name}_Not_Found")
                self.logger.error(f"Search element not found: {element_name} on Video Catalogues Page")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate search element: {str(e)} on Video Catalogues Page")
                all_elements_present = False
                missing_elements.append(element_name)
            return all_elements_present, missing_elements
        
    # Check Table Elements
    
    def verify_all_catalogue_table_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
            Tuple[bool, list]: _description_
        """
        self.logger.info("Checking if all Video Catalogue table elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        table_elements ={
            "Name Header": self.VideoCataloguesTableElements.CATALOGUE_NAME_HEADER,
            "Organization Header": self.VideoCataloguesTableElements.CATALOGUE_ORGANIZATION_HEADER,
            "Description Header": self.VideoCataloguesTableElements.CATALGOUE_DESCRIPTION_HEADER,
            "Last Edited By Header": self.VideoCataloguesTableElements.CATALOGUE_LAST_EDITED_BY_HEADER,
            "Last Edited Date Header": self.VideoCataloguesTableElements.CATALOGUE_LAST_EDITED_DATE_HEADER,
            "Name Sorting Button": self.VideoCataloguesSortingElements.NAME_SORT
        }
        for element_name, table_locator in table_elements.items():
            try:
                if self.locator.is_element_present(table_locator):
                    self.logger.info(f"Element found: {element_name} in Video Catalogues Table")
                else:
                    raise NoSuchElementException(f"Element not found: {element_name} in Video Catalogues Table")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Video_Catalogue_Table_Element_Not_Found_{element_name}")
                self.logger.error(f"Element not found: {element_name} in Video Catalogues table")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate element: {str(e)} in Video Catalogues Table")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements