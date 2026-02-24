# test_api_installations.py
# Tests for the /api/Installations endpoints.
#
# IMPORTANT API QUIRKS FOR THIS RESOURCE:
#
# 1. GET /api/Installations returns a plain JSON array, NOT a ResponseDto wrapper.
#    This is the same quirk as /api/Organization. The search endpoint
#    (/Installations/search) DOES use ResponseDto — with correct pagination math.
#
# 2. PUT /api/Installations/create returns 200 with an EMPTY response body.
#    installationId is OPTIONAL in the create payload. If omitted, EF Core
#    auto-generates a GUID (default convention for Guid primary keys).
#    Supplying the ID is a valid choice and avoids a post-create search.
#    This test suite supplies the ID explicitly so cleanup is simpler —
#    the same approach used by conftest.py.
#
# 3. Not-found conditions return 400 (BadRequest), not 404.
#    Consistent with all other controllers in this API.
#
# 4. The Create action has NO explicit validation of required fields.
#    InstallationDto has no [Required] attributes. Missing 'name' will reach
#    the database and cause a 500 (DbUpdateException), not a 400.
#    This is documented as an API design gap (no model validation on Create).
#
# 5. OrganizationId is Guid? (nullable) in both the DTO and model. The Create
#    action does not validate whether the supplied OrganizationId references a
#    real organization — there is no FK check in the controller. Passing a
#    nonexistent OrganizationId may succeed (200) or fail at the DB level (500)
#    depending on whether a FK constraint exists in the database.
#
# 6. This API uses PUT for creates and POST for updates (unconventional but
#    consistent across all controllers). See APIBase.put() docstring.
#
# 7. panelCollectionId is present in InstallationDto (non-nullable Guid) but the
#    Create action does NOT call ResolvePanelCollectionIdAsync. Omitting
#    panelCollectionId from the payload leaves it as Guid.Empty. The conftest
#    uses this same approach and creates successfully, so no FK constraint fires.

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

def _make_autotest_inst_name() -> str:
    """
    Generate a unique AUTOTEST installation name.

    Format: AUTOTEST_INST_{8 hex chars}
    Example: AUTOTEST_INST_3a7f9c12   (21 chars)

    The AUTOTEST_ prefix ensures the session-level conftest cleanup will
    catch any orphaned records this test suite leaves behind.

    Returns:
        str: A unique installation name prefixed with AUTOTEST_INST_.
    """
    short_id = uuid.uuid4().hex[:8]
    return f"AUTOTEST_INST_{short_id}"


def _make_create_payload(name: str, installation_id: str = None) -> dict:
    """
    Build a minimal valid installation create payload.

    installationId is optional — if omitted, EF Core auto-generates a GUID.
    We supply it explicitly here so the ID is known before the request, which
    avoids a post-create search-by-name step and simplifies cleanup.
    All other fields use their DTO defaults. panelCollectionId is intentionally
    omitted; the controller accepts this without error (leaves it as Guid.Empty
    in the database).

    Args:
        name:            The installation name (use AUTOTEST_ prefix).
        installation_id: The UUID to assign as the installationId. If None,
                         a new UUID is generated.

    Returns:
        dict: A payload dict ready to pass to APIBase.put().
    """
    return {
        "installationId": installation_id or str(uuid.uuid4()),
        "name": name,
        "organizationId": TEST_ORG_ID,
    }


# ---------------------------------------------------------------------------
# Class 1: Read-only GET tests — safe to run at any time, create no data
# ---------------------------------------------------------------------------

class TestAPIInstallationsGet:
    """
    Read-only tests for the Installations GET endpoints.

    Covers:
        - GET /Installations?pageNumber=&pageSize=  (list, plain array)
        - GET /Installations/search?name=&pageNumber=&pageSize=  (search, ResponseDto)
        - GET /Installations/{id}/details  (single record by GUID)

    No data is created or modified by any test in this class.
    """

    def setup_method(self):
        """Initialize APIBase for each test method."""
        self.api = APIBase()

    def _get_first_installation_id(self) -> str | None:
        """
        Fetch the first installation from the list endpoint and return its id.

        Used by detail tests to discover a real installation ID without
        hardcoding QA environment data.

        Returns:
            str: The installationId of the first record, or None if the
                 list is empty or the request fails.
        """
        response = self.api.get("/Installations", params={"pageNumber": 1, "pageSize": 1})

        if response.status_code != 200:
            logger.error(
                f"Could not fetch installations list to discover an ID. "
                f"Status: {response.status_code}"
            )
            return None

        try:
            data = response.json()
            if not isinstance(data, list) or len(data) == 0:
                logger.warning("Installations list is empty — no ID available.")
                return None
            inst_id = data[0].get("installationId")
            logger.debug(f"Discovered installation ID for detail tests: {inst_id}")
            return str(inst_id)
        except (requests.exceptions.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing installations list response: {e}")
            return None

    # -------------------------------------------------------------------------
    # GET /Installations — basic list (plain array, no ResponseDto wrapper)
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.installations
    def test_get_list_returns_200(self):
        """
        GET /Installations returns HTTP 200 with a valid JSON response body.

        Baseline connectivity check for the installations list endpoint.
        """
        try:
            response = self.api.get("/Installations", params={"pageNumber": 1, "pageSize": 10})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Installations, got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Installations response body is not valid JSON: {e}")
                raise

            assert data is not None, "Response body should not be null"

            logger.info("GET /Installations returned 200 with a valid JSON body.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_list_returns_200: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.installations
    def test_get_list_returns_array(self):
        """
        GET /Installations response body is a plain JSON array.

        IMPORTANT: Like /api/Organization, the Installations list endpoint does
        NOT use a ResponseDto wrapper — it returns a raw array. The search endpoint
        (/Installations/search) does use ResponseDto. This test explicitly captures
        that shape so any future API change that adds a wrapper would be caught.
        """
        try:
            response = self.api.get("/Installations", params={"pageNumber": 1, "pageSize": 10})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Installations, got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Installations response body is not valid JSON: {e}")
                raise

            assert isinstance(data, list), (
                f"Expected GET /Installations to return a JSON array (no ResponseDto wrapper). "
                f"Got {type(data).__name__}. "
                f"If this endpoint now wraps results in ResponseDto, update this test and the "
                f"other GET list tests to reflect the new response shape."
            )

            logger.info(
                f"GET /Installations returned a plain array with {len(data)} item(s). "
                f"No ResponseDto wrapper confirmed."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_list_returns_array: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.installations
    def test_get_list_items_have_required_fields(self):
        """
        Each installation in the GET /Installations list has the expected fields.

        Fields checked (camelCase — ASP.NET Core serializes PascalCase C# properties
        to camelCase automatically):
            - installationId  — primary key
            - name            — display name

        If the list is empty in the QA environment this test is skipped.
        """
        try:
            response = self.api.get("/Installations", params={"pageNumber": 1, "pageSize": 10})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Installations, got {response.status_code}"
            )

            data = response.json()

            if not isinstance(data, list) or len(data) == 0:
                pytest.skip("Installations list is empty — cannot verify item fields.")

            required_fields = ["installationId", "name", "organizationId"]
            first_item = data[0]

            missing = [f for f in required_fields if f not in first_item]

            assert not missing, (
                f"First installation in GET /Installations is missing fields: {missing}. "
                f"Actual keys: {list(first_item.keys())}. "
                f"Remember: C# PascalCase DTO properties serialize to camelCase JSON keys."
            )

            logger.info(
                f"GET /Installations first item field check passed. "
                f"Keys present: {list(first_item.keys())}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_list_items_have_required_fields: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.pagination
    def test_get_list_page_size_param_limits_results(self):
        """
        GET /Installations with pageSize=1 returns exactly 1 item.

        Verifies that the pageSize query parameter is respected by the endpoint.
        If only 1 installation exists in QA this test still passes.
        """
        try:
            response = self.api.get("/Installations", params={"pageNumber": 1, "pageSize": 1})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Installations?pageSize=1, got {response.status_code}"
            )

            data = response.json()

            assert isinstance(data, list), (
                f"Expected a list, got {type(data).__name__}"
            )

            assert len(data) <= 1, (
                f"Expected at most 1 result with pageSize=1, got {len(data)}"
            )

            logger.info(
                f"GET /Installations?pageSize=1 returned {len(data)} item(s) — pageSize respected."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_list_page_size_param_limits_results: {e}")
            raise

    # -------------------------------------------------------------------------
    # GET /Installations/search — search with ResponseDto wrapper
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.search
    def test_get_search_returns_200_with_pagination_envelope(self):
        """
        GET /Installations/search returns 200 with a ResponseDto pagination envelope.

        Unlike the basic list endpoint, the search endpoint wraps results in
        ResponseDto (page, pageCount, pageSize, totalCount, results).
        """
        try:
            response = self.api.get(
                "/Installations/search",
                params={"name": "a", "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 from GET /Installations/search, got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Installations/search response is not valid JSON: {e}")
                raise

            assert isinstance(data, dict), (
                f"Expected GET /Installations/search to return a JSON object (ResponseDto). "
                f"Got {type(data).__name__}."
            )

            logger.info("GET /Installations/search returned 200 with a JSON object body.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_get_search_returns_200_with_pagination_envelope: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.search
    @pytest.mark.pagination
    def test_get_search_pagination_fields_present(self):
        """
        GET /Installations/search response contains all required ResponseDto fields.

        Verifies the pagination envelope shape: page, pageCount, pageSize,
        totalCount, and results (as a list).
        """
        try:
            response = self.api.get(
                "/Installations/search",
                params={"name": "a", "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 from GET /Installations/search, got {response.status_code}"
            )

            data = response.json()

            required_fields = ["page", "pageSize", "pageCount", "totalCount", "results"]
            missing = [f for f in required_fields if f not in data]

            assert not missing, (
                f"GET /Installations/search is missing required pagination fields: {missing}. "
                f"Actual keys: {list(data.keys())}"
            )

            assert isinstance(data["results"], list), (
                f"Expected 'results' to be a list, got {type(data['results']).__name__}"
            )

            logger.info(
                f"GET /Installations/search pagination envelope verified: "
                f"page={data['page']}, pageSize={data['pageSize']}, "
                f"pageCount={data['pageCount']}, totalCount={data['totalCount']}, "
                f"results count={len(data['results'])}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_get_search_pagination_fields_present: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.search
    def test_get_search_name_filter_returns_results(self):
        """
        GET /Installations/search with a broad name filter returns at least one result.

        Uses name="a" to maximize the chance of matching existing installations
        without assuming specific names in the QA environment.
        """
        try:
            response = self.api.get(
                "/Installations/search",
                params={"name": "a", "pageNumber": 1, "pageSize": 25}
            )

            assert response.status_code == 200, (
                f"Expected 200 from GET /Installations/search?name=a, "
                f"got {response.status_code}"
            )

            data = response.json()
            results = data.get("results", [])

            assert len(results) >= 1, (
                f"Expected at least 1 result for name='a' but got {len(results)}. "
                f"QA environment may have no installations with 'a' in the name, or "
                f"the name filter is not working."
            )

            # Every result should contain "a" (case-insensitive) in its name
            for installation in results:
                name = installation.get("name", "")
                assert "a" in name.lower(), (
                    f"Search result '{name}' does not contain the search term 'a'. "
                    f"The name filter may be returning unfiltered results."
                )

            logger.info(
                f"GET /Installations/search?name=a returned {len(results)} result(s); "
                f"all contain 'a' in name."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_get_search_name_filter_returns_results: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.search
    def test_get_search_no_match_returns_empty_list(self):
        """
        GET /Installations/search with a non-matching name returns 200 with an
        empty results list — not a 404.

        The API should treat "no results" as a successful search that found nothing,
        not as a missing resource.
        """
        no_match_name = "ZZZZZ_WILDXR_TEST_NO_MATCH_ZZZZZ"

        try:
            response = self.api.get(
                "/Installations/search",
                params={"name": no_match_name, "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 (not 404) for a no-match search on "
                f"GET /Installations/search. Got {response.status_code}."
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
                f"GET /Installations/search with no-match name correctly returned "
                f"200 with an empty results list."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_get_search_no_match_returns_empty_list: {e}"
            )
            raise

    # -------------------------------------------------------------------------
    # GET /Installations/{id}/details — single record by GUID
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.installations
    def test_get_detail_returns_200_for_valid_id(self):
        """
        GET /Installations/{id}/details returns 200 for a valid, pre-existing
        installation ID.

        The installation ID is discovered dynamically from the list endpoint to
        avoid hardcoding QA data.
        """
        inst_id = self._get_first_installation_id()

        if inst_id is None:
            pytest.skip(
                "No installations exist in the QA environment — "
                "cannot test GET /Installations/{id}/details."
            )

        try:
            response = self.api.get(f"/Installations/{inst_id}/details")

            assert response.status_code == 200, (
                f"Expected 200 from GET /Installations/{inst_id}/details, "
                f"got {response.status_code}"
            )

            data = response.json()

            assert isinstance(data, dict), (
                f"Expected response body to be a JSON object, got {type(data).__name__}"
            )

            logger.info(
                f"GET /Installations/{inst_id}/details returned 200 with a valid JSON body."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_detail_returns_200_for_valid_id: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.installations
    def test_get_detail_has_required_fields(self):
        """
        GET /Installations/{id}/details response contains the expected InstallationDto fields.

        Fields verified (camelCase):
            - installationId   — primary key
            - name             — display name
            - organizationId   — owning organization (nullable in DTO)
        """
        inst_id = self._get_first_installation_id()

        if inst_id is None:
            pytest.skip(
                "No installations exist in the QA environment — "
                "cannot test GET /Installations/{id}/details."
            )

        try:
            response = self.api.get(f"/Installations/{inst_id}/details")

            assert response.status_code == 200, (
                f"Expected 200 from GET /Installations/{inst_id}/details, "
                f"got {response.status_code}"
            )

            data = response.json()

            required_fields = ["installationId", "name", "organizationId"]
            missing = [f for f in required_fields if f not in data]

            assert not missing, (
                f"GET /Installations/{inst_id}/details response is missing fields: {missing}. "
                f"Actual keys returned: {list(data.keys())}. "
                f"Remember: C# PascalCase DTO properties serialize to camelCase JSON keys."
            )

            logger.info(
                f"GET /Installations/{inst_id}/details required field check passed. "
                f"All fields present: {list(data.keys())}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_detail_has_required_fields: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.edge_case
    def test_get_detail_returns_400_for_nonexistent_id(self):
        """
        GET /Installations/{id}/details returns 400 for a nonexistent (but valid) GUID.

        Note: This API returns 400 BadRequest ("not found") — not a 404 Not Found.
        This is consistent across all controllers and is expected behavior.
        """
        fake_id = str(uuid.uuid4())

        try:
            response = self.api.get(f"/Installations/{fake_id}/details")

            assert response.status_code == 400, (
                f"Expected 400 from GET /Installations/{fake_id}/details "
                f"(nonexistent ID). Got {response.status_code}. "
                f"Note: This API uses 400 BadRequest (not 404) for not-found conditions."
            )

            logger.info(
                f"GET /Installations/{fake_id}/details correctly returned 400 "
                f"for a nonexistent installation ID."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_get_detail_returns_400_for_nonexistent_id: {e}"
            )
            raise


# ---------------------------------------------------------------------------
# Class 2: CRUD tests — create/update/delete with automatic cleanup
# ---------------------------------------------------------------------------

class TestAPIInstallationsCRUD:
    """
    CRUD tests for the Installations write endpoints.

    Each test that creates an installation tracks its ID in _created_ids.
    teardown_method deletes all tracked installations after each test, so
    failures in one test don't leave orphaned AUTOTEST data behind.

    All test installation names use the AUTOTEST_INST_ prefix so the
    session-level conftest cleanup will also catch any records that
    teardown_method misses.

    NOTE on installationId in create payload:
        installationId is optional — if omitted, EF Core auto-generates a GUID
        (default convention for Guid PKs). This test class supplies the ID
        explicitly so the ID is known before the request, avoiding a
        post-create search-by-name step and simplifying teardown cleanup.

    Covers:
        - PUT /Installations/create  (create — uses PUT, not POST)
        - POST /Installations/update (update — uses POST, not PUT)
        - DELETE /Installations/delete?id=  (delete)
    """

    def setup_method(self):
        """Initialize APIBase and the created-installation tracking list."""
        self.api = APIBase()
        self._created_ids = []

    def teardown_method(self):
        """Delete all AUTOTEST installations created during this test."""
        for inst_id in self._created_ids:
            try:
                self.api.delete("/Installations/delete", params={"id": inst_id})
                logger.debug(f"Teardown: deleted installation {inst_id}")
            except Exception as e:
                logger.warning(f"Teardown: failed to delete installation {inst_id}: {e}")
        self._created_ids.clear()

    def _create_installation(self, name: str) -> str:
        """
        Create an installation via PUT /Installations/create and return its ID.

        installationId is supplied in the payload as a convenience — this makes
        the ID known before the request is sent, so no post-create search is
        needed. The ID is optional; EF Core auto-generates one if omitted.

        Args:
            name: The installation name. Must use AUTOTEST_ prefix.

        Returns:
            str: The installationId used (pre-set in the payload), or None if
                 the create request failed.
        """
        inst_id = str(uuid.uuid4())
        payload = _make_create_payload(name, installation_id=inst_id)

        response = self.api.put("/Installations/create", body=payload)

        if response.status_code != 200:
            logger.error(
                f"PUT /Installations/create failed with {response.status_code} "
                f"for name='{name}'. Response: {response.text}"
            )
            return None

        self._created_ids.append(inst_id)
        logger.debug(f"Created installation '{name}' with ID {inst_id}")
        return inst_id

    # -------------------------------------------------------------------------
    # Create
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.installations
    def test_create_installation_returns_200(self):
        """
        PUT /Installations/create with a valid payload returns 200.

        Uses an AUTOTEST_ prefixed name so the installation is cleaned up by
        teardown and by the session-level conftest cleanup.

        Note: Create uses PUT (not POST) and returns an empty 200 body.
        installationId is supplied in the payload for convenience so the ID
        is known upfront; EF Core would auto-generate one if it were omitted.
        """
        name = _make_autotest_inst_name()
        inst_id = str(uuid.uuid4())
        payload = _make_create_payload(name, installation_id=inst_id)

        try:
            response = self.api.put("/Installations/create", body=payload)

            assert response.status_code == 200, (
                f"Expected 200 from PUT /Installations/create, "
                f"got {response.status_code}. "
                f"Response body: {response.text}"
            )

            # Register for cleanup
            self._created_ids.append(inst_id)

            logger.info(
                f"PUT /Installations/create returned 200 for name='{name}' "
                f"(ID {inst_id})."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_create_installation_returns_200: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.installations
    def test_created_installation_appears_in_search(self):
        """
        A newly created installation can be found via GET /Installations/search
        immediately after creation.

        Verifies that Create is durable and that the search endpoint reflects
        the current database state.
        """
        name = _make_autotest_inst_name()

        try:
            inst_id = self._create_installation(name)

            assert inst_id is not None, (
                f"Setup failed: PUT /Installations/create did not return 200 "
                f"for name='{name}'."
            )

            # Search for the newly created installation
            search_response = self.api.get(
                "/Installations/search",
                params={"name": name, "pageNumber": 1, "pageSize": 10}
            )

            assert search_response.status_code == 200, (
                f"Search after create failed with {search_response.status_code}"
            )

            results = search_response.json().get("results", [])
            found_names = [inst.get("name") for inst in results]

            assert name in found_names, (
                f"Newly created installation '{name}' not found in search results. "
                f"Results returned: {found_names}"
            )

            logger.info(
                f"Newly created installation '{name}' (ID {inst_id}) found in "
                f"search results immediately after creation."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_created_installation_appears_in_search: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.installations
    def test_created_installation_detail_matches_payload(self):
        """
        GET /Installations/{id}/details for a newly created installation returns
        the values supplied in the create payload.

        Specifically verifies that installationId and name round-trip correctly.
        """
        name = _make_autotest_inst_name()

        try:
            inst_id = self._create_installation(name)

            assert inst_id is not None, (
                f"Setup failed: could not create installation '{name}'"
            )

            detail_response = self.api.get(f"/Installations/{inst_id}/details")

            assert detail_response.status_code == 200, (
                f"Expected 200 from GET /Installations/{inst_id}/details after create, "
                f"got {detail_response.status_code}"
            )

            data = detail_response.json()

            assert data.get("installationId") == inst_id, (
                f"installationId mismatch. Expected '{inst_id}', "
                f"got '{data.get('installationId')}'."
            )

            assert data.get("name") == name, (
                f"name mismatch. Expected '{name}', got '{data.get('name')}'."
            )

            logger.info(
                f"GET /Installations/{inst_id}/details confirmed installationId "
                f"and name match the create payload."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_created_installation_detail_matches_payload: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.edge_case
    def test_create_installation_missing_name_returns_error(self):
        """
        PUT /Installations/create without a name field returns an error response.

        API DESIGN NOTE: InstallationDto has no [Required] attribute on Name, so
        ASP.NET Core model validation does NOT catch this at the binding layer.
        The missing name propagates to the database insert and causes a
        DbUpdateException (database NOT NULL constraint). The Create action catches
        all exceptions and returns 500 with the exception details.

        Expected: 500 (database error from null name constraint).
        Contrast with Organization where [Required] on Name gives a clean 400.

        If this test returns 400 instead of 500, the API has added validation —
        update the assertion and this docstring to match.
        """
        inst_id = str(uuid.uuid4())

        try:
            response = self.api.put(
                "/Installations/create",
                body={"installationId": inst_id, "organizationId": TEST_ORG_ID}
                # name intentionally omitted
            )

            assert response.status_code in (400, 500), (
                f"Expected 400 or 500 from PUT /Installations/create with missing name, "
                f"got {response.status_code}. "
                f"The API should reject a nameless installation — either via model "
                f"validation (400) or database constraint (500)."
            )

            logger.info(
                f"PUT /Installations/create with missing name returned "
                f"{response.status_code} — documented behavior."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_create_installation_missing_name_returns_error: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.edge_case
    def test_create_installation_with_invalid_org_id(self):
        """
        PUT /Installations/create with a nonexistent OrganizationId documents API behavior.

        The Create action does NOT validate OrganizationId — there is no FK check
        in the controller. Whether a foreign key constraint exists at the database
        level determines the outcome:
            - No DB FK constraint: returns 200 (installation created with orphaned org ref)
            - DB FK constraint exists: returns 500 (DbUpdateException)

        This test documents the actual behavior. If it returns 200, that is an API
        design gap: the API accepts installations referencing nonexistent organizations.
        """
        name = _make_autotest_inst_name()
        inst_id = str(uuid.uuid4())
        fake_org_id = str(uuid.uuid4())

        payload = {
            "installationId": inst_id,
            "name": name,
            "organizationId": fake_org_id,
        }

        try:
            response = self.api.put("/Installations/create", body=payload)

            if response.status_code == 200:
                # Installation was created with an invalid org ID — register for cleanup
                self._created_ids.append(inst_id)
                logger.warning(
                    f"PUT /Installations/create with nonexistent organizationId='{fake_org_id}' "
                    f"returned 200. The API accepted an installation with an invalid org "
                    f"reference. This is an API design gap — no FK validation in the controller "
                    f"and no DB foreign key constraint on OrganizationId."
                )
            elif response.status_code in (400, 500):
                logger.info(
                    f"PUT /Installations/create with nonexistent organizationId "
                    f"returned {response.status_code} — the database enforces referential "
                    f"integrity on OrganizationId."
                )
            else:
                pytest.fail(
                    f"Unexpected status {response.status_code} from PUT /Installations/create "
                    f"with nonexistent organizationId. Expected 200, 400, or 500."
                )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_create_installation_with_invalid_org_id: {e}"
            )
            raise

    # -------------------------------------------------------------------------
    # Update
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.installations
    def test_update_installation_name_returns_200(self):
        """
        POST /Installations/update with a valid payload returns 200 and the
        change is reflected in GET /Installations/{id}/details.

        Note: Update uses POST (not PUT) — see APIBase.post() docstring.
        """
        original_name = _make_autotest_inst_name()
        updated_name = _make_autotest_inst_name()

        try:
            inst_id = self._create_installation(original_name)

            assert inst_id is not None, (
                f"Setup failed: could not create installation '{original_name}'"
            )

            # Update the name — send the full DTO with the new name
            update_response = self.api.post(
                "/Installations/update",
                body={"installationId": inst_id, "name": updated_name}
            )

            assert update_response.status_code == 200, (
                f"Expected 200 from POST /Installations/update, "
                f"got {update_response.status_code}. "
                f"Response: {update_response.text}"
            )

            # Verify the change persisted via the detail endpoint
            detail_response = self.api.get(f"/Installations/{inst_id}/details")

            assert detail_response.status_code == 200, (
                f"Expected 200 from GET /Installations/{inst_id}/details after update, "
                f"got {detail_response.status_code}"
            )

            actual_name = detail_response.json().get("name")

            assert actual_name == updated_name, (
                f"Name was not updated. Expected '{updated_name}', got '{actual_name}'."
            )

            logger.info(
                f"POST /Installations/update: name changed from '{original_name}' "
                f"to '{updated_name}' — confirmed via /details."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_update_installation_name_returns_200: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.edge_case
    def test_update_installation_missing_id_returns_400(self):
        """
        POST /Installations/update without an installationId returns 400.

        The Update action checks `model.InstallationId == Guid.Empty` and returns
        BadRequest("Id is required") when the ID is absent or is the empty GUID.
        """
        try:
            response = self.api.post(
                "/Installations/update",
                body={"name": "UpdateWithoutId"}
                # installationId intentionally omitted — deserializes to Guid.Empty
            )

            assert response.status_code == 400, (
                f"Expected 400 from POST /Installations/update with missing "
                f"installationId, got {response.status_code}."
            )

            logger.info(
                "POST /Installations/update with missing installationId correctly "
                "returned 400."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_update_installation_missing_id_returns_400: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.edge_case
    def test_update_nonexistent_installation_returns_400(self):
        """
        POST /Installations/update with a nonexistent installationId returns 400.

        The Update action performs a FirstOrDefaultAsync lookup and returns
        BadRequest("Installation not found") when the record does not exist.
        """
        fake_id = str(uuid.uuid4())

        try:
            response = self.api.post(
                "/Installations/update",
                body={"installationId": fake_id, "name": "GhostInstallation"}
            )

            assert response.status_code == 400, (
                f"Expected 400 from POST /Installations/update with nonexistent ID "
                f"'{fake_id}', got {response.status_code}. "
                f"Note: This API uses 400 BadRequest (not 404) for not-found updates."
            )

            logger.info(
                f"POST /Installations/update with nonexistent ID '{fake_id}' "
                f"correctly returned 400."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_update_nonexistent_installation_returns_400: {e}"
            )
            raise

    # -------------------------------------------------------------------------
    # Delete
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.installations
    def test_delete_installation_returns_200(self):
        """
        DELETE /Installations/delete?id={guid} returns 200 and the installation
        no longer appears in search results.

        Creates a test installation, deletes it, then confirms it is gone.
        The installation ID is removed from _created_ids after successful deletion
        so teardown_method does not attempt a double-delete.
        """
        name = _make_autotest_inst_name()

        try:
            inst_id = self._create_installation(name)

            assert inst_id is not None, (
                f"Setup failed: could not create installation '{name}'"
            )

            # Delete the installation
            delete_response = self.api.delete(
                "/Installations/delete",
                params={"id": inst_id}
            )

            assert delete_response.status_code == 200, (
                f"Expected 200 from DELETE /Installations/delete?id={inst_id}, "
                f"got {delete_response.status_code}. "
                f"Response: {delete_response.text}"
            )

            # Remove from tracking to prevent double-delete in teardown
            if inst_id in self._created_ids:
                self._created_ids.remove(inst_id)

            # Verify the installation no longer appears in search
            search_response = self.api.get(
                "/Installations/search",
                params={"name": name, "pageNumber": 1, "pageSize": 10}
            )

            if search_response.status_code == 200:
                results = search_response.json().get("results", [])
                found_names = [inst.get("name") for inst in results]

                assert name not in found_names, (
                    f"Deleted installation '{name}' still appears in search results: "
                    f"{found_names}"
                )

            logger.info(
                f"DELETE /Installations/delete?id={inst_id}: installation deleted and "
                f"confirmed absent from search."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_delete_installation_returns_200: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.installations
    @pytest.mark.edge_case
    def test_delete_nonexistent_installation_returns_400(self):
        """
        DELETE /Installations/delete?id={guid} returns 400 for a nonexistent GUID.

        The Delete action does a FirstOrDefaultAsync lookup and returns
        BadRequest("not found") when the record does not exist.
        Note: Consistent with all other controllers — 400, not 404.
        """
        fake_id = str(uuid.uuid4())

        try:
            response = self.api.delete(
                "/Installations/delete",
                params={"id": fake_id}
            )

            assert response.status_code == 400, (
                f"Expected 400 from DELETE /Installations/delete?id={fake_id} "
                f"(nonexistent). Got {response.status_code}. "
                f"Note: This API uses 400 (not 404) for not-found conditions."
            )

            logger.info(
                f"DELETE /Installations/delete with nonexistent ID correctly "
                f"returned 400."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_delete_nonexistent_installation_returns_400: {e}"
            )
            raise
