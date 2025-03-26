# videos_page.py
import os
from typing import Tuple
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT, PAGE_SIZE
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
        VIDEO_PAGE_TITLE = "//h1[contains(text(),'Videos')]"
        
    class VideoSearchElements:
        SEARCH_BUTTON = "//button[text()='Search']"
        CANCEL_BUTTON = "//div//button[2]"
        ADD_VIDEO_LINK = "//a[@href='/video/add']"
        
    class VideoTableElements:
        VIDEO_TABLE_BODY = "//table//tbody"
        THUMBNAIL_HEADER = "//table/thead/tr/th[text()='Thumbnail']"
        NAME_HEADER = "//table/thead/tr/div[text()='Name']"
        ORGANIZATION_HEADER = "//table/thead/tr/div[text()='Organization']"
        DESCRIPTION_HEADER = "//table/thead/tr/th[text()='Description']"
        COUNTRY_HEADER = "//table/thead/tr/th[text()='Country']"
        VIDEO_TABLE_ROW = "//table//tbody/tr"
    
    class SortingElements:
        NAME_SORT = "//table//div[text()='Name']//button//i"
        ## PUBLISHED_SORT = "//table//div[text()='Published']//button//i"

    # Check Title Element presence
    def verify_page_title_present(self):
        return super().verify_page_title_present(self.VideoElements.VIDEO_PAGE_TITLE)
    
    # Check Search Elements
    
    def verify_all_video_search_elements_present(self) -> Tuple[bool, list]:
        """_summary_

        Raises:
            NoSuchElementException: _description_

        Returns:
            Tuple[bool, list]: _description_
        """
        self.logger.info("Verifying that all expected video search elements are present in: Video Page")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        search_elements = {
            "Search Button": self.VideoSearchElements.SEARCH_BUTTON,
            "Clear Search Button": self.VideoSearchElements.CANCEL_BUTTON,
            "Add Video Button": self.VideoSearchElements.ADD_VIDEO_LINK,
        }
        for element_name, search_locator in search_elements.items():
            try:
                if self.locator.is_element_present(search_locator):
                    self.logger.info(f"{element_name} was located successfully.")
                else:
                    raise NoSuchElementException(f"Search element {element_name} Not Found on Videos Page")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"Video_search_{element_name}_Not_Found")
                self.logger.error(f"Could not find {element_name} on page.")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while finding elements: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
    # Check Table Elements
    
    def verify_all_video_table_elements_present(self) -> Tuple[bool, list]:

        self.logger.info("Verifying that all expected pagination elements are present in: Videos Table")
        all_elements_present = True
        missing_elements = []
        # Define elements with readable names
        table_elements = {
            "Thumbnail Header": self.VideoTableElements.THUMBNAIL_HEADER,
            "Video Name": self.VideoTableElements.NAME_HEADER,
            "Organization Header": self.VideoTableElements.ORGANIZATION_HEADER,
            "Description Header": self.VideoTableElements.DESCRIPTION_HEADER,
            "Country Header": self.VideoTableElements.COUNTRY_HEADER,
            "Sorting Arrows": self.SortingElements.NAME_SORT,
                        ## self.SortingElements.PUBLISHED_SORT
        }
        for element_name, table_locator in table_elements.items():
            try:        
                if self.locator.is_element_present(table_locator):
                    self.logger.info(f"{element_name} was located successfully.")
                else:
                    raise NoSuchElementException(f"Element {element_name} was Not Found")
            except NoSuchElementException:
                self.screenshot.take_screenshot(self.driver, f"video_table_{element_name}_Not_Found")
                self.logger.error(f"Could not find {element_name} in video table.")
                all_elements_present = False
                missing_elements.append(element_name)
            except Exception as e:
                self.logger.error(f"Unexpected error while finding element in video table: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements

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
                
# TODO - with names, check sort functionality
# TODO - check if published column should be populated
# TODO - gather other table data if needed
# TODO - with Published, check sort functionality
# TODO - Check search functionality - modal window interaction                
                
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