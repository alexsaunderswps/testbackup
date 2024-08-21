# videos_page.py
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

class VideosPage(BasePage):
    """_summary_

    Args:
        BasePage (_type_): _description_
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.locator = ElementLocator()
        self.interactor = ElementInteractor()
        self.screenshot = ScreenshotManager()
        self.logger = logger
        
    class VideoElements:
        FILTER_NAME_FIELD = "//div//input[@placeholder='Filter by name']"
        SEARCH_BUTTON = "//button[text()='Search']"
        CANCEL_BUTTON = "//div//button[2]"
        ADD_BUTTON = "//a[@href='/video/add']"
        
        
    class PaginationElements:
        PREVIOUS_PAGE = "//ul//a[@aria-label='Previous page']"
        NEXT_PAGE= "//ul//a[@aria-label='Next page']"
        CURRENT_PAGE = "//ul//a[@aria-current='page']"
        FW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump forward']"
        BW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump backward']"
        SHOWING_COUNT = "//span[contains(text(),'Showing')]"
        
        def get_page_locator(page_number):
            return f"//ul//a[@aria-label='Page 1']"
        