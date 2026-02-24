# WildXR.test — Gap Analysis & Testing Todo List

Generated: 2026-02-19

## How to Read This List

Items are grouped by area and roughly ordered by priority within each section. "High" = fundamental coverage gaps; "Medium" = important but not blocking; "Low" = nice-to-have or edge cases.

---

## 1. Missing Page Objects (Prerequisites for UI/Functional Tests)

These pages exist in the frontend but have zero page object coverage. Nothing else below can move forward for these areas without them.

- [x] ~~**Create `PanelsPage` page object** — `panels/` component has `ManagePanelsPage`, `AddEditPanel`, `PanelsList`; no page object or tests exist~~ ✅ Completed 2026-02-20: `page_objects/admin_menu/panels_page.py` created (WILDXR-1870)
- [x] ~~**Create `PanelCollectionsPage` page object** — `panelCollections/` has `ManagePanelCollectionsPage`, `AddEditPanelCollection`; no page object or tests exist~~ ✅ Completed 2026-02-20: `page_objects/admin_menu/panel_collections_page.py` created (404 lines; list page, Add/Edit form, verification methods, action methods)

> **Note:** SpeciesCategory, VideoFormat, VideoResolution, VideoStatus, ContentType, VisualType, and Roles are backend lookup tables that populate dropdown menus on other pages but are not served as navigable pages in the web portal. They do not need page objects or UI tests. They are covered at the API level in Section 5.

---

## 2. UI Tests — Pages With No Coverage

For each page below, follow the existing pattern: page title, nav elements, admin/definitions dropdowns, table columns, action buttons, pagination.

- [x] ~~**`test_panels_page_ui.py`** — page title, nav, admin dropdown, definitions dropdown, table elements (Name, Description columns per component), pagination, Add button~~ ✅ Completed 2026-02-20: `tests/ui/test_panels_page.py` — 15 tests covering page title, nav elements, admin/definitions dropdowns, list controls, all 7 table columns, pagination, Add Panel form elements, Save disabled state, View Sample Panel modal, required field validation, Cancel navigation, Edit form navigation, and search filter (WILDXR-1870)
- [x] ~~**`test_panel_collections_page_ui.py`** — same structure; also verify the panels sub-list within a collection~~ ✅ Completed 2026-02-20: `tests/ui/test_panel_collections_page_ui.py` — 14 tests covering page title, nav elements, admin/definitions dropdowns, list controls, all 5 table columns, pagination, Add Panel Collection form elements, Save disabled state, required field validation, Cancel navigation, Edit form navigation, and search filter

---

## 3. UI Tests — Improvements to Existing Pages

These pages have UI tests but are missing important element checks.

- [ ] **Tags page** — `test_tags_page_ui.py` only checks the "development notice"; once Tags is fully live, add table elements, action buttons, pagination, and data retrieval tests (currently a placeholder)
- [ ] **Users page** — missing pagination test (page object likely supports it); add `test_users_pagination_elements()`
- [x] ~~**Users page** — missing table row data presence check (similar to `test_countries_table_data_presence`)~~ ✅ Completed 2026-02-24: Added `test_users_table_data_presence` to `tests/ui/adminUI/test_users_page_ui.py`; added `count_table_rows()` to `UsersPage`
- [x] ~~**Devices page** — missing search element and search functionality tests (component has search; countries page is the model)~~ ✅ Completed 2026-02-24: Added `test_devices_search_with_no_match_shows_empty_table` and `test_devices_search_clears_to_show_results` to `tests/ui/adminUI/test_devices_page_ui.py`; added `search_devices()` to `DevicesPage`
- [x] ~~**Devices page** — missing table row data check~~ ✅ Completed 2026-02-24: Added `test_devices_table_data_presence` to `tests/ui/adminUI/test_devices_page_ui.py`; added `count_table_rows()` to `DevicesPage`
- [ ] **Organizations page** — missing search tests (organizations list is searchable per the API; search UI is not currently functional — skip until UI is updated)
- [ ] **Map Markers page** — missing pagination tests (`MapMarkersPage` has pagination controls but no pagination test)
- [x] ~~**Video page** — verify card-level data: video name, thumbnail presence, and any status badges visible on grid cards~~ ✅ Covered by existing `test_video_grid_elements` and `test_video_name_retrieval` — no status badges exist in the current component
- [x] ~~**Videos page** — add filter/sort UI element checks (the `VideoSearchModal` component exists; verify its trigger button is present)~~ ✅ Completed 2026-02-24: Added `test_video_search_modal_opens_and_shows_filter_fields` to `tests/ui/dashboardUI/test_videos_page_ui.py`; added full `VideoSearchModal` locator and action methods to `VideosPage`
- [x] ~~**Video Catalogues page** — add search functionality test (similar to Countries search test)~~ ✅ Completed 2026-02-24: Added `test_video_catalogue_search_with_no_match_shows_empty_table` to `tests/ui/dashboardUI/test_video_catalogues_page_ui.py`; added `search_catalogues()` to `VideoCataloguesPage`
- [ ] **Installations page** — `test_installations_pagination_elements_with_sufficient_data` creates test data; verify that test cleans up properly via `AUTOTEST_` prefix
- [x] ~~**Installations page** — missing panel collection field checks on the Installation Details (edit) form~~ ✅ Completed 2026-02-20: Added `test_installation_edit_form_panel_collection_field_present` and `test_installation_edit_form_panel_collection_has_selected_value` to `tests/ui/adminUI/test_installations_page_ui.py` (WILDXR-1868)
- [x] ~~**Installations page** — corrected WILDXR-1868 panel collection test: `test_installation_edit_form_panel_collection_has_selected_value` was failing because WILDXR-1868's 'WildXR Panels' default only applies to the Add form, not existing records~~ ✅ Completed 2026-02-24: Renamed to `test_add_installation_form_panel_collection_defaults_to_wildxr_panels`; now navigates to the Add form and asserts the exact 'WildXR Panels' default; added unconditional Cancel to prevent accidental record creation; added `navigate_to_add_installation()` to `InstallationsPage`
- [x] ~~**Devices page** — add positive search test with known device name~~ ✅ Completed 2026-02-24: Added `test_devices_search_returns_matching_result` with `KNOWN_DEVICE_NAME = "Alex's QA Headset - F7V07HK - Managed"` constant to `tests/ui/adminUI/test_devices_page_ui.py`
- [x] ~~**Species page** — verify the search field clears correctly (test the clear/reset behavior)~~ ✅ Completed 2026-02-24: Added `test_species_search_clears_to_show_results` to `tests/ui/dashboardUI/test_species_page_ui.py`; added `search_species()` to `SpeciesPage`

---

## 4. API Tests — CRUD for Core Resources

The biggest gap: only Videos has meaningful API tests. Every resource below needs GET (list, detail), POST (create), PUT (update), and DELETE coverage.

### 4a. Organizations API (`/api/Organization`)

> **Key API facts (discovered 2026-02-24 Session B):**
> - `GET /api/Organization` returns a plain array, NOT a `ResponseDto` wrapper — unique among all resources
> - `PUT /api/Organization/Create` returns 200 with empty body; search by name to retrieve the created org's ID
> - Not-found returns 400 (not 404) — consistent with all other controllers
> - `Organization.Name` is `VARCHAR(50)` — AUTOTEST names must be ≤ 50 chars

- [x] ~~**`test_api_organizations.py`** — GET list: status 200, response is a plain array~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**GET list items have required fields** — each item has `organizationId` and `name`~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**GET list pageSize param limits results** — `pageSize=1` returns exactly 1 item~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**GET search** — filter by name; verify results contain search term; pagination envelope present~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**GET search — no match** — no-match returns 200 with empty results list (not 404)~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**GET details by ID** — valid GUID returns org; verify `organizationId`, `name` fields~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**GET details — not found** — nonexistent GUID returns 400~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**PUT create** — valid payload (`name` field) returns 200; org appears in search~~ ✅ Completed 2026-02-24 (Session B): Note — Create uses PUT (not POST); returns empty body
- [x] ~~**PUT create — missing required field** — omit `name`; expect 400~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**POST update** — update `name` of existing org; verify change persists in /Details~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**POST update — missing ID** — omit `organizationId`; expect 400 "Id is required"~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**DELETE** — delete `AUTOTEST_` org; verify it no longer appears in search~~ ✅ Completed 2026-02-24 (Session B)
- [x] ~~**DELETE — not found** — delete nonexistent GUID returns 400~~ ✅ Completed 2026-02-24 (Session B)
- [ ] **GET list pagination** — page 1 vs page 2 return different records; verify count is consistent (deferred: needs sufficient org count in QA)
- [ ] **Schema validation** — validate GET list and GET detail responses against JSON schema files

### 4b. Installations API (`/api/Installations`)

- [ ] **`test_api_installations.py`** — GET list: status 200, `ResponseDto` structure
- [ ] **GET pagination** — verify math across multiple pages
- [ ] **GET search** — filter by name
- [ ] **GET details by ID** — verify `InstallationDto` fields: `InstallationId`, `Name`, `OrganizationId`
- [ ] **POST create** — valid payload; use `AUTOTEST_` prefix; verify returned GUID
- [ ] **POST create — missing `Name`** — expect 400
- [ ] **POST create — invalid `OrganizationId`** — nonexistent org GUID; expect 400
- [ ] **PUT update** — change name; verify
- [ ] **DELETE** — cleanup `AUTOTEST_` record
- [ ] **Schema validation** — GET list and detail schemas

### 4c. Devices API (`/api/Device`)

- [ ] **`test_api_devices.py`** — GET list: status 200, response structure
- [ ] **GET search / lookup** — DeviceController has a lookup action; test it
- [ ] **GET details by ID** — verify `DeviceDto` fields: `DeviceId`, `Name`, `WildXRNumber`, `InstallationId`, `OrganizationId`
- [ ] **POST create** — valid payload; `AUTOTEST_` prefix
- [ ] **POST create — missing required fields** — `Name` omitted; expect 400
- [ ] **GET associated installation** — DeviceController has a route to get the device's installation; verify it works
- [ ] **PUT update** — change device name; verify
- [ ] **DELETE** — cleanup
- [ ] **RowVersion concurrency** — DeviceDto has `RowVersion`; test that stale update returns 409

### 4d. Users API (`/api/Users`)

- [ ] **`test_api_users.py`** — GET list: status 200; verify `UserDto` fields
- [ ] **GET search** — filter by username or name
- [ ] **GET details by ID** — verify user fields including `IsSystemAdmin`, `IsHeadsetAdmin`, `Roles`, `Organizations`
- [ ] **POST create** — valid payload; `AUTOTEST_` username; verify `UserId` returned
- [ ] **POST create — missing `UserName`** — expect 400
- [ ] **POST create — `UserName` too short (< 4 chars)** — expect 400
- [ ] **POST create — `Password` too short (< 6 chars)** — expect 400
- [ ] **POST create — duplicate `UserName`** — expect 400 or 409
- [ ] **PUT update** — change user name fields; verify
- [ ] **DELETE** — cleanup test user
- [ ] **Authenticate endpoint** — already exists in connection test; add detailed schema validation of token response

### 4e. Map Markers API (`/api/MapMarker`)

- [ ] **`test_api_map_markers.py`** — GET list: status 200, `ResponseDto` structure
- [ ] **GET search** — filter by name
- [ ] **GET details by ID** — verify `MapMarkerDto` fields
- [ ] **POST create** — valid payload; `AUTOTEST_` prefix
- [ ] **POST AddVideo** — associate a video with a map marker; verify relationship
- [ ] **POST RemoveVideo** — remove video association; verify
- [ ] **POST SetVideos** — set entire video list at once; verify with `SetVideosRequest` DTO
- [ ] **DELETE** — cleanup
- [ ] **RowVersion concurrency** — MapMarker uses `RowVersion`; stale update should return 409
- [ ] **Schema validation** — validate GET response shape

### 4f. Videos API — Expand Existing Coverage

Already has pagination and schema tests; these are the missing CRUD operations:

- [ ] **POST create** — valid payload with all required fields from `VideoDto` (Name, Overview, ThumbnailUrl, VideoResolutionId, CountryObtainedId); use `AUTOTEST_` prefix
- [ ] **POST create — missing `Name`** — expect 400
- [ ] **POST create — missing `VideoResolutionId`** — required field; expect 400
- [ ] **POST create — `Name` > 250 chars** — expect 400
- [ ] **POST create — `Overview` > 1200 chars** — expect 400
- [ ] **PUT update** — change video name; verify
- [ ] **DELETE** — cleanup `AUTOTEST_` video
- [ ] **GET map marker videos** — `VideosController` has a route for videos on a map marker; verify
- [ ] **GET folder SAS token** — verify endpoint returns a valid SAS token structure

### 4g. Video Catalogues API (`/api/VideoCatalogue`)

- [ ] **`test_api_video_catalogues.py`** — GET list, pagination, search
- [ ] **GET details by ID** — verify `VideoCatalogueDto` fields
- [ ] **POST create** — valid payload; `AUTOTEST_` prefix
- [ ] **PUT update** — change name
- [ ] **DELETE** — cleanup
- [ ] **Schema validation**

### 4h. Species API (`/api/Species`)

- [ ] **`test_api_species.py`** — GET list, pagination
- [ ] **GET search** — `SpeciesSearchQuery` DTO has filtering fields; test name/category filters
- [ ] **GET details by ID** — verify `SpeciesDto` fields (including IUCN status, population trend, category relationships)
- [ ] **POST create** — valid payload; `AUTOTEST_` prefix
- [ ] **POST create — missing required fields** — expect 400
- [ ] **PUT update** — change species data
- [ ] **DELETE** — cleanup
- [ ] **Schema validation**

### 4i. Tags API (`/api/Tag`)

- [ ] **`test_api_tags.py`** — GET list, pagination
- [ ] **GET search**
- [ ] **GET details by ID**
- [ ] **POST create** — valid payload; `AUTOTEST_` prefix
- [ ] **POST AddVideo** — associate a video with a tag; verify
- [ ] **POST RemoveVideo** — remove association
- [ ] **PUT update**
- [ ] **DELETE** — cleanup

---

## 5. API Tests — Definition/Lookup Resources

These have connectivity tests only. Need full read coverage and schema validation.

- [ ] **Countries** — GET list with pagination; GET detail; schema validation; POST/PUT/DELETE (admin-only)
- [ ] **IUCN Status** — same pattern as Countries
- [ ] **Population Trend** — same pattern as Countries
- [ ] **Species Category** — GET list; schema; verify all categories returned match known set
- [ ] **Video Format** — GET list; verify expected formats present (e.g., MP4, etc.)
- [ ] **Video Resolution** — GET list; verify expected resolutions
- [ ] **Video Status** — GET list; verify statuses (Active, Inactive, etc.)
- [ ] **Content Type** — GET list; schema validation
- [ ] **Visual Type** — GET list; schema validation
- [ ] **Roles** — GET list; verify at least SystemAdmin and OrgAdmin roles exist

---

## 6. API Tests — Authorization (Role-Based Access)

> **Key facts discovered 2026-02-24 (Session C):**
> - Authorization uses `[Authorize]` at class level on all controllers — missing/invalid token → 401 before any controller logic runs
> - Org filtering is via `AuthorizationManager.CanAccessResource(user, OrganizationAction)` — non-sysadmins see only their own org(s) plus the `AlwaysAccessibleId` WPS internal org
> - Cross-org resource access returns 403 (`Forbid()`), not 404
> - `AlwaysAccessibleId = "B1DF7F5A-5ED7-4AE9-97DC-E78B9137A0B3"` — the WildXR internal org; resources with this org ID visible to all authenticated users
> - Org-admin tokens acquired via `get_token_for_user(username, password)` in `utilities/auth.py`; `APIBase(token=...)` accepts a pre-fetched token

- [x] ~~**No token — all endpoints** — request without `Authorization` header returns 401 for all protected endpoints~~ ✅ Completed 2026-02-24 (Session C): `TestAPIUnauthenticated.test_get_without_token_returns_401` parametrized across 6 endpoints; plus PUT and DELETE variants
- [x] ~~**Invalid/expired token** — request with malformed JWT returns 401~~ ✅ Completed 2026-02-24 (Session C): `test_invalid_token_returns_401`
- [x] ~~**Org Admin sees only their org's data** — log in as an org admin; verify that organizations and installations only return records for their org~~ ✅ Completed 2026-02-24 (Session C): `test_bp_admin_search_excludes_dta_org`, `test_dta_admin_search_excludes_bp_org`, installation access sanity checks
- [x] ~~**Org Admin cannot see system-wide data** — verify org admin GET `/api/Organization` does not return orgs they don't belong to~~ ✅ Completed 2026-02-24 (Session C): `test_bp_admin_search_excludes_dta_org` and `test_dta_admin_search_excludes_bp_org`
- [ ] **Org Admin cannot create resources for another org** — POST with a different `OrganizationId`; expect 403 (controllers currently have no explicit auth check on Create — potential gap to document)
- [x] ~~**System Admin can see all orgs** — log in as system admin; verify full list returned~~ ✅ Completed 2026-02-24 (Session C): `test_sysadmin_search_returns_both_bp_and_dta_orgs`, `test_sysadmin_sees_more_orgs_than_bp_admin`
- [ ] **System Admin can create resources in any org**
- [ ] **AlwaysAccessibleId (WPS org) resources visible to all orgs** — verify map markers/videos from the WPS org appear for non-WPS org admin users
- [x] ~~**Unauthenticated create/update/delete** — POST/PUT/DELETE without token returns 401, not 500~~ ✅ Completed 2026-02-24 (Session C): `test_write_without_token_returns_401` (PUT) and `test_delete_without_token_returns_401` (DELETE)

---

## 7. API Tests — Error Handling and Validation

Currently only Video GET edge cases are tested. Every resource needs systematic error coverage.

- [ ] **GET with invalid GUID format** — `/api/Organization/not-a-guid/details` — expect 400, not 500
- [ ] **GET with nonexistent but valid GUID** — expect 400 or 404 (document actual behavior)
- [ ] **POST with empty body** — all resources; expect 400
- [ ] **POST with extra/unknown fields** — should be ignored or rejected (document behavior)
- [ ] **POST with wrong data types** — e.g., send string where GUID expected; expect 400
- [ ] **Pagination edge cases for all resources** — page 0, negative page, page beyond total, `pageSize=0`, `pageSize=-1` (video tests exist but others don't)
- [ ] **Search with empty string** — should return all results or error; document behavior
- [ ] **Search with special characters** — SQL injection probe (should sanitize, not error)
- [ ] **Concurrent update conflict** — `RowVersion` on MapMarker and Device; stale update should return 409
- [ ] **Cascade behavior** — delete an org that has installations/devices; document and test the behavior
- [ ] **Panels known bug (WILDXR-1907)** — add a regression test for the `Math.Abs(count / pageSize) + 1` pagination formula; test should fail with current code and pass after fix is deployed
  - *Note: `tests/api/test_api_panels.py` was completed 2026-02-20 — covers GET list (pagination envelope), search (match and no-match), and single panel details with required field verification (WILDXR-1864). CREATE/UPDATE deferred until DELETE endpoint exists.*

---

## 8. Functional Tests — CRUD Workflows

Only Installations (add) and Organizations (add) have functional tests. Everything else is missing.

### 8a. Organizations

- [ ] **Edit organization** — find an `AUTOTEST_` org, click Edit, change name, save, verify updated name in table
- [ ] **Delete organization** — create via API, verify in UI, delete via UI, verify gone
- [ ] **Duplicate name** — attempt to create two orgs with same name; verify error message shown

### 8b. Installations

- [x] ~~**Add installation** — fill form via UI, verify in table, clean up via API~~ ✅ Completed (prior session): `test_add_installation` in `test_installations_page_functional.py`; updated 2026-02-20 to explicitly select panel collection via `_create_installation_via_ui` helper (WILDXR-1868)
- [ ] **Edit installation** — create via API, navigate to UI, edit name, verify change
- [ ] **Delete installation** — create via API, delete via UI, verify removed
- [ ] **Search clears** — search for a term, then clear search, verify all results return

### 8c. Devices

- [ ] **Add device** — fill form with `AUTOTEST_` prefix, assign to installation, verify in table
- [ ] **Edit device** — change name; verify
- [ ] **Device-installation relationship** — assign device to installation, navigate to installation, verify device appears

### 8d. Users

- [ ] **Add user** — create user with `AUTOTEST_` credentials, verify in table
- [ ] **Edit user** — change first/last name
- [ ] **Change password** — `ChangePasswordModal` exists in frontend; test the modal and password change flow
- [ ] **Assign role** — assign org admin role to user; verify role appears
- [ ] **Disable user** — `IsDisabled` field exists; verify disable/enable toggle works

### 8e. Videos

- [ ] **Upload video flow** — `UploadVideoForm` component exists; test the multi-step upload process (may require file handling)
- [ ] **Add video** — `AddEditVideo` form; fill required fields (Name, Overview, Resolution, Country); save and verify in list
- [ ] **Edit video** — find existing video, edit name, verify updated
- [ ] **Search video** — `VideoSearchModal` exists; test search returns filtered results
- [ ] **Video filter** — test any available filter options on the video list

### 8f. Video Catalogues

- [ ] **Add catalogue** — create with `AUTOTEST_` prefix; verify
- [ ] **Edit catalogue** — change name; verify
- [ ] **Add video to catalogue** — open catalogue, add a video, verify video appears in catalogue
- [ ] **Remove video from catalogue**
- [ ] **Delete catalogue** — cleanup

### 8g. Map Markers

- [ ] **Add map marker** — form requires coordinates and name; create with `AUTOTEST_` prefix
- [ ] **Edit map marker**
- [ ] **Add video to map marker** — verify many-to-many relationship works in UI
- [ ] **Remove video from map marker**
- [ ] **Delete map marker**

### 8h. Species

- [ ] **Add species** — form includes IUCN status, population trend, category dropdowns; verify dropdowns populate from lookup endpoints
- [ ] **Edit species**
- [ ] **Delete species**

### 8i. Panels and Panel Collections (No coverage at all)

- [ ] **Add panel** — create with `AUTOTEST_` prefix; verify in table
- [ ] **Edit panel**
- [ ] **Delete panel**
- [ ] **Add panel collection** — create collection
- [ ] **Add panel to collection** — many-to-many relationship; verify panel appears in collection
- [ ] **Remove panel from collection**
- [ ] **Delete panel collection**

### 8j. Countries / Definitions (Admin only)

- [ ] **Add country** — admin can add; verify in list
- [ ] **Edit country** — change name; verify
- [ ] **Add IUCN Status** — verify new status appears in species form dropdown
- [ ] **Add Population Trend** — same pattern

---

## 9. End-to-End Workflow Tests

These cross-feature tests validate that the system works as a whole, not just individual pages.

- [ ] **Full video lifecycle** — create org → create installation → create map marker → upload/add video → assign video to map marker → assign video to catalogue → verify all relationships via API
- [ ] **Org admin isolation** — log in as org A admin, create installation, log out; log in as org B admin, verify installation not visible
- [ ] **Device assignment flow** — create device → assign to installation → verify device appears on installation's device list
- [ ] **Species with relationships** — create species with IUCN status and population trend → verify relationships in detail view
- [ ] **Video with tags** — add tags to video → verify tags appear on video detail → search by tag
- [ ] **Panel collection workflow** — create panels → create collection → add panels to collection → verify collection shows correct panel count
- [ ] **Cross-session state** — create record in one browser session, open new session, verify record persists

---

## 10. Schema Validation — Expand to All Resources

Currently only the Video GET endpoint has schema validation. Every resource needs a JSON schema file and validation test.

- [ ] **Organization schema** — `GET /api/Organization` list and detail
- [ ] **Installation schema** — list and detail
- [ ] **Device schema** — list and detail
- [ ] **User schema** — list and detail (exclude sensitive fields like `Password` in response)
- [ ] **Map Marker schema** — list and detail
- [ ] **Video Catalogue schema** — list and detail
- [ ] **Species schema** — list and detail (complex: includes nested IUCN, PopulationTrend, Category)
- [ ] **Tag schema** — list and detail
- [ ] **Countries schema** — list and detail
- [ ] **IUCN Status schema** — list
- [ ] **Population Trend schema** — list
- [ ] **Panels schema** — list and detail
- [ ] **Panel Collections schema** — list and detail (includes nested panels array)
- [ ] **Pagination wrapper schema** — `ResponseDto` shape is shared; create a reusable base schema that all paginated responses extend
- [ ] **Error response schema** — validate that 400 responses have a consistent error shape

---

## 11. Accessibility and Responsive UI Tests

Currently only the login page has these tests. Consider expanding:

- [ ] **Organizations page** — accessibility attributes on form fields in the Add/Edit modal
- [ ] **Videos page** — ARIA labels on video cards and filter controls
- [ ] **Navigation** — keyboard navigation through the nav bar works in expected order
- [ ] **Pagination controls** — accessible labels on Previous/Next/page number buttons
- [ ] **Mobile viewport** — nav collapses appropriately; tables scroll or reflow on small screens

---

## 12. Test Infrastructure Improvements

- [ ] **API test for token refresh / expiry** — 30-day JWT lifetime is a known concern; document and test what happens when a token expires mid-session
- [x] ~~**Reduce xdist auth calls from N to 1** — with `-n auto`, each worker made its own `/Users/Authenticate` call; wasted tokens and added startup latency~~ ✅ Completed 2026-02-24 (Session C): Added `pytest_configure_node` hook + `_seed_token_cache` autouse fixture to `conftest.py`; controller fetches token once via singleton, injects into all workers via `workerinput`; serial runs unaffected
- [ ] **Parallel test isolation** — verify that `pytest-xdist` workers don't conflict on shared test data (e.g., two workers both creating `AUTOTEST_` records with the same name)
- [x] ~~**Fix pytest-xdist collection divergence** — `test_login_functionality.py` used unseeded `Faker` at module level for `@pytest.mark.parametrize`, causing different test IDs across workers and a "Different tests were collected" crash~~ ✅ Completed 2026-02-24: Added `Faker.seed(0)` immediately after `fake = Faker()`
- [ ] **Add `AUTOTEST_` cleanup to more entities** — currently conftest only cleans up installations, video catalogues, and organizations; extend cleanup to devices, users, map markers, species, tags, panels, panel collections
- [ ] **CI marker filter** — audit which tests are tagged `@pytest.mark.github` for CI and ensure all stable, non-slow tests are included
- [ ] **Flaky test detection** — add `pytest-rerunfailures` for known-flaky UI tests (e.g., pagination tests that depend on QA data state)
- [ ] **Response time baselines** — `APIBase` measures response times; add assertions for acceptable thresholds (e.g., list endpoints < 3s)
- [x] ~~**Fix page title locators across all page objects** — `get_by_role("heading", name="...")` was unreliable and broken in 3 files where `self.get_by_role(...)` was called instead of `self.page.get_by_role(...)`~~ ✅ Completed 2026-02-24: Replaced all 13 affected page objects with `page.locator("h1", has_text="...")`
- [x] ~~**Remove dead `get_page_title_text()` methods** — method defined in 11 page objects but never called; title checks go through `BasePage.verify_page_title()` directly~~ ✅ Completed 2026-02-24: Removed from all 11 page objects
- [x] ~~**Fix search URL matcher race condition** — `devices_page.py` and `species_page.py` used broad matchers (`"device" in url`) that could capture the page-load response instead of the search response, causing stale row counts in tests~~ ✅ Completed 2026-02-24: Narrowed to `/Device/search` and `/species/search`; added 500ms post-response wait for React re-render
- [x] ~~**Handle intentional QA test data in video integrity checks** — video "#01 Test No Species" intentionally has no species, causing `test_video_data_integrity` to fail non-deterministically when that video is randomly selected~~ ✅ Completed 2026-02-24: Added `INTEGRITY_CHECK_EXCLUDED_NAME_PREFIX = "#"` constant; `_validate_video_content` skips any video whose name starts with `#`
- [x] ~~**Fix `find_tags_link()` typo in base_page.py** — `find_tags_link()` called `get_tages_link()` (typo), a method that doesn't exist; would raise `AttributeError` on any test using that method~~ ✅ Completed 2026-02-24 (Session B): Changed to `get_tags_link()`
- [x] ~~**Add `put()` and `delete()` methods to `APIBase`** — prerequisite for all CRUD API tests in Section 4; only `get()` and `post()` existed; tests would have to call `requests` directly, bypassing the abstraction~~ ✅ Completed 2026-02-24 (Session B): Added `put()` and `delete()` with full docstrings explaining unconventional verb usage (PUT=create, DELETE takes query params)
- [x] ~~**Fix flaky `test_installations_pagination_navigation`** — compared exact set of page-1 record names before and after a page-2 round-trip; failed when API returned records in different order on the second call (sort instability at the page boundary)~~ ✅ Completed 2026-02-24 (Session B): Replaced set equality with pagination-state check (back_start, back_total, row count)
- [x] ~~**Remove duplicate `github` marker from pytest.ini`** — marker was defined twice (lines 29 and 60)~~ ✅ Completed 2026-02-24 (Session B)

---

## Priority Summary

| Priority | Area | Items |
|---|---|---|
| **High** | Missing page objects (blockers for 2 pages) | 2 |
| **High** | API CRUD for core resources (no write tests exist) | ~60 |
| **High** | Authorization tests (entirely missing) | 9 |
| **Medium** | Functional tests — CRUD workflows | ~35 |
| **Medium** | Schema validation for all resources | 15 |
| **Medium** | UI tests for missing pages | 2 |
| **Medium** | API error handling and validation | 11 |
| **Lower** | UI test improvements to existing pages | 12 |
| **Lower** | End-to-end workflow tests | 7 |
| **Lower** | Accessibility/responsive expansion | 5 |
| **Lower** | Test infrastructure improvements | 6 |

The highest-value work is in **API CRUD tests** and **authorization tests** — those are the areas where real bugs would hide and where the current suite offers almost no protection.
