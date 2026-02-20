# WILDXR-1864 — Panels API Test Plan Summary

**Date:** 2026-02-20
**Jira Ticket:** [WILDXR-1864](https://wildlifeprotectionsolutions.atlassian.net/browse/WILDXR-1864)
**Ticket Title:** API - PanelDto & Functions
**Status at time of planning:** IN QA

---

## Background

WILDXR-1864 introduces the `PanelDto` and associated CRUD/query functions for the `/api/Panels` endpoint. Panels represent individual content panels used in the WildXR VR app's menu/navigation system. This ticket is foundational — WILDXR-1866, WILDXR-1867, WILDXR-1868, and WILDXR-1870 build on top of it.

---

## Key Decision: No Creation Tests

Because there is no DELETE endpoint for panels, any record created during testing is permanent in the QA environment. To avoid flooding the database with non-removable test data, **all tests that require creating panel records are deferred** until a DELETE endpoint is implemented.

---

## Endpoints in Scope

| Verb | Route |
|------|-------|
| GET | `/api/Panels?pageNumber=&pageSize=` |
| GET | `/api/Panels/search?name=&pageNumber=&pageSize=` |
| GET | `/api/Panels/{id}/details` |

---

## Test Categories

### 1. Happy Path / Read
- GET list returns 200 with correct pagination envelope
- GET search returns matching panels; empty result (not 404) when no match
- GET details returns a single `PanelDto` for a valid pre-existing panel ID

### 2. JSON Serialization & Schema
The DTO uses intentional mixed casing — this is a primary concern flagged in the ticket.

| Field | Expected JSON Key | Casing |
|-------|------------------|--------|
| PanelId | `panelId` | camelCase |
| Name | `name` | camelCase |
| Description | `description` | camelCase |
| VisualType | `VisualType` | PascalCase |
| Contents | `Contents` | PascalCase |
| VideoCatalogueId | `VideoCatalogueId` | PascalCase |
| BackgroundImageUrl | `backgroundImageUrl` | camelCase |
| Header | `header` | camelCase |
| NewFlag | `NewFlag` | PascalCase |
| RowVersion | `rowVersion` | camelCase |

Null-handling rules to verify:
- `VisualType = null` → field **omitted** from JSON (NullValueHandling.Ignore)
- `Contents = null` → field **present as `null`** (no NullValueHandling attribute)
- `BackgroundImageUrl = null` → field **omitted** from JSON

### 3. Invalid Input on Read Endpoints
- Malformed (non-UUID) path param on GET details → expect 400, not 500
- Valid UUID but non-existent panel → expect 404
- `pageNumber=0` or `pageSize=0` → verify reset to 1
- Negative pagination values → verify reset to 1
- `name` param omitted from search → document actual behavior

### 4. Known Pagination Bug (WILDXR-1907)
The Panels controller uses `Math.Abs(count / pageSize) + 1` instead of
`Math.Ceiling((double)count / pageSize)`. Test will be marked as **expected fail**
with WILDXR-1907 as the reference.

### 5. Authorization
- No token → 401 on all endpoints
- Invalid/expired token → 401
- Org admin sees only their org's panels
- Org admin cannot see another org's panels
- System admin sees all panels
- Panels with `OrganizationId = "00000000-0000-0000-0000-000000000000"` visible to org admins

---

## Deferred (Until DELETE Exists)

| Deferred | Reason |
|----------|--------|
| PUT `/api/Panels/create` | No DELETE → permanent test data |
| POST `/api/Panels/update` | Modifies shared QA data without safe rollback |
| POST `/api/Panels/UploadBackgroundImage` | Writes to Azure blob; no cleanup path |
| Default value verification | Requires creation |
| Concurrency / `RowVersion` | Requires create + concurrent update |

---

## Implementation Order

1. Happy path read tests
2. Schema / serialization validation
3. Invalid input edge cases
4. Pagination bug documentation test
5. Authorization tests

---

## Related Tickets

- WILDXR-1866 — VideoDatabaseDto
- WILDXR-1867 — InstallationDto
- WILDXR-1868 — Frontend
- WILDXR-1870 — Panels page
- WILDXR-1907 — Pagination formula bug in Panels controller
