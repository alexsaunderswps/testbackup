# Orphaned Test Data Cleanup — Summary

**Date:** 2026-02-19
**Branch:** `feature/pytest-xdist` (merged into `main`)
**Commit:** `f970197`

---

## Background

After enabling pytest-xdist parallel execution, the QA environment accumulated a large number of orphaned test records — installations and organizations that were created during test runs but never deleted. This document explains why it happened, what was fixed, and how the cleanup system now works.

---

## Problem: Why Records Were Accumulating

Four separate bugs combined to cause the orphaned data:

### Bug 1 — Wrong API endpoint for organizations

`conftest.py` had `list_endpoint: f"{api_url}/Organizations"` (plural).
The actual endpoint is `/Organization` (singular). The plural form returns **404**.
This meant `cleanup_orphaned_test_records` silently failed for organizations every time.

### Bug 2 — Missing pagination parameters

Both `/Installations` and `/Organization` require `?pageNumber=1&pageSize=N` query parameters.
Without them, the API's `GetPage(0, 0)` call defaults to returning **only 1 record**.
So even when the endpoint was correct, the cleanup only saw 1 record and could never find the orphaned ones.

This is confirmed by the backend controller code (`InstallationsController.cs`):
```csharp
var queryableResult = await queryable.GetPage(pageNumber, pageSize).ToListAsync(...);
```
No default page size is applied — if you pass 0, you get 0 (or 1) records back.

### Bug 3 — Prefix mismatch between create and cleanup

`create_test_record_payload()` in `conftest.py` used the `AUTO_` prefix:
```python
base_name = f"AUTO_{username}_{timestamp}_{test_run_id}"
```

But `cleanup_orphaned_test_records()` only searched for the `AUTOTEST_` prefix:
```python
if record[name_field].startswith("AUTOTEST_"):
```

So every bulk pagination record created by the fixtures was invisible to the cleanup function.

### Bug 4 — `test_add_organization` had no teardown

`test_add_organization` created organizations through the UI using the name format:
```
"Test Organization UI 20260219171519"
```
There was no teardown to delete them. Since this name doesn't match any automated prefix, they were never caught by any cleanup mechanism.

---

## What Was Cleaned Up

Running `cleanup_test_data.py` against the QA environment:

| Resource | Records Deleted |
|---|---|
| Installations (AUTO_QASysAdmin_… bulk pagination records) | 27 |
| Installations (AUTOTEST_UI_unknown_… legacy record) | 1 |
| Organizations (Test Organization UI …) | 4 |
| **Total** | **32** |

Zero failures. QA environment is now clean.

---

## Code Changes

### `cleanup_test_data.py` (new file, committed)

Standalone one-shot cleanup script. Run it any time to delete orphaned test records:

```bash
# Preview what would be deleted:
python cleanup_test_data.py --dry-run

# Actually delete:
python cleanup_test_data.py
```

**Fixes in this file:**
- Organizations list URL changed: `/Organizations` → `/Organization`
- Pagination params added to both list URLs: `?pageNumber=1&pageSize=500`
- Added `"Test Organization UI"` to `TEST_PREFIXES` for one-time legacy cleanup

### `conftest.py`

**Fix 1 — Organizations list endpoint:**
```python
# Before:
"list_endpoint": f"{api_url}/Organizations",

# After:
"list_endpoint": f"{api_url}/Organization",  # (/Organizations returns 404)
```

**Fix 2 — Pagination params in `cleanup_orphaned_test_records`:**
```python
# Before:
list_response = requests.get(config["list_endpoint"], headers=headers)

# After:
list_response = requests.get(
    config["list_endpoint"],
    params={"pageNumber": 1, "pageSize": 500},
    headers=headers,
)
```

**Fix 3 — Prefix alignment in `create_test_record_payload`:**
```python
# Before:
base_name = f"AUTO_{username}_{timestamp}_{test_run_id}"

# After:
base_name = f"AUTOTEST_{username}_{timestamp}_{test_run_id}"
```
`AUTOTEST_` now matches the prefix that `cleanup_orphaned_test_records` looks for, so bulk pagination records created by fixtures are automatically cleaned up at the start of the next test run.

### `tests/functional/adminFunctional/test_organizations_page_functional.py`

**Fix 1 — Name prefix:**
```python
# Before:
test_organization_name = f"Test Organization UI {datetime.now().strftime('%Y%m%d%H%M%S')}"

# After:
test_organization_name = f"AUTOTEST_Org_{datetime.now().strftime('%Y%m%d%H%M%S')}"
```

**Fix 2 — Added API teardown:**
The test now wraps its body in `try/finally`. After assertions complete, it:
1. Calls `/Organization/search?name=AUTOTEST_Org_...` to find the created org's ID
2. Calls `DELETE /Organization/Delete?id={id}` to remove it

If the ID lookup fails, the `AUTOTEST_Org_` prefix ensures `cleanup_orphaned_test_records` will catch it on the next run.

---

## How the Cleanup System Works Now

### Automatic cleanup (runs before each functional/pagination test)

`cleanup_orphaned_test_records("installations", headers, logger)` is called in fixture teardown. It:
1. Fetches `GET /Installations?pageNumber=1&pageSize=500` (sysadmin token = all installations)
2. Filters for names starting with `AUTOTEST_`
3. Deletes each match via `DELETE /Installations/delete?id={id}`

Same logic for `organizations` using the correct `/Organization` endpoint.

### Manual cleanup (run on demand)

```bash
python cleanup_test_data.py --dry-run   # safe preview
python cleanup_test_data.py             # live delete
```

Catches: `AUTOTEST_`, `AUTO_`, `DEL_` prefixes across Installations and Organizations.

---

## Why xdist Can Still Cause Orphaned Records

If a pytest-xdist worker crashes mid-test (OOM, timeout, SIGKILL), fixture teardown does not run. This means `AUTOTEST_` records can be left behind even with correct teardown logic.

This is expected and acceptable. The `AUTOTEST_` prefix + `cleanup_orphaned_test_records` running at the start of the next test run catches these automatically. The `cleanup_test_data.py` script is the safety net for longer-lived orphans.

---

## Reference: API Endpoint Summary

| Operation | Method | URL |
|---|---|---|
| List all installations | GET | `/api/Installations?pageNumber=1&pageSize=500` |
| Delete installation | DELETE | `/api/Installations/delete?id={guid}` |
| List all organizations | GET | `/api/Organization?pageNumber=1&pageSize=500` |
| Search organizations by name | GET | `/api/Organization/search?pageNumber=1&pageSize=10&name={name}` |
| Delete organization | DELETE | `/api/Organization/Delete?id={guid}` |

Note: `/api/Organizations` (plural) does **not** exist — returns 404.
