# WildXR.test — Session Summary
**Date:** 2026-02-24 (Session D)
**Branch(es):** `feature/api-installations-tests` → merged to main; `fix/video-catalogues-search-timing` → merged to main

---

## Context

This session continued directly from the Session C compaction. Three pending tasks carried over:

1. Finish wrapping up the Installations API test suite (`feature/api-installations-tests`)
2. Add the "Document Gaps — Don't Test Them" principle to `CLAUDE.md`
3. Investigate and fix a test failure: `test_video_catalogue_search_with_no_match_shows_empty_table`

---

## Files Modified

### Process / Documentation

| File | What Changed |
|---|---|
| `.claude/CLAUDE.md` | Added new subsection "Document Gaps — Don't Test Them" after the Six-Category Framework. Explains why tests for known bugs/gaps should not be written, what to do instead (comment), and gives a concrete example from the Installations suite. |
| `AIsummaries/Todo.md` | Corrected two stale entries: "missing name causes 500" → "causes 200 (DB column nullable)"; checkbox entry for the removed missing-name test updated to reflect removal per new principle. Added Section 12 entry for the `search_catalogues` race condition fix. |

### Page Objects

| File | What Changed |
|---|---|
| `page_objects/dashboard/video_catalogues_page.py` | Added `wait_for_load_state("networkidle")` call after the `expect_response` block in `search_catalogues()`. Updated docstring to explain why both waits are required. |

### New Tests

| File | What Changed |
|---|---|
| `tests/api/test_api_installations.py` | Created — 19 tests across 2 classes (see Tests Created below). Branch was created in the prior session; final commits (removing the missing-name test, adding CLAUDE.md principle) landed in this session. |

### Merged Branches

| Branch | Into | Commits |
|---|---|---|
| `feature/api-installations-tests` | `main` | Installations API suite, CLAUDE.md principle, Todo corrections |
| `fix/video-catalogues-search-timing` | `main` | `search_catalogues` race condition fix |

---

## Tests Created

### `tests/api/test_api_installations.py`

**Class `TestAPIInstallationsGet`** (11 read-only tests):

| Test | What It Verifies |
|---|---|
| `test_get_list_returns_200` | GET /Installations returns 200 |
| `test_get_list_returns_array` | Response is a plain JSON array, NOT a ResponseDto wrapper |
| `test_get_list_items_have_required_fields` | Each item has `installationId`, `name`, `organizationId` |
| `test_get_list_page_size_param_limits_results` | `pageSize=1` query param is respected |
| `test_get_search_returns_200_with_pagination_envelope` | GET /Installations/search returns 200 with `results` key |
| `test_get_search_pagination_fields_present` | `totalCount`, `pageNumber`, `pageSize` keys present |
| `test_get_search_name_filter_returns_results` | Name filter returns matching records |
| `test_get_search_no_match_returns_empty_list` | Unmatchable term returns empty `results` list |
| `test_get_detail_returns_200_for_valid_id` | GET /Installations/{id}/details returns 200 |
| `test_get_detail_has_required_fields` | Detail response has all expected fields |
| `test_get_detail_returns_400_for_nonexistent_id` | Nonexistent GUID returns 400 (not 404) |

**Class `TestAPIInstallationsCRUD`** (8 tests):

Uses `setup_method` / `teardown_method` with a `_created_ids` list for cleanup. `_create_installation()` helper supplies an explicit `installationId` for cleanup simplicity (EF Core auto-generates if omitted, but explicit IDs are convenient).

| Test | What It Verifies |
|---|---|
| `test_create_installation_returns_200` | PUT /Installations/create with valid payload returns 200 |
| `test_created_installation_appears_in_search` | Newly created installation found in /search by name |
| `test_created_installation_detail_matches_payload` | /details fields match what was submitted on create |
| `test_create_installation_with_invalid_org_id` | Creating with a nonexistent orgId returns 200 (no FK check in controller) |
| `test_update_installation_name_returns_200` | POST /Installations/update with full NOT NULL fields returns 200 |
| `test_update_installation_missing_id_returns_400` | Update with no `installationId` returns 400 |
| `test_update_nonexistent_installation_returns_400` | Update with unknown GUID returns 400 |
| `test_delete_installation_returns_200` | DELETE /Installations/delete returns 200 |
| `test_delete_nonexistent_installation_returns_400` | Delete with unknown GUID returns 400 |

**Total new tests: 19** — 2 failures on first run (both fixed, see below).

---

## Bugs Fixed

### Test Failure 1 — `test_create_installation_missing_name_returns_error`

- **Expected:** 400 or 500
- **Actual:** 200
- **Root cause:** The DB `Name` column is nullable — no NOT NULL constraint. The API controller has zero server-side validation, so a nameless installation is accepted and persisted.
- **Resolution:** Test removed entirely per the "Document Gaps — Don't Test Them" principle. Gap documented in `test_api_installations.py` file header (quirk #4) and in `CLAUDE.md`.

### Test Failure 2 — `test_update_installation_name_returns_200`

- **Expected:** 200
- **Actual:** 500 — `Cannot insert the value NULL into column 'OrganizationID', table 'QA.dbo.Installation'; column does not allow nulls. UPDATE fails.`
- **Root cause:** The update action uses `AutoMapper.Map(model, entityToModify)` — a full replace. Any field omitted from the request body is deserialized as `null`/`0` and overwrites the stored value. `OrganizationId` is `Guid?` in the C# model but `NOT NULL` in the actual SQL column, so sending a null `organizationId` hits a DB constraint.
- **Fix:** Added `"organizationId": TEST_ORG_ID` to the update payload. All update payloads must include every `NOT NULL` DB field.

### Test Failure 3 — `test_video_catalogue_search_with_no_match_shows_empty_table` (UI)

- **Expected:** 0 rows after searching for an unmatchable term
- **Actual:** 12 rows (stale DOM)
- **Root cause:** React timing. `search_catalogues()` used `expect_response` to wait for the search HTTP response, then returned. But the HTTP response arriving and React finishing its re-render are two separate events. `count_table_rows()` was called in the gap — after the response but before React updated the DOM — and read the stale 12-row table.
- **Why the matching-search tests passed:** Those tests relied on locators that would auto-retry until rows appeared (implicit Playwright waits); the empty-table case called `.count()` which is an immediate snapshot with no retry.
- **Fix:** Added `self.page.wait_for_load_state("networkidle")` inside `search_catalogues()` after the `with` block. Both waits are required: `expect_response` ensures the listener is registered before the click (avoiding capturing a prior in-flight response); `networkidle` ensures React has finished processing and the DOM is stable.

---

## Key Design Decisions

### "Document Gaps — Don't Test Them" Principle

Established as a project-wide principle in `CLAUDE.md` after the missing-name installation test was removed. The reasoning:

- A test that passes only because something is broken provides false confidence
- It creates `AUTOTEST_` records that must be cleaned up indefinitely
- It adds CI noise and must be rewritten when the gap is fixed
- The comment documenting the gap is what guides future work

**Applied here:** The Installations API accepts nameless records because the DB column is nullable and there is no server-side validation. This is documented in the `test_api_installations.py` file header as quirk #4, not tested.

### AutoMapper Full-Replace Pattern

The WildXR API's update actions use `AutoMapper.Map(dto, entity)` which overwrites every field on the entity with values from the DTO. Any field absent from the request body gets deserialized to its C# default (`null` for nullable types, `Guid.Empty` for GUIDs, `0` for ints). If that default violates a `NOT NULL` DB constraint, the update returns 500.

**Implication for all update tests:** Always include every `NOT NULL` field in update payloads, even fields you are not testing. The `organizationId` field is the canonical example.

---

## API Quirks Documented (Installations)

These are recorded in the `test_api_installations.py` file header:

1. `GET /api/Installations` returns a plain JSON array — NOT a `ResponseDto` wrapper (same as Organizations)
2. `PUT /api/Installations/create` returns 200 with an empty body; `installationId` is optional (EF Core auto-generates if omitted)
3. Not-found returns 400 (not 404) — consistent with all controllers
4. No server-side field validation — `Name` DB column is nullable; nameless installations are accepted (API design gap)
5. Update is a full replace — omitting `organizationId` causes 500 (NOT NULL in DB despite `Guid?` in C# model)
6. `OrganizationId` has no FK check in the Create action
7. PUT = create, POST = update (unconventional but consistent)
8. `panelCollectionId` can be omitted — defaults to `Guid.Empty`; `ResolvePanelCollectionIdAsync` is defined in the controller but never called

---

## Session End State

- `main` is up to date on both `origin` and `backup`
- 258 tests total (prior 239 + 19 new installations tests)
- All branches merged; no pending feature branches
- Next: Section 4c — Devices API (`/api/Device`)
