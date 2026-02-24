# test_api_authorization.py
# Tests for authentication and authorization enforcement across the WildXR API.
#
# AUTHORIZATION MODEL (see reference/wildxr.api/ for source):
#
#   - All controllers (except /Users/Authenticate) are decorated with [Authorize]
#     at the class level. A missing or invalid JWT token → 401 Unauthorized before
#     any controller logic runs.
#
#   - Inside controller actions, a JwtMiddleware attaches the authenticated UserDto
#     to HttpContext.Items["User"]. Role checks use two flags:
#       IsSystemAdmin  — sees all data, bypasses all org filters
#       IsHeadsetAdmin — for headset-specific operations (not tested here)
#
#   - Organization filtering is handled by AuthorizationManager.CanAccessResource()
#     using the OrganizationAction resource type. Non-system-admins only see data
#     whose organizationId matches one of their own org IDs, OR equals the
#     "AlwaysAccessibleId" magic UUID (the WildXR internal org visible to all).
#
#   - Unauthorized resource access (valid token, wrong org) returns 403 Forbidden
#     (Forbid()) not 404 or 400.
#
# REQUIRED ENV VARS:
#   ORG_ADMIN_BP_USERNAME / ORG_ADMIN_BP_PASSWORD   — Butterfly Pavilion org admin
#   ORG_ADMIN_DTA_USERNAME / ORG_ADMIN_DTA_PASSWORD — Downtown Aquarium org admin
#
#   If any of these vars are absent, TestAPIOrgAdminIsolation is skipped entirely.
#
# KEY CONSTANTS:
#   ALWAYS_ACCESSIBLE_ORG_ID — Resources tagged with this org ID (B1DF7F5A-...)
#   are visible to ALL authenticated users regardless of their own org.
#   This is the WildXR internal org defined in AuthorizationManager.cs.

import os
import uuid
import pytest
from .api_base import APIBase
from utilities.auth import get_token_for_user
from utilities.utils import logger

# ---------------------------------------------------------------------------
# The WildXR internal "always accessible" organization UUID.
# Defined as AuthorizationManager.AlwaysAccessibleId in the reference codebase.
# Resources tagged with this org are visible to all authenticated users.
# ---------------------------------------------------------------------------
ALWAYS_ACCESSIBLE_ORG_ID = "B1DF7F5A-5ED7-4AE9-97DC-E78B9137A0B3"

# ---------------------------------------------------------------------------
# Org-admin credentials (from .env — not hard-coded here)
# ---------------------------------------------------------------------------
ORG_ADMIN_BP_USERNAME = os.getenv("ORG_ADMIN_BP_USERNAME")
ORG_ADMIN_BP_PASSWORD = os.getenv("ORG_ADMIN_BP_PASSWORD")
ORG_ADMIN_DTA_USERNAME = os.getenv("ORG_ADMIN_DTA_USERNAME")
ORG_ADMIN_DTA_PASSWORD = os.getenv("ORG_ADMIN_DTA_PASSWORD")


# ---------------------------------------------------------------------------
# Class 1: Unauthenticated requests — missing or invalid token → 401
# ---------------------------------------------------------------------------

class TestAPIUnauthenticated:
    """
    Verify that all protected endpoints reject requests with no token or an
    invalid token, returning HTTP 401 Unauthorized.

    Uses auth_type='none' (no Authorization header at all) and auth_type='invalid'
    (a garbage string instead of a real JWT) — both are supported by
    APIBase.get_headers(). No test data is created or modified.

    Why 401 and not 403?
    The [Authorize] attribute on the controller class causes ASP.NET to reject
    the request at the middleware layer — before any controller action runs.
    The framework returns 401 for missing/invalid credentials. 403 is reserved
    for cases where the token IS valid but the user lacks permission for the
    specific resource.
    """

    def setup_method(self):
        """Initialize APIBase for each test method."""
        self.api = APIBase()

    @pytest.mark.api
    @pytest.mark.security
    @pytest.mark.parametrize("endpoint,params", [
        ("/Organization", {"pageNumber": 1, "pageSize": 10}),
        ("/Installations", {"pageNumber": 1, "pageSize": 10}),
        ("/Videos", {"pageNumber": 1, "pageSize": 10}),
        ("/Device", {"pageNumber": 1, "pageSize": 10}),
        ("/MapMarker", {"pageNumber": 1, "pageSize": 10}),
        ("/Users", {"pageNumber": 1, "pageSize": 10}),
    ])
    def test_get_without_token_returns_401(self, endpoint, params):
        """
        GET request to a protected list endpoint without an Authorization header
        returns 401 Unauthorized.

        All main resource controllers are decorated with [Authorize] at the class
        level. A missing Authorization header means the JWT middleware never
        attaches a UserDto to the request — the framework rejects the request
        entirely before any controller logic runs.
        """
        try:
            response = self.api.get(endpoint, auth_type='none', params=params)

            assert response.status_code == 401, (
                f"Expected 401 from GET {endpoint} with no Authorization header. "
                f"Got {response.status_code}. "
                f"This endpoint may be missing the [Authorize] attribute."
            )

            logger.info(f"GET {endpoint} with no token correctly returned 401.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.security
    def test_write_without_token_returns_401(self):
        """
        PUT /Organization/Create without an Authorization header returns 401.

        Verifies that write (create) endpoints are also protected — not just
        read endpoints. The [Authorize] attribute is at the class level so ALL
        endpoints in the controller require authentication.
        """
        try:
            response = self.api.put(
                "/Organization/Create",
                auth_type='none',
                body={"name": "AUTOTEST_NOAUTH_SHOULD_NOT_CREATE"}
            )

            assert response.status_code == 401, (
                f"Expected 401 from PUT /Organization/Create with no token. "
                f"Got {response.status_code}. "
                f"Write endpoints must be protected by [Authorize]."
            )

            logger.info("PUT /Organization/Create with no token correctly returned 401.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.security
    def test_delete_without_token_returns_401(self):
        """
        DELETE /Organization/Delete without an Authorization header returns 401.

        Uses a fake GUID — the request should be rejected at the authentication
        layer before any database lookup occurs, so no data is affected.
        """
        fake_id = str(uuid.uuid4())

        try:
            response = self.api.delete(
                "/Organization/Delete",
                auth_type='none',
                params={"id": fake_id}
            )

            assert response.status_code == 401, (
                f"Expected 401 from DELETE /Organization/Delete with no token. "
                f"Got {response.status_code}."
            )

            logger.info("DELETE /Organization/Delete with no token correctly returned 401.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.security
    def test_invalid_token_returns_401(self):
        """
        A request with a malformed (non-JWT garbage string) Authorization token
        returns 401 Unauthorized.

        APIBase sends "Bearer invalid_token" when auth_type='invalid'. The
        JwtMiddleware in the API validates the token signature and rejects it
        if it cannot be parsed as a valid JWT — the request never reaches any
        controller logic.
        """
        try:
            response = self.api.get(
                "/Organization",
                auth_type='invalid',
                params={"pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 401, (
                f"Expected 401 from GET /Organization with invalid token. "
                f"Got {response.status_code}."
            )

            logger.info("GET /Organization with invalid token correctly returned 401.")

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise


# ---------------------------------------------------------------------------
# Class 2: Org-admin data isolation
# ---------------------------------------------------------------------------

# Module-level flag used by pytest.mark.skipif so the skip happens at
# collection time when credentials are absent (before setup_class runs).
_ORG_ADMIN_CREDS_PRESENT = all([
    ORG_ADMIN_BP_USERNAME,
    ORG_ADMIN_BP_PASSWORD,
    ORG_ADMIN_DTA_USERNAME,
    ORG_ADMIN_DTA_PASSWORD,
])

_ORG_SKIP_REASON = (
    "Org-admin credentials not configured in environment. "
    "Set ORG_ADMIN_BP_USERNAME, ORG_ADMIN_BP_PASSWORD, "
    "ORG_ADMIN_DTA_USERNAME, ORG_ADMIN_DTA_PASSWORD in .env."
)


@pytest.mark.skipif(not _ORG_ADMIN_CREDS_PRESENT, reason=_ORG_SKIP_REASON)
class TestAPIOrgAdminIsolation:
    """
    Verify that org-admin accounts only see their own organization's data,
    and that the system admin (IsSystemAdmin=true) sees all data.

    Uses two QA org-admin accounts:
        Butterfly Pavilion (BP):   QAOrgBPADMIN
        Downtown Aquarium (DTA):   QAOrgDTAADMIN

    Each account belongs to exactly one organization. The tests verify:
      1. Each org admin can successfully query their own data (sanity).
      2. Each org admin's /Organization/search results exclude the other org.
      3. Each org admin is denied access (403) to the other org's /Details.
      4. The system admin sees both orgs in /Organization/search (bypass proof).
      5. The system admin sees more total orgs than any single org admin (filter proof).
      6. Both org admins can access the /Installations/search endpoint.
      7. The system admin sees at least as many installations as either org admin.
      8. Both org admins can access the /Videos endpoint.

    Org IDs are discovered dynamically by each org admin's own search results —
    no hardcoded QA environment data.
    """

    @classmethod
    def setup_class(cls):
        """
        Initialize API instances and discover org IDs for BP and DTA.

        setup_class runs once before all tests in this class. Acquiring tokens
        here (rather than in setup_method) avoids making 3 auth network calls
        per test.
        """
        # System admin — uses the default shared token from SYS_ADMIN credentials
        cls.sysadmin_api = APIBase()

        # Butterfly Pavilion org admin
        bp_token = get_token_for_user(ORG_ADMIN_BP_USERNAME, ORG_ADMIN_BP_PASSWORD)
        cls.bp_api = APIBase(token=bp_token)

        # Downtown Aquarium org admin
        dta_token = get_token_for_user(ORG_ADMIN_DTA_USERNAME, ORG_ADMIN_DTA_PASSWORD)
        cls.dta_api = APIBase(token=dta_token)

        # Discover each org's ID from that org admin's own search results.
        # Org admins only see their own org(s), so the first result IS their org.
        cls.bp_org_id = cls._discover_own_org_id(cls.bp_api, "BP")
        cls.dta_org_id = cls._discover_own_org_id(cls.dta_api, "DTA")

        logger.info(
            f"TestAPIOrgAdminIsolation setup complete. "
            f"bp_org_id={cls.bp_org_id}, dta_org_id={cls.dta_org_id}"
        )

    @staticmethod
    def _discover_own_org_id(api: APIBase, label: str) -> str | None:
        """
        Fetch the organization ID for the org admin logged in via the given api.

        Org admins only see their own org(s) in /Organization/search results.
        Calling search with a blank name filter and pageSize=10 returns all orgs
        visible to that admin — which should be exactly 1 for a single-org admin.

        Args:
            api:   An APIBase instance authenticated as an org admin.
            label: Short label for the org (e.g. "BP", "DTA") used in log messages.

        Returns:
            str: The organizationId GUID of the first org returned, or None if
                 discovery fails.
        """
        response = api.get(
            "/Organization/search",
            params={"name": "", "pageNumber": 1, "pageSize": 10}
        )

        if response.status_code != 200:
            logger.error(
                f"{label} org ID discovery failed — /Organization/search "
                f"returned {response.status_code}"
            )
            return None

        results = response.json().get("results", [])

        if not results:
            logger.error(
                f"{label} org ID discovery failed — no orgs returned in search. "
                f"The org-admin account may not belong to any organization."
            )
            return None

        org_id = str(results[0].get("organizationId"))
        org_name = results[0].get("name", "<unknown>")
        logger.debug(f"{label} discovered org: '{org_name}' (ID: {org_id})")
        return org_id

    # -------------------------------------------------------------------------
    # Sanity: each org admin can query their own organization data
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.security
    def test_bp_admin_can_search_organizations(self):
        """
        BP org admin's GET /Organization/search returns 200 with at least 1 result.

        Confirms the BP token is valid and the account has OrganizationAction
        access needed to call the search endpoint.
        """
        try:
            response = self.bp_api.get(
                "/Organization/search",
                params={"name": "", "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 from BP admin GET /Organization/search. "
                f"Got {response.status_code}."
            )

            results = response.json().get("results", [])

            assert len(results) >= 1, (
                "BP org admin's /Organization/search returned 0 results. "
                "The account should belong to at least one organization."
            )

            logger.info(
                f"BP admin /Organization/search returned {len(results)} org(s): "
                f"{[r.get('name') for r in results]}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.security
    def test_dta_admin_can_search_organizations(self):
        """
        DTA org admin's GET /Organization/search returns 200 with at least 1 result.

        Parallel sanity check to test_bp_admin_can_search_organizations.
        """
        try:
            response = self.dta_api.get(
                "/Organization/search",
                params={"name": "", "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 from DTA admin GET /Organization/search. "
                f"Got {response.status_code}."
            )

            results = response.json().get("results", [])

            assert len(results) >= 1, (
                "DTA org admin's /Organization/search returned 0 results. "
                "The account should belong to at least one organization."
            )

            logger.info(
                f"DTA admin /Organization/search returned {len(results)} org(s): "
                f"{[r.get('name') for r in results]}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    # -------------------------------------------------------------------------
    # Data isolation: org admin search excludes the other org
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.security
    def test_bp_admin_search_excludes_dta_org(self):
        """
        BP org admin's /Organization/search results do NOT include Downtown Aquarium.

        The OrganizationController.Search() filters results by the requesting
        user's organization IDs when IsSystemAdmin is false. BP admin does not
        belong to Downtown Aquarium, so DTA's org ID must not appear.
        """
        if self.dta_org_id is None:
            pytest.skip("DTA org ID could not be discovered — skipping isolation check.")

        try:
            response = self.bp_api.get(
                "/Organization/search",
                params={"name": "", "pageNumber": 1, "pageSize": 50}
            )

            assert response.status_code == 200, (
                f"Expected 200 from BP admin /Organization/search. "
                f"Got {response.status_code}."
            )

            results = response.json().get("results", [])
            returned_ids = [str(r.get("organizationId")) for r in results]

            assert self.dta_org_id.upper() not in [i.upper() for i in returned_ids], (
                f"BP org admin's search returned DTA org ID ({self.dta_org_id}). "
                f"An org admin should only see their own organization(s). "
                f"Returned org IDs: {returned_ids}"
            )

            logger.info(
                f"BP admin search correctly excluded DTA org ({self.dta_org_id}). "
                f"Returned IDs: {returned_ids}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.security
    def test_dta_admin_search_excludes_bp_org(self):
        """
        DTA org admin's /Organization/search results do NOT include Butterfly Pavilion.

        Parallel check to test_bp_admin_search_excludes_dta_org.
        """
        if self.bp_org_id is None:
            pytest.skip("BP org ID could not be discovered — skipping isolation check.")

        try:
            response = self.dta_api.get(
                "/Organization/search",
                params={"name": "", "pageNumber": 1, "pageSize": 50}
            )

            assert response.status_code == 200, (
                f"Expected 200 from DTA admin /Organization/search. "
                f"Got {response.status_code}."
            )

            results = response.json().get("results", [])
            returned_ids = [str(r.get("organizationId")) for r in results]

            assert self.bp_org_id.upper() not in [i.upper() for i in returned_ids], (
                f"DTA org admin's search returned BP org ID ({self.bp_org_id}). "
                f"An org admin should only see their own organization(s). "
                f"Returned org IDs: {returned_ids}"
            )

            logger.info(
                f"DTA admin search correctly excluded BP org ({self.bp_org_id}). "
                f"Returned IDs: {returned_ids}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    # -------------------------------------------------------------------------
    # Cross-org access: org admin cannot access another org's /Details → 403
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.security
    def test_bp_admin_cannot_access_dta_org_details(self):
        """
        BP org admin trying to GET /Organization/{dta_id}/Details returns 403 Forbidden.

        OrganizationController.Details() checks:
            if (!requestingUser.IsSystemAdmin && !orgIds.Contains(id)) return Forbid();

        BP admin does not belong to Downtown Aquarium → the controller returns
        403 (not 404 — the org exists, the user just cannot access it).
        """
        if self.dta_org_id is None:
            pytest.skip("DTA org ID could not be discovered — skipping cross-org access test.")

        try:
            response = self.bp_api.get(f"/Organization/{self.dta_org_id}/Details")

            assert response.status_code == 403, (
                f"Expected 403 from BP admin GET /Organization/{self.dta_org_id}/Details "
                f"(Downtown Aquarium's org ID). Got {response.status_code}. "
                f"An org admin should not be able to access another organization's details."
            )

            logger.info(
                f"BP admin correctly received 403 for DTA org /Details "
                f"(org ID: {self.dta_org_id})."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.security
    def test_dta_admin_cannot_access_bp_org_details(self):
        """
        DTA org admin trying to GET /Organization/{bp_id}/Details returns 403 Forbidden.

        Parallel check to test_bp_admin_cannot_access_dta_org_details.
        """
        if self.bp_org_id is None:
            pytest.skip("BP org ID could not be discovered — skipping cross-org access test.")

        try:
            response = self.dta_api.get(f"/Organization/{self.bp_org_id}/Details")

            assert response.status_code == 403, (
                f"Expected 403 from DTA admin GET /Organization/{self.bp_org_id}/Details "
                f"(Butterfly Pavilion's org ID). Got {response.status_code}. "
                f"An org admin should not be able to access another organization's details."
            )

            logger.info(
                f"DTA admin correctly received 403 for BP org /Details "
                f"(org ID: {self.bp_org_id})."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    # -------------------------------------------------------------------------
    # System admin bypass: sysadmin sees all orgs in search
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.security
    def test_sysadmin_search_returns_both_bp_and_dta_orgs(self):
        """
        System admin's /Organization/search results include BOTH Butterfly Pavilion
        and Downtown Aquarium.

        The OrganizationController.Search() skips org filtering entirely when
        IsSystemAdmin is true. This verifies the bypass is working correctly —
        neither org is hidden from the system admin.
        """
        if self.bp_org_id is None or self.dta_org_id is None:
            pytest.skip("Could not discover one or both org IDs — skipping sysadmin check.")

        try:
            response = self.sysadmin_api.get(
                "/Organization/search",
                params={"name": "", "pageNumber": 1, "pageSize": 100}
            )

            assert response.status_code == 200, (
                f"Expected 200 from sysadmin /Organization/search. "
                f"Got {response.status_code}."
            )

            results = response.json().get("results", [])
            returned_ids = [str(r.get("organizationId")).upper() for r in results]

            assert self.bp_org_id.upper() in returned_ids, (
                f"System admin /Organization/search did not return BP org "
                f"(ID: {self.bp_org_id}). "
                f"System admin should see all organizations. "
                f"Returned IDs: {returned_ids}"
            )

            assert self.dta_org_id.upper() in returned_ids, (
                f"System admin /Organization/search did not return DTA org "
                f"(ID: {self.dta_org_id}). "
                f"System admin should see all organizations. "
                f"Returned IDs: {returned_ids}"
            )

            logger.info(
                f"System admin search returned both BP and DTA orgs. "
                f"Total orgs visible to sysadmin: {len(returned_ids)}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.security
    def test_sysadmin_sees_more_orgs_than_bp_admin(self):
        """
        System admin's /Organization/search totalCount is greater than BP admin's.

        This is a second proof of filtering: the sysadmin count being higher
        confirms that filtering is actively hiding records from the org admin,
        not just that the QA environment happens to have one org.

        If this test fails with "only N org(s) visible to sysadmin", the QA
        environment has a single org — the test cannot prove filtering and is
        skipped rather than failed.
        """
        try:
            sysadmin_response = self.sysadmin_api.get(
                "/Organization/search",
                params={"name": "", "pageNumber": 1, "pageSize": 100}
            )
            bp_response = self.bp_api.get(
                "/Organization/search",
                params={"name": "", "pageNumber": 1, "pageSize": 100}
            )

            assert sysadmin_response.status_code == 200
            assert bp_response.status_code == 200

            sysadmin_total = sysadmin_response.json().get("totalCount", 0)
            bp_total = bp_response.json().get("totalCount", 0)

            if sysadmin_total <= 1:
                pytest.skip(
                    f"Only {sysadmin_total} org(s) visible to sysadmin — cannot "
                    f"prove org filtering in a single-org environment."
                )

            assert sysadmin_total > bp_total, (
                f"Expected sysadmin to see more orgs than BP admin. "
                f"Sysadmin sees {sysadmin_total}, BP admin sees {bp_total}. "
                f"Either org filtering is not working, or all orgs in the QA "
                f"environment belong to BP's organization."
            )

            logger.info(
                f"Org count comparison: sysadmin={sysadmin_total}, BP admin={bp_total}. "
                f"Filtering confirmed."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    # -------------------------------------------------------------------------
    # Installation search: org admins can access their own data
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.security
    def test_bp_admin_can_search_installations(self):
        """
        BP org admin's GET /Installations/search returns 200.

        The InstallationsController.Search() requires OrganizationAction access.
        Non-admin users see installations from their own org(s) plus the
        AlwaysAccessibleId org. This test confirms the BP admin has access.
        """
        try:
            response = self.bp_api.get(
                "/Installations/search",
                params={"name": "", "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 from BP admin GET /Installations/search. "
                f"Got {response.status_code}."
            )

            logger.info(
                f"BP admin GET /Installations/search returned 200. "
                f"totalCount: {response.json().get('totalCount')}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.security
    def test_dta_admin_can_search_installations(self):
        """
        DTA org admin's GET /Installations/search returns 200.

        Parallel check to test_bp_admin_can_search_installations.
        """
        try:
            response = self.dta_api.get(
                "/Installations/search",
                params={"name": "", "pageNumber": 1, "pageSize": 10}
            )

            assert response.status_code == 200, (
                f"Expected 200 from DTA admin GET /Installations/search. "
                f"Got {response.status_code}."
            )

            logger.info(
                f"DTA admin GET /Installations/search returned 200. "
                f"totalCount: {response.json().get('totalCount')}"
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    @pytest.mark.api
    @pytest.mark.security
    def test_sysadmin_sees_at_least_as_many_installations_as_org_admins(self):
        """
        System admin's /Installations/search totalCount is ≥ both org admins' counts.

        The InstallationsController.Search() skips org filtering for system admins.
        A lower sysadmin count would indicate the bypass is broken.

        Note: sysadmin could equal org admin if all QA installations happen to
        belong to the same org — the assertion is ≥, not strictly >.
        """
        try:
            sysadmin_response = self.sysadmin_api.get(
                "/Installations/search",
                params={"name": "", "pageNumber": 1, "pageSize": 10}
            )
            bp_response = self.bp_api.get(
                "/Installations/search",
                params={"name": "", "pageNumber": 1, "pageSize": 10}
            )
            dta_response = self.dta_api.get(
                "/Installations/search",
                params={"name": "", "pageNumber": 1, "pageSize": 10}
            )

            assert sysadmin_response.status_code == 200
            assert bp_response.status_code == 200
            assert dta_response.status_code == 200

            sysadmin_total = sysadmin_response.json().get("totalCount", 0)
            bp_total = bp_response.json().get("totalCount", 0)
            dta_total = dta_response.json().get("totalCount", 0)

            assert sysadmin_total >= bp_total, (
                f"System admin sees {sysadmin_total} installations but BP admin sees "
                f"{bp_total}. Sysadmin should always see ≥ what any org admin sees."
            )

            assert sysadmin_total >= dta_total, (
                f"System admin sees {sysadmin_total} installations but DTA admin sees "
                f"{dta_total}. Sysadmin should always see ≥ what any org admin sees."
            )

            logger.info(
                f"Installations totalCount: sysadmin={sysadmin_total}, "
                f"BP={bp_total}, DTA={dta_total}."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise

    # -------------------------------------------------------------------------
    # Videos: org admins can access the videos endpoint
    # -------------------------------------------------------------------------

    @pytest.mark.api
    @pytest.mark.security
    def test_org_admins_can_access_videos_endpoint(self):
        """
        Both BP and DTA org admins can call GET /Videos and receive 200.

        GET /Videos (the basic list endpoint) is protected by [Authorize] but
        does not apply org filtering — all authenticated users see all videos.
        This test confirms the org-admin token is accepted by the Videos controller.

        Note: org-filtered video access is via GET /Videos/search (which filters
        by org). That endpoint is tested separately if its query params are known.
        """
        try:
            bp_response = self.bp_api.get(
                "/Videos",
                params={"pageNumber": 1, "pageSize": 10}
            )
            dta_response = self.dta_api.get(
                "/Videos",
                params={"pageNumber": 1, "pageSize": 10}
            )

            assert bp_response.status_code == 200, (
                f"Expected 200 from BP admin GET /Videos. "
                f"Got {bp_response.status_code}."
            )

            assert dta_response.status_code == 200, (
                f"Expected 200 from DTA admin GET /Videos. "
                f"Got {dta_response.status_code}."
            )

            bp_total = bp_response.json().get("totalCount", 0)
            dta_total = dta_response.json().get("totalCount", 0)

            logger.info(
                f"Both org admins can access GET /Videos. "
                f"BP totalCount={bp_total}, DTA totalCount={dta_total}."
            )

        except AssertionError as e:
            logger.error(f"Assertion failed: {e}")
            raise
