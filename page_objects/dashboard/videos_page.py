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
        self.locator = ElementLocator(driver)
        self.interactor = ElementInteractor(driver)
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
        return f"//ul//a[@aria-label='Page {page_number}']"
            
    def check_current_page(page_number):
        return f"//ul//a[@aria-label='Page {page_number} is your current page']"
        
    def verify_all_nav_elements_present(self) -> bool:

        self.logger.info("Verifying that all expected navigation elements are present on: Videos Page")
        try:
            for page_element in [self.CommonLocators.HEADER_LOGO,
                            self.CommonLocators.LOGOUT_BUTTON,
                            self.NavigationLocators.VIDEOS_LINK,
                            self.NavigationLocators.COLLECTIONS_LINK,
                            self.NavigationLocators.PORTALS_LINK,
                            self.NavigationLocators.USERS_LINK,
                            self.NavigationLocators.DEFINITIONS_BUTTON,
                            self.NavigationLocators.ORGS_LINK,
                            self.NavigationLocators.INSTA_LINK,
                            ]:
                self.locator.check_elements_present(page_element)
                self.logger.info(f"{page_element} was located successfully.")
            return True
        except NoSuchElementException:
            self.logger.error(f"Could not find {page_element} on page.")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while finding elements: {str(e)}")
            return False
        
    def verify_all_definition_links_present(self) -> bool:

        self.logger.info("Verifying that all expected naivigation elements are present in: Definintions Dropdown")
        try:
            self.interactor.element_click(self.NavigationLocators.DEFINITIONS_BUTTON)
            for page_element in [self.NavigationLocators.COUNTRIES_LINK,
                            self.NavigationLocators.IUCNSTATUS_LINK,
                            self.NavigationLocators.POP_TREND_LINK,
                            self.NavigationLocators.SPECIES_LINK,
                            self.NavigationLocators.TAGS_LINK,
                            ]:
                self.locator.check_elements_present(page_element)
                self.logger.info(f"{page_element} was located successfully.")
            self.interactor.element_click(self.NavigationLocators.DEFINITIONS_BUTTON)
            return True
        except NoSuchElementException:
            self.logger.error(f"Could not find {page_element} on page.")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while finding elements: {str(e)}")
            return False
    
    def verify_all_video_search_elements_present(self) -> bool:

        self.logger.info("Verifying that all expected video search elements are present in: Definintions Dropdown")
        try:
            for page_element in [self.VideoElements.FILTER_NAME_FIELD,
                            self.VideoElements.SEARCH_BUTTON,
                            self.VideoElements.CANCEL_BUTTON,
                            self.VideoElements.ADD_BUTTON,
                            ]:
                self.locator.check_elements_present(page_element)
                self.logger.info(f"{page_element} was located successfully.")
            return True
        except NoSuchElementException:
            self.logger.error(f"Could not find {page_element} on page.")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while finding elements: {str(e)}")
            return False
    
    def verify_all_video_pagination_elements_present(self) -> bool:

        self.logger.info("Verifying that all expected pagination elements are present in: Definintions Dropdown")
        try:
            for page_element in [self.PaginationElements.PREVIOUS_PAGE,
                            self.PaginationElements.CURRENT_PAGE,
                            self.PaginationElements.FW_BREAK_ELIPSIS,
                            self.PaginationElements.NEXT_PAGE,
                            self.PaginationElements.SHOWING_COUNT
                            ]:
                self.locator.check_elements_present(page_element)
                self.logger.info(f"{page_element} was located successfully.")
            return True
        except NoSuchElementException:
            self.logger.error(f"Could not find {page_element} on page.")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while finding elements: {str(e)}")
            return False
    
