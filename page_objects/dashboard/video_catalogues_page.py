# video_catalogues_page.py
import os
from dotenv import load_dotenv
from typing import Tuple, List
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
    
    def verify_all_catalogue_search_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected video catalogue search elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected video catalogue search elements are present in: Video Catalogues Page")

        # Define elements with readable names
        search_elements ={
            "Search Text": self.VideoCataloguesSearchElements.SEARCH_TEXT,
            "Search Button": self.VideoCataloguesSearchElements.SEARCH_BUTTON,
            "Add Video Catalogue Link": self.VideoCataloguesSearchElements.ADD_VIDEO_CATALOGUE_LINK
        }
        return self.verify_page_elements_present(search_elements, "Video Catalogue Search Elements")
        
    # Check Table Elements
    
    def verify_all_catalogue_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected video catalogue table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Checking if all Video Catalogue table elements are present")

        # Define elements with readable names
        table_elements ={
            "Name Header": self.VideoCataloguesTableElements.CATALOGUE_NAME_HEADER,
            "Organization Header": self.VideoCataloguesTableElements.CATALOGUE_ORGANIZATION_HEADER,
            "Description Header": self.VideoCataloguesTableElements.CATALGOUE_DESCRIPTION_HEADER,
            "Last Edited By Header": self.VideoCataloguesTableElements.CATALOGUE_LAST_EDITED_BY_HEADER,
            "Last Edited Date Header": self.VideoCataloguesTableElements.CATALOGUE_LAST_EDITED_DATE_HEADER,
            "Name Sorting Button": self.VideoCataloguesSortingElements.NAME_SORT
        }
        return self.verify_page_elements_present(table_elements, "Video Catalogue Table Elements")