#test_installations_page.py (Playwright version)
import os
import math
import pytest
import requests
from datetime import datetime
from pytest_check import check
from page_objects.admin_menu.installations_page import InstallationsPage
from page_objects.common.base_page import BasePage
from utilities.utils import get_browser_name,logger

@pytest.fixture
def installations_page(logged_in_page):
    """
    Fixture that provides the Installations page for each test

    Args:
        logged_in_page: A fixture providing a logged-in browser instance from conftest.py

    Yields:
        List[UsersPage]: A list of InstallationsPage objects for each logged-in browser instance
    """
    logger.debug("Staring installations_page fixture")
    installation_pages = []
    for page in logged_in_page:
        logger.info("=" * 80)
        logger.info(f"Navigating to Installations page on {get_browser_name(page)}")
        logger.info("=" * 80)
        
        #Navigate to Installations page
        page.get_by_role("button", name="Admin").click()
        page.get_by_role("link", name="Installations").click()
        
        # Create the page object
        installations_page = InstallationsPage(page)
        
        # Verify that we're on the Installations page
        if installations_page.verify_page_title():
            logger.info("Successfully navigated to Installations page")
            installation_pages.append(installations_page)
        else:
            logger.error(f"Failed to navigate to Installations page on {get_browser_name(page)}")
            
    logger.info(f"installations_page fixture: yielding {len(installation_pages)} installations page(s)")
    yield installation_pages
    logger.debug("installations_page fixture: finished")
    
class TestInstallationsPageUI:
    
    @pytest.mark.UI 
    @pytest.mark.installations
    def test_installations_page_title(self, installations_page):
        """
        Test that the Installations page title is present.
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        logger.debug("Starting test_installations_page_title")
        for ip in installations_page:
            title = ip.verify_page_title()
            check.is_true(title, "Installations title does not match")
            logger.info("Verification Successful :: Installations Page Title found")
            
    @pytest.mark.UI 
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_nav_elements(self, installations_page, verify_ui_elements):
        """
        Test that all navigation elements are present on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.nav_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations navigation elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Navigation Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_admin_elements(self, installations_page, verify_ui_elements):
        """
        Test that all admin elements are present in the Admin dropdown on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.admin_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations admin elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Admin Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_page_definition_elements(self, installations_page, verify_ui_elements):
        """
        Test that all definition elements are present in the Definitions dropdown on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
        """
        results = verify_ui_elements.definition_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations definition elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Definition Elements found on {get_browser_name(page)}")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installations_action_elements(self, installations_page):
        """
        Test that the Add Installation button, Search textbox, and Serch button are present on the Users page.
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        logger.debug("Starting test_installations_action_elements")
        for ip in installations_page:
            all_elements, missing_elements = ip.verify_all_installation_action_elements_present()
            check.is_true(all_elements, f"Missing installations action elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Installations Action Elements found")
    
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.table
    def test_installations_table_elements(self, installations_page):
        """
        Test that all table elements are present on the Installations page.
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        for ip in installations_page:
            all_elements, missing_elements = ip.verify_all_installation_table_elements_present()
            check.is_true(all_elements, f"Missing installations table elements: {', '.join(missing_elements)}")
            logger.info("Verification Successful :: All Installations Table Elements found")
            
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.pagination
    def test_installations_pagination_elements(self, installations_page, verify_ui_elements):
        """
        Test that pagination elements are correctly displayed on the Installations page.
    
        Args:
            installations_page: The InstallationsPage fixture
            verify_ui_elements: The fixture providing UI element verification functions
    """
        results = verify_ui_elements.pagination_elements(installations_page)
        for page, all_elements, missing_elements in results:
            check.is_true(all_elements, f"Missing installations pagination elements: {', '.join(missing_elements)}")
            logger.info(f"Verification Successful :: All Installations Pagination Elements found on {get_browser_name(page)}")
            
    @pytest.mark.UI 
    @pytest.mark.installations
    @pytest.mark.pagination
    def test_installations_pagination_navigation(self, installations_page, installations_pagination_test_data, verify_ui_elements):
        """
        Test that pagination navigation works properly on the Installations paage.
        
        This test verifies that:
        1. Pagination elements are correctly displayed
        2. Navigation between pages works correctly
        3. The correct data is displayed on each page

        Args:
            installations_page: The InstallationsPage fixture
            installations_pagination_test_data: Fixture that creates test installations
            verify_ui_elements: The UI verification fixture
        """
        logger.info("Starting installations pagination navigation test")
        
        # Verify the fixture created enough installations for pagination
        installation_ids = installations_pagination_test_data
        assert len(installation_ids) > 25, "Need more than 25 installatins to test pagination."
        
        for ip in installations_page:
            # Refresh the page to ensure that all installations are loaded
            ip.page.reload()
            ip.page.wait_for_load_state("networkidle")
            
            # 1. Verify pagination elements are present
            results = verify_ui_elements.pagination_elements([ip])
            for page, all_elements, missing_elements in results:
                check.is_true(all_elements,
                            f"Missing pagination elements {', '.join(missing_elements)}")
            
            # 2. Get data about current page
            counts = ip.get_pagination_counts()
            check.is_not_none(counts, "Could not get pagination counts")
            
            if counts:
                current_start, current_end, total_records = counts
                page_size = current_end - current_start + 1
                logger.info(f"Page counts: {current_start} to {current_end} of {total_records}")
                
                # Verify our fixture records are part of the total
                check.greater_equal(total_records, len(installation_ids), 
                                    "Total records should include our test installations")

                # Save first page installtions for comparison
                ip.page.wait_for_selector("table tbody tr")
                first_page_rows = ip.get_installations_table_rows()
                first_page_count = first_page_rows.count()
                logger.info(f"Found first page with {first_page_count} rows")
                
                first_page_names = []
                for i in range(first_page_count):
                    try:
                        name_cell = first_page_rows.nth(i).locator("td").first
                        name = name_cell.inner_text(timeout=3000)
                        first_page_names.append(name)
                    except Exception as e:
                        logger.warning(f"Error getting name from row {i} on first page: {str(e)}")
                        
                logger.info(f"Collected {len(first_page_names)} names from first page")
                
                # Calculate total pages and verify if we can test pagination
                total_pages = math.ceil(total_records / page_size)
                logger.info(f"Total pages: {total_pages}")
                
                if total_pages > 1:
                
                    # Navigate directly to the next page
                    next_button = ip.get_next_page_button()
                    check.is_true(next_button.count() > 0, "Next page button not found")
                    
                    if next_button.count() > 0:
                        # click and wait for the page to load
                        logger.info("Clicking next page button")
                        next_button.click()
                        ip.page.wait_for_load_state("networkidle")
                        ip.page.wait_for_timeout(500)
                        
                        # Get the second page rows with better error handling
                        second_page_rows = ip.get_installations_table_rows()
                        second_page_count = second_page_rows.count()
                        logger.info(f"Found second page with {second_page_count} rows")
                        
                        # Get the names from the second page
                        second_page_names = []
                        
                        # Get the names from second page rows
                        for i in range(second_page_count):  # Only iterate through rows that exist
                            try:
                                name_cell = second_page_rows.nth(i).locator("td").first
                                name = name_cell.inner_text(timeout=3000)  # Short timeout
                                second_page_names.append(name)
                            except Exception as e:
                                logger.warning(f"Error getting name from row {i} on second page: {str(e)}")
                        
                        logger.info(f"Collected {len(second_page_names)} names from second page")
                        
                        # Check that pages show different data
                        check.is_true(len(set(second_page_names)) > 0,
                                    "Second page should have data")
                        check.is_true(set(first_page_names) != set(second_page_names),
                                    "Second page should show different installations than first page")
                        
                        # Navigate back to the first page
                        prev_button = ip.get_previous_page_button()
                        check.is_true(prev_button.count() > 0, "Previous page button not found")
                        
                        if prev_button.count() > 0:
                            logger.info("Clicking previous page button")
                            prev_button.click()
                            ip.page.wait_for_load_state("networkidle")
                            ip.page.wait_for_timeout(500)
                            
                            # Get current page rows after navigating back  
                            current_rows = ip.get_installations_table_rows()
                            current_rows_count = current_rows.count()
                            logger.info(f"Found {current_rows_count} rows after navigating back to first page")
                            
                            # Get names current page
                            current_page_names = []
                            
                            for i in range(current_rows_count):
                                try:
                                    name_cell = current_rows.nth(i).locator("td").first
                                    name = name_cell.inner_text(timeout=3000)
                                    current_page_names.append(name)
                                except Exception as e:
                                    logger.warning(f"Error getting name from row {i} on current page: {str(e)}")
                            
                            logger.info(f"Collected {len(current_page_names)} names from current page")
                            
                            # Compare sets instead of lists to handle potential ordering differences
                            check.equal(set(first_page_names), set(current_page_names),
                                        "Navigating back should show the same information on first page")
                    else:
                        logger.info("Not enough pages to test navigation")
                else:
                    logger.info("Could not get pagination counts, skipping test")
                
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.search
    def test_installations_search(self, installations_page, installations_pagination_test_data):
        """
        Test the search functionality on the Installations page.
        
        This test verifies:
        1. Searching for a known installation name returns that installation
        2. Searching for a partial name returns matching installations
        3. Searching for a non-existent name returns no results
        
        Args:
            installations_page: The InstallationsPage fixture
            installations_pagination_test_data: Fixture that creates test installations
        """
        logger.info("Starting installations search test")
        
        # Get the names of our test installations
        # We'll need to query the API since the fixture only returns IDs
        api_base_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
        api_token = os.getenv("API_TOKEN")
        headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        
        # Get an installation name to search for
        test_installation_id = installations_pagination_test_data[0]
        installation_name = None
        
        try:
            response = requests.get(f"{api_base_url}/Installations/{test_installation_id}", headers=headers)
            if response.status_code == 200:
                installation_data = response.json()
                installation_name = installation_data.get("name")
        except Exception as e:
            logger.error(f"Failed to get installation name: {str(e)}")
        
        if not installation_name:
            logger.warning("Could not get installation name for search test")
            return
        
        for ip in installations_page:
            # 1. Search for the exact name
            search_box = ip.get_installation_search_text()
            search_button = ip.get_installation_search_button()
            
            # Clear any existing text and enter search term
            search_box.clear()
            search_box.fill(installation_name)
            search_button.click()
            
            # Wait for results to load
            ip.page.wait_for_load_state("networkidle")
            
            # Check if our installation is in the results
            results = ip.get_installations_table_rows()
            found = False
            for i in range(results.count()):
                name_cell = results.nth(i).locator("td").first
                if name_cell.inner_text() == installation_name:
                    found = True
                    break
            
            check.is_true(found, f"Installation '{installation_name}' not found in search results")
            
            # 2. Search for a partial name (first 5 characters)
            partial_name = installation_name[:5]
            search_box.clear()
            search_box.fill(partial_name)
            search_button.click()
            
            # Wait for results to load
            ip.page.wait_for_load_state("networkidle")
            
            # Check if we have results
            results = ip.get_installations_table_rows()
            check.greater(results.count(), 0, f"No results found for partial name '{partial_name}'")
            
            # 3. Search for a non-existent name
            non_existent = "ZZZZZ_NonExistentInstallation_ZZZZ"
            search_box.clear()
            search_box.fill(non_existent)
            search_button.click()
            
            # Wait for results to load
            ip.page.wait_for_load_state("networkidle")
            
            # Check that no results are found
            results = ip.get_installations_table_rows()
            check.equal(results.count(), 0, f"Found unexpected results for '{non_existent}'")
            
            # Clear the search to restore all results
            search_box.clear()
            search_button.click()
        
    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.functionality
    def test_installation_details_navigation(self, installations_page, installations_pagination_test_data):
        """
        Test navigation to installation details page.
        
        This test verifies:
        1. Clicking on an installation name navigates to the details page
        2. The details page displays the correct installation information
        
        Args:
            installations_page: The InstallationsPage fixture
            installations_pagination_test_data: Fixture that creates test installations
        """
        logger.info("Starting installation details navigation test")
        
        for ip in installations_page:
            # Refresh the page to ensure all installations are loaded
            ip.page.reload()
            
            # Find an installation in the table
            rows = ip.get_installations_table_rows()
            if rows.count() > 0:
                # Get the name from the first row
                first_row = rows.first
                name_cell = first_row.locator("td").first
                installation_name = name_cell.inner_text()
                
                # Click on the name to navigate to details
                name_cell.click()
                
                # Wait for page to load
                ip.page.wait_for_load_state("networkidle")
                
                # Verify we're on the details page
                url = ip.page.url
                check.is_true("/installation/" in url, 
                            f"URL should contain '/installation/', got: {url}")
                
                # Verify the installation name is in the page title
                page_title = ip.page.get_by_role("heading", level=1)
                check.is_true(page_title.count() > 0, "Details page should have a title")
                
                if page_title.count() > 0:
                    title_text = page_title.inner_text()
                    check.is_true(installation_name in title_text, 
                                f"Title should contain installation name '{installation_name}', got: '{title_text}'")
                
                # Navigate back to the installations page
                ip.page.go_back()
                
                # Verify we're back on the installations page
                page_title = ip.page.get_by_role("heading", level=1)
                check.equal(page_title.inner_text(), "Installations", 
                        "Should be back on Installations page")
            else:
                logger.warning("No installations found to test details navigation")

    @pytest.mark.UI
    @pytest.mark.installations
    @pytest.mark.functionality
    def test_add_installation(self, installations_page):
        """
        Test creating a new installation through the UI.
        
        This test verifies:
        1. Clicking the Add button opens the creation form
        2. Filling out the form and submitting creates a new installation
        3. The new installation appears in the list
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        logger.info("Starting installation creation test")
        
        # Generate a unique name for the test installation
        test_installation_name = f"Test Installation UI {datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        for ip in installations_page:
            # Click the Add button
            add_button = ip.get_installation_add_button()
            add_button.click()
            
            # Wait for the form to appear
            ip.page.wait_for_selector("input[name=\"name\"]")
            
            # Fill out the form
            ip.get_installation_name_textbox().fill(test_installation_name)
            
            # Select an organization from the dropdown
            organization_dropdown = ip.get_installation_select_organization_dropdown()
            organization_dropdown.click()
            # Select the first option in the dropdown
            ip.page.locator(".css-1n7v3ny-option").first.click()
            
            # Fill out tips
            ip.get_installations_tips_textbox().fill("Test tips from UI automation")
            
            # Fill out numeric fields
            ip.get_installations_globestartlatitude_textbox().fill("0")
            ip.get_installations_globestartlongitude_textbox().fill("0")
            ip.get_installations_apptimerlengthseconds_textbox().fill("0")
            ip.get_installations_idletimerlengthseconds_textbox().fill("0")
            ip.get_installations_idletimerdelayseconds_textbox().fill("0")
            
            # Select video catalogue
            video_catalogue_dropdown = ip.get_installations_select_video_catalogue_dropdown()
            video_catalogue_dropdown.click()
            # Select the first option in the dropdown
            ip.page.locator(".css-1n7v3ny-option").first.click()
            
            # Click Save
            ip.get_save_button().click()
            
            # Wait for the page to refresh
            ip.page.wait_for_load_state("networkidle")
            
            # Verify we're back on the installations list page
            page_title = ip.page.get_by_role("heading", level=1)
            check.equal(page_title.inner_text(), "Installations", 
                    "Should be back on Installations page after saving")
            
            # Search for the new installation
            search_box = ip.get_installation_search_text()
            search_button = ip.get_installation_search_button()
            
            search_box.clear()
            search_box.fill(test_installation_name)
            search_button.click()
            
            # Wait for results to load
            ip.page.wait_for_load_state("networkidle")
            
            # Verify the new installation is in the results
            rows = ip.get_installations_table_rows()
            found = False
            for i in range(rows.count()):
                name_cell = rows.nth(i).locator("td").first
                if name_cell.inner_text() == test_installation_name:
                    found = True
                    break
            
            check.is_true(found, f"New installation '{test_installation_name}' not found after creation")