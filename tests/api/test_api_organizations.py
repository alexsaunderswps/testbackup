# test_api_organizations.py
# Tests for the /api/Organization endpoints.
#
# IMPORTANT API QUIRKS FOR THIS RESOURCE:
#
# 1. GET /api/Organization returns a plain JSON array, NOT a ResponseDto wrapper.
#    Every other resource uses ResponseDto for list endpoints; Organizations does not.
#    The search endpoint (/Organization/search) does use ResponseDto.
#
# 2. PUT /api/Organization/Create returns 200 with an EMPTY response body.
#    The created org's ID is not returned. To get the ID after creating an org,
#    search for it by the exact name you used.
#
# 3. Not-found conditions return 400 (BadRequest), not 404.
#    Consistent with all other controllers in this API.
#
# 4. Organization.Name is VARCHAR(50) — names must be 50 characters or fewer.
#
# 5. This API uses PUT for creates and POST for updates (unconventional but
#    consistent across all controllers). See APIBase.put() docstring.

import uuid
import pytest
import requests
from datetime import datetime
from .api_base import APIBase
from utilities.utils import logger


# ---------------------------------------------------------------------------
# Shared helper — generate a unique, short AUTOTEST org name
# ---------------------------------------------------------------------------

def _make_autotest_org_name() -> str:
    """
    Generate a unique AUTOTEST organization name within the 50-char VARCHAR limit.

    Format: AUTOTEST_ORG_{8 hex chars}
    Example: AUTOTEST_ORG_3a7f9c12   (21 chars — well within the 50-char limit)

    Returns:
        str: A unique org name prefixed with AUTOTEST_ORG_.
    """
    short_id = uuid.uuid4().hex[:8]
    return f"AUTOTEST_ORG_{short_id}"


# ---------------------------------------------------------------------------
# Class 1: Read-only GET tests — safe to run at any time, create no data
# ---------------------------------------------------------------------------

class TestAPIOrganizationsGet:
    """
    Read-only tests for the Organization GET endpoints.

    Covers:
        - GET /Organization?pageNumber=&pageSize=  (basic list, plain array)
        - GET /Organization/search?name=&pageNumber=&pageSize=  (search, ResponseDto)
        - GET /Organization/{id}/Details  (single org by GUID)

    No data is created or modified by any test in this class.
    """

    def setup_method(self):
        """Initialize APIBase for each test method."""
        self.api = APIBase()

    def _get_first_org_id(self) -> str | None:
        """
        Fetch the first organization from the list endpoint and return its organizationId.

        Used by detail tests to discover a valid org ID without hardcoding
        QA environment data.

        Returns:
            str: The organizationId of the first org in the list, or None if the
                 list is empty or the request fails.
        """
        response = self.api.get("/Organization", params={"pageNumber": 1, "pageSize": 1})

        if response.status_code != 200:
            logger.error(
                f"Could not fetch org list to discover an org ID. "
                f"Status: {response.status_code}"
            )
            return None

        try:
            data = response.json()
            if not isinstance(data, list) or len(data) == 0:
                logger.warning("Organization list is empty — no org ID available.")
                return None
            org_id = data[0].get("organizationId")
            logger.debug(f"Discovered org ID for details tests: {org_id}")
            return str(org_id)
        except (requests.exceptions.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing org list response to get org ID: {e}")
            return None

    # -------------------------------------------------------------------------
    # GET /Organization — basic list (plain array, no ResponseDto wrapper)
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.organizations
    def test_get_list_returns_200(self):
        """
        GET /Organization returns HTTP 200 with a valid JSON response body.

        Baseline connectivity check for the organizations list endpoint.
        """
        try:
            response = self.api.get("/Organization", params={"pageNumber": 1, "pageSize": 10})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Organization, got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Organization response body is not valid JSON: {e}")
                raise

            assert data is not None, "Response body should not be null"

            logger.info("GET /Organization returned 200 with a valid JSON body.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_list_returns_200: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    def test_get_list_returns_array(self):
        """
        GET /Organization response body is a plain JSON array.

        IMPORTANT: Unlike all other list endpoints in this API, /Organization does
        NOT use a ResponseDto wrapper. It returns a raw list. This test explicitly
        verifies that shape so any future API change that wraps the response would
        be caught.
        """
        try:
            response = self.api.get("/Organization", params={"pageNumber": 1, "pageSize": 10})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Organization, got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Organization response body is not valid JSON: {e}")
                raise

            assert isinstance(data, list), (
                f"Expected GET /Organization to return a JSON array (no ResponseDto wrapper). "
                f"Got {type(data).__name__}. "
                f"If this endpoint now returns a ResponseDto, update this test and the "
                f"other GET list tests in this class to reflect the new response shape."
            )

            logger.info(
                f"GET /Organization returned a plain array with {len(data)} item(s). "
                f"No ResponseDto wrapper confirmed."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_list_returns_array: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    def test_get_list_items_have_required_fields(self):
        """
        Each organization in the GET /Organization list has the expected fields.

        Fields checked (camelCase — ASP.NET Core serializes PascalCase C# properties
        to camelCase automatically):
            - organizationId  — primary key
            - name            — [Required] in OrganizationDto

        If the list is empty in the QA environment this test is skipped.
        """
        try:
            response = self.api.get("/Organization", params={"pageNumber": 1, "pageSize": 10})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Organization, got {response.status_code}"
            )

            data = response.json()

            if not isinstance(data, list) or len(data) == 0:
                pytest.skip("Organization list is empty — cannot verify item fields.")

            required_fields = ["organizationId", "name"]
            first_item = data[0]

            missing = [f for f in required_fields if f not in first_item]

            assert not missing, (
                f"First org in GET /Organization list is missing fields: {missing}. "
                f"Actual keys: {list(first_item.keys())}. "
                f"Remember: C# PascalCase properties serialize to camelCase JSON keys."
            )

            logger.info(
                f"GET /Organization first item field check passed. "
                f"Keys present: {list(first_item.keys())}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_list_items_have_required_fields: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    @pytest.mark.pagination
    def test_get_list_page_size_param_limits_results(self):
        """
        GET /Organization with pageSize=1 returns exactly 1 item.

        Verifies that the pageSize query parameter is respected by the endpoint.
        If only 1 org exists in QA this test still passes (1 returned ≤ 1 requested).
        """
        try:
            response = self.api.get("/Organization", params={"pageNumber": 1, "pageSize": 1})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Organization?pageSize=1, got {response.status_code}"
            )

            data = response.json()

            assert isinstance(data, list), (
                f"Expected a list, got {type(data).__name__}"
            )

            assert len(data) <= 1, (
                f"Expected at most 1 result with pageSize=1, got {len(data)}"
            )

            logger.info(f"GET /Organization?pageSize=1 returned {len(data)} item(s) — pageSize respected.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_list_page_size_param_limits_results: {e}")
            raise

    # -------------------------------------------------------------------------
    # GET /Organization/search — search with ResponseDto wrapper
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.organizations
    @pytest.mark.search
    def test_get_search_returns_200_with_pagination_envelope(self):
        """
        GET /Organization/search returns 200 with a ResponseDto pagination envelope.

        Unlike the basic list endpoint, the search endpoint wraps results in a
        ResponseDto (page, pageCount, pageSize, totalCount, results).
        """
        try:
            response = self.api.get(
                "/Organization/search",
                params={"name": "a", "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 from GET /Organization/search, got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Organization/search response is not valid JSON: {e}")
                raise

            assert isinstance(data, dict), (
                f"Expected GET /Organization/search to return a JSON object (ResponseDto). "
                f"Got {type(data).__name__}."
            )

            logger.info("GET /Organization/search returned 200 with a JSON object body.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_get_search_returns_200_with_pagination_envelope: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    @pytest.mark.search
    @pytest.mark.pagination
    def test_get_search_pagination_fields_present(self):
        """
        GET /Organization/search response contains all required ResponseDto fields.

        Verifies the pagination envelope shape: page, pageCount, pageSize,
        totalCount, and results (as a list).
        """
        try:
            response = self.api.get(
                "/Organization/search",
                params={"name": "a", "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 from GET /Organization/search, got {response.status_code}"
            )

            data = response.json()

            required_fields = ["page", "pageSize", "pageCount", "totalCount", "results"]
            missing = [f for f in required_fields if f not in data]

            assert not missing, (
                f"GET /Organization/search is missing required pagination fields: {missing}. "
                f"Actual keys: {list(data.keys())}"
            )

            assert isinstance(data["results"], list), (
                f"Expected 'results' to be a list, got {type(data['results']).__name__}"
            )

            logger.info(
                f"GET /Organization/search pagination envelope verified: "
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
    @pytest.mark.organizations
    @pytest.mark.search
    def test_get_search_name_filter_returns_results(self):
        """
        GET /Organization/search with a broad name filter returns at least one result.

        Uses name="a" to maximize the chance of matching existing orgs without
        assuming specific org names in the QA environment.
        """
        try:
            response = self.api.get(
                "/Organization/search",
                params={"name": "a", "pageNumber": 1, "pageSize": 25}
            )

            assert response.status_code == 200, (
                f"Expected 200 from GET /Organization/search?name=a, got {response.status_code}"
            )

            data = response.json()
            results = data.get("results", [])

            assert len(results) >= 1, (
                f"Expected at least 1 result for name='a' but got {len(results)}. "
                f"QA environment may have no orgs with 'a' in the name, or the name "
                f"filter is not working."
            )

            # Every result should contain "a" (case-insensitive) in its name
            for org in results:
                name = org.get("name", "")
                assert "a" in name.lower(), (
                    f"Search result '{name}' does not contain the search term 'a'. "
                    f"The name filter may be returning unfiltered results."
                )

            logger.info(
                f"GET /Organization/search?name=a returned {len(results)} result(s); "
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
    @pytest.mark.organizations
    @pytest.mark.search
    def test_get_search_no_match_returns_empty_list(self):
        """
        GET /Organization/search with a non-matching name returns 200 with an
        empty results list — not a 404.

        The API should treat "no results" as a successful search that found nothing,
        not as a missing resource.
        """
        no_match_name = "ZZZZZ_WILDXR_TEST_NO_MATCH_ZZZZZ"

        try:
            response = self.api.get(
                "/Organization/search",
                params={"name": no_match_name, "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 (not 404) for a no-match search on GET /Organization/search. "
                f"Got {response.status_code}."
            )

            data = response.json()
            results = data.get("results", [])

            assert isinstance(results, list), (
                f"Expected 'results' to be a list, got {type(results).__name__}"
            )

            assert len(results) == 0, (
                f"Expected 0 results for no-match name='{no_match_name}', got {len(results)}"
            )

            logger.info(
                f"GET /Organization/search with no-match name correctly returned "
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
    # GET /Organization/{id}/Details — single org by GUID
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.organizations
    def test_get_detail_returns_200_for_valid_id(self):
        """
        GET /Organization/{id}/Details returns 200 for a valid, pre-existing org ID.

        The org ID is discovered dynamically from the list endpoint to avoid
        hardcoding QA data.
        """
        org_id = self._get_first_org_id()

        if org_id is None:
            pytest.skip(
                "No organizations exist in the QA environment — "
                "cannot test GET /Organization/{id}/Details."
            )

        try:
            response = self.api.get(f"/Organization/{org_id}/Details")

            assert response.status_code == 200, (
                f"Expected 200 from GET /Organization/{org_id}/Details, "
                f"got {response.status_code}"
            )

            data = response.json()

            assert isinstance(data, dict), (
                f"Expected response body to be a JSON object, got {type(data).__name__}"
            )

            logger.info(
                f"GET /Organization/{org_id}/Details returned 200 with a valid JSON body."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_detail_returns_200_for_valid_id: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    def test_get_detail_has_required_fields(self):
        """
        GET /Organization/{id}/Details response contains the expected OrganizationDto fields.

        Fields verified (camelCase):
            - organizationId  — primary key, always present
            - name            — [Required] in DTO, always present
        """
        org_id = self._get_first_org_id()

        if org_id is None:
            pytest.skip(
                "No organizations exist in the QA environment — "
                "cannot test GET /Organization/{id}/Details."
            )

        try:
            response = self.api.get(f"/Organization/{org_id}/Details")

            assert response.status_code == 200, (
                f"Expected 200 from GET /Organization/{org_id}/Details, "
                f"got {response.status_code}"
            )

            data = response.json()

            required_fields = ["organizationId", "name"]
            missing = [f for f in required_fields if f not in data]

            assert not missing, (
                f"GET /Organization/{org_id}/Details response is missing fields: {missing}. "
                f"Actual keys returned: {list(data.keys())}. "
                f"Remember: C# PascalCase DTO properties serialize to camelCase JSON keys."
            )

            logger.info(
                f"GET /Organization/{org_id}/Details required field check passed. "
                f"All fields present: {list(data.keys())}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_get_detail_has_required_fields: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    @pytest.mark.edge_case
    def test_get_detail_returns_400_for_nonexistent_id(self):
        """
        GET /Organization/{id}/Details returns 400 for a nonexistent (but valid) GUID.

        Note: This API returns 400 BadRequest with "not found" as the body —
        not a 404 Not Found. This is consistent across all controllers and should
        be treated as the expected behavior, not a bug.
        """
        fake_id = str(uuid.uuid4())

        try:
            response = self.api.get(f"/Organization/{fake_id}/Details")

            assert response.status_code == 400, (
                f"Expected 400 from GET /Organization/{fake_id}/Details (nonexistent ID). "
                f"Got {response.status_code}. "
                f"Note: This API uses 400 BadRequest (not 404) for not-found conditions."
            )

            logger.info(
                f"GET /Organization/{fake_id}/Details correctly returned 400 for "
                f"a nonexistent org ID."
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

class TestAPIOrganizationsCRUD:
    """
    CRUD tests for the Organization write endpoints.

    Each test that creates an org tracks the ID in _created_org_ids.
    teardown_method deletes all tracked orgs after each test, so failures
    in one test don't leave orphaned AUTOTEST data behind.

    All test org names use the AUTOTEST_ORG_ prefix so the session-level
    conftest cleanup will also catch any records that teardown_method misses.

    Covers:
        - PUT /Organization/Create  (create — uses PUT, not POST)
        - POST /Organization/Update (update — uses POST, not PUT)
        - DELETE /Organization/Delete?id=  (delete)
    """

    def setup_method(self):
        """Initialize APIBase and the created-org tracking list."""
        self.api = APIBase()
        self._created_org_ids = []

    def teardown_method(self):
        """Delete all AUTOTEST orgs created during this test."""
        for org_id in self._created_org_ids:
            try:
                self.api.delete("/Organization/Delete", params={"id": org_id})
                logger.debug(f"Teardown: deleted org {org_id}")
            except Exception as e:
                logger.warning(f"Teardown: failed to delete org {org_id}: {e}")
        self._created_org_ids.clear()

    def _create_org_and_get_id(self, name: str) -> str | None:
        """
        Create an organization via PUT /Organization/Create and return its ID.

        Because Create returns an empty 200 body, the ID is retrieved by
        searching for the org by its exact name immediately after creation.

        Args:
            name: The organization name. Must be 50 chars or fewer (VARCHAR(50)).

        Returns:
            str: The organizationId GUID if found, or None if creation or
                 lookup failed.
        """
        create_response = self.api.put("/Organization/Create", body={"name": name})

        if create_response.status_code != 200:
            logger.error(
                f"PUT /Organization/Create failed with {create_response.status_code} "
                f"for name='{name}'"
            )
            return None

        # Create returns an empty body — search to get the ID
        search_response = self.api.get(
            "/Organization/search",
            params={"name": name, "pageNumber": 1, "pageSize": 10}
        )

        if search_response.status_code != 200:
            logger.error(
                f"Search after create failed with {search_response.status_code} "
                f"for name='{name}'"
            )
            return None

        results = search_response.json().get("results", [])
        for org in results:
            if org.get("name") == name:
                org_id = str(org.get("organizationId"))
                self._created_org_ids.append(org_id)
                logger.debug(f"Created org '{name}' with ID {org_id}")
                return org_id

        logger.error(f"Created org '{name}' but could not find it in search results.")
        return None

    # -------------------------------------------------------------------------
    # Create
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.organizations
    def test_create_organization_returns_200(self):
        """
        PUT /Organization/Create with a valid payload returns 200.

        Uses an AUTOTEST_ prefixed name so the org is cleaned up by teardown
        and by the session-level conftest cleanup.

        Note: Create uses PUT (not POST) — see APIBase.put() for why.
        """
        name = _make_autotest_org_name()

        try:
            response = self.api.put("/Organization/Create", body={"name": name})

            assert response.status_code == 200, (
                f"Expected 200 from PUT /Organization/Create, got {response.status_code}. "
                f"Response body: {response.text}"
            )

            # Register for cleanup — search to get the ID
            search_response = self.api.get(
                "/Organization/search",
                params={"name": name, "pageNumber": 1, "pageSize": 10}
            )
            if search_response.status_code == 200:
                for org in search_response.json().get("results", []):
                    if org.get("name") == name:
                        self._created_org_ids.append(str(org["organizationId"]))
                        break

            logger.info(f"PUT /Organization/Create returned 200 for name='{name}'.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_create_organization_returns_200: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    def test_created_organization_appears_in_search(self):
        """
        A newly created org can be found via GET /Organization/search immediately
        after creation.

        This verifies that Create is durable (not eventually consistent) and that
        the search endpoint reflects the current database state.
        """
        name = _make_autotest_org_name()

        try:
            org_id = self._create_org_and_get_id(name)

            assert org_id is not None, (
                f"Could not create org with name='{name}' or could not retrieve its ID. "
                f"Check that PUT /Organization/Create is working and that search returns "
                f"newly created records."
            )

            # Verify it appears in a fresh search
            search_response = self.api.get(
                "/Organization/search",
                params={"name": name, "pageNumber": 1, "pageSize": 10}
            )

            assert search_response.status_code == 200, (
                f"Search after create failed with {search_response.status_code}"
            )

            results = search_response.json().get("results", [])
            found_names = [org.get("name") for org in results]

            assert name in found_names, (
                f"Newly created org '{name}' not found in search results. "
                f"Results returned: {found_names}"
            )

            logger.info(
                f"Newly created org '{name}' (ID {org_id}) found in search results."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_created_organization_appears_in_search: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    @pytest.mark.edge_case
    def test_create_organization_missing_name_returns_400(self):
        """
        PUT /Organization/Create without a name returns 400.

        OrganizationDto has [Required] on the Name field — the server should
        reject the request with a validation error.
        """
        try:
            response = self.api.put("/Organization/Create", body={})

            assert response.status_code == 400, (
                f"Expected 400 from PUT /Organization/Create with empty body, "
                f"got {response.status_code}. "
                f"The [Required] attribute on OrganizationDto.Name should reject this."
            )

            logger.info(
                f"PUT /Organization/Create with missing name correctly returned 400."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_create_organization_missing_name_returns_400: {e}"
            )
            raise

    # -------------------------------------------------------------------------
    # Update
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.organizations
    def test_update_organization_name_returns_200(self):
        """
        POST /Organization/Update with a valid payload returns 200 and the
        change is reflected in GET /Organization/{id}/Details.

        Note: Update uses POST (not PUT) — see APIBase.post() for why.
        """
        original_name = _make_autotest_org_name()
        updated_name = _make_autotest_org_name()

        try:
            org_id = self._create_org_and_get_id(original_name)

            assert org_id is not None, (
                f"Setup failed: could not create org '{original_name}'"
            )

            # Update the name
            update_response = self.api.post(
                "/Organization/Update",
                body={"organizationId": org_id, "name": updated_name}
            )

            assert update_response.status_code == 200, (
                f"Expected 200 from POST /Organization/Update, "
                f"got {update_response.status_code}. "
                f"Response: {update_response.text}"
            )

            # Verify the change persisted
            detail_response = self.api.get(f"/Organization/{org_id}/Details")

            assert detail_response.status_code == 200, (
                f"Expected 200 from GET /Organization/{org_id}/Details after update, "
                f"got {detail_response.status_code}"
            )

            detail_data = detail_response.json()
            actual_name = detail_data.get("name")

            assert actual_name == updated_name, (
                f"Name was not updated. Expected '{updated_name}', got '{actual_name}'."
            )

            logger.info(
                f"POST /Organization/Update: name changed from '{original_name}' "
                f"to '{updated_name}' — confirmed via /Details."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_update_organization_name_returns_200: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    @pytest.mark.edge_case
    def test_update_organization_missing_id_returns_400(self):
        """
        POST /Organization/Update without an organizationId returns 400.

        The Update action checks `if (!model.OrganizationId.HasValue)` and returns
        BadRequest("Id is required") when the ID is absent.
        """
        try:
            response = self.api.post(
                "/Organization/Update",
                body={"name": "UpdateWithoutId"}
            )

            assert response.status_code == 400, (
                f"Expected 400 from POST /Organization/Update with missing organizationId, "
                f"got {response.status_code}."
            )

            logger.info(
                f"POST /Organization/Update with missing ID correctly returned 400."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_update_organization_missing_id_returns_400: {e}"
            )
            raise

    # -------------------------------------------------------------------------
    # Delete
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.organizations
    def test_delete_organization_returns_200(self):
        """
        DELETE /Organization/Delete?id={guid} returns 200 and the org no longer
        appears in search results.

        Creates a test org, deletes it, then confirms it is gone.
        The org ID is removed from _created_org_ids after successful deletion so
        teardown_method does not attempt to double-delete.
        """
        name = _make_autotest_org_name()

        try:
            org_id = self._create_org_and_get_id(name)

            assert org_id is not None, (
                f"Setup failed: could not create org '{name}'"
            )

            # Delete
            delete_response = self.api.delete(
                "/Organization/Delete",
                params={"id": org_id}
            )

            assert delete_response.status_code == 200, (
                f"Expected 200 from DELETE /Organization/Delete?id={org_id}, "
                f"got {delete_response.status_code}. "
                f"Response: {delete_response.text}"
            )

            # Remove from tracking so teardown doesn't double-delete
            if org_id in self._created_org_ids:
                self._created_org_ids.remove(org_id)

            # Verify it no longer appears in search
            search_response = self.api.get(
                "/Organization/search",
                params={"name": name, "pageNumber": 1, "pageSize": 10}
            )

            if search_response.status_code == 200:
                results = search_response.json().get("results", [])
                found_names = [org.get("name") for org in results]

                assert name not in found_names, (
                    f"Deleted org '{name}' still appears in search results: {found_names}"
                )

            logger.info(
                f"DELETE /Organization/Delete?id={org_id}: org deleted and "
                f"confirmed absent from search."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_delete_organization_returns_200: {e}"
            )
            raise

    @pytest.mark.api
    @pytest.mark.organizations
    @pytest.mark.edge_case
    def test_delete_nonexistent_organization_returns_400(self):
        """
        DELETE /Organization/Delete?id={guid} returns 400 for a nonexistent GUID.

        Note: This API returns 400 BadRequest (not 404) for not-found deletions.
        Consistent with other controllers in this API.
        """
        fake_id = str(uuid.uuid4())

        try:
            response = self.api.delete(
                "/Organization/Delete",
                params={"id": fake_id}
            )

            assert response.status_code == 400, (
                f"Expected 400 from DELETE /Organization/Delete?id={fake_id} (nonexistent). "
                f"Got {response.status_code}. "
                f"Note: This API uses 400 (not 404) for not-found conditions."
            )

            logger.info(
                f"DELETE /Organization/Delete with nonexistent ID correctly returned 400."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_delete_nonexistent_organization_returns_400: {e}"
            )
            raise
