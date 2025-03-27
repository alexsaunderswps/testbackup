# map_markers_page.py
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

class MapMarkersPage(BasePage):
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
        
    class MapMarkersPageElements:
        """_summary_
        
        Args:
            object (_type_): _description_
        """
        MAP_MARKERS_PAGE_TITLE = "//h1[contains(text(),'Map Marker')]"
        MAP_MARKERS_CORE_TAB = "//label[(text()='Map Markers')]"
        MAP_MARKERS_CUSTOM_TAB = "//label[(text()='Custom Map Markers')]"
        ADD_MAP_MARKER_LINK = "//a[contains(text(),'Add Map Marker')]"
        
    class MapMarkersTableElements:
        MAP_MARKERS_TABLE_BODY = "//table//tbody"
        MAP_MARKERS_TABLE_ROWS = "//table//tbody/tr"
        MAP_MARKERS_ICON_HEADER = "//table/thead/tr/th/div[text()='Icon']"
        MAP_MARKER_NAME_HEADER = "//table/thead/tr/th/div[text()='Name']"
        MAP_MARKER_DESCRIPTION_HEADER = "//table/thead/tr/th/div[text()='Description']"
        MAP_MARKER_ORGANIZATION_HEADER = "//table/thead/tr/th[text()='Organization']"
        MAP_MARKER_VIDEOS_HEADER = "//table/thead/tr/th[text()='Videos']"
        MAP_MARKER_LOCATION_HEADER = "//table/thead/tr/th[text()='Location']"
        # MAP_MARKERS_TABLE_HEADER = 
        # MAP_MARKERS_TABLE_FOOTER = 
        
    # Check Title Element presence
    
    def verify_page_title_present(self):
        return super().verify_page_title_present(self.MapMarkersPageElements.MAP_MARKERS_PAGE_TITLE)
    
    # Check Action Elements
    
    def verify_all_map_marker_action_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected map marker action elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifiying that all expected Map Marker action elements are present")

        # Define elements with readable names
        action_elements = {
            "Core Tab": self.MapMarkersPageElements.MAP_MARKERS_CORE_TAB,
            "Custom Tab": self.MapMarkersPageElements.MAP_MARKERS_CUSTOM_TAB,
            "Add Map Marker Link": self.MapMarkersPageElements.ADD_MAP_MARKER_LINK
        }
        return self.verify_page_elements_present(action_elements, "Map Marker Action Elements")
    
    # Check Table Elements

    def verify_all_core_map_marker_table_elements_present(self) -> Tuple[bool, list]:
        """
        Verify that all expected core map marker table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Checking if all Map Marker Core elements are present")

        # Define elements with readable names
        core_table_elements = {
            "Icon Header": self.MapMarkersTableElements.MAP_MARKERS_ICON_HEADER,
            "Name Header": self.MapMarkersTableElements.MAP_MARKER_NAME_HEADER,
            "Description Header": self.MapMarkersTableElements.MAP_MARKER_DESCRIPTION_HEADER,
            "Videos Header": self.MapMarkersTableElements.MAP_MARKER_VIDEOS_HEADER,
            "Location Header": self.MapMarkersTableElements.MAP_MARKER_LOCATION_HEADER
        }
        return self.verify_page_elements_present(core_table_elements, "Map Marker Core Table Elements")

    def verify_all_custom_map_marker_table_elements_present(self) -> Tuple[bool, list]:
        """
        Verify that all expected custom map marker table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Checking if all Custom Map Marker elements are present")
        self.interactor.element_click(self.MapMarkersPageElements.MAP_MARKERS_CUSTOM_TAB)
        # Define elements with readable names
        custom_table_elements = {
            "Custom MM Icon Header": self.MapMarkersTableElements.MAP_MARKERS_ICON_HEADER,
            "Custom MM Name Header": self.MapMarkersTableElements.MAP_MARKER_NAME_HEADER,
            "Custom MM Decription Header": self.MapMarkersTableElements.MAP_MARKER_DESCRIPTION_HEADER,
            "Custom MM Videos Header": self.MapMarkersTableElements.MAP_MARKER_VIDEOS_HEADER,
            "Custom MM Organization Header": self.MapMarkersTableElements.MAP_MARKER_ORGANIZATION_HEADER,
            "Custom MM Location Header": self.MapMarkersTableElements.MAP_MARKER_LOCATION_HEADER
        }
        return self.verify_page_elements_present(custom_table_elements, "Map Marker Custom Table Elements")
    

            