# devices_page.py
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

class DevicesPage(BasePage):
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
        
    class DevicePageElements:
        """_summary_
        """
        DEVICES_PAGE_TITLE = "//h1[text()='Devices']"
        
    class DeviceSearchElements:
        """_summary_
        """
        SEARCH_TEXT = '//input[@placeholder="Filter by name"]'
        SEARCH_BUTTON = "//button[text()='Search']"
        ADD_DEVICE_LINK = "//a[@href='/device/add']"
        
    class DeviceTableElements:
        """_summary_
        """
        DEVICE_TABLE_BODY = "//table//tbody"
        DEVICE_TABLE_ROWS = "//table//tbody/tr"
        DEVICE_NAME_HEADER = "//table//th[text()='Name']"
        DEVICE_SERIAL_HEADER = "//table//th[text()='Serial Number']"
        DEVICE_INSTALLTION_HEADER = "//table//th[text()='Installation']"
        DEVICE_ORGANIZATION_HEADER = "//table//th[text()='Organization']"
        
    # Check Page Element presence
    def verify_page_title_present(self):
        """_summary_
        """
        return super().verify_page_title_present(self.DevicePageElements.DEVICES_PAGE_TITLE)
    
    def verify_all_devices_search_elements_present(self) -> Tuple[bool,list]:
        """_summary_
        """
        self.logger.info("Verifying that all exepcted device search elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        search_elements = {
            "Search Text Box": self.DeviceSearchElements.SEARCH_TEXT,
            "Search Button": self.DeviceSearchElements.SEARCH_BUTTON,
            "Add Device Button": self.DeviceSearchElements.ADD_DEVICE_LINK,
        }
        for element_name, element_locator in search_elements.items():
            try:
                if self.locator.is_element_present(element_locator):
                    self.logger.info(f"Element found: {element_name}")
                else:
                    raise NoSuchElementException(f"Search Element not found: {element_name}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"device_search_elements_not_found: {element_name}")
                self.logger.error(f"Search Element not found: {element_name}")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to find search element: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
    def verify_all_device_table_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Returns:
            bool: _description_
        """
        self.logger.info("Check if all Device Table elements are present")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        table_elements = {
            "Table Body": self.DeviceTableElements.DEVICE_TABLE_BODY,
            "Table Rows": self.DeviceTableElements.DEVICE_TABLE_ROWS,
            "Device Name": self.DeviceTableElements.DEVICE_NAME_HEADER,
            "Device Serial": self.DeviceTableElements.DEVICE_SERIAL_HEADER,
            "Device Installation": self.DeviceTableElements.DEVICE_INSTALLTION_HEADER,
            "Device Organization": self.DeviceTableElements.DEVICE_ORGANIZATION_HEADER,
        }
        for element_name, table_element in table_elements.items():
            try:
                if self.locator.is_element_presnet(table_element):
                    self.logger.info(f"Table element found: {element_name}")
                else:
                    raise NoSuchElementException(f"Table Element not found: {element_name}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"device_table_elements_not_found: {element_name}")
                self.logger.error(f"Table Element not found: {element_name}")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to find table element: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements