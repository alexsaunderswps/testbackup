# iucn_status_page.py
import os
from typing import Tuple, List
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

class IUCNStatusPage(BasePage):
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
    
    class IUCNStatusPageElements:
        """_summary_
        """
        IUCN_STATUS_PAGE_TITLE = "//h1[contains(text(),'IUCN Status')]"
        
    class IUCNStatusTableElemenets:
        IUCN_STATUS_TABLE_BODY = "//table//tbody"
        IUCN_STUTUS_TABLE_ROWS = "//table//tbody/tr"
        
    # Check IUCN Status Page Title presence
    
    def verify_iucn_page_title_present(self):
        """_summary_
        """
        return super().verify_page_title_present(self.IUCNStatusPageElements.IUCN_STATUS_PAGE_TITLE)
    
    # Check IUCN Status Table presence
    
    def verify_iucn_page_table_elements_present(self) -> Tuple[bool, List[str]]:
        """_summary_
        """
        self.logger.info("Checking IUCN Status Table Elements")

        #Define elements with readable names
        table_elements = {
            "IUCN Table Body": self.IUCNStatusTableElemenets.IUCN_STATUS_TABLE_BODY,
            "IUCN Table Rows": self.IUCNStatusTableElemenets.IUCN_STUTUS_TABLE_ROWS
        }
        return self.verify_page_elements_present(table_elements, "IUCN Table Elements")