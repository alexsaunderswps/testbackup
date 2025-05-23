# videos_page.py
import os
import re
from typing import Tuple, List
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class VideosPage(BasePage):
    """
    Page object for the Videos page using Playwright.

    This class provides methods to interact with elements on the Videos page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators
    def get_page_title(self):
        """Get the page title for the Videos page."""
        return self.page.get_by_role("heading", name="Videos")
    
    def get_page_title_text(self):
        """Get the text of the page title for the Videos page."""
        return self.get_by_role("heading", level=1).inner_text()
    
    def get_videos_search_button(self):
        """Get the search button element."""
        return self.page.get_by_role("button", name="Search")
    
    def get_videos_search_clear_button(self):
        """Get the clear search button element."""
        return self.page.get_by_role("button").filter(has_text=re.compile(r"^$"))
    
    def get_add_video_button(self):
        """Get the add video button element."""
        return self.page.get_by_role("link", name="Add Video")
    
    # Video Table Elements
    def get_videos_table_body(self):
        """Get the videos table body element."""
        return self.page.locator("table tbody")
    
    def get_videos_table_rows(self):
        """Get the video table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_videos_table_thumbnail_header(self):
        """Get the video table thumbnail header element."""
        return self.page.get_by_role("cell", name="Thumbnail")
    
    def get_videos_table_name_header(self):
        """Get the video table name header element."""
        return self.page.get_by_role("cell", name="Name")
    
    def get_videos_table_sort_by_name_arrows(self):
        """Get the video table sort by name arrows element."""
        return self.page.get_by_role("row", name="Thumbnail Name Organization").get_by_role("button")
    
    def get_videos_table_organization_header(self):
        """Get the video table organization header element."""
        return self.page.get_by_role("cell", name="Organization")
    
    def get_videos_table_description_header(self):
        """Get the video table description header element."""
        return self.page.get_by_role("cell", name="Description")
    
    def get_videos_table_country_header(self):
        """Get the video table country header element."""
        return self.page.get_by_role("cell", name="Country")
    
    def get_video_by_name(self, name):
        """ Find an video in the table by name. """
        rows = self.get_videos_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").nth(1)
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None
    
    # Videos Pagination Elements
    def get_videos_count_text(self):
        """ Get the videos count text element."""
        showing_element = self.get_showing_count()
        if showing_element.count() > 0:
            return showing_element.inner_text()
        return None
    
    def get_pagination_counts(self):
        """
        Extract the pagination counts from the "Showing X to Y of Z" text.

        Returns:
            Tuple[int, int, int]: A tuple containing:
                - start_count (int): The starting index of the current page.
                - end_count (int): The ending index of the current page.
                - total_count (int): The total number of items.
        """
        return super().get_pagination_counts()
    
    # Videos Add Modal Elements locators
    def get_add_video_position_button(self):
        """Get the add video position button element."""
        return self.page.get_by_role("button", name="Add Video")
    
    def get_map_marker_position_button(self):
        """Get the map marker position button element."""
        return self.page.get_by_role("button", name="Map Marker")
    
    def get_review_save_position_button(self):
        """Get the review save position button element."""
        return self.page.get_by_role("button", name="Review & Save")
    
    def get_add_video_back_button(self):
        """Get the add video back button element."""
        return self.page.get_by_role("button", name="Back")
    
    def get_add_video_next_button(self):
        """Get the add video next button element."""
        return self.page.get_by_role("button", name="Next")
    
    def get_add_video_save_button(self):
        """Get the add video save button element."""
        return self.page.get_by_role("button", name="Save")
    
    def get_add_video_name_label(self):
        """Get the add video name label element."""
        return self.page.get_by_text("Name*")
    
    def get_add_video_name_input(self):
        """Get the add video name input element."""
        return self.page.get_by_role("textbox", name="Enter Name")
    
    def get_add_video_thumbnail_label(self):
        """Get the add video thumbnail label element."""
        return self.page.get_by_text("Thumbnail*")
    
    def get_add_video_choose_png_link(self):
        """Get the choose PNG link element."""
        return self.page.get_by_text("Choose a PNG file")
    
    def get_add_video_file_name_label(self):
        """Get the add video file name label element."""
        return self.page.get_by_text("Video File Name")
    
    def get_add_video_file_name_input(self):
        """Get the add video file name input element."""
        return self.page.locator("input[name=\"VideoFileName\"]")
    
    def get_add_video_overview_label(self):
        """Get the add video overview label element."""
        return self.page.get_by_text("Overview*")
    
    def get_add_video_overview_input(self):
        """Get the add video overview input element."""
        return self.page.get_by_role("textbox", name="Enter Overview")
    
    def get_add_video_youtube_label(self):
        """Get the add video YouTube label element."""
        return self.page.get_by_text("YouTube URL")
    
    def get_add_video_youtube_input(self):
        """Get the add video YouTube input element."""
        return self.page.get_by_role("textbox", name="Enter Youtube URL")
    
    def get_add_video_start_time_label(self):
        """Get the add video start time label element."""
        return self.page.get_by_text("Start Time")
    
    def get_add_video_start_time_input(self):
        """Get the add video start time input element."""
        return self.page.locator("input[name=\"startTime\"]")
    
    def get_add_video_end_time_label(self):
        """Get the add video end time label element."""
        return self.page.get_by_text("End Time")
    
    def get_add_video_end_time_input(self):
        """Get the add video end time input element."""
        return self.page.locator("input[name=\"endTime\"]")
    
    def get_add_video_organization_label(self):
        """Get the add video organization label element."""
        return self.page.get_by_text("Organization*")
    
    def get_add_video_organization_dropdown(self):
        """Get the add video organization dropdown element."""
        return self.page.locator(".css-19bb58m").first
    
    def get_add_video_country_label(self):
        """Get the add video country label element."""
        return self.page.get_by_text("Country*")
    
    def get_add_video_country_dropdown(self):
        """Get the add video country dropdown element."""
        return self.page.locator(".css-19bb58m").nth(1)
    
    def get_add_video_video_format_label(self):
        """Get the add video video format label element."""
        return self.page.get_by_text("Video Format*")
    
    def get_add_video_video_format_dropdown(self):
        """Get the add video video format dropdown element."""
        return self.page.locator(".css-19bb58m").nth(2)
    
    def get_add_video_video_resolution_label(self):
        """Get the add video video resolution label element."""
        return self.page.get_by_text("Video Resolution*")
    
    def get_add_video_video_resolution_dropdown(self):
        """Get the add video video resolution dropdown element."""
        return self.page.locator(".css-19bb58m").nth(3)
    
    def get_add_video_species_label(self):
        """Get the add video species label element."""
        return self.page.get_by_text("Species*")
    
    def get_add_video_species_dropdown(self):
        """Get the add video species dropdown element."""
        return self.page.locator(".css-19bb58m").nth(4)
    
    def get_add_video_tags_label(self):
        """Get the add video tags label element."""
        return self.page.get_by_text("Tags")

    def get_add_video_tags_dropdown(self):
        """Get the add video tags dropdown element."""
        return self.page.locator(".css-19bb58m").nth(5)
    
    def get_add_video_core_map_markers_tab(self):
        """Get the add video core map markers tab element."""
        return self.page.locator("form").get_by_text("Map Markers", exact=True)
    
    def get_add_video_custom_map_markers_tab(self):
        """Get the add video custom map markers tab element."""
        return self.page.locator("form").get_by_text("Custom Map Markers", exact=True)
    
    def get_add_video_map_markers_table(self):
        """Get the add video map markers table element."""
        return self.page.locator("table tbody")
    
    def get_add_video_map_markers_table_rows(self):
        """Get the add video map markers table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_add_video_select_all_map_markers_label(self):
        """Get the add video select all map markers label element."""
        return self.page.get_by_role("cell", name="Select All Map Markers")
    
    def get_add_video_select_all_map_markers_checkbox(self):
        """Get the add video select all map markers checkbox element."""
        return self.page.get_by_role("cell", name="Select All Map Markers").locator("#checkbox")
    
    def get_add_video_map_marker_icon_label(self):
        """Get the add video map marker icon label element."""
        return self.page.get_by_role("cell", name="Icon")
    
    def get_add_video_map_marker_name_label(self):
        """Get the add video map marker name label element."""
        return self.page.get_by_role("cell", name="Name")
    
    def get_add_video_map_marker_description_label(self):
        """Get the add video map marker description label element."""
        return self.page.get_by_role("cell", name="Description")
    
    def get_add_video_map_marker_videos_label(self):
        """Get the add video map marker videos label element."""
        return self.page.get_by_role("cell", name="Videos")
    
    def get_add_video_map_marker_location_label(self):
        """Get the add video map marker location label element."""
        return self.page.get_by_role("cell", name="Location")
    
    # Organization lable only shows on the Custom Map Markers tab
    def get_add_video_map_marker_organization_label(self):
        """Get the add video map marker organization label element."""
        return self.page.get_by_role("cell", name="Organization")

    # Check Page Element presence
    def verify_page_title_present(self) -> bool:
        r""" Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying page title is present")
        return super().verify_page_title("Videos")
    
    def verify_page_title(self) -> bool:
        """
        Verify that the page title is present and is the correct "Videos" title.

        Returns:
            bool: True if the page title is correct, False otherwise.
        """
        return super().verify_page_title("Videos", tag="h1")

    def verify_all_videos_action_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected videos action elements are present.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected videos action elements are present")

        # Define elements with readable names
        action_elements = {
            "Search Button": self.get_videos_search_button,
            "Clear Search Button": self.get_videos_search_clear_button,
            "Add Video Button": self.get_add_video_button,
        }
        return self.verify_page_elements_present(action_elements, "Videos Action Elements")
    
    def verify_all_video_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected video table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected pagination elements are present in: Videos Table")

        # Define elements with readable names
        table_elements = {
            "Table Body": self.get_videos_table_body,
            "Table Rows": self.get_videos_table_rows,
            "Thumbnail Header": self.get_videos_table_thumbnail_header,
            "Video Name": self.get_videos_table_name_header,
            "Organization Header": self.get_videos_table_organization_header,
            "Description Header": self.get_videos_table_description_header,
            "Country Header": self.get_videos_table_country_header,
            "Sorting Arrows": self.get_videos_table_sort_by_name_arrows,
        }
        return self.verify_page_elements_present(table_elements, "Video Table Elements")

    def count_table_rows(self) -> int:
        """
        Count the number of rows in the Videos Table.

        Returns:
            int: The number of rows in the Videos Table.
        """
        self.logger.info("Counting the number of rows in the Videos Table")
        num_rows = 0
        try:
            rows = self.get_videos_table_rows()
            rows_count = rows.count()
            self.logger.info(f"Found {rows_count} rows in the Videos Table")
            return rows_count
        except Exception as e:
            self.logger.error(f"An error occurred while trying to count the number of rows in the Countries Table: {str(e)}")
            return 0

    def get_video_name_values(self) -> List[str]:
        """
        Get the names of all videos visible in the current page of the table.

        Returns:
            List[str]: A list of video names, or empty list if none found
        """
        self.logger.info("Getting the names of all videos in the table on current page")
        video_names = []
        try:
            rows = self.get_videos_table_rows()
            rows_count = rows.count()
            
            for i in range(rows_count):
                try:
                    # Get the first cell (video name) from each row
                    name_cell = rows.nth(i).locator("td").first
                    video_name = name_cell.inner_text()
                    video_names.append(video_name)
                    self.logger.info(f"Found {len(video_names)} video names")
                except Exception as row_error:
                    self.logger.error(f"An error occurred while trying to get the video name from row {i}: {str(row_error)}")
                    continue
            self.logger.info(f"Found a total of {len(video_names)} video names")
            return video_names
        except Exception as e:
            self.logger.error(f"An error occurred while trying to get the video names: {str(e)}")
            return []
                
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