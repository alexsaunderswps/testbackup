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

    The Videos page renders a responsive grid of video cards, not a table.
    Each card contains a thumbnail image, video name (h2), overview text (p),
    organization name (bold span), and country name (span).

    This class provides methods to interact with elements on the Videos page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger

    # -------------------------------------------------------------------------
    # Page Header Elements
    # -------------------------------------------------------------------------

    def get_page_title(self):
        """Get the page title for the Videos page."""
        return self.page.get_by_role("heading", name="Videos")

    def get_page_title_text(self):
        """Get the text of the page title for the Videos page."""
        return self.get_by_role("heading", level=1).inner_text()

    # -------------------------------------------------------------------------
    # Action Button Elements (Search, Clear, Add)
    # -------------------------------------------------------------------------

    def get_videos_search_button(self):
        """Get the search button element."""
        return self.page.get_by_role("button", name="Search")

    def get_videos_search_clear_button(self):
        """Get the clear search button element (icon-only button with no text)."""
        return self.page.get_by_role("button").filter(has_text=re.compile(r"^$"))

    def get_add_video_button(self):
        """Get the add video button element."""
        return self.page.get_by_role("link", name="Add")

    # -------------------------------------------------------------------------
    # Video Grid & Card Elements
    #
    # The Videos page uses a CSS grid layout (div.grid) containing individual
    # video cards (div.group). Each card contains:
    #   - <img>  thumbnail
    #   - <h2>   video name
    #   - <p>    overview text
    #   - <span class="font-bold"> organization name
    #   - <span> country name
    # -------------------------------------------------------------------------

    def get_video_grid(self):
        """Get the video grid container element."""
        return self.page.locator("div.grid").filter(has=self.page.locator("div.group"))

    def get_video_cards(self):
        """Get all video card elements within the grid."""
        return self.page.locator("div.group")

    def get_video_card_thumbnails(self):
        """Get the thumbnail img elements within video cards."""
        return self.page.locator("div.group img")

    def get_video_card_names(self):
        """Get the video name h2 elements within video cards."""
        return self.page.locator("div.group h2")

    def get_video_card_overviews(self):
        """Get the overview p elements within video cards."""
        return self.page.locator("div.group p")

    def get_video_card_organizations(self):
        """Get the organization label (bold span) elements within video cards."""
        return self.page.locator("div.group .mt-auto span.font-bold")

    def get_video_card_countries(self):
        """Get the country label (plain span) elements within video cards."""
        return self.page.locator("div.group .mt-auto span:last-child")

    def get_video_card_by_name(self, name: str):
        """
        Find a video card by its title text.

        Args:
            name: The video name to search for.

        Returns:
            Locator: The matching video card element, or None if not found.
        """
        return self.page.locator("div.group").filter(
            has=self.page.locator("h2", has_text=name)
        )

    # -------------------------------------------------------------------------
    # Videos Pagination Elements
    # -------------------------------------------------------------------------

    def get_videos_count_text(self):
        """Get the videos count text element."""
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

    # -------------------------------------------------------------------------
    # Add / Edit Video Form Elements
    # -------------------------------------------------------------------------

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

    # Organization label only shows on the Custom Map Markers tab
    def get_add_video_map_marker_organization_label(self):
        """Get the add video map marker organization label element."""
        return self.page.get_by_role("cell", name="Organization")

    # -------------------------------------------------------------------------
    # VideoSearchModal Elements
    #
    # The VideoSearchModal renders as a fixed-position full-screen overlay
    # (div.fixed.inset-0) that is completely removed from the DOM when closed
    # (the component returns null when isOpen is false). All locators below are
    # scoped to that container so they cannot accidentally match nav elements
    # (e.g. the "Species" nav link) that are present on the same page.
    #
    # Source component: VideoSearchModal.tsx
    # -------------------------------------------------------------------------

    def _get_search_modal_container(self):
        """
        Get the VideoSearchModal overlay container.

        This element only exists in the DOM while the modal is open — the
        component returns null when isOpen is false. Used to scope all other
        modal locators so they cannot match elements behind the overlay.
        """
        return self.page.locator("div.fixed.inset-0")

    def get_search_modal_heading(self):
        """Get the 'Filter Videos' h2 heading inside the VideoSearchModal."""
        return self._get_search_modal_container().get_by_role(
            "heading", name="Filter Videos"
        )

    def get_search_modal_close_button(self):
        """Get the × close button in the VideoSearchModal header."""
        return self._get_search_modal_container().get_by_role("button", name="×")

    def get_search_modal_name_input(self):
        """Get the Name text input inside the modal (placeholder: 'Search by name')."""
        return self._get_search_modal_container().get_by_placeholder("Search by name")

    def get_search_modal_overview_input(self):
        """Get the Overview text input inside the modal (placeholder: 'Search by overview')."""
        return self._get_search_modal_container().get_by_placeholder(
            "Search by overview"
        )

    def get_search_modal_country_label(self):
        """Get the 'Country' dropdown label inside the VideoSearchModal."""
        return self._get_search_modal_container().get_by_text("Country", exact=True)

    def get_search_modal_resolution_label(self):
        """Get the 'Resolution' dropdown label inside the VideoSearchModal."""
        return self._get_search_modal_container().get_by_text("Resolution", exact=True)

    def get_search_modal_species_label(self):
        """Get the 'Species' dropdown label inside the VideoSearchModal."""
        return self._get_search_modal_container().get_by_text("Species", exact=True)

    def get_search_modal_tags_label(self):
        """Get the 'Tags' dropdown label inside the VideoSearchModal."""
        return self._get_search_modal_container().get_by_text("Tags", exact=True)

    def get_search_modal_status_label(self):
        """Get the 'Statuses' dropdown label inside the VideoSearchModal."""
        return self._get_search_modal_container().get_by_text("Statuses", exact=True)

    def get_search_modal_reset_button(self):
        """Get the Reset button in the VideoSearchModal footer."""
        return self._get_search_modal_container().get_by_role("button", name="Reset")

    def get_search_modal_apply_button(self):
        """Get the Apply button in the VideoSearchModal footer."""
        return self._get_search_modal_container().get_by_role("button", name="Apply")

    def open_search_modal(self) -> None:
        """
        Click the Search button to open the VideoSearchModal, then wait for
        the 'Filter Videos' heading to become visible.

        The modal renders as a React overlay and does not trigger a network
        request, so this method waits for the heading element rather than
        relying on wait_for_load_state("networkidle").
        """
        self.logger.info("Opening VideoSearchModal by clicking the Search button")
        self.get_videos_search_button().click()
        self.get_search_modal_heading().wait_for(state="visible")

    def close_search_modal(self) -> None:
        """
        Click the × close button to dismiss the VideoSearchModal, then wait
        for the 'Filter Videos' heading to be removed from the DOM.
        """
        self.logger.info("Closing VideoSearchModal by clicking the × button")
        self.get_search_modal_close_button().click()
        self.get_search_modal_heading().wait_for(state="hidden")

    def verify_all_search_modal_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected elements are visible inside the VideoSearchModal.

        Checks the heading, two text inputs, five filter dropdown labels,
        the Reset button, the Apply button, and the × close button.
        The modal must be open before calling this method.

        Filter fields (from VideoSearchModal.tsx):
          Name, Overview, Country, Resolution, Species, Tags, Statuses

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise.
                - List[str]: List of missing element names (empty if all found).
        """
        self.logger.info("Verifying all expected VideoSearchModal elements are present")
        modal_elements = {
            "Modal Heading": self.get_search_modal_heading,
            "Name Input": self.get_search_modal_name_input,
            "Overview Input": self.get_search_modal_overview_input,
            "Country Label": self.get_search_modal_country_label,
            "Resolution Label": self.get_search_modal_resolution_label,
            "Species Label": self.get_search_modal_species_label,
            "Tags Label": self.get_search_modal_tags_label,
            "Statuses Label": self.get_search_modal_status_label,
            "Reset Button": self.get_search_modal_reset_button,
            "Apply Button": self.get_search_modal_apply_button,
            "Close Button": self.get_search_modal_close_button,
        }
        return self.verify_page_elements_present(
            modal_elements, "VideoSearchModal Elements"
        )

    # -------------------------------------------------------------------------
    # Verification Methods
    # -------------------------------------------------------------------------

    def verify_page_title_present(self) -> bool:
        r"""Verify that the page title is present.

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

        Checks for: Search button, Clear search button, and Add Video link.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected videos action elements are present")

        action_elements = {
            "Search Button": self.get_videos_search_button,
            "Clear Search Button": self.get_videos_search_clear_button,
            "Add Video Button": self.get_add_video_button,
        }
        return self.verify_page_elements_present(action_elements, "Videos Action Elements")

    def verify_all_video_grid_elements_present(self) -> Tuple[bool, List[str]]:
        """
        Verify that all expected video grid and card elements are present.

        The Videos page uses a card grid layout. This method checks that the
        grid container, at least one video card, and the key content elements
        within cards (thumbnails, names, overviews, organizations, countries)
        are all present.

        Returns:
            Tuple containing:
                - bool: True if all elements were found, False otherwise
                - List[str]: List of missing element names (empty if all found)
        """
        self.logger.info("Verifying that all expected video grid/card elements are present")

        grid_elements = {
            "Video Grid": self.get_video_grid,
            "Video Cards": self.get_video_cards,
            "Card Thumbnails": self.get_video_card_thumbnails,
            "Card Names": self.get_video_card_names,
            "Card Overviews": self.get_video_card_overviews,
            "Card Organizations": self.get_video_card_organizations,
            "Card Countries": self.get_video_card_countries,
        }
        return self.verify_page_elements_present(grid_elements, "Video Grid Elements")

    def count_video_cards(self) -> int:
        """
        Count the number of video cards rendered in the grid.

        Returns:
            int: The number of video cards in the grid.
        """
        self.logger.info("Counting the number of video cards in the grid")
        try:
            cards = self.get_video_cards()
            card_count = cards.count()
            self.logger.info(f"Found {card_count} video cards in the grid")
            return card_count
        except Exception as e:
            self.logger.error(f"An error occurred while counting video cards: {str(e)}")
            return 0

    def get_video_name_values(self) -> List[str]:
        """
        Get the names of all videos visible in the current page of the grid.

        Returns:
            List[str]: A list of video names, or an empty list if none found.
        """
        self.logger.info("Getting the names of all videos in the grid on the current page")
        video_names = []
        try:
            name_elements = self.get_video_card_names()
            count = name_elements.count()

            for i in range(count):
                try:
                    video_name = name_elements.nth(i).inner_text()
                    video_names.append(video_name)
                    self.logger.debug(f"Found video name: '{video_name}'")
                except Exception as row_error:
                    self.logger.error(f"Error getting video name at index {i}: {str(row_error)}")
                    continue

            self.logger.info(f"Found a total of {len(video_names)} video names")
            return video_names
        except Exception as e:
            self.logger.error(f"An error occurred while trying to get video names: {str(e)}")
            return []
