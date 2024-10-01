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
        
    class VideoTableElements:
        VIDEO_TABLE_BODY = "//table//tbody"
        THUMBNAIL_HEADER = "//table//th[text()='Thumbnail']"
        NAME_HEADER = "//table//div[text()='Name']"
        PUBLISHED_HEADER = "//table//div[text()='Published']"
        DESCRIPTION_HEADER = "//table//th[text()='Description']"
        COUNTRY_HEADER = "//table//th[text()='Country']"
        VIDEO_TABLE_ROW = "//table//tbody/tr"
    
    class SortingElements:
        NAME_SORT = "//table//div[text()='Name']//button//i"
        PUBLISHED_SORT = "//table//div[text()='Published']//button//i"
        
        
    class PaginationElements:
        PREVIOUS_PAGE = "//ul//a[@aria-label='Previous page']"
        PREVIOUS_PAGE_DISABLED = "//ul//a[@aria-label='Previous page']"
        NEXT_PAGE= "//ul//a[@aria-label='Next page']"
        CURRENT_PAGE = "//ul//a[@aria-current='page']"
        FW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump forward']"
        BW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump backward']"
        SHOWING_COUNT = "//span[contains(text(),'Showing')]"


# Check Element presence
    def verify_all_nav_elements_present(self) -> bool:

        self.logger.info("Verifying that all expected navigation elements are present on: Videos Page")
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
                    self.logger.info(f"{page_element} was located successfully.")
                else:
                    raise NoSuchElementException(f"Element {page_element} Not Found")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{page_element}_Not_Found")
                self.logger.error(f"Could not find {page_element} on page.")
                all_elements_present = False
                missing_elements.append(page_element)
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
                missing_elements.append(page_element)
        if not all_elements_present:
            self.logger.error(f"Missing elements: {', '.join(missing_elements)}")
            
        return all_elements_present
        
    def verify_all_definition_links_present(self) -> bool:

        self.logger.info("Verifying that all expected naivigation elements are present in: Definintions Dropdown")
        all_elements_present = True
        self.interactor.element_click(self.NavigationLocators.DEFINITIONS_BUTTON)
        
        for page_element in [self.NavigationLocators.COUNTRIES_LINK,
                        self.NavigationLocators.IUCNSTATUS_LINK,
                        self.NavigationLocators.POP_TREND_LINK,
                        self.NavigationLocators.SPECIES_LINK,
                        self.NavigationLocators.TAGS_LINK,
        ]:
            try:
                if self.locator.is_element_present(page_element):
                    self.logger.info(f"{page_element} was located successfully.")
                else:
                    raise NoSuchElementException(f"Element {page_element} Not Found")
                # self.interactor.element_click(self.NavigationLocators.DEFINITIONS_BUTTON)
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{page_element}_Not_Found")
                self.logger.error(f"Could not find {page_element} on page.")
                all_elements_present = False
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
        return all_elements_present
    
    def verify_all_video_search_elements_present(self) -> bool:

        self.logger.info("Verifying that all expected video search elements are present in: Definintions Dropdown")
        all_elements_present = True
        
        for page_element in [self.VideoElements.FILTER_NAME_FIELD,
                        self.VideoElements.SEARCH_BUTTON,
                        self.VideoElements.CANCEL_BUTTON,
                        self.VideoElements.ADD_BUTTON,
        ]:
            try:
                if self.locator.is_element_present(page_element):
                    self.logger.info(f"{page_element} was located successfully.")
                else:
                    raise NoSuchElementException(f"Element {page_element} Not Found")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{page_element}_Not_Found")
                self.logger.error(f"Could not find {page_element} on page.")
                all_elements_present = False
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
        return all_elements_present
    
    def verify_all_video_pagination_elements_present(self) -> bool:

        self.logger.info("Verifying that all expected pagination elements are present in: Definintions Dropdown")
        all_elements_present = True
        
        for page_element in [self.PaginationElements.PREVIOUS_PAGE,
                        self.PaginationElements.CURRENT_PAGE,
                        self.PaginationElements.FW_BREAK_ELIPSIS,
                        self.PaginationElements.NEXT_PAGE,
                        self.PaginationElements.SHOWING_COUNT
        ]:
                
            try:
                if self.locator.is_element_present(page_element):
                    self.logger.info(f"{page_element} was located successfully.")
                else:
                    raise NoSuchElementException(f"Element {page_element} Not Found")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{page_element}_Not_Found")
                self.logger.error(f"Could not find {page_element} on page.")
                all_elements_present = False
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
        return all_elements_present
    
    def verify_all_video_table_elements_present(self) -> bool:

        self.logger.info("Verifying that all expected pagination elements are present in: Definintions Dropdown")
        all_elements_present = True
        
        for page_element in [self.VideoTableElements.THUMBNAIL_HEADER,
                        self.VideoTableElements.NAME_HEADER,
                        self.VideoTableElements.PUBLISHED_HEADER,
                        self.VideoTableElements.DESCRIPTION_HEADER,
                        self.VideoTableElements.COUNTRY_HEADER,
                        self.SortingElements.NAME_SORT,
                        self.SortingElements.PUBLISHED_SORT
        ]:
            try:        
                if self.locator.is_element_present(page_element):
                    self.logger.info(f"{page_element} was located successfully.")
                else:
                    raise NoSuchElementException(f"Element {page_element} was Not Found")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"{page_element}_Not_Found")
                self.logger.error(f"Could not find {page_element} on page.")
                all_elements_present = False
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
        return all_elements_present
    
# Check Table Body contents

    def count_table_rows(self) -> int:
        
        self.logger.info("Attempting to count the number of rows in the Videos table")
        num_rows = 0
        try:
            table = self.locator.check_elements_present(self.VideoTableElements.VIDEO_TABLE_BODY)
            if table:
                table_rows = self.locator.get_elements(self.VideoTableElements.VIDEO_TABLE_ROW)
                num_rows = len(table_rows)
                logger.info(f'Found {num_rows} rows in table')
                return num_rows
            else:
                self.screenshot.take_screenshot(self.driver, "Video_Table_Not_Found")
                logger.error(f"Unable to find the video table on this page.")
        except Exception as e:
            logger.error(f"Unable to count table rows: {str(e)}")
            
    def get_video_name_values(self) -> list[str]:
        
        self.logger.info("Attempting to get the names of videos in the Videos table")
        video_names = []
        try:
            table = self.locator.check_elements_present(self.VideoTableElements.VIDEO_TABLE_BODY)
            if table:
                table_rows = self.locator.get_elements(self.VideoTableElements.VIDEO_TABLE_ROW)
                for index, row in enumerate(table_rows, start=1):
                    text_container = self.locator.get_element(f"({self.VideoTableElements.VIDEO_TABLE_ROW})[{index}]/td[2]")
                    name = text_container.text
                    video_names.append(name)
                    logger.debug(f"Here is the row: {name}")
                    logger.debug(f"Here is the names list: {video_names}")
                return video_names
            else:
                logger.error(f"Unable to find table with locator: {table}")
        except Exception as e:
            logger.error(f"Unable to count table rows: {str(e)}")
                
    # def count_total_videos_shown(self) -> int:
    #     total_videos = 0
    #     while 
    

# Check Pagination



    def get_page_locator(page_number):
        return f"//ul//a[@aria-label='Page {page_number}']"
            
    def check_current_page(page_number):
        return f"//ul//a[@aria-label='Page {page_number} is your current page']"
    
    def move_next_page_arrow(self):
        self.interactor.element_click(self.PaginationElements.NEXT_PAGE)
    
    def move_prev_page_arrow(self):
        self.interactor.element_click(self.PaginationElements.PREVIOUS_PAGE)
        
    def move_next_page_jump(self):
        self.interactor.element_click(self.PaginationElements.FW_BREAK_ELIPSIS)
    
    def move_prev_page_jump(self):
        self.interactor.element_click(self.PaginationElements.BW_BREAK_ELIPSIS)