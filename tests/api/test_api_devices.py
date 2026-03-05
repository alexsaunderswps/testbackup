# test_api_devices.py
# Tests for the /api/Device endpoints.
#
# IMPORTANT API QUIRKS FOR THIS RESOURCE:
#
# 1. Device creation follows a TWO-STEP WORKFLOW:
#      Step 1: POST /api/Device/InitializeNew — creates a bare device record with a
#              system-generated deviceId (UUID) and wildXRNumber (Proquint-encoded
#              sequential ID). Returns the full DeviceDto in the response body.
#              The device has NO name, org, or installation at this point.
#      Step 2: POST /api/Device/Update — "registers" the device by assigning it a
#              name, organizationId, and optionally an installationId. This is how
#              devices are registered in the UI via the "Device Lookup" button.
#    There is also PUT /api/Device/Create which does a low-level insert (used by
#    these tests for edge cases), but the production workflow is InitializeNew → Update.
#
# 2. GET /api/Device returns a plain JSON array, NOT a ResponseDto wrapper.
#    Same quirk as /api/Organization and /api/Installations.
#    GET /api/Device/search DOES use ResponseDto with correct pagination math.
#
# 3. GET /api/Device/device-lookup?wildXRNumber= finds devices that have NO
#    OrganizationId (i.e., unregistered/initialized-only devices). Once a device
#    is registered (has an org), it no longer appears in device-lookup results.
#
# 4. The search endpoint enforces org-based access control:
#    - System admins see all devices that have an OrganizationId
#    - Org admins see only devices belonging to their org(s)
#    - Devices with no OrganizationId are excluded from search results entirely
#
# 5. Details endpoint (GET /Device/{id}/details) returns 404 (not 400) for not-found.
#    Update endpoint (POST /Device/Update) also returns 404 for not-found.
#    This differs from other controllers that return 400 for not-found.
#
# 6. Update is a PARTIAL field-level update (not a full replace like Installations).
#    It sets: Name, WildXRNumber, InstallationId, OrganizationId.
#    Omitting a field in the update payload sets it to null/default.
#
# 7. DeviceDto has a RowVersion field (byte[]) for optimistic concurrency.
#    This is not currently enforced by the Update action (no concurrency check
#    in the controller code), but the field exists in the DTO and model.
#
# 8. DELETE /api/Device/delete?id= enforces org-based access: system admins can
#    delete any device; org admins can only delete devices in their org.
#    Not-found returns 400 ("not found") — same as other delete endpoints.
#
# API DESIGN GAPS (documented, not tested — see CLAUDE.md):
#
# - InitializeNew has no rate limiting or access control beyond [Authorize].
#   Any authenticated user can generate unlimited device records.
# - PUT /api/Device/Create has no field validation — accepts empty payloads.
# - Update does not check RowVersion for concurrency conflicts.

import os
import uuid
import pytest
import requests
from .api_base import APIBase
from utilities.utils import logger


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

# Default QA test organization — matches conftest.py and CI workflow env var.
TEST_ORG_ID = os.environ.get(
    "TEST_ORGANIZATION_ID",
    "4ffbb8fe-d8b4-49d9-982d-5617856c9cce"
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _make_autotest_device_name() -> str:
    """
    Generate a unique AUTOTEST device name.

    Format: AUTOTEST_DEV_{8 hex chars}
    Example: AUTOTEST_DEV_3a7f9c12   (20 chars)

    The AUTOTEST_ prefix ensures the session-level conftest cleanup will
    catch any orphaned records this test suite leaves behind.

    Returns:
        str: A unique device name prefixed with AUTOTEST_DEV_.
    """
    short_id = uuid.uuid4().hex[:8]
    return f"AUTOTEST_DEV_{short_id}"


# ---------------------------------------------------------------------------
# Class 1: Read-only GET tests — safe to run at any time, create no data
# ---------------------------------------------------------------------------

class TestAPIDevicesGet:
    """
    Read-only tests for the Device GET endpoints.

    Covers:
        - GET /Device?pageNumber=&pageSize=  (list, plain array)
        - GET /Device/search?name=&pageNumber=&pageSize=  (search, ResponseDto)
        - GET /Device/{id}/details  (single record by GUID)

    No data is created or modified by any test in this class.
    """

    def setup_method(self):
        """Initialize APIBase for each test method."""
        self.api = APIBase()

    def _get_first_device_id(self) -> str | None:
        """
        Fetch the first device from the search endpoint and return its id.

        Uses the search endpoint (not the plain list) because search enforces
        org-based access and only returns devices with an OrganizationId — these
        are "registered" devices that will also work with the details endpoint.

        Returns:
            str: The deviceId of the first record, or None if no devices found.
        """
        response = self.api.get(
            "/Device/search",
            params={"pageNumber": 1, "pageSize": 1}
        )

        if response.status_code != 200:
            logger.error(
                f"Could not fetch device search to discover an ID. "
                f"Status: {response.status_code}"
            )
            return None

        try:
            data = response.json()
            results = data.get("results", [])
            if len(results) == 0:
                logger.warning("Device search returned no results — no ID available.")
                return None
            device_id = results[0].get("deviceId")
            logger.debug(f"Discovered device ID for detail tests: {device_id}")
            return str(device_id)
        except (requests.exceptions.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing device search response: {e}")
            return None

    # -------------------------------------------------------------------------
    # GET /Device — basic list (plain array, no ResponseDto wrapper)
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.devices
    def test_get_list_returns_200(self):
        """
        GET /Device returns HTTP 200 with a valid JSON response body.

        Baseline connectivity check for the device list endpoint.
        """
        response = self.api.get("/Device", params={"pageNumber": 1, "pageSize": 10})

        assert response.status_code == 200, (
            f"Expected 200 from GET /Device, got {response.status_code}"
        )

        data = response.json()
        assert data is not None, "Response body should not be null"

        logger.info("GET /Device returned 200 with a valid JSON body.")

    @pytest.mark.api
    @pytest.mark.devices
    def test_get_list_returns_array(self):
        """
        GET /Device response body is a plain JSON array.

        Like /api/Organization and /api/Installations, the Device list endpoint
        does NOT use a ResponseDto wrapper — it returns a raw array. The search
        endpoint (/Device/search) does use ResponseDto.
        """
        response = self.api.get("/Device", params={"pageNumber": 1, "pageSize": 10})

        assert response.status_code == 200, (
            f"Expected 200 from GET /Device, got {response.status_code}"
        )

        data = response.json()

        assert isinstance(data, list), (
            f"Expected GET /Device to return a JSON array (no ResponseDto wrapper). "
            f"Got {type(data).__name__}."
        )

        logger.info(
            f"GET /Device returned a plain array with {len(data)} item(s). "
            f"No ResponseDto wrapper confirmed."
        )

    @pytest.mark.api
    @pytest.mark.devices
    def test_get_list_items_have_required_fields(self):
        """
        Each device in the GET /Device list has the expected DeviceDto fields.

        Fields checked (camelCase — ASP.NET Core serializes PascalCase C# DTO
        properties to camelCase automatically):
            - deviceId       — primary key (GUID)
            - wildXRNumber   — Proquint-encoded device identifier
        """
        response = self.api.get("/Device", params={"pageNumber": 1, "pageSize": 10})

        assert response.status_code == 200, (
            f"Expected 200 from GET /Device, got {response.status_code}"
        )

        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            pytest.skip("Device list is empty — cannot verify item fields.")

        required_fields = ["deviceId", "wildXRNumber"]
        first_item = data[0]

        missing = [f for f in required_fields if f not in first_item]

        assert not missing, (
            f"First device in GET /Device is missing fields: {missing}. "
            f"Actual keys: {list(first_item.keys())}. "
            f"Remember: C# PascalCase DTO properties serialize to camelCase JSON keys."
        )

        logger.info(
            f"GET /Device first item field check passed. "
            f"Keys present: {list(first_item.keys())}"
        )

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.pagination
    def test_get_list_page_size_param_limits_results(self):
        """
        GET /Device with pageSize=1 returns exactly 1 item.

        Verifies that the pageSize query parameter is respected by the endpoint.
        """
        response = self.api.get("/Device", params={"pageNumber": 1, "pageSize": 1})

        assert response.status_code == 200, (
            f"Expected 200 from GET /Device?pageSize=1, got {response.status_code}"
        )

        data = response.json()

        assert isinstance(data, list), (
            f"Expected a list, got {type(data).__name__}"
        )

        assert len(data) <= 1, (
            f"Expected at most 1 result with pageSize=1, got {len(data)}"
        )

        logger.info(
            f"GET /Device?pageSize=1 returned {len(data)} item(s) — pageSize respected."
        )

    # -------------------------------------------------------------------------
    # GET /Device/search — search with ResponseDto wrapper
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.search
    def test_get_search_returns_200_with_pagination_envelope(self):
        """
        GET /Device/search returns 200 with a ResponseDto pagination envelope.

        Unlike the basic list endpoint, the search endpoint wraps results in
        ResponseDto (page, pageCount, pageSize, totalCount, results).
        """
        response = self.api.get(
            "/Device/search",
            params={"pageNumber": 1, "pageSize": 10}
        )

        assert response.status_code == 200, (
            f"Expected 200 from GET /Device/search, got {response.status_code}"
        )

        data = response.json()

        assert isinstance(data, dict), (
            f"Expected GET /Device/search to return a JSON object (ResponseDto). "
            f"Got {type(data).__name__}."
        )

        logger.info("GET /Device/search returned 200 with a JSON object body.")

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.search
    @pytest.mark.pagination
    def test_get_search_pagination_fields_present(self):
        """
        GET /Device/search response contains all required ResponseDto fields.

        Verifies the pagination envelope shape: page, pageCount, pageSize,
        totalCount, and results (as a list).
        """
        response = self.api.get(
            "/Device/search",
            params={"pageNumber": 1, "pageSize": 10}
        )

        assert response.status_code == 200, (
            f"Expected 200 from GET /Device/search, got {response.status_code}"
        )

        data = response.json()

        required_fields = ["page", "pageSize", "pageCount", "totalCount", "results"]
        missing = [f for f in required_fields if f not in data]

        assert not missing, (
            f"GET /Device/search is missing required pagination fields: {missing}. "
            f"Actual keys: {list(data.keys())}"
        )

        assert isinstance(data["results"], list), (
            f"Expected 'results' to be a list, got {type(data['results']).__name__}"
        )

        logger.info(
            f"GET /Device/search pagination envelope verified: "
            f"page={data['page']}, pageSize={data['pageSize']}, "
            f"pageCount={data['pageCount']}, totalCount={data['totalCount']}, "
            f"results count={len(data['results'])}"
        )

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.search
    def test_get_search_name_filter_returns_results(self):
        """
        GET /Device/search with a broad name filter returns at least one result.

        Uses name="a" to maximize the chance of matching existing devices.
        Search only returns devices with an OrganizationId (registered devices).
        """
        response = self.api.get(
            "/Device/search",
            params={"name": "a", "pageNumber": 1, "pageSize": 25}
        )

        assert response.status_code == 200, (
            f"Expected 200 from GET /Device/search?name=a, "
            f"got {response.status_code}"
        )

        data = response.json()
        results = data.get("results", [])

        assert len(results) >= 1, (
            f"Expected at least 1 result for name='a' but got {len(results)}. "
            f"QA environment may have no registered devices with 'a' in the name."
        )

        for device in results:
            name = device.get("name", "")
            assert "a" in name.lower(), (
                f"Search result '{name}' does not contain the search term 'a'. "
                f"The name filter may be returning unfiltered results."
            )

        logger.info(
            f"GET /Device/search?name=a returned {len(results)} result(s); "
            f"all contain 'a' in name."
        )

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.search
    def test_get_search_no_match_returns_empty_list(self):
        """
        GET /Device/search with a non-matching name returns 200 with an
        empty results list — not a 404.
        """
        no_match_name = "ZZZZZ_WILDXR_TEST_NO_MATCH_ZZZZZ"

        response = self.api.get(
            "/Device/search",
            params={"name": no_match_name, "pageNumber": 1, "pageSize": 10}
        )

        assert response.status_code == 200, (
            f"Expected 200 (not 404) for a no-match search on "
            f"GET /Device/search. Got {response.status_code}."
        )

        data = response.json()
        results = data.get("results", [])

        assert isinstance(results, list), (
            f"Expected 'results' to be a list, got {type(results).__name__}"
        )

        assert len(results) == 0, (
            f"Expected 0 results for no-match name='{no_match_name}', "
            f"got {len(results)}"
        )

        logger.info(
            f"GET /Device/search with no-match name correctly returned "
            f"200 with an empty results list."
        )

    # -------------------------------------------------------------------------
    # GET /Device/{id}/details — single record by GUID
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.devices
    def test_get_detail_returns_200_for_valid_id(self):
        """
        GET /Device/{id}/details returns 200 for a valid, pre-existing device ID.

        The device ID is discovered dynamically from the search endpoint.
        """
        device_id = self._get_first_device_id()

        if device_id is None:
            pytest.skip(
                "No registered devices exist in QA — "
                "cannot test GET /Device/{id}/details."
            )

        response = self.api.get(f"/Device/{device_id}/details")

        assert response.status_code == 200, (
            f"Expected 200 from GET /Device/{device_id}/details, "
            f"got {response.status_code}"
        )

        data = response.json()

        assert isinstance(data, dict), (
            f"Expected response body to be a JSON object, got {type(data).__name__}"
        )

        logger.info(
            f"GET /Device/{device_id}/details returned 200 with a valid JSON body."
        )

    @pytest.mark.api
    @pytest.mark.devices
    def test_get_detail_has_required_fields(self):
        """
        GET /Device/{id}/details response contains the expected DeviceDto fields.

        Fields verified (camelCase):
            - deviceId         — primary key (GUID)
            - wildXRNumber     — Proquint device identifier
            - name             — display name (may be null for unregistered devices)
            - organizationId   — owning org (null for unregistered devices)
        """
        device_id = self._get_first_device_id()

        if device_id is None:
            pytest.skip(
                "No registered devices exist in QA — "
                "cannot test GET /Device/{id}/details."
            )

        response = self.api.get(f"/Device/{device_id}/details")

        assert response.status_code == 200, (
            f"Expected 200 from GET /Device/{device_id}/details, "
            f"got {response.status_code}"
        )

        data = response.json()

        required_fields = ["deviceId", "wildXRNumber"]
        missing = [f for f in required_fields if f not in data]

        assert not missing, (
            f"GET /Device/{device_id}/details response is missing fields: {missing}. "
            f"Actual keys returned: {list(data.keys())}."
        )

        logger.info(
            f"GET /Device/{device_id}/details required field check passed. "
            f"All fields present: {list(data.keys())}"
        )

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.edge_case
    def test_get_detail_returns_404_for_nonexistent_id(self):
        """
        GET /Device/{id}/details returns 404 for a nonexistent (but valid) GUID.

        Note: Unlike most controllers in this API that return 400 for not-found,
        the Device details endpoint returns 404 Not Found. This is because the
        controller checks for null after the query and returns NotFound().
        """
        fake_id = str(uuid.uuid4())

        response = self.api.get(f"/Device/{fake_id}/details")

        assert response.status_code == 404, (
            f"Expected 404 from GET /Device/{fake_id}/details "
            f"(nonexistent ID). Got {response.status_code}. "
            f"The Device details endpoint uses 404 (not 400) for not-found."
        )

        logger.info(
            f"GET /Device/{fake_id}/details correctly returned 404 "
            f"for a nonexistent device ID."
        )


# ---------------------------------------------------------------------------
# Class 2: Device Lookup tests
# ---------------------------------------------------------------------------

class TestAPIDeviceLookup:
    """
    Tests for the GET /Device/device-lookup endpoint.

    Device lookup finds unregistered devices by their wildXRNumber. A device is
    "unregistered" if it has no OrganizationId — i.e., it was initialized via
    InitializeNew but not yet assigned to an org via Update.

    These tests create a device via InitializeNew and clean up via Delete.
    """

    def setup_method(self):
        """Initialize APIBase and tracking list for cleanup."""
        self.api = APIBase()
        self._created_ids = []

    def teardown_method(self):
        """Delete all devices created during this test."""
        for device_id in self._created_ids:
            try:
                self.api.delete("/Device/delete", params={"id": device_id})
                logger.debug(f"Teardown: deleted device {device_id}")
            except Exception as e:
                logger.warning(f"Teardown: failed to delete device {device_id}: {e}")
        self._created_ids.clear()

    @pytest.mark.api
    @pytest.mark.devices
    def test_device_lookup_finds_unregistered_device(self):
        """
        GET /Device/device-lookup returns the initialized device by wildXRNumber.

        Workflow:
        1. POST /Device/InitializeNew to create a bare device
        2. GET /Device/device-lookup?wildXRNumber= to find it
        3. Verify the returned device matches the initialized one
        """
        # Step 1: Initialize a new device
        init_response = self.api.post("/Device/InitializeNew")

        assert init_response.status_code == 200, (
            f"Expected 200 from POST /Device/InitializeNew, "
            f"got {init_response.status_code}. Response: {init_response.text}"
        )

        device_data = init_response.json()
        device_id = device_data.get("deviceId")
        wildxr_number = device_data.get("wildXRNumber")
        self._created_ids.append(str(device_id))

        assert device_id is not None, "InitializeNew response missing deviceId"
        assert wildxr_number is not None, "InitializeNew response missing wildXRNumber"

        logger.info(
            f"Initialized new device: deviceId={device_id}, "
            f"wildXRNumber={wildxr_number}"
        )

        # Step 2: Look up the device by wildXRNumber
        lookup_response = self.api.get(
            "/Device/device-lookup",
            params={"wildXRNumber": wildxr_number}
        )

        assert lookup_response.status_code == 200, (
            f"Expected 200 from device-lookup with wildXRNumber={wildxr_number}, "
            f"got {lookup_response.status_code}"
        )

        lookup_data = lookup_response.json()

        assert str(lookup_data.get("deviceId")) == str(device_id), (
            f"Lookup returned deviceId={lookup_data.get('deviceId')}, "
            f"expected {device_id}"
        )

        assert lookup_data.get("wildXRNumber") == wildxr_number, (
            f"Lookup returned wildXRNumber={lookup_data.get('wildXRNumber')}, "
            f"expected {wildxr_number}"
        )

        logger.info(
            f"Device lookup correctly found unregistered device by "
            f"wildXRNumber={wildxr_number}."
        )

    @pytest.mark.api
    @pytest.mark.devices
    def test_device_lookup_returns_404_for_nonexistent_number(self):
        """
        GET /Device/device-lookup with a non-matching wildXRNumber returns 404.
        """
        response = self.api.get(
            "/Device/device-lookup",
            params={"wildXRNumber": "ZZZZZ-NONEXISTENT"}
        )

        assert response.status_code == 404, (
            f"Expected 404 for device-lookup with non-matching wildXRNumber, "
            f"got {response.status_code}"
        )

        logger.info("Device lookup correctly returned 404 for non-matching wildXRNumber.")

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.edge_case
    def test_device_lookup_returns_400_for_missing_param(self):
        """
        GET /Device/device-lookup with no wildXRNumber parameter returns 400.

        The controller explicitly checks for null/empty wildXRNumber and returns
        BadRequest("WildXRNumber is required.").
        """
        response = self.api.get("/Device/device-lookup")

        assert response.status_code == 400, (
            f"Expected 400 for device-lookup with no wildXRNumber param, "
            f"got {response.status_code}"
        )

        logger.info("Device lookup correctly returned 400 for missing wildXRNumber.")


# ---------------------------------------------------------------------------
# Class 3: CRUD tests — InitializeNew → Update → Delete workflow
# ---------------------------------------------------------------------------

class TestAPIDevicesCRUD:
    """
    CRUD tests for the Device write endpoints.

    Follows the production two-step workflow:
    1. POST /Device/InitializeNew — creates a bare device (deviceId + wildXRNumber)
    2. POST /Device/Update — "registers" the device (assigns name, org, installation)

    Each test that creates a device tracks its ID in _created_ids.
    teardown_method deletes all tracked devices after each test.

    Covers:
        - POST /Device/InitializeNew  (step 1: generate device)
        - POST /Device/Update  (step 2: register/edit device)
        - DELETE /Device/delete?id=  (cleanup)
    """

    def setup_method(self):
        """Initialize APIBase and the created-device tracking list."""
        self.api = APIBase()
        self._created_ids = []

    def teardown_method(self):
        """Delete all AUTOTEST devices created during this test."""
        for device_id in self._created_ids:
            try:
                self.api.delete("/Device/delete", params={"id": device_id})
                logger.debug(f"Teardown: deleted device {device_id}")
            except Exception as e:
                logger.warning(f"Teardown: failed to delete device {device_id}: {e}")
        self._created_ids.clear()

    def _initialize_device(self) -> dict | None:
        """
        Initialize a new device via POST /Device/InitializeNew.

        Returns:
            dict: The DeviceDto from the response (deviceId, wildXRNumber), or
                  None if the request failed. The device is tracked for cleanup.
        """
        response = self.api.post("/Device/InitializeNew")

        if response.status_code != 200:
            logger.error(
                f"POST /Device/InitializeNew failed with {response.status_code}. "
                f"Response: {response.text}"
            )
            return None

        device_data = response.json()
        device_id = str(device_data.get("deviceId"))
        self._created_ids.append(device_id)
        logger.debug(
            f"Initialized device: deviceId={device_id}, "
            f"wildXRNumber={device_data.get('wildXRNumber')}"
        )
        return device_data

    def _register_device(self, device_data: dict, name: str) -> requests.Response:
        """
        Register (update) an initialized device with a name and organization.

        This is step 2 of the device creation workflow — the equivalent of
        looking up a device by wildXRNumber in the UI and filling in the edit form.

        Args:
            device_data: The DeviceDto returned from InitializeNew.
            name:        The device name to assign. Use AUTOTEST_ prefix.

        Returns:
            requests.Response: The raw response from POST /Device/Update.
        """
        payload = {
            "deviceId": str(device_data["deviceId"]),
            "name": name,
            "wildXRNumber": device_data["wildXRNumber"],
            "organizationId": TEST_ORG_ID,
        }

        return self.api.post("/Device/Update", body=payload)

    # -------------------------------------------------------------------------
    # InitializeNew
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.devices
    def test_initialize_new_returns_200_with_device_data(self):
        """
        POST /Device/InitializeNew returns 200 with a DeviceDto containing
        a deviceId and wildXRNumber.

        This is step 1 of the device creation workflow. The response body
        contains the auto-generated device record.
        """
        response = self.api.post("/Device/InitializeNew")

        assert response.status_code == 200, (
            f"Expected 200 from POST /Device/InitializeNew, "
            f"got {response.status_code}. Response: {response.text}"
        )

        data = response.json()
        device_id = data.get("deviceId")
        wildxr_number = data.get("wildXRNumber")
        self._created_ids.append(str(device_id))

        assert device_id is not None, (
            "InitializeNew response missing 'deviceId'. "
            f"Actual keys: {list(data.keys())}"
        )

        assert wildxr_number is not None, (
            "InitializeNew response missing 'wildXRNumber'. "
            f"Actual keys: {list(data.keys())}"
        )

        # deviceId should be a valid GUID (not all zeros)
        assert str(device_id) != "00000000-0000-0000-0000-000000000000", (
            "InitializeNew returned an all-zero deviceId — EF Core may not be "
            "generating the GUID correctly."
        )

        logger.info(
            f"POST /Device/InitializeNew returned 200 with "
            f"deviceId={device_id}, wildXRNumber={wildxr_number}"
        )

    @pytest.mark.api
    @pytest.mark.devices
    def test_initialized_device_has_no_org_or_name(self):
        """
        A freshly initialized device has no name and no organizationId.

        After InitializeNew, the device exists in the DB with only deviceId and
        wildXRNumber populated. Name and organizationId are null until the device
        is registered via Update.
        """
        device_data = self._initialize_device()

        assert device_data is not None, "Failed to initialize device"

        # Verify unregistered state
        assert device_data.get("name") is None or device_data.get("name") == "", (
            f"Expected name to be null/empty for uninitialized device, "
            f"got '{device_data.get('name')}'"
        )

        assert device_data.get("organizationId") is None or device_data.get("organizationId") == "", (
            f"Expected organizationId to be null/empty for uninitialized device, "
            f"got '{device_data.get('organizationId')}'"
        )

        logger.info(
            "Initialized device confirmed: no name or organizationId assigned."
        )

    # -------------------------------------------------------------------------
    # Register (Update) — step 2 of device workflow
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.devices
    def test_register_device_returns_200(self):
        """
        POST /Device/Update with a valid payload returns 200.

        This is step 2 of the two-step workflow: assign a name and org to a
        freshly initialized device.
        """
        device_data = self._initialize_device()
        assert device_data is not None, "Failed to initialize device"

        name = _make_autotest_device_name()
        response = self._register_device(device_data, name)

        assert response.status_code == 200, (
            f"Expected 200 from POST /Device/Update (register), "
            f"got {response.status_code}. Response: {response.text}"
        )

        logger.info(
            f"POST /Device/Update returned 200 — device registered as '{name}'."
        )

    @pytest.mark.api
    @pytest.mark.devices
    def test_registered_device_appears_in_search(self):
        """
        After registering a device, it appears in search results by name.

        The search endpoint only returns devices with an OrganizationId, so a
        freshly initialized (unregistered) device would not appear. After
        registration via Update, it should be searchable.
        """
        device_data = self._initialize_device()
        assert device_data is not None, "Failed to initialize device"

        name = _make_autotest_device_name()
        reg_response = self._register_device(device_data, name)
        assert reg_response.status_code == 200, (
            f"Registration failed: {reg_response.status_code}"
        )

        # Search for the registered device by name
        search_response = self.api.get(
            "/Device/search",
            params={"name": name, "pageNumber": 1, "pageSize": 10}
        )

        assert search_response.status_code == 200, (
            f"Expected 200 from search, got {search_response.status_code}"
        )

        data = search_response.json()
        results = data.get("results", [])

        assert len(results) >= 1, (
            f"Expected registered device '{name}' to appear in search results, "
            f"but got {len(results)} results."
        )

        found_ids = [str(r.get("deviceId")) for r in results]
        device_id = str(device_data["deviceId"])

        assert device_id in found_ids, (
            f"Registered device {device_id} not found in search results for "
            f"name='{name}'. Found IDs: {found_ids}"
        )

        logger.info(
            f"Registered device '{name}' ({device_id}) confirmed in search results."
        )

    @pytest.mark.api
    @pytest.mark.devices
    def test_registered_device_detail_matches_payload(self):
        """
        After registering a device, its details reflect the update payload.

        Verifies the full round-trip: InitializeNew → Update → Details.
        """
        device_data = self._initialize_device()
        assert device_data is not None, "Failed to initialize device"

        name = _make_autotest_device_name()
        device_id = str(device_data["deviceId"])
        wildxr_number = device_data["wildXRNumber"]

        reg_response = self._register_device(device_data, name)
        assert reg_response.status_code == 200, (
            f"Registration failed: {reg_response.status_code}"
        )

        # Fetch details
        detail_response = self.api.get(f"/Device/{device_id}/details")

        assert detail_response.status_code == 200, (
            f"Expected 200 from GET /Device/{device_id}/details, "
            f"got {detail_response.status_code}"
        )

        detail = detail_response.json()

        assert detail.get("name") == name, (
            f"Expected name='{name}', got '{detail.get('name')}'"
        )

        assert detail.get("wildXRNumber") == wildxr_number, (
            f"Expected wildXRNumber='{wildxr_number}', "
            f"got '{detail.get('wildXRNumber')}'"
        )

        assert detail.get("organizationId") == TEST_ORG_ID, (
            f"Expected organizationId='{TEST_ORG_ID}', "
            f"got '{detail.get('organizationId')}'"
        )

        logger.info(
            f"Device details match registration payload: "
            f"name='{name}', wildXRNumber='{wildxr_number}', "
            f"organizationId='{TEST_ORG_ID}'."
        )

    # -------------------------------------------------------------------------
    # Update — modify an existing registered device
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.devices
    def test_update_device_name_returns_200(self):
        """
        POST /Device/Update to change the name of a registered device returns 200.

        Verifies the name change persists by fetching details afterward.
        """
        # Initialize and register
        device_data = self._initialize_device()
        assert device_data is not None, "Failed to initialize device"

        original_name = _make_autotest_device_name()
        reg_response = self._register_device(device_data, original_name)
        assert reg_response.status_code == 200, "Registration failed"

        # Update the name
        updated_name = _make_autotest_device_name()
        device_id = str(device_data["deviceId"])

        update_payload = {
            "deviceId": device_id,
            "name": updated_name,
            "wildXRNumber": device_data["wildXRNumber"],
            "organizationId": TEST_ORG_ID,
        }

        update_response = self.api.post("/Device/Update", body=update_payload)

        assert update_response.status_code == 200, (
            f"Expected 200 from POST /Device/Update (name change), "
            f"got {update_response.status_code}. Response: {update_response.text}"
        )

        # Verify the name change persisted
        detail_response = self.api.get(f"/Device/{device_id}/details")
        assert detail_response.status_code == 200, "Failed to fetch details after update"

        detail = detail_response.json()

        assert detail.get("name") == updated_name, (
            f"Expected updated name='{updated_name}', got '{detail.get('name')}'"
        )

        logger.info(
            f"Device name successfully updated from '{original_name}' to "
            f"'{updated_name}'."
        )

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.edge_case
    def test_update_device_missing_id_returns_400(self):
        """
        POST /Device/Update with an empty/zero deviceId returns 400.

        The controller explicitly checks for Guid.Empty and returns
        BadRequest("Id is required").
        """
        payload = {
            "deviceId": "00000000-0000-0000-0000-000000000000",
            "name": "AUTOTEST_should_fail",
            "organizationId": TEST_ORG_ID,
        }

        response = self.api.post("/Device/Update", body=payload)

        assert response.status_code == 400, (
            f"Expected 400 from POST /Device/Update with empty deviceId, "
            f"got {response.status_code}"
        )

        logger.info(
            "POST /Device/Update correctly returned 400 for missing deviceId."
        )

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.edge_case
    def test_update_nonexistent_device_returns_404(self):
        """
        POST /Device/Update with a nonexistent deviceId returns 404.

        Unlike most controllers that return 400 for not-found, the Device
        Update action returns NotFound("Device not found.").
        """
        fake_id = str(uuid.uuid4())

        payload = {
            "deviceId": fake_id,
            "name": "AUTOTEST_should_not_exist",
            "organizationId": TEST_ORG_ID,
        }

        response = self.api.post("/Device/Update", body=payload)

        assert response.status_code == 404, (
            f"Expected 404 from POST /Device/Update with nonexistent deviceId, "
            f"got {response.status_code}. "
            f"Device Update uses 404 (not 400) for not-found."
        )

        logger.info(
            "POST /Device/Update correctly returned 404 for nonexistent deviceId."
        )

    # -------------------------------------------------------------------------
    # Delete
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.devices
    def test_delete_device_returns_200(self):
        """
        DELETE /Device/delete?id= returns 200 for an existing device.

        Creates a device via InitializeNew, then deletes it. The device is
        removed from _created_ids since the test itself handles deletion.
        """
        device_data = self._initialize_device()
        assert device_data is not None, "Failed to initialize device"

        device_id = str(device_data["deviceId"])

        response = self.api.delete("/Device/delete", params={"id": device_id})

        assert response.status_code == 200, (
            f"Expected 200 from DELETE /Device/delete?id={device_id}, "
            f"got {response.status_code}. Response: {response.text}"
        )

        # Remove from tracking since we just deleted it
        self._created_ids.remove(device_id)

        logger.info(f"DELETE /Device/delete returned 200 for device {device_id}.")

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.edge_case
    def test_delete_nonexistent_device_returns_400(self):
        """
        DELETE /Device/delete?id= with a nonexistent GUID returns 400.

        The controller checks for null after the query and returns
        BadRequest("not found").
        """
        fake_id = str(uuid.uuid4())

        response = self.api.delete("/Device/delete", params={"id": fake_id})

        assert response.status_code == 400, (
            f"Expected 400 from DELETE /Device/delete with nonexistent ID, "
            f"got {response.status_code}"
        )

        logger.info(
            "DELETE /Device/delete correctly returned 400 for nonexistent device."
        )

    # -------------------------------------------------------------------------
    # Lookup no longer finds registered device
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.devices
    def test_registered_device_not_in_lookup(self):
        """
        After registering a device (assigning OrganizationId), it no longer
        appears in device-lookup results.

        Device lookup only finds devices with no OrganizationId. Once a device
        is registered via Update, it should return 404 for its wildXRNumber.
        """
        device_data = self._initialize_device()
        assert device_data is not None, "Failed to initialize device"

        wildxr_number = device_data["wildXRNumber"]

        # Confirm it's findable before registration
        pre_lookup = self.api.get(
            "/Device/device-lookup",
            params={"wildXRNumber": wildxr_number}
        )
        assert pre_lookup.status_code == 200, (
            f"Expected initialized device to be findable via lookup, "
            f"got {pre_lookup.status_code}"
        )

        # Register the device (assigns OrganizationId)
        name = _make_autotest_device_name()
        reg_response = self._register_device(device_data, name)
        assert reg_response.status_code == 200, "Registration failed"

        # Now lookup should return 404
        post_lookup = self.api.get(
            "/Device/device-lookup",
            params={"wildXRNumber": wildxr_number}
        )

        assert post_lookup.status_code == 404, (
            f"Expected 404 from device-lookup after registration "
            f"(device now has OrganizationId), got {post_lookup.status_code}. "
            f"Lookup should only find unregistered devices."
        )

        logger.info(
            f"Registered device (wildXRNumber={wildxr_number}) correctly "
            f"no longer appears in device-lookup results."
        )


# ---------------------------------------------------------------------------
# Class 4: GetAssociatedInstallation tests
# ---------------------------------------------------------------------------

class TestAPIDeviceAssociatedInstallation:
    """
    Tests for the GET /Device/GetAssociatedInstallation endpoint.

    This endpoint takes a wildXRNumber and returns the installation associated
    with the device (if any). It requires the device to have an installationId.
    """

    def setup_method(self):
        """Initialize APIBase."""
        self.api = APIBase()

    @pytest.mark.api
    @pytest.mark.devices
    @pytest.mark.installations
    def test_get_associated_installation_for_device_without_installation(self):
        """
        GET /Device/GetAssociatedInstallation returns 400 when the device has
        no associated installation.

        The controller checks for null installationId and returns
        BadRequest("Device has no assosciated installation") — note the typo
        in the controller response.
        """
        # Find a device in the search results to get its wildXRNumber
        search_response = self.api.get(
            "/Device/search",
            params={"pageNumber": 1, "pageSize": 10}
        )

        if search_response.status_code != 200:
            pytest.skip("Could not fetch devices for associated installation test.")

        data = search_response.json()
        results = data.get("results", [])

        # Look for a device with no installationId
        device_without_install = None
        for device in results:
            if not device.get("installationId"):
                device_without_install = device
                break

        if device_without_install is None:
            pytest.skip(
                "No device without installationId found in search results — "
                "cannot test the no-installation case."
            )

        wildxr_number = device_without_install.get("wildXRNumber")

        response = self.api.get(
            "/Device/GetAssociatedInstallation",
            params={"WildXRNumber": wildxr_number}
        )

        assert response.status_code == 400, (
            f"Expected 400 for device with no installation, "
            f"got {response.status_code}"
        )

        logger.info(
            f"GetAssociatedInstallation correctly returned 400 for device "
            f"without installation (wildXRNumber={wildxr_number})."
        )
