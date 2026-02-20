#test_installations_page.py (Playwright version)
import os
import math
import pytest
import requests
import uuid
from datetime import datetime
from fixtures.admin_menu.installations_fixtures import installations_page, installations_pagination_test_data
from pytest_check import check
from page_objects.common.base_page import BasePage
from utilities.search_mixins import SimpleSearchMixin
from utilities.utils import logger
from utilities.auth import get_auth_headers, get_auth_token
from urllib.parse import urlparse
    
class TestInstallationsPageFunctional(SimpleSearchMixin):
    """
    Test suite for Installations page functionality.
    
    Now inherits from SimpleSearchMixin to get robust search testing capabilities.
    """
        
    @pytest.mark.functional
    @pytest.mark.installations
    @pytest.mark.pagination
    def test_installations_pagination_navigation(self, installations_page, installations_pagination_test_data, verify_ui_elements):
        """
        Test that pagination navigation works properly on the Installations page.

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
        assert len(installation_ids) > 25, "Need more than 25 installations to test pagination."
        
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
                        # Click and wait for the page to load
                        logger.info("Clicking next page button")
                        next_button.click()
                        ip.page.wait_for_load_state("networkidle")
                        ip.page.wait_for_timeout(500)
                        
                        # Get the second page rows with error handling
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
                            
                            # Get names on current page
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
                    logger.info("Could not get pagination counts, skipping installation pagination test")

    @pytest.mark.functional
    @pytest.mark.installations
    @pytest.mark.search
    @pytest.mark.debug
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
        logger.info("Starting installations search test with search mixin")
        
        # Get the names of our test installations
        # We'll need to query the API since the fixture only returns IDs
        api_base_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
        headers = get_auth_headers()
        
        # Get an installation name to search for
        test_installation_id = installations_pagination_test_data[0]
        logger.info(f"Test installation ID: {test_installation_id}")
        installation_name = None
        
        try:
            response = requests.get(f"{api_base_url}/Installations/{test_installation_id}/details", headers=headers)
            if response.status_code == 200:
                installation_data = response.json()
                installation_name = installation_data.get("name")
                logger.info(f"Installation name: {installation_name}")
        except Exception as e:
            logger.error(f"Failed to get installation name: {str(e)}")
        
        if not installation_name:
            logger.warning("Could not get installation name for search test")
            return
        
        for ip in installations_page:
            # Define the search configuration for installations
            search_config = {
                'search_input_getter': ip.get_installation_search_text,
                'search_button_getter': ip.get_installation_search_button,
                'results_container_getter': ip.get_installations_table_rows,
                'results_selector': "table tbody tr:has(td:not(:empty))",
            }
            
            # Define the test cases for installations search
            test_cases = [
                {
                    'name': 'Exact Name Match',
                    'search_term': installation_name,
                    'expected_min_results': 1,
                    'description': f'Should find the test installation with ID {test_installation_id}'
                },
                {
                    'name': 'Partial Name Match',
                    'search_term': installation_name[-8:],  # Last 8 characters
                    'expected_min_results': 1,
                    'description': f'Should find installations with names containing "{installation_name[-8:]}"'
                },
                {
                    'name': 'Non-Existent Name',
                    'search_term': "ZZZZZ_NonExistentInstallation_ZZZZ",
                    'expected_min_results': 0,
                    'description': 'Should not find any installations with a non-existent name'
                }
            ]
            
            # Execute the sarch test suite using the mixin
            self.execute_simple_search_test(ip, search_config, test_cases)
        
    @pytest.mark.functional
    @pytest.mark.installations
    @pytest.mark.navigation
    def test_installation_details_navigation(self, installations_page):
        """
        Test basic navigation to installation details page.
        
        This test verifies:
        1. Clicking on an installation name navigates to the details page
        2. The URL and page title are correct
        3. We can navigate back to the installations list
        """
        logger.info("Starting installation details navigation test")
        
        for ip in installations_page:
            # Refresh the page to ensure installations are loaded
            ip.page.reload()
            ip.page.wait_for_load_state("networkidle")
            ip.page.wait_for_selector("table tbody tr:has(td:not(:empty))")
            ip.page.wait_for_timeout(2000)
            
            # Find an installation in the table
            rows = ip.get_installations_table_rows()
            rows_count = rows.count()
            logger.info(f"Found {rows_count} installations to test with")
            
            if rows_count > 0:
                try:
                    # Get the name from the first row
                    first_row = rows.first
                    name_cell = first_row.locator("td").first
                    installation_name = name_cell.inner_text(timeout=2000)
                    logger.info(f"Selected installation: {installation_name}")
                    
                    # Click on the name to navigate to details
                    name_cell.click()
                    
                    # Wait for details page to load
                    ip.page.wait_for_load_state("networkidle")
                    ip.page.wait_for_selector("h1")
                    ip.page.wait_for_timeout(1000)
                    
                    # Verify URL and title
                    url = ip.page.url
                    logger.info(f"Navigated to URL: {url}")
                    check.is_true("/installation/" in url, 
                                f"URL should contain '/installation/', got: {url}")
                    
                    page_title = ip.page.get_by_role("heading", level=1)
                    title_text = page_title.inner_text(timeout=2000)
                    logger.info(f"Details page title: {title_text}")
                    check.is_true("Installation Details" in title_text, 
                                f"Title should be 'Installation Details', got: {title_text}")
                    
                    # Navigate back
                    logger.info("Navigating back to installations page")
                    ip.page.go_back()
                    
                    # Verify we returned to installations page
                    ip.page.wait_for_load_state("networkidle")
                    ip.page.wait_for_selector("h1")
                    
                    page_title = ip.page.get_by_role("heading", level=1)
                    title_text = page_title.inner_text(timeout=2000)
                    check.equal(title_text, "Installations", 
                            "Should be back on Installations page")
                    
                except Exception as e:
                    logger.error(f"Error during navigation test: {str(e)}")
                    check.fail(f"Navigation test failed with error: {str(e)}")
            else:
                logger.warning("No installations found to test details navigation")
                
    @pytest.mark.functional
    @pytest.mark.installations
    @pytest.mark.verification
    def test_installation_details_content(self, installations_page, installations_pagination_test_data):
        """
        Test that installation details page displays correct information.
        
        This test verifies:
        1. The details page accurately displays the installation's properties
        2. All expected fields match what was created via the fixture
        """
        logger.info("Starting installation details content verification test")
        
        # We need to get the details for a test installation from the API
        if not installations_pagination_test_data or len(installations_pagination_test_data) == 0:
            logger.warning("No test installations available for content verification")
            return
        
        # Get details for the first test installation
        test_installation_id = installations_pagination_test_data[0]
        logger.info(f"Using test installation ID: {test_installation_id}")
        
        # Get installation details from API for comparison
        api_base_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
        headers = get_auth_headers()
        expected_data = None
        
        try:
            response = requests.get(f"{api_base_url}/Installations/{test_installation_id}/details", headers=headers)
            if response.status_code == 200:
                expected_data = response.json()
                installation_name = expected_data.get("name")
                logger.info(f"Got details for installation: {installation_name}")
            else:
                logger.error(f"Failed to get installation details: {response.status_code}")
                return
        except Exception as e:
            logger.error(f"API error getting installation details: {str(e)}")
            return
        
        # Now let's search for this installation and navigate to its details
        for ip in installations_page:
            try:
                # Refresh and wait for page to load
                ip.page.reload()
                ip.page.wait_for_load_state("networkidle")
                
                # Search for our specific installation
                search_box = ip.get_installation_search_text()
                search_button = ip.get_installation_search_button()
                
                search_box.clear()
                search_box.fill(installation_name)
                logger.info(f"Searching for installation: {installation_name}")
                search_button.click()
                
                # Wait for search results
                ip.page.wait_for_load_state("networkidle")
                ip.page.wait_for_selector("table tbody tr:has(td:not(:empty))")
                ip.page.wait_for_timeout(3000)
                
                # Find and click on our installation
                results_rows = ip.get_installations_table_rows()
                found = False
                
                for i in range(results_rows.count()):
                    try:
                        name_cell = results_rows.nth(i).locator("td").first
                        name = name_cell.inner_text(timeout=2000)
                        
                        if name == installation_name:
                            logger.info(f"Found installation '{installation_name}' in search results")
                            name_cell.click()
                            found = True
                            break
                    except Exception as e:
                        logger.warning(f"Error checking row {i}: {str(e)}")
                        continue
                
                if not found:
                    logger.error(f"Installation '{installation_name}' not found in search results")
                    check.fail(f"Could not find installation '{installation_name}' to verify details")
                    return
                
                # Wait for details page to load
                ip.page.wait_for_load_state("networkidle")
                ip.page.wait_for_selector("h1")
                ip.page.wait_for_timeout(2000)
                
                # Verify page title as requested
                page_title = ip.page.get_by_role("heading", level=1)
                title_text = page_title.inner_text(timeout=2000)
                logger.info(f"Details page title: {title_text}")
                check.is_true("Installation Details" in title_text, 
                            f"Title should be 'Installation Details', got: {title_text}")
                
                # Define a function to get field values from the page
                def get_field_value(label_getter, input_getter, is_input=True):
                    """Helper function to get field values using getters"""
                    try:
                        # First check if the label exists
                        label = label_getter()
                        if label.count() == 0:
                            logger.warning(f"Label not found for {label_getter.__name__}")
                            return None
                        
                        # Get the value based on the input type
                        value_element = input_getter()
                        if value_element.count() == 0:
                            logger.warning(f"Value element not found for {input_getter.__name__}")
                            return None
                        
                        if is_input:
                            # For input fields, get the value attribute
                            # For different input types, we might need different approaches
                            tag_name = value_element.evaluate("el => el.tagName.toLowerCase()")
                            
                            if tag_name == "input":
                                input_type = value_element.evaluate("el => el.type")
                                if input_type == "checkbox":
                                    return value_element.is_checked()
                                else:
                                    return value_element.input_value()
                            elif tag_name == "textarea":
                                return value_element.input_value()
                            elif tag_name == "select":
                                return value_element.evaluate("el => el.value")
                            else:
                                # For other elements, use inner text
                                return value_element.inner_text(timeout=2000).strip()
                        else:
                            # For display-only elements
                            return value_element.inner_text(timeout=2000).strip()
                            
                    except Exception as e:
                        logger.warning(f"Error getting field value: {str(e)}")
                        return None
                
                # Define the fields to verify using our getter methods
                fields_to_verify = [
                    # Format: (label_getter, input_getter, data_key, transform_func, is_input)
                    (ip.get_installation_name_label, ip.get_installation_name_textbox, "name", None, True),
                    (ip.get_installations_tips_label, ip.get_installations_tips_textbox, "tips", None, True),
                    (ip.get_installations_globestartlatitude_label, ip.get_installations_globestartlatitude_textbox, "globeStartLat", str, True),
                    (ip.get_installations_globestartlongitude_label, ip.get_installations_globestartlongitude_textbox, "globeStartLong", str, True),
                    (ip.get_installations_apptimerlengthseconds_label, ip.get_installations_apptimerlengthseconds_textbox, "appTimerLengthSeconds", str, True),
                    (ip.get_installations_idletimerlengthseconds_label, ip.get_installations_idletimerlengthseconds_textbox, "idleTimerLengthSeconds", str, True),
                    (ip.get_installations_idletimerdelayseconds_label, ip.get_installations_idletimerdelayseconds_textbox, "idleTimerDelaySeconds", str, True),
                    (ip.get_installations_show_graphic_death_label, ip.get_installations_show_graphic_death_checkbox, "showGraphicDeath", None, True),
                    (ip.get_installations_show_graphic_sex_label, ip.get_installations_show_graphic_sex_checkbox, "showGraphicSex", None, True)
                ]
                
                # Verify each field
                for label_getter, input_getter, data_key, transform_func, is_input in fields_to_verify:
                    # Get the field's displayed value
                    actual_value = get_field_value(label_getter, input_getter, is_input)
                    
                    if actual_value is not None:
                        # Get expected value and transform if needed
                        expected_value = expected_data.get(data_key)
                        
                        # Apply transformation if specified
                        if transform_func:
                            expected_value = transform_func(expected_value)
                        
                        # Convert to string if not already (except for booleans)
                        if not isinstance(expected_value, bool) and not isinstance(actual_value, bool):
                            expected_value = str(expected_value)
                            actual_value = str(actual_value)
                        
                        field_name = label_getter.__name__.replace("get_", "").replace("_label", "")
                        logger.info(f"Checking field '{field_name}': Expected '{expected_value}', Got '{actual_value}'")
                        
                        check.equal(actual_value, expected_value, 
                                f"Field '{field_name}' value mismatch. Expected: '{expected_value}', Got: '{actual_value}'")
                    else:
                        logger.warning(f"Skipping verification for {label_getter.__name__} - could not get value")
                
                logger.info("Details verification complete")
                
            except Exception as e:
                logger.error(f"Error during details verification: {str(e)}")
                check.fail(f"Details verification failed: {str(e)}")

    @pytest.mark.installations
    @pytest.mark.functional
    def test_add_installation(self, installations_page):
        """
        Test creating a new installation through the UI.
        
        This test verifies:
        1. Clicking the Add button opens the creation form
        2. Filling out the form and submitting creates a new installation
        3. The new installation appears in the list
        4. We can navigate to the installation details
        5. Clean up the created installation via API    
        
        Args:
            installations_page: The InstallationsPage fixture
        """
        logger.info("Starting installation creation test")
        
        # Generate a unique identifier for this test run.
        # Format: AUTOTEST_UI_{YYYYMMDD_HHMMSS}_{8-char UUID} = 36 chars max.
        # Username was previously included but caused 500 errors because the
        # Installation.Name column is capped at 50 characters in the database.
        test_run_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_installation_name = f"AUTOTEST_UI_{timestamp}_{test_run_id}"
        
        created_installation_id = None  # To store the ID of the created installation
        
        try:
            for ip in installations_page:
                # Step 1 - Create the installation through the UI
                logger.info(f"Creating new installation: {test_installation_name}")
                created_installation_id = self._create_installation_via_ui(ip, test_installation_name)
                
                # Step 2 - Verify the installation was created and is accessible
                self._verify_installation_creation(ip, test_installation_name)
                
                logger.info(f"Successfully created installation: {test_installation_name} with ID {created_installation_id}")
                
        finally:
            # Step 3 - Clean up the created installation via API
            if created_installation_id:
                self._cleanup_test_installation(created_installation_id, test_installation_name)
            else:
                logger.warning("No installation was created, skipping cleanup")
            
    def _create_installation_via_ui(self, ip, test_installation_name):
        """
        Create an installation through the UI and return its ID.
        
        This method handles the UI interaction and extracts the installation ID
        from the details page URL after creation.
        
        Returns:
            str: The installation ID (UUID) for the created installation
        """
        logger.info("Creating installation through UI")
        
        # Click the Add button to open the creation form
        add_button = ip.get_installation_add_button()
        add_button.click()
        
        # Wait for the form to appear
        ip.page.wait_for_selector("input[name=\'name\']")
        
        # Fill out the form fields
        ip.get_installation_name_textbox().fill(test_installation_name)
        
        # Select an organization from the dropdown
        organization_dropdown = ip.get_installation_select_organization_dropdown()
        organization_dropdown.click()
        ip.page.get_by_text("Test Organization - Used for Automation Tests", exact=True).click()
        
        # Fill out Tips
        ip.get_installations_tips_textbox().fill("Test tips from UI automation")
        
        # Fill out numeric fields
        ip.get_installations_globestartlatitude_textbox().fill("1")
        ip.get_installations_globestartlongitude_textbox().fill("1")
        ip.get_installations_apptimerlengthseconds_textbox().fill("5")
        ip.get_installations_idletimerlengthseconds_textbox().fill("10")
        ip.get_installations_idletimerdelayseconds_textbox().fill("15")
        
        # Select video catalogue
        video_catalogue_dropdown = ip.get_installations_select_video_catalogue_dropdown()
        video_catalogue_dropdown.click()
        ip.page.get_by_text("Test Organization Catalogue").click()

        # Select panel collection (WILDXR-1868)
        panel_collection_dropdown = ip.get_installations_select_panel_collection_dropdown()
        panel_collection_dropdown.click()
        ip.page.get_by_text("Test Panel Collection - Used for Automation Tests", exact=True).click()

        # Select automatic download mode
        # The mode names are seeded reference data so we select the first available
        # option rather than hardcoding a name that might differ across environments.
        automatic_download_dropdown = ip.get_installations_select_automatic_download_mode_dropdown()
        automatic_download_dropdown.click()
        ip.page.locator("[id$='-option-0']").first.click()

        # Click Save
        ip.get_save_button().click()

        # Wait for the page to refresh
        ip.page.wait_for_load_state("networkidle")
        
        # Verify we're back on the installations list page
        page_title = ip.page.get_by_role("heading", level=1)
        check.equal(page_title.inner_text(), "Installations",
                    "Should be back on Installations page after creation")
        
        # Find installation and get its ID from the details page URL
        installation_id = self._find_and_extract_installation_id(ip, test_installation_name)
        
        if not installation_id:
            raise Exception(f"Could not extract installation ID for '{test_installation_name}'")
        
        logger.info(f"Successfully created installation '{test_installation_name}' with ID {installation_id}")
        return installation_id
    
    def _find_and_extract_installation_id(self, ip, test_installation_name):
        """
        Find the created installation and extract its ID by navigating to details.
        
        This method searches for the installation, clicks on it to go to details,
        and extracts the UUID from the URL.
        
        Returns:
            str: The installation ID (UUID) or None if not found
        """
        logger.info(f"Searching for installation '{test_installation_name}' to extract ID")
        
        # Search for new installation
        search_box = ip.get_installation_search_text()
        search_button = ip.get_installation_search_button()
        
        search_box.clear()
        search_box.fill(test_installation_name)
        search_button.click()
        
        # Wait for results to load
        ip.page.wait_for_load_state("networkidle")
        ip.page.wait_for_selector("table tbody tr:has(td:not(:empty))")
        ip.page.wait_for_timeout(3000)
        
        rows = ip.get_installations_table_rows()
        installation_found = False
        
        for i in range(rows.count()):
            name_cell = rows.nth(i).locator("td").first
            displayed_name = name_cell.inner_text()
            
            if displayed_name == test_installation_name:
                logger.info(f"Found installation '{test_installation_name}' in search results")
                installation_found = True
                
                # Click on the instalation name to navigate to details
                
                name_cell.click()
                break
        
        if not installation_found:
            logger.error(f"Installation '{test_installation_name}' not found in search results")
            return None
        
        # Wait for details page to load
        ip.page.wait_for_load_state("networkidle")
        ip.page.wait_for_selector("h1")
        ip.page.wait_for_timeout(2000)
        
        # Extract the installation ID from the URL
        current_url = ip.page.url
        logger.info(f"Details page URL after creation: {current_url}")
        
        # The URL should be .../installations/{uuid}/details
        # We need to extract the UUID part
        installation_id = self._extract_id_from_url(current_url)
        
        if installation_id:
            logger.info(f"Extracted installation ID: {installation_id}")
        else:
            logger.error(f"Could not extract installation ID from URL: {current_url}")
            
        return installation_id
    
    def _extract_id_from_url(self, url):
        """
        Extract the installation ID (UUID) from the details page URL.
        
        Expected URL format: .../installation/{uuid}/details
        or: .../Installations/{uuid}/details
        
        Returns:
            str: The UUID if found, None otherwise
        """
        try:
            # Parse the URL to get the path
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.split('/')
            
            # Look for the UUID in the path
            # UUIDs are typically 36 characters long with hyphens
            for part in path_parts:
                # Check if this part looks like a UUID
                if len(part) == 36 and part.count('-') == 4:
                    # Additional validationL try to parse as UUID
                    try:
                        uuid.UUID(part)  # This will raise ValueError if not a valid UUID
                        logger.info(f"Found valid UUID in URL: {part}")
                        return part
                    except ValueError:
                        logger.warning(f"Part '{part}' is not a valid UUID")
                        continue
                    
            logger.warning(f"No UUID found in URL path: {parsed_url.path}")
            return None
        
        except Exception as e:
            logger.error(f"Error extracting ID from URL '{url}': {str(e)}")
            return None
        
    def _verify_installation_creation(self, ip, test_installation_name):            
        """
        Verify that the installation was successfully created and is accessible.
        
        This method performs additional validation beyond just finding the installation
        in the search results.
        """
        logger.info(f"Verifying installation creation for '{test_installation_name}'")
        
        # Chek that we're on the details page with the correct title
        page_title = ip.page.get_by_role("heading", level=1)
        title_text = page_title.inner_text()
        check.is_true("Installation Details" in title_text,
                    f"Expected title to contain 'Installation Details', got: {title_text}")
        
        # Verify the installation name is displayed correctly on the details page
        try:
            name_field = ip.get_installation_name_textbox()
            displayed_name = name_field.input_value()
            check.equal(displayed_name, test_installation_name,
                        f"Installation name mismatch. Expected: '{test_installation_name}', "
                        f"Got: '{displayed_name}'")
            logger.info(f"Installation name verified: {displayed_name}")
        except Exception as e:
            logger.error(f"Error verifying installation name: {str(e)}")
            
    def _cleanup_test_installation(self, installation_id, installation_name):
        """
        Clean up the test installation using the API.
        
        This method attempts to delete the installation and handles any errors gracefully.
        Even if cleanup fails, it won't cause the test to fail.
        """
        logger.info(f"Starting cleanup for installation '{installation_name}' with ID {installation_id}")
        
        try:
            # Get API configuration
            api_base_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")

            if not api_base_url:
                logger.error("API_BASE_URL not set, cannot clean up installation")
                return

            # Prepare the delete request
            headers = get_auth_headers()
            
            delete_endpoint = f"{api_base_url}/Installations/delete?id={installation_id}"
            
            # Attempt deletion
            logger.info(f"Sending DELETE request to {delete_endpoint}")
            delete_response = requests.delete(delete_endpoint, headers=headers, timeout=30)
            
            if delete_response.status_code in [200,204]:
                logger.info(f"Successfully deleted installation '{installation_name}' with ID {installation_id}")
            else:
                logger.error(f"Failed to delete installation '{installation_name}' (ID: {installation_id}). "
                            f"Status code: {delete_response.status_code}, Response: {delete_response.text}")   
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while trying to delete installation '{installation_name}' (ID: {installation_id})")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during cleanup of installation '{installation_name}' (ID: {installation_id}): {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during cleanup of installation '{installation_name}' (ID: {installation_id}): {str(e)}")
            
    # Helper method to get the installation name for search testing
    def _get_test_installation_name(self, installations_pagination_test_data):
        """
        Get the name of a test installation for search testing.
        
        This is your existing logic extracted into a helper method.
        """
        api_base_url = os.getenv("API_BASE_URL").replace("\\x3a", ":")
        headers = get_auth_headers()

        test_installation_id = installations_pagination_test_data[0]
        
        try:
            response = requests.get(f"{api_base_url}/Installations/{test_installation_id}/details", headers=headers)
            if response.status_code == 200:
                installation_data = response.json()
                installation_name = installation_data.get("name")
                logger.info(f"Using test installation: {installation_name}")
                return installation_name
        except Exception as e:
            logger.error(f"Failed to get installation name: {str(e)}")
        
        pytest.skip("Could not get test installation name for search testing")            
