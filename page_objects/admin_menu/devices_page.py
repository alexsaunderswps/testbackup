# devices_page.py
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

    class PaginationElements:
        PREVIOUS_PAGE = "//ul//a[@aria-label='Previous page']"
        PREVIOUS_PAGE_DISABLED = "//ul//a[@aria-label='Previous page']"
        NEXT_PAGE = "//ul//a[@aria-lable='Next page']"
        CURRENT_PAGE = "//ul//a[@aria-current='page']"
        FW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump forward']"
        BW_BREAK_ELIPSPS = "//ul//a[@aria-label='Jump backward']"
        SHOWING_COUNT = "//span[contains(text(), 'Showing')]"
        
    # Check Page Element presence
    def verify_page_title_present(self):
        """_summary_
        """
        return super().verify_page_title_present(self.DevicePageElements.DEVICES_PAGE_TITLE)
    
    def verify_all_devices_search_elements_present(self) -> bool:
        """_summary_
        """
        self.logger.info("Verifying that all exepcted device search elements are present")
        all_elements_present = True
        
        for search_element in [self.DeviceSearchElements.SEARCH_TEXT,
                            self.DeviceSearchElements.SEARCH_BUTTON,
                            self.DeviceSearchElements.ADD_DEVICE_LINK,
        ]:
            try:
                if self.locator.is_element_present(search_element):
                    self.logger.info(f"Element found: {search_element}")
                else:
                    raise NoSuchElementException(f"Search Element not found: {search_element}")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, "device_search_elements_not_found: {search_element}")
                self.logger.error(f"Search Element not found: {search_element}")
                all_elements_present = False
            except Exception as e:
                self.logger.error(f"Unexpected error while trying to find search element: {str(e)}")
                all_elements_present = False
            return all_elements_present