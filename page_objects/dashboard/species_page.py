# species_page.py
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

class SpeciesPage(BasePage):
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
        
        class SpeciesPageElements:
            """_summary_
            """
            SPECIES_PAGE_TITLE = "//h1[text()='Species']"
            SEARCH_TEXT = '//input[@placeholder="Filter by name"]'
            SEARCH_BUTTON = "//button[text()='Search']"
            ADD_SPECIES_LINK = "//a[@href='/species/add']"

        class SpeciesTableElements:
            """_summary_
            """
            SPECIES_TABLE_BODY = "//table//tbody"
            SPECIES_TABLE_ROWS = "//table//tbody/tr"
            SPECIES_NAME_HEADER = "//table//div[text()='Name']"
            SPECIES_COLLOQUIAL_HEADER = "//table//div[text()='Colloquial Name']"
            SPECIES_SCIENTIFIC_HEADER = "//table//th[text()='Scientific Name']"
            SPECIES_DESCRIPTION_HEADER = "//table//th[text()='Description']"
            SPECIES_IUCN_HEADER = "//table//th[text()='IUCN Status']"
            SPECIES_POPULATION_HEADER = "//table//th[text()='Population Trend']"
            SPECIES_CATEGORY_HEADER = "//table//th[text()='Species Category']"
            
        class PaginationElements:
            PREVIOUS_PAGE = "//ul//a[@aria-label='Previous page']"
            PREVIOUS_PAGE_DISABLED = "//ul//a[@aria-label='Previous page']"
            NEXT_PAGE= "//ul//a[@aria-label='Next page']"
            CURRENT_PAGE = "//ul//a[@aria-current='page']"
            FW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump forward']"
            BW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump backward']"
            SHOWING_COUNT = "//span[contains(text(),'Showing')]"