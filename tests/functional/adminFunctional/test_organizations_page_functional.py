#test_organizations_page.py (Playwright version)
import os
import math
import pytest
import requests
from datetime import datetime
from fixtures.admin_menu.organizations_fixtures import organizations_page, organizations_pagination_test_data
from pytest_check import check
from page_objects.common.base_page import BasePage
from utilities.utils import logger
from utilities.auth import get_auth_headers
from conftest import api_url

class TestOrganizationsPageFunctional:
    
#     @pytest.mark.functional
#     @pytest.mark.organizations
#     @pytest.mark.pagination
#     @pytest.mark.debug
#     def test_organizations_pagination_navigation(self, organizations_page, organizations_pagination_test_data, verify_ui_elements):
#         """
#         Test that pagination navigation works properly on the Organizations page.

#         This test verifies that:
#         1. Pagination elements are correctly displayed
#         2. Navigation between pages works correctly
#         3. The correct data is displayed on each page

#         Args:
#             organizations_page: The OrganizationsPage fixture
#             organizations_pagination_test_data: Fixture that creates test organizations
#             verify_ui_elements: The UI verification fixture
#         """
#         logger.info("Starting organizations pagination navigation test")
        
#         # Verify the fixture created enough organizations for pagination
        
#         organization_ids = organizations_pagination_test_data
#         assert len(organization_ids) > 25, "Need more than 25 organizations for pagination test"
    
#         for op in organizations_page:
#             # Refresh the page to ensure that all organizations are loaded
#             op.page.reload()
#             op.page.wait_for_load_state("networkidle")
            
#             # 1. Verify pagination elements are present
#             results = verify_ui_elements.pagination_elements([op])
#             for page, all_elements, missing_elements in results:
#                 check.is_true(all_elements, f"Missing pagination elements {', '.join(missing_elements)}")
                
#             # 2. Get data about current page
#             counts = op.get_pagination_counts()
#             check.is_not_none(counts, "Could not get pagination counts")
            
#             if counts:
#                 current_start, current_end, total_records = counts
#                 page_size = current_end - current_start + 1
#                 logger.info(f"Page counts: {current_start} - {current_end} of {total_records}")
                
#                 # Verify our fixture records are part of the total
#                 check.greater_equal(total_records, len(organization_ids),
#                                     "Total records in pagination should be greater than or equal to created organizations")
                
#                 # Save first page organization for comparison
#                 op.page.wait_for_selector("table tbody tr")
#                 first_page_rows = op.get_organization_table_rows()
#                 first_page_count = first_page_rows.count()
#                 logger.info(f"Found first page with {first_page_count} organizations")

#                 first_page_names = []
#                 for i in range(first_page_count):
#                     try:
#                         name_cell = first_page_rows.nth(i).locator("td").first
#                         name = name_cell.inner_text(timeout=3000)
#                         first_page_names.append(name)
#                     except Exception as e:
#                         logger.warning(f"Error getting name from row {i} on first page: {str(e)}")
                
#                 logger.info(f"Collected {len(first_page_names)} names from first page")
                
#                 # Calculate total pages and verify if we can test pagination
#                 total_pages = math.ceil(total_records / page_size)
#                 logger.info(f"Total pages: {total_pages}")
                
#                 if total_pages > 1:
                    
#                     # Navigate directly to the next page
#                     next_button = op.get_next_page_button()
#                     check.is_true(next_button.count() > 0, "Next page button not found")
                    
#                     if next_button.count() > 0:
#                         # Click and wait for the page to load
#                         logger.info("Clicking the next page button")
#                         next_button.click()
#                         op.page.wait_for_load_state("networkidle")
#                         op.page.wait_for_timeout(500)
                        
#                         # Get the second page rows with error handling
#                         second_page_rows = op.get_organization_table_rows()
#                         second_page_count = second_page_rows.count()
#                         logger.info(f"Found second page with {second_page_count} organizations")
                        
#                         # Get the names from the second page
#                         second_page_names = []
                        
#                         # Get the names from the second page rows
#                         for i in range(second_page_count): # Only iterate through rows that exist
#                             try:
#                                 name_cell = second_page_rows.nth(i).locator("td").first
#                                 name = name_cell.inner_text(timeout=3000) # Short timeout
#                                 second_page_names.append(name)
#                             except Exception as e:
#                                 logger.warning(f"Error getting name from row {i} on second page: {str(e)}")
                                
#                         logger.info(f"Collected {len(second_page_names)} names from second page")
                        
#                         # Check that pages show different data
#                         check.is_true(len(set(second_page_names)) > 0,
#                                     "Second page should have data")
#                         check.is_true(set(first_page_names) != set(second_page_names),
#                                     "First and second pages should show different data")
                        
#                         # Navigate back to the first apge
#                         prev_button = op.get_previous_page_button()
#                         check.is_true(prev_button.count() > 0, "Previous page button not found")
                        
#                         if prev_button.count() > 0:
#                             logger.info("Clicking the previous page button")
#                             prev_button.click()
#                             op.page.wait_for_load_state("networkidle")
#                             op.page.wait_for_timeout(500)
                            
#                             # Get current page rows after navigation back to page 1
#                             current_rows = op.get_organization_table_rows()
#                             current_rows_count = current_rows.count()
#                             logger.info(f"Found {current_rows_count} organizations on current page after navigating back to first page")
                            
#                             # Get names on current page
#                             current_page_names = []
                            
#                             for i in range(current_rows_count):
#                                 try:
#                                     name_cell = current_rows.nth(i).locator("td").first
#                                     name = name_cell.inner_text(timeout=3000)
#                                     current_page_names.append(name)
#                                 except Exception as e:
#                                     logger.warning(f"Error getting name from row {i} on current page: {str(e)}")
                                    
#                             logger.info(f"Collected {len(current_page_names)} names from current page")
                            
#                             # Compare sets instead of lists to handle potential ordering differences
#                             check.equal(set(first_page_names), set(current_page_names),
#                                         "Navigating back to first page should show same data as first page")
                            
#                     else:
#                         logger.info("Not enough pages to test navigation")
#                 else:
#                     logger.info("Could not get pagination counts, skipping organization pagination test")

    @pytest.mark.organizations
    @pytest.mark.functional
    @pytest.mark.debug
    def test_add_organization(self, organizations_page):
        """
        Test creating a new organization through the UI.

        This test verifies:
        1. Clicking the Add button opens the creation form
        2. Filling out the form and submitting creates a new organization
        3. The new organization appears in the list

        Teardown: the created organization is deleted via API after the test
        so it does not accumulate as orphaned test data in QA.

        Args:
            organizations_page: The OrganizationsPage fixture
        """
        logger.info("Starting organization creation test")

        # AUTOTEST_ prefix ensures cleanup_orphaned_test_records catches this record
        # if teardown fails for any reason.
        test_organization_name = f"AUTOTEST_Org_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"Test organization name: {test_organization_name}")

        created_org_id = None

        try:
            for op in organizations_page:
                # Click the Add button
                add_button = op.get_add_organization_button()
                add_button.click()

                # Wait for the form to appear
                op.page.wait_for_selector("input[name=\"name\"]")

                # Fill out the form
                op.get_add_organization_textbox().fill(test_organization_name)

                # Click Save
                op.get_save_button().click()

                # Wait for the page to refresh
                op.page.wait_for_load_state("networkidle")

                # Navigate back to Organizations page
                # Hopefully this can be removed once bug is fixed
                op.page.get_by_role("button", name="Admin").click()
                op.page.get_by_role("link", name="Organizations").click()

                # Verify we're back on the organizations list page
                page_title = op.page.get_by_role("heading", level=1)
                check.equal(page_title.inner_text(), "Organizations",
                        "Should be back on Organizations page after saving")

                # Wait for results to load
                op.page.wait_for_load_state("networkidle")

                # Verify the new organization is in the results
                rows = op.get_organization_table_rows()
                found = False
                for i in range(rows.count()):
                    name_cell = rows.nth(i).locator("td").first
                    if name_cell.inner_text() == test_organization_name:
                        found = True
                        break

                check.is_true(found, f"New organization '{test_organization_name}' not found after creation")

            # Locate the created org via the search API so we can clean it up.
            # This runs once after all browser iterations complete.
            headers = get_auth_headers()
            search_resp = requests.get(
                f"{api_url}/Organization/search",
                params={"pageNumber": 1, "pageSize": 10, "name": test_organization_name},
                headers=headers,
                timeout=30,
            )
            if search_resp.status_code == 200:
                for org in search_resp.json().get("results", []):
                    if org.get("name") == test_organization_name:
                        created_org_id = org.get("organizationId")
                        break
            else:
                logger.warning(
                    f"Could not search for created org (status {search_resp.status_code}) — "
                    "will rely on AUTOTEST_ prefix cleanup"
                )

        finally:
            # Delete the test organization so it does not linger in QA.
            if created_org_id:
                headers = get_auth_headers()
                del_resp = requests.delete(
                    f"{api_url}/Organization/Delete",
                    params={"id": created_org_id},
                    headers=headers,
                    timeout=30,
                )
                if del_resp.status_code in (200, 204):
                    logger.info(f"Cleaned up test organization '{test_organization_name}' (ID: {created_org_id})")
                else:
                    logger.warning(
                        f"Failed to delete test organization '{test_organization_name}' "
                        f"(ID: {created_org_id}): {del_resp.status_code}"
                    )
            else:
                logger.warning(
                    f"No ID found for test organization '{test_organization_name}' — "
                    "record may need manual cleanup or will be caught by AUTOTEST_ prefix cleanup"
                )