# devices_page.py
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
        SEARCH_TEXT = "//input[@placeholder='Filter by name']"
        SEARCH_BUTTON = "//button[text()='Search']"
        ADD_DEVICE_LINK = "//a[@href='/device/add']"
        
    class DeviceTableElements:
        """_summary_
        """
        DEVICE_TABLE_BODY = "//table//tbody"
        DEVICE_TABLE_ROWS = "//table//tbody/tr"
        DEVICE_NAME_HEADER = "//table//th[text()='Name']"
        DEVICE_SERIAL_HEADER = "//table//th[text()='Serial Number ']"
        DEVICE_INSTALLATION_HEADER = "//table//th[text()='Installation']"
        DEVICE_ORGANIZATION_HEADER = "//table//th[text()='Organization']"
        
    # Check Page Element presence
    def verify_page_title_present(self):
        """_summary_
        """
        return super().verify_page_title_present(self.DevicePageElements.DEVICES_PAGE_TITLE)
    
    def verify_all_devices_search_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected device search elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all exepcted device search elements are present")

        # Define elements with readable names
        search_elements = {
            "Search Text Box": self.DeviceSearchElements.SEARCH_TEXT,
            "Search Button": self.DeviceSearchElements.SEARCH_BUTTON,
            "Add Device Button": self.DeviceSearchElements.ADD_DEVICE_LINK,
        }
        
        return self.verify_page_elements_present(search_elements, "Device Search Elements")
    
    def verify_all_device_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected device table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Check if all Device Table elements are present")
        
        # Define elements with readable names
        table_elements = {
            "Table Body": self.DeviceTableElements.DEVICE_TABLE_BODY,
            "Table Rows": self.DeviceTableElements.DEVICE_TABLE_ROWS,
            "Device Name": self.DeviceTableElements.DEVICE_NAME_HEADER,
            "Device Serial": self.DeviceTableElements.DEVICE_SERIAL_HEADER,
            "Device Installation": self.DeviceTableElements.DEVICE_INSTALLATION_HEADER,
            "Device Organization": self.DeviceTableElements.DEVICE_ORGANIZATION_HEADER,
        }
        return self.verify_page_elements_present(table_elements, "Device Table Elements")