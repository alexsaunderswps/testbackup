# map_markers_page.py
import os
from dotenv import load_dotenv
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
        MAP_MARKERS_ICON_HEADER = "//table//div[text()='Icon']"
        MAP_MARKER_NAME_HEADER = "//table//div[text()='Name']"
        MAP_MARKER_DESCRIPTION_HEADER = "//table//div[text()='Description']"
        MAP_MARKER_ORGANIZATION_HEADER = "//table//th[text()='Organization']"
        MAP_MARKER_VIDEOS_HEADER = "//table//th[text()='Videos']"
        MAP_MARKER_LOCATIONS_HEADER = "//table//th[text()='Location']"
        # MAP_MARKERS_TABLE_HEADER = 
        # MAP_MARKERS_TABLE_FOOTER = 
        
    # Check Page Element presence
    def verify_page_title_present(self) -> bool:
        """Checks if the Map Markers Page Title is present
        
        Returns:
            bool: True if the Map Markers Page Title is present, False otherwise
        """
        self.logger.info("Checking if Map Markers Page Title is present")
        try:
            if self.locator.is_element_present(self.MapMarkersPageElements.MAP_MARKERS_PAGE_TITLE):
                logger.info("Map Markers Page Title was located successfully")
                return True
            else:
                raise NoSuchElementException("Map Markers Page Title not found")
        except NoSuchElementException:
            self.screenshot.take_screenshot(self.driver, "Map_Markers_Page_Title_Not_Found")
            self.logger.error("Could not find Map Markers Page title on page")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while trying to locate Map Markers Page Title: {str(e)}")
            return False

    def verify_all_core_map_marker_table_elements_present(self) -> bool:
        """_summary_
        
        Returns:
            _type_: _description_
        """
        self.logger.info("Checking if all Video Table elements are present")
        all_elements_present = True
        
        for page_element in [self.MapMarkersTableElemenets.MAP_MARKERS_ICON_HEADER,
                                self.MapMarkersTableElemenets.MAP_MARKER_NAME_HEADER,
                                self.MapMarkersTableElemenets.MAP_MARKER_DESCRIPTION_HEADER,
                                self.MapMarkersTableElemenets.MAP_MARKER_VIDEOS_HEADER,
                                self.MapMarkersTableElemenets.MAP_MARKER_LOCATIONS_HEADER
        ]:
            self.interactor.element_click(self.MapMarkersPageElements.MAP_MARKERS_CORE_TAB)
            try:
                if self.locator.is_element_present(page_element):
                    self.logger.info(f"Element found: {page_element}")
                else:
                    raise NoSuchElementException(f"Element not found: {page_element}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Map_Markers_Core_Table_Element_Not_Found")
                self.logger.error(f"Element not found: {page_element}")
                all_elements_present = False
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate element: {str(e)}")
                all_elements_present = False
        return all_elements_present

    def verify_all_custom_map_marker_table_elements_present(self) -> bool:
        """_summary_
        
        Returns:
            _type_: _description_
        """
        self.logger.info("Checking if all Video Table elements are present")
        all_elements_present = True
        
        for page_element in [self.MapMarkersTableElemenets.MAP_MARKERS_ICON_HEADER,
                                self.MapMarkersTableElemenets.MAP_MARKER_NAME_HEADER,
                                self.MapMarkersTableElemenets.MAP_MARKER_DESCRIPTION_HEADER,
                                self.MapMarkersTableElemenets.MAP_MARKER_VIDEOS_HEADER,
                                self.MapMarkersTableElemenets.MAP_MARKER_ORGANIZATION_HEADER,
                                self.MapMarkersTableElemenets.MAP_MARKER_LOCATIONS_HEADER
        ]:
            self.interactor.element_click(self.MapMarkersPageElements.MAP_MARKERS_CUSTOM_TAB)
            try:
                if self.locator.is_element_present(page_element):
                    self.logger.info(f"Element found: {page_element}")
                else:
                    raise NoSuchElementException(f"Element not found: {page_element}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Map_Markers_Core_Table_Element_Not_Found")
                self.logger.error(f"Element not found: {page_element}")
                all_elements_present = False
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to locate element: {str(e)}")
                all_elements_present = False
        return all_elements_present
    

            