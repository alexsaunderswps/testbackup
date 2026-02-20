# test_api_panels.py
# Tests for the /api/Panels endpoints introduced in WILDXR-1864.
#
# SCOPE: Read-only (GET) happy path tests only.
#
# Create, Update, and UploadBackgroundImage tests are intentionally excluded
# because no DELETE endpoint exists for panels. Creating test records would
# leave permanent, non-removable data in the QA environment. Those tests will
# be added once a DELETE endpoint is available. See:
# AIsummaries/WILDXR-1864_PANELS_API_TEST_PLAN.md

import pytest
import requests
from .api_base import APIBase
from utilities.utils import logger


class TestAPIPanelsHappyPath:
    """
    Happy path tests for the GET /api/Panels endpoints.

    Covers:
        - GET /Panels?pageNumber=&pageSize= (paginated list)
        - GET /Panels/search?name=&pageNumber=&pageSize= (name search)
        - GET /Panels/{id}/details (single panel by ID)

    Panel IDs are discovered dynamically from the list endpoint rather than
    hardcoded, so these tests remain valid as QA data changes over time.
    """

    def setup_method(self):
        """Initialize APIBase for each test method."""
        self.api = APIBase()

    def _get_first_panel_id(self) -> str | None:
        """
        Fetch the first panel from the list endpoint and return its panelId.

        Used by detail tests to discover a valid panel ID without hardcoding
        QA environment data.

        Returns:
            str: The panelId of the first panel in the list, or None if the
                 list is empty or the request fails.
        """
        response = self.api.get("/Panels", params={"pageNumber": 1, "pageSize": 1})

        if response.status_code != 200:
            logger.error(
                f"Could not fetch panels list to discover a panel ID. "
                f"Status: {response.status_code}"
            )
            return None

        try:
            data = response.json()
            results = data.get("results", [])
            if not results:
                logger.warning("Panels list is empty — no panel ID available for details tests.")
                return None
            panel_id = results[0].get("panelId")
            logger.debug(f"Discovered panel ID for details tests: {panel_id}")
            return panel_id
        except (requests.exceptions.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing panels list response to get panel ID: {e}")
            return None

    # -------------------------------------------------------------------------
    # GET /Panels — paginated list
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.panels
    def test_get_panels_list_returns_200(self):
        """
        GET /Panels returns HTTP 200 with a valid JSON response body.

        This is the baseline connectivity check for the panels list endpoint.
        """
        try:
            response = self.api.get("/Panels", params={"pageNumber": 1, "pageSize": 10})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Panels, got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Panels response body is not valid JSON: {e}")
                raise

            assert isinstance(data, dict), (
                f"Expected response body to be a JSON object, got {type(data).__name__}"
            )

            logger.info("GET /Panels returned 200 with a valid JSON body.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_panels_list_returns_200: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.panels
    @pytest.mark.pagination
    def test_get_panels_list_has_pagination_envelope(self):
        """
        GET /Panels response body contains all required pagination fields.

        Verifies that the standard pagination envelope is present and that
        'results' is a list, not null or a non-list type.
        """
        try:
            response = self.api.get("/Panels", params={"pageNumber": 1, "pageSize": 10})

            assert response.status_code == 200, (
                f"Expected 200 from GET /Panels, got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Panels response body is not valid JSON: {e}")
                raise

            required_fields = ["page", "pageSize", "pageCount", "totalCount", "results"]
            missing = [f for f in required_fields if f not in data]

            assert not missing, (
                f"GET /Panels response is missing required pagination fields: {missing}. "
                f"Actual keys present: {list(data.keys())}"
            )

            assert isinstance(data["results"], list), (
                f"Expected 'results' to be a list, got {type(data['results']).__name__}"
            )

            logger.info("GET /Panels pagination envelope verified:")
            logger.info(
                f"  page={data['page']}, pageSize={data['pageSize']}, "
                f"pageCount={data['pageCount']}, totalCount={data['totalCount']}, "
                f"results count={len(data['results'])}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_panels_list_has_pagination_envelope: {e}")
            raise

    # -------------------------------------------------------------------------
    # GET /Panels/search — name search
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.panels
    @pytest.mark.search
    def test_get_panels_search_returns_200(self):
        """
        GET /Panels/search with a name param returns 200 with a results list.

        Uses a single-character query ('a') to maximize the chance of matching
        existing panel records without assuming specific names in QA.
        """
        try:
            response = self.api.get(
                "/Panels/search",
                params={"name": "a", "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 from GET /Panels/search, got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Panels/search response body is not valid JSON: {e}")
                raise

            assert isinstance(data, dict), (
                f"Expected response body to be a JSON object, got {type(data).__name__}"
            )

            assert "results" in data, (
                "GET /Panels/search response is missing the 'results' field"
            )

            assert isinstance(data["results"], list), (
                f"Expected 'results' to be a list, got {type(data['results']).__name__}"
            )

            logger.info(
                f"GET /Panels/search returned 200 with {len(data['results'])} result(s)."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_panels_search_returns_200: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.panels
    @pytest.mark.search
    def test_get_panels_search_no_match_returns_empty_not_404(self):
        """
        GET /Panels/search with a non-matching name returns 200 with an empty
        results list — not a 404.

        The API should treat "no results" as a successful search that found
        nothing, not as a missing resource. This test uses a name string
        deliberately designed to match no panel in any environment.
        """
        no_match_name = "ZZZZZ_WILDXR_TEST_NO_MATCH_ZZZZZ"

        try:
            response = self.api.get(
                "/Panels/search",
                params={"name": no_match_name, "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 (not 404) for a no-match search on GET /Panels/search. "
                f"Got {response.status_code}. The API should return an empty results "
                f"list, not a 404, when no panels match the search term."
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"GET /Panels/search response body is not valid JSON: {e}")
                raise

            results = data.get("results", [])

            assert isinstance(results, list), (
                f"Expected 'results' to be a list, got {type(results).__name__}"
            )

            assert len(results) == 0, (
                f"Expected 0 results for no-match search name='{no_match_name}', "
                f"got {len(results)}"
            )

            logger.info(
                f"GET /Panels/search with name='{no_match_name}' correctly returned "
                f"200 with an empty results list."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_get_panels_search_no_match_returns_empty_not_404: {e}"
            )
            raise

    # -------------------------------------------------------------------------
    # GET /Panels/{id}/details — single panel
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.panels
    def test_get_panel_details_returns_200(self):
        """
        GET /Panels/{id}/details returns 200 for a valid, pre-existing panel ID.

        The panel ID is discovered dynamically from the list endpoint. If no
        panels exist in the QA environment, this test is skipped rather than
        failed, since that is a data condition rather than a test failure.
        """
        panel_id = self._get_first_panel_id()

        if panel_id is None:
            pytest.skip(
                "No panels exist in the QA environment — "
                "cannot test GET /Panels/{id}/details."
            )

        try:
            response = self.api.get(f"/Panels/{panel_id}/details")

            assert response.status_code == 200, (
                f"Expected 200 from GET /Panels/{panel_id}/details, "
                f"got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"Response body is not valid JSON: {e}")
                raise

            assert isinstance(data, dict), (
                f"Expected response body to be a JSON object, got {type(data).__name__}"
            )

            logger.info(f"GET /Panels/{panel_id}/details returned 200 with a valid JSON body.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test_get_panel_details_returns_200: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.panels
    def test_get_panel_details_has_required_fields(self):
        """
        GET /Panels/{id}/details response contains the fields expected from
        a PanelDto. All JSON keys are camelCase — ASP.NET Core serializes
        PascalCase C# properties to camelCase automatically.

        Fields verified here are a subset chosen for their stable presence
        regardless of panel data values:
          - panelId          — primary key, always present
          - videoCatalogueId — has a SQL/C# default of "All Videos", always present
          - newFlag          — bool NOT NULL DEFAULT 0, always present
          - contents         — int?, present even when null (no NullValueHandling
                               attributes on this DTO, so nulls serialize explicitly)

        Note: name, description, backgroundImageUrl, and header are NOT checked
        here because the API has no server-side [Required] validation for those
        fields — only the UI enforces them as required. See WILDXR bug report
        for missing API-level validation on Panel Create/Update.
        """
        panel_id = self._get_first_panel_id()

        if panel_id is None:
            pytest.skip(
                "No panels exist in the QA environment — "
                "cannot test GET /Panels/{id}/details."
            )

        try:
            response = self.api.get(f"/Panels/{panel_id}/details")

            assert response.status_code == 200, (
                f"Expected 200 from GET /Panels/{panel_id}/details, "
                f"got {response.status_code}"
            )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"Response body is not valid JSON: {e}")
                raise

            always_present_fields = [
                "panelId",
                "videoCatalogueId",
                "newFlag",
                "contents",
            ]

            missing = [f for f in always_present_fields if f not in data]

            assert not missing, (
                f"GET /Panels/{panel_id}/details response is missing expected fields: {missing}. "
                f"Actual keys returned: {list(data.keys())}. "
                f"Check DTO field names and casing against the actual API response."
            )

            logger.info(f"GET /Panels/{panel_id}/details required field check passed.")
            logger.info(f"All fields present in response: {list(data.keys())}")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in test_get_panel_details_has_required_fields: {e}"
            )
            raise
