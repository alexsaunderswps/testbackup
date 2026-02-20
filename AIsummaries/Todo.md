# WildXR.test — Gap Analysis & Testing Todo List

Generated: 2026-02-19

## How to Read This List

Items are grouped by area and roughly ordered by priority within each section. "High" = fundamental coverage gaps; "Medium" = important but not blocking; "Low" = nice-to-have or edge cases.

---

## 1. Missing Page Objects (Prerequisites for UI/Functional Tests)

These pages exist in the frontend but have zero page object coverage. Nothing else below can move forward for these areas without them.

- [x] ~~**Create `PanelsPage` page object** — `panels/` component has `ManagePanelsPage`, `AddEditPanel`, `PanelsList`; no page object or tests exist~~ ✅ Completed 2026-02-20: `page_objects/admin_menu/panels_page.py` created (WILDXR-1870)
- [ ] **Create `PanelCollectionsPage` page object** — `panelCollections/` has `ManagePanelCollectionsPage`, `AddEditPanelCollection`; no page object or tests exist

> **Note:** SpeciesCategory, VideoFormat, VideoResolution, VideoStatus, ContentType, VisualType, and Roles are backend lookup tables that populate dropdown menus on other pages but are not served as navigable pages in the web portal. They do not need page objects or UI tests. They are covered at the API level in Section 5.

---

## 2. UI Tests — Pages With No Coverage

For each page below, follow the existing pattern: page title, nav elements, admin/definitions dropdowns, table columns, action buttons, pagination.

- [x] ~~**`test_panels_page_ui.py`** — page title, nav, admin dropdown, definitions dropdown, table elements (Name, Description columns per component), pagination, Add button~~ ✅ Completed 2026-02-20: `tests/ui/test_panels_page.py` — 15 tests covering page title, nav elements, admin/definitions dropdowns, list controls, all 7 table columns, pagination, Add Panel form elements, Save disabled state, View Sample Panel modal, required field validation, Cancel navigation, Edit form navigation, and search filter (WILDXR-1870)
- [ ] **`test_panel_collections_page_ui.py`** — same structure; also verify the panels sub-list within a collection

---

## 3. UI Tests — Improvements to Existing Pages

These pages have UI tests but are missing important element checks.

- [ ] **Tags page** — `test_tags_page_ui.py` only checks the "development notice"; once Tags is fully live, add table elements, action buttons, pagination, and data retrieval tests (currently a placeholder)
- [ ] **Users page** — missing pagination test (page object likely supports it); add `test_users_pagination_elements()`
- [ ] **Users page** — missing table row data presence check (similar to `test_countries_table_data_presence`)
- [ ] **Devices page** — missing search element and search functionality tests (component has search; countries page is the model)
- [ ] **Devices page** — missing table row data check
- [ ] **Organizations page** — missing search tests (organizations list is searchable per the API)
- [ ] **Map Markers page** — missing pagination tests (`MapMarkersPage` has pagination controls but no pagination test)
- [ ] **Video page** — verify card-level data: video name, thumbnail presence, and any status badges visible on grid cards
- [ ] **Videos page** — add filter/sort UI element checks (the `VideoSearchModal` component exists; verify its trigger button is present)
- [ ] **Video Catalogues page** — add search functionality test (similar to Countries search test)
- [ ] **Installations page** — `test_installations_pagination_elements_with_sufficient_data` creates test data; verify that test cleans up properly via `AUTOTEST_` prefix
- [ ] **Species page** — verify the search field clears correctly (test the clear/reset behavior)

---

## 4. API Tests — CRUD for Core Resources

The biggest gap: only Videos has meaningful API tests. Every resource below needs GET (list, detail), POST (create), PUT (update), and DELETE coverage.

### 4a. Organizations API (`/api/Organization`)

- [ ] **`test_api_organizations.py`** — GET list: status 200, response structure matches `ResponseDto`, pagination fields present
- [ ] **GET list pagination** — page 1 vs page 2 return different records; `TotalCount` consistent across pages
- [ ] **GET search** — filter by name; verify results contain search term
- [ ] **GET details by ID** — valid GUID returns org; verify `OrganizationId`, `Name` fields
- [ ] **GET details — not found** — nonexistent GUID returns 400/404
- [ ] **POST create** — valid payload (`Name` field) returns new org with GUID; use `AUTOTEST_` prefix
- [ ] **POST create — missing required field** — omit `Name`; expect 400
- [ ] **POST create — name too long** — `Name` beyond max length; expect 400
- [ ] **PUT update** — update `Name` of existing org; verify change persists
- [ ] **DELETE** — delete `AUTOTEST_` org; verify it no longer appears in list
- [ ] **Schema validation** — validate GET list response and GET detail against JSON schemas

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

This is entirely untested. The app has multi-tenant filtering by `OrganizationId` and role-based access control.

- [ ] **No token — all endpoints** — request without `Authorization` header returns 401 for all protected endpoints
- [ ] **Invalid/expired token** — request with malformed JWT returns 401
- [ ] **Org Admin sees only their org's data** — log in as an org admin; verify that organizations, installations, devices, map markers, videos, video catalogues only return records for their org
- [ ] **Org Admin cannot see system-wide data** — verify org admin GET `/api/Organization` does not return orgs they don't belong to
- [ ] **Org Admin cannot create resources for another org** — POST with a different `OrganizationId`; expect 403
- [ ] **System Admin can see all orgs** — log in as system admin; verify full list returned
- [ ] **System Admin can create resources in any org**
- [ ] **AlwaysAccessibleId (WPS org) resources visible to all orgs** — verify map markers/videos from the WPS org appear for non-WPS org admin users
- [ ] **Unauthenticated create/update/delete** — POST/PUT/DELETE without token returns 401, not 500

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
- [ ] **Parallel test isolation** — verify that `pytest-xdist` workers don't conflict on shared test data (e.g., two workers both creating `AUTOTEST_` records with the same name)
- [ ] **Add `AUTOTEST_` cleanup to more entities** — currently conftest only cleans up installations, video catalogues, and organizations; extend cleanup to devices, users, map markers, species, tags, panels, panel collections
- [ ] **CI marker filter** — audit which tests are tagged `@pytest.mark.github` for CI and ensure all stable, non-slow tests are included
- [ ] **Flaky test detection** — add `pytest-rerunfailures` for known-flaky UI tests (e.g., pagination tests that depend on QA data state)
- [ ] **Response time baselines** — `APIBase` measures response times; add assertions for acceptable thresholds (e.g., list endpoints < 3s)

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
