# map_markers_page.py
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
        
    class MapMarkersTableElemenets:
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
        
    # Check Page Element presence
    
    def verify_page_title_present(self):
        return super().verify_page_title_present(self.MapMarkersPageElements.MAP_MARKERS_PAGE_TITLE)
    
    def verify_all_map_marker_action_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
            Tuple[bool, list]: _description_
        """
        self.logger.info("Verifiying that all expected Map Marker action elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        action_elements = {
            "Core Tab": self.MapMarkersPageElements.MAP_MARKERS_CORE_TAB,
            "Custom Tab": self.MapMarkersPageElements.MAP_MARKERS_CUSTOM_TAB,
            "Add Map Marker Link": self.MapMarkersPageElements.ADD_MAP_MARKER_LINK
        }
        for element_name, action_element in action_elements.items():
            try:
                if self.locator.is_element_present(action_element):
                    self.logger.info(f"Element found: {element_name} on Map Markers Page")
                else:
                    raise NoSuchElementException(f"Element not found: {element_name} on Map Markers Page")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Map_Markers_Page_Element_Not_Found_{element_name}")
                self.logger.error(f"Element not found: {element_name} on Map Markers Page")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate element: {str(e)} on Map Markers Page")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements

    def verify_all_core_map_marker_table_elements_present(self) -> Tuple[bool, list]:
        """_summary_
        
        Returns:
            _type_: _description_
        """
        self.logger.info("Checking if all Map Marker Core elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        core_table_elements = {
            "Icon Header": self.MapMarkersTableElemenets.MAP_MARKERS_ICON_HEADER,
            "Name Header": self.MapMarkersTableElemenets.MAP_MARKER_NAME_HEADER,
            "Description Header": self.MapMarkersTableElemenets.MAP_MARKER_DESCRIPTION_HEADER,
            "Videos Header": self.MapMarkersTableElemenets.MAP_MARKER_VIDEOS_HEADER,
            "Location Header": self.MapMarkersTableElemenets.MAP_MARKER_LOCATION_HEADER
        }
        self.interactor.element_click(self.MapMarkersPageElements.MAP_MARKERS_CORE_TAB)
        for element_name, core_element in core_table_elements.items():
            try:
                if self.locator.is_element_present(core_element):
                    self.logger.info(f"Element found: {element_name} on Map Markers Core Table")
                else:
                    raise NoSuchElementException(f"Element not found: {element_name} on Map Markers Core Table")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Map_Markers_Core_Table_Element_Not_Found_{element_name}")
                self.logger.error(f"Element not found: {element_name} on Map Markers Core Table")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate element: {str(e)} on Map Markers Core Table")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements

    def verify_all_custom_map_marker_table_elements_present(self) -> Tuple[bool, list]:
        """_summary_
        
        Returns:
            _type_: _description_
        """
        self.logger.info("Checking if all Custom Map Marker elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        custom_table_elements = {
            "Custom MM Icon Header": self.MapMarkersTableElemenets.MAP_MARKERS_ICON_HEADER,
            "Custom MM Name Header": self.MapMarkersTableElemenets.MAP_MARKER_NAME_HEADER,
            "Custom MM Decription Header": self.MapMarkersTableElemenets.MAP_MARKER_DESCRIPTION_HEADER,
            "Custom MM Videos Header": self.MapMarkersTableElemenets.MAP_MARKER_VIDEOS_HEADER,
            "Custom MM Organization Header": self.MapMarkersTableElemenets.MAP_MARKER_ORGANIZATION_HEADER,
            "Custom MM Location Header": self.MapMarkersTableElemenets.MAP_MARKER_LOCATION_HEADER
        }
        self.interactor.element_click(self.MapMarkersPageElements.MAP_MARKERS_CUSTOM_TAB)
        for element_name, custom_element in custom_table_elements.items():
            try:
                if self.locator.is_element_present(custom_element):
                    self.logger.info(f"Element found: {element_name} on Custom Map Markers Table")
                else:
                    raise NoSuchElementException(f"Element not found: {element_name} on Custom Map Markers Table")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Map_Markers_Custom_Table_Element_Not_Found_{element_name}")
                self.logger.error(f"Element not found: {element_name} on Custom Map Markers Table")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate element: {str(e)} on Custom Map Markers Table")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    

            