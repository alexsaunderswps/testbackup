# videos_page.py
import os
import re
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
        THUMBNAIL_HEADER = "//table//th[text()='Thumbnail']"
        NAME_HEADER = "//table//div[text()='Name']"
        ORGANIZATION_HEADER = "//table//div[text()='Organization']"
        DESCRIPTION_HEADER = "//table//th[text()='Description']"
        COUNTRY_HEADER = "//table//th[text()='Country']"
        VIDEO_TABLE_ROW = "//table//tbody/tr"
    
    class SortingElements:
        NAME_SORT = "//table//div[text()='Name']//button//i"
        ## PUBLISHED_SORT = "//table//div[text()='Published']//button//i"
        
        
    class PaginationElements:
        PREVIOUS_PAGE = "//ul//a[@aria-label='Previous page']"
        PREVIOUS_PAGE_DISABLED = "//ul//a[@aria-label='Previous page']"
        NEXT_PAGE= "//ul//a[@aria-label='Next page']"
        CURRENT_PAGE = "//ul//a[@aria-current='page']"
        FW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump forward']"
        BW_BREAK_ELIPSIS = "//ul//a[@aria-label='Jump backward']"
        SHOWING_COUNT = "//span[contains(text(),'Showing')]"


    # Check Element presence
    def verify_page_title_present(self):
        return super().verify_page_title_present(self.VideoElements.VIDEO_PAGE_TITLE)
    
    def verify_all_video_search_elements_present(self) -> Tuple[bool, list]:

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
    
    def verify_video_pagination_elements_present(self) -> Tuple[bool,list]:
        """
        Verifies pagination elements based on page size and current record count.
    
        Returns:
            Tuple[bool, list]: A tuple containing a boolean (all expected elements present)
                        and a list of missing expected elements
        """
        self.logger.info("Checking that all expected pagination elements are present in on Videos Page")
        all_elements_present = True
        missing_elements = []
        # Get the page size from utilities.config
        page_size = PAGE_SIZE
        
        # Extract information from the showing count
        current_start = 1
        total_records = 0
        
        try:
            if self.locator.is_element_present(self.PaginationElements.SHOWING_COUNT):
                showing_element = self.locator.get_element(self.PaginationElements.SHOWING_COUNT)
                showing_text = showing_element.text
                
                # Parse the showing text to get the current start and total records
                match = re.match(r'Showing\s+(\d+)\s+to\s+(\d+)\s+of\s+(\d+)', showing_text)
                if match:
                    current_start = int(match.group(1))
                    current_end = int(match.group(2))
                    total_records = int(match.group(3))
                    self.logger.info(f"Showing {current_start} to {current_end} of {total_records} records")
                else:
                    self.logger.warning(f"Cound not parse showing text: {showing_text}")
            else:
                self.logger.warning("Could not find the showing count element")
        except Exception as e:
            self.logger.error(f"Error while getting showing count: {str(e)}")
            
        # Determine which pagination elements should be present based on the current record count
        is_first_page = current_start == 1
        has_multiple_pages = total_records > page_size
        is_last_page = total_records <= current_start + (page_size -1)
            
        # Define elements with readable names
        pagination_element_locators = {
            "Previous Page": self.PaginationElements.PREVIOUS_PAGE,
            "Next Page": self.PaginationElements.NEXT_PAGE,
            "Current Page": self.PaginationElements.CURRENT_PAGE,
            "Forward Break Elipsis": self.PaginationElements.FW_BREAK_ELIPSIS,
            "Backward Break Elipsis": self.PaginationElements.BW_BREAK_ELIPSIS,
            "Showing Count": self.PaginationElements.SHOWING_COUNT
        }
        
        # Define expected state of pagination elements
        expected_elements = {
            "Previous Page": True,
            "Next Page": has_multiple_pages and not is_last_page,
            "Current Page": True,
            "Forward Break Elipsis": total_records > (page_size * 2), # Need at least 3 pages to show
            "Backward Break Elipsis": current_start > (page_size * 2), # Need to be at least on page 3 to show
            "Showing Count": True
        }
        for element_name, element_locator in pagination_element_locators.items():
            element_should_be_present = expected_elements[element_name]
            expected_state = "present" if element_should_be_present else "not present"
            try:
                is_present = self.locator.is_element_present(element_locator)
                if is_present == element_should_be_present:
                    self.logger.info(F'{element_name} correctly {expected_state}')
                else:
                    self.logger.error(f"{element_name} should be {expected_state} but is {'present' if is_present else 'not present'}")
                    all_elements_present = False
                    missing_elements.append(element_name)
                    self.screenshot.take_screenshot(self.driver, f"{element_name}_unexpected_state")
            except Exception as e:
                self.logger.error(f"Error checking pagination element {element_name}: {str(e)}")
                all_elements_present = False
                missing_elements.append(element_name)
        return all_elements_present, missing_elements
    
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