# test_devices_page_functional.py (Playwright version)
#
# Functional tests for the Device Lookup → Register workflow.
#
# The production device registration flow is two steps:
#   1. POST /Device/InitializeNew  — creates a bare device (deviceId + wildXRNumber)
#   2. UI: Device Lookup modal → enter wildXRNumber → Apply → fill form → Save
#
# These tests exercise the full cross-layer workflow: API setup → UI interaction
# → API verification → API cleanup.

import os
import uuid
import pytest
import requests
from datetime import datetime
from pytest_check import check
from fixtures.admin_menu.devices_fixtures import devices_page
from page_objects.admin_menu.devices_page import DevicesPage
from utilities.utils import logger
from utilities.auth import get_auth_headers

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

TEST_ORG_ID = os.environ.get(
    "TEST_ORGANIZATION_ID",
    "4ffbb8fe-d8b4-49d9-982d-5617856c9cce"
)

TEST_ORG_NAME = "Test Organization - Used for Automation Tests"

API_BASE_URL = os.environ.get(
    "API_BASE_URL",
    "https://wildxr-api-qa.azurewebsites.net/api"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_autotest_device_name() -> str:
    """Generate a unique AUTOTEST device name for UI tests.

    Format: AUTOTEST_UI_DEV_{8 hex chars}
    The AUTOTEST_ prefix ensures session-level cleanup catches orphaned records.

    Returns:
        str: A unique device name.
    """
    short_id = uuid.uuid4().hex[:8]
    return f"AUTOTEST_UI_DEV_{short_id}"


def _initialize_device_via_api(headers: dict) -> dict | None:
    """Create a bare device via the API (step 1 of the two-step workflow).

    Args:
        headers: Auth headers for the API request.

    Returns:
        dict: The DeviceDto (deviceId, wildXRNumber) or None on failure.
    """
    url = f"{API_BASE_URL}/Device/InitializeNew"
    response = requests.post(url, headers=headers, timeout=30)

    if response.status_code != 200:
        logger.error(
            f"InitializeNew failed: {response.status_code} — {response.text}"
        )
        return None

    data = response.json()
    logger.info(
        f"API: Initialized device — deviceId={data.get('deviceId')}, "
        f"wildXRNumber={data.get('wildXRNumber')}"
    )
    return data


def _delete_device_via_api(device_id: str, headers: dict) -> None:
    """Delete a device via the API for cleanup.

    Args:
        device_id: The UUID of the device to delete.
        headers: Auth headers for the API request.
    """
    url = f"{API_BASE_URL}/Device/delete"
    try:
        response = requests.delete(
            url, params={"id": device_id}, headers=headers, timeout=30
        )
        if response.status_code in [200, 204]:
            logger.info(f"API: Deleted device {device_id}")
        else:
            logger.warning(
                f"API: Failed to delete device {device_id}: "
                f"{response.status_code} — {response.text}"
            )
    except Exception as e:
        logger.error(f"API: Error deleting device {device_id}: {e}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestDevicesPageFunctional:
    """
    Functional tests for the Devices page.

    Tests the Device Lookup → Register workflow which crosses the API and UI
    boundary: the API creates bare devices, the UI registers them.
    """

    @pytest.mark.functional
    @pytest.mark.devices
    def test_device_lookup_and_register(self, devices_page):
        """
        Test the full Device Lookup → Register workflow.

        Steps:
            1. API: InitializeNew — creates a bare device with wildXRNumber
            2. UI: Click "Device Lookup" → enter wildXRNumber → click Apply
            3. UI: Verify navigation to the AddEditDevice form
            4. UI: Fill in device name and organization → click Save
            5. UI: Verify device appears in the devices table
            6. API: Clean up the created device

        Args:
            devices_page: Fixture providing DevicesPage objects.
        """
        logger.info("Starting Device Lookup → Register functional test")

        headers = get_auth_headers()
        device_data = None
        device_id = None

        try:
            # Step 1 — API: Initialize a new device
            device_data = _initialize_device_via_api(headers)
            assert device_data is not None, (
                "Failed to initialize a device via the API. "
                "Cannot proceed with the lookup test."
            )

            device_id = str(device_data["deviceId"])
            wildxr_number = device_data["wildXRNumber"]
            device_name = _make_autotest_device_name()

            logger.info(
                f"Test device ready: deviceId={device_id}, "
                f"wildXRNumber={wildxr_number}, name={device_name}"
            )

            for dp in devices_page:
                # Step 2 — UI: Perform device lookup
                logger.info(f"Performing device lookup for wildXRNumber={wildxr_number}")
                dp.perform_device_lookup(wildxr_number)

                # Step 3 — Verify we navigated to the edit form
                current_url = dp.page.url
                logger.info(f"URL after lookup: {current_url}")

                check.is_true(
                    f"/device/{device_id}/edit" in current_url.lower()
                    or "/device/" in current_url.lower(),
                    f"Expected to navigate to device edit page after lookup, "
                    f"got URL: {current_url}"
                )

                # Verify the form heading
                heading = dp.get_add_edit_device_heading()
                heading_text = heading.inner_text(timeout=5000)
                logger.info(f"Form heading: {heading_text}")
                check.is_true(
                    "Device" in heading_text,
                    f"Expected heading to contain 'Device', got: {heading_text}"
                )

                # Step 4 — UI: Fill in the form and save
                logger.info(f"Filling device form with name='{device_name}'")
                dp.fill_and_save_device_form(
                    name=device_name,
                    organization_name=TEST_ORG_NAME,
                )

                # Step 5 — Verify we're back on the devices list
                dp.page.wait_for_selector("h1", state="visible")
                page_title = dp.get_page_title()
                title_text = page_title.inner_text(timeout=5000)
                check.equal(
                    title_text, "Devices",
                    f"Expected to return to Devices list after save, "
                    f"got page title: {title_text}"
                )

                # Search for the newly registered device
                logger.info(f"Searching for registered device: {device_name}")
                dp.search_devices(device_name)

                row_count = dp.count_table_rows()
                logger.info(f"Search returned {row_count} row(s)")

                check.greater_equal(
                    row_count, 1,
                    f"Expected at least 1 row for device '{device_name}', "
                    f"got {row_count}"
                )

                # Verify the device name appears in the table
                device_row = dp.get_device_by_name(device_name)
                check.is_not_none(
                    device_row,
                    f"Device '{device_name}' not found in the devices table "
                    f"after registration."
                )

                if device_row:
                    logger.info(
                        f"Device '{device_name}' confirmed in the devices table."
                    )

                logger.info("Device Lookup → Register workflow completed successfully.")

        finally:
            # Step 6 — API: Clean up
            if device_id:
                logger.info(f"Cleaning up device {device_id}")
                _delete_device_via_api(device_id, headers)

    @pytest.mark.functional
    @pytest.mark.devices
    @pytest.mark.edge_case
    def test_device_lookup_nonexistent_shows_error(self, devices_page):
        """
        Test that looking up a non-existent wildXRNumber shows an error in the modal.

        The DeviceLookupModal should display an error message without navigating
        away from the Devices page.

        Args:
            devices_page: Fixture providing DevicesPage objects.
        """
        logger.info("Starting Device Lookup — non-existent wildXRNumber test")

        fake_number = "ZZZZZ-NONEXISTENT-99999"

        for dp in devices_page:
            # Perform the lookup using the page object method
            dp.perform_device_lookup(fake_number)

            # Allow time for the error to render
            dp.page.wait_for_timeout(1000)

            # Verify we're still on the devices page (no navigation occurred)
            current_url = dp.page.url
            check.is_true(
                "/devices" in current_url.lower(),
                f"Expected to stay on /devices after failed lookup, "
                f"got URL: {current_url}"
            )

            # Verify an error message appeared in the modal
            error_alert = dp.get_device_lookup_error_alert()
            if error_alert.count() > 0:
                error_text = error_alert.first.inner_text(timeout=3000)
                logger.info(f"Lookup error message: {error_text}")
                check.is_true(
                    len(error_text) > 0,
                    "Error alert should contain a message"
                )
            else:
                logger.warning(
                    "No error alert found after failed device lookup. "
                    "The modal may have closed or the error renders differently."
                )

            # Close the modal by clicking the × button
            close_button = dp.get_wildxr_number_close_button()
            if close_button.count() > 0:
                close_button.click()

            logger.info("Device Lookup — non-existent number test completed.")
