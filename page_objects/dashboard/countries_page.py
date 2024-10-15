# countries_page.py
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

class CountriesPage(BasePage):
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
        self.screenshot = ScreenshotManager(driver)
        self.logger = logger
        
    class CountryPageElements:
        """_summary_

        Args:
            object (_type_): _description_
        """
        COUNTRIES_PAGE_TITLE = "//h1[contains(text(),'Countries')]"
        
    class CountryTableElemenets:
        COUNTRIES_TABLE_SEARCH = "//input[@placeholder='Search...']"
        COUNTRIES_TABLE_BODY = "//table//tbody"
        COUNTRIES_TABLE_ROWS = "//table//tbody/tr"
        # COUNTRIES_TABLE_COLUMNS = 
        # COUNTRIES_TABLE_HEADER = 
        # COUNTRIES_TABLE_FOOTER = 
        
    # Check Element presence
    def verify_page_title_present(self) -> bool:
        """_summary_

        Returns:
            _type_: _description_
        """
        self.logger.info("Checking if Countries Page Title is present")
        try:
            if self.locator.is_element_present(self.CountryPageElements.COUNTRIES_PAGE_TITLE):
                logger.info("Countries Page Title was located successfully")
                return True
            else:
                raise NoSuchElementException("Countries Page Title not found")
        except NoSuchElementException:
            self.screenshot.take_screenshot(self.driver, "Countries_Page_Title_Not_Found")
            self.logger.error("Could not find Countries Page title on page")
            return False
        except Exception as e:
            self.logger.error(f"An error occurred while trying to locate Countries Page Title: {e}")
            return False
        
    def verify_all_nav_elements_present(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        self.logger.info("Verifying all expected navigation elements are present on: Countries page")
        all_elements_present = True
        missing_elements = []
        for page_element in [self.CommonLocators.HEADER_LOGO,
                        self.CommonLocators.LOGOUT_BUTTON,
                        self.NavigationLocators.VIDEOS_LINK,
                        self.NavigationLocators.VIDEO_CATALOGUES_LINK,
                        self.NavigationLocators.MAP_MARKERS_LINK,
                        self.NavigationLocators.USERS_LINK,
                        self.NavigationLocators.DEFINITIONS_BUTTON,
                        self.NavigationLocators.ORGS_LINK,
                        self.NavigationLocators.INSTA_LINK,
        ]:
            try:
                if self.locator.is_element_present(page_element):
                    self.logger.info(f"Element {page_element} was located successfully")
                else:
                    raise NoSuchElementException(f"Element {page_element} not found")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{page_element}_Not_Found")
                self.logger.error(f"Could not find {page_element} on page")
                all_elements_present = False
                missing_elements.append(page_element)
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
                missing_elements.append(page_element)
        if not all_elements_present:
            self.logger.error(f"Missing elements: {', '.join(missing_elements)}")
        return all_elements_present
    