# video_catalogues_page.py
import os
import re
from typing import Tuple, List
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables
BASE_URL = os.getenv("QA_BASE_URL")

class VideoCataloguesPage(BasePage):
    """
    Page object for the Video Catalogues page using Playwright.

    This class provides methods to interact with elements on the Video Catalogues page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators
    def get_page_title(self):
        """Get the page title for the Video Catalogues page."""
        return self.page.get_by_role("heading", name="Video Catalogues")
    
    def get_page_title_text(self):
        """Get the text of the page title for the Video Catalogues page."""
        return self.get_by_role("heading", level=1).inner_text()
    
    def get_video_catalogues_search_input(self):
        """Get the video catalogues search input element."""
        return self.page.get_by_placeholder("Filter by name")
    
    def get_video_catalogues_search_button(self):
        """Get the search button element."""
        return self.page.get_by_role("button", name="Search")
    
    def get_add_video_catalogue_button(self):
        """Get the add video catalogue button element."""
        return self.page.get_by_role("link", name="Add")
    
    # Video Catalogues Table Elements
    def get_video_catalogues_table_body(self):
        """Get the video catalogues table body element."""
        return self.page.locator("table tbody")
    
    def get_video_catalogues_table_rows(self):
        """Get the video catalogues table rows element."""
        return self.page.locator("table tbody tr")
    
    def get_video_catalogues_table_name_header(self):
        """Get the video catalogues table name header element."""
        return self.page.get_by_role("cell", name="Name")
    
    def get_video_catalogues_table_organization_header(self):
        """Get the video catalogues table organization header element."""
        return self.page.get_by_role("cell", name="Organization")
    
    def get_video_catalogues_table_description_header(self):
        """Get the video catalogues table description header element."""
        return self.page.get_by_role("cell", name="Description")
    
    def get_video_catalogues_table_last_edited_date_header(self):
        """Get the video catalogues table last edited date header element."""
        return self.page.get_by_role("cell", name="Last Edited Date")
    
    # def get_video_catalogues_table_sort_by_name_arrows(self):
    #     """Get the video catalogues table sort by name arrows element."""
    #     return self.page.get_by_role("row", name="Name Organization Description Last Edited By Last Edited Date").get_by_role("button")
    
    def get_video_catalogue_by_name(self, name):
        """ Find a video catalogue in the table by name. """
        rows = self.get_video_catalogues_table_rows()
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").nth(0)
            if name_cell.inner_text() == name:
                return rows.nth(i)
        return None
    
    # Video Catalogues Pagination Elements
    def get_video_catalogues_count_text(self):
        """ Get the video catalogues count text element."""
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
    
    # Catalogues Add Wizard Elements
    def get_next_button(self):
        """Get the next button element in the Add Catalogue Wizard."""
        return self.page.get_by_role("button", name="Next")
    
    def get_back_button(self):
        """Get the back button element in the Add Catalogue Wizard."""
        return self.page.get_by_role("button", name="Back")
    
    def get_add_video_catalogue_position_button(self):
        """Get the Add Video Catalogue button element. This is also a positional display element."""
        return self.page.get_by_role("button", name="Add Video Catalogue")
    
    def get_map_markers_position_button(self):
        """Get the Map Markers button element. This is also a positional display element."""
        return self.page.get_by_role("button", name="Map Markers")
    
    def get_videos_position_button(self):
        """Get the Videos button element. This is also a positional display element."""
        return self.page.get_by_role("button", name="Videos")
    
    def get_review_and_save_position_button(self):
        """Get the Review and Save button element. This is also a positional display element."""
        return self.page.get_by_role("button", name="Review & Save")
    
    # Catalogues Add Wizard Catalogue fields
    def get_catalogue_name_label(self):
        """Get the Catalogue Name label element in the Add Catalogue Wizard."""
        return self.page.get_by_text("Name*", exact=True)
    
    def get_catalogue_name_input(self):
        """Get the Catalogue Name input element in the Add Catalogue Wizard."""
        return self.page.get_by_role("textbox", name="Enter Name", exact=True)
    
    def get_overview_label(self):
        """Get the Overview label element in the Add Catalogue Wizard."""
        return self.page.get_by_text("Overview*", exact=True)
    
    def get_overview_input(self):
        """Get the Overview input element in the Add Catalogue Wizard."""
        return self.page.get_by_role("textbox", name="Enter Overview...")
    
    def get_organization_label(self):
        """Get the Organization label element in the Add Catalogue Wizard."""
        return self.page.get_by_text("Select Organization*")
    
    def get_organization_dropdown(self):
        """Get the Organization dropdown element in the Add Catalogue Wizard."""
        return self.page.locator(".css-19bb58m").first

    # Catalogues Add Wizard Map Markers checkboxes
    def get_map_markers_tab(self):
        """Get the Map Markers tab element in the Add Catalogue Wizard."""
        return self.page.locator("label").filter(has_text=re.compile(r"^Map Markers$"))
    
    def get_custom_map_markers_tab(self):
        """Get the Custom Map Markers tab element in the Add Catalogue Wizard."""
        return self.page.get_by_text("Custom Map Markers")
    
    def get_select_all_map_markers_checkbox(self):
        """Get the Select All Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell", name="Select All Map Markers").locator("#checkbox")
    
    def get_select_north_america_map_markers_checkbox(self):
        """Get the Select North America Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="North America").locator("#checkbox")
    
    def get_select_africa_map_markers_checkbox(self):
        """Get the Select Africa Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="Africa").locator("#checkbox")
    
    def get_select_oceans_first_map_markers_checkbox(self):
        """Get the first Select Oceans Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="Oceans and Rivers").first.locator("#checkbox")

    def get_select_oceans_second_map_markers_checkbox(self):
        """Get the second Select Oceans Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="Oceans and Rivers").nth(1).locator("#checkbox")

    def get_select_oceans_third_map_markers_checkbox(self):
        """Get the third Select Oceans Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="Oceans and Rivers").nth(2).locator("#checkbox")

    def get_select_central_america_map_markers_checkbox(self):
        """Get the Select Central America Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="Central America").locator("#checkbox")
    
    def get_select_south_america_map_markers_checkbox(self):
        """Get the Select South America Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="South America").locator("#checkbox")
    
    def get_select_asia_map_markers_checkbox(self):
        """Get the Select Asia Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="Asia").locator("#checkbox")
    
    def get_select_europe_map_markers_checkbox(self):
        """Get the Select Europe Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="Europe").locator("#checkbox")
    
    def get_select_australia_map_markers_checkbox(self):
        """Get the Select Australia Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="Australia").locator("#checkbox")

    def get_select_falkland_islands_map_markers_checkbox(self):
        """Get the Select Falkland Islands Map Markers checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("row", name="Falkland Islands").locator("#checkbox")

    # Catalogues Add Wizard Videos checkboxes
    def get_first_video_checkbox(self):
        """Get the first video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(5).locator("#checkbox")

    def get_second_video_checkbox(self):
        """Get the second video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(10).locator("#checkbox")
    
    def get_third_video_checkbox(self):
        """Get the third video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(15).locator("#checkbox")
    
    def get_fourth_video_checkbox(self):
        """Get the fourth video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(20).locator("#checkbox")
    
    def get_fifth_video_checkbox(self):
        """Get the fifth video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(25).locator("#checkbox")
    
    def get_sixth_video_checkbox(self):
        """Get the sixth video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(30).locator("#checkbox")
    
    def get_seventh_video_checkbox(self):
        """Get the seventh video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(35).locator("#checkbox")
    
    def get_eighth_video_checkbox(self):
        """Get the eighth video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(40).locator("#checkbox")
    
    def get_ninth_video_checkbox(self):
        """Get the ninth video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(45).locator("#checkbox")
    
    def get_tenth_video_checkbox(self):
        """Get the tenth video checkbox element in the Add Catalogue Wizard."""
        return self.page.get_by_role("cell").nth(50).locator("#checkbox")
    
    # Catalogues Add Wizard Review and Save elements
    # These aren't well defined in the UI so we are skipping them for now

    # Check Page Element presence
    def verify_page_title_present(self) -> bool:
        r""" Verify that the page title is present.
        
        Returns:
            bool: True if the page title is present, False otherwise.
        """
        self.logger.info("Verifying page title is present")
        return super().verify_page_title("Video Catalogues")
    
    def verify_page_title(self) -> bool:
        """
        Verify that the page title is present and is the correct "Video Catalogues" title.

        Returns:
            bool: True if the page title is correct, False otherwise.
        """
        return super().verify_page_title("Video Catalogues", tag="h1")

    def verify_all_video_catalogues_search_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected video catalogues search elements are present.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected video catalogues search elements are present")

        # Define elements with readable names
        search_elements = {
            "Search Input": self.get_video_catalogues_search_input,
            "Search Button": self.get_video_catalogues_search_button,
            "Add Video Catalogue Button": self.get_add_video_catalogue_button,
        }
        return self.verify_page_elements_present(search_elements, "Video Catalogues Search Elements")
    
    def verify_all_video_catalogues_table_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected video catalogues table elements are present.
        
        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected video catalogues table elements are present")

        # Define elements with readable names
        table_elements = {
            "Table Body": self.get_video_catalogues_table_body,
            "Table Rows": self.get_video_catalogues_table_rows,
            "Name Header": self.get_video_catalogues_table_name_header,
            "Organization Header": self.get_video_catalogues_table_organization_header,
            "Description Header": self.get_video_catalogues_table_description_header,
            "Last Edited Date Header": self.get_video_catalogues_table_last_edited_date_header,
            # "Sort by Name Arrows": self.get_video_catalogues_table_sort_by_name_arrows,
        }
        return self.verify_page_elements_present(table_elements, "Video Catalogues Table Elements")

    def count_table_rows(self) -> int:
        """
        Count the number of rows in the Video Catalogues Table.

        Returns:
            int: The number of rows in the Video Catalogues Table.
        """
        self.logger.info("Counting the number of rows in the Video Catalogues Table")
        num_rows = 0
        try:
            rows = self.get_video_catalogues_table_rows()
            rows_count = rows.count()
            self.logger.info(f"Found {rows_count} rows in the Video Catalogues Table")
            return rows_count
        except Exception as e:
            self.logger.error(f"An error occurred while trying to count the number of rows in the Video Catalogues Table: {str(e)}")
            return 0

    def get_video_catalogue_name_values(self) -> List[str]:
        """
        Get the names of all video catalogues visible in the current page of the table.

        Returns:
            List[str]: A list of video catalogue names, or empty list if none found
        """
        self.logger.info("Getting the names of all video catalogues in the table on current page")
        catalogue_names = []
        try:
            rows = self.get_video_catalogues_table_rows()
            rows_count = rows.count()
            
            for i in range(rows_count):
                try:
                    # Get the first cell (catalogue name) from each row
                    name_cell = rows.nth(i).locator("td").first
                    catalogue_name = name_cell.inner_text()
                    catalogue_names.append(catalogue_name)
                    self.logger.info(f"Found {len(catalogue_names)} video catalogue names")
                except Exception as row_error:
                    self.logger.error(f"An error occurred while trying to get the video catalogue name from row {i}: {str(row_error)}")
                    continue
            self.logger.info(f"Found a total of {len(catalogue_names)} video catalogue names")
            return catalogue_names
        except Exception as e:
            self.logger.error(f"An error occurred while trying to get the video catalogue names: {str(e)}")
            return []