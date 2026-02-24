Scaffold a new API test file for the resource named: $ARGUMENTS

Follow these steps exactly, in order:

## Step 1 — Read the Reference Files

1. Find the controller in `reference/wildxr.api/WildXR.Api/Controllers/` matching the resource name. Read it.
   - Note: the exact route(s), HTTP method(s), and any `[Authorize]` or role attributes
2. Find the DTO(s) in `reference/wildxr.api/WildXR.Api/Dto/` matching the resource. Read them.
   - **IMPORTANT:** C# PascalCase properties serialize to camelCase JSON automatically. `VideoCatalogueId` → `videoCatalogueId`. Never copy property names verbatim as JSON keys.
3. Find the entity model in `reference/wildxr.api/WildXR.Data/Models/`. Read it.
   - Note which fields are nullable (optional) vs required and any relationships.
4. Check if an existing API test file in `tests/api/` already covers this resource. If one exists, open it and extend it rather than creating a new file.

## Step 2 — Review Existing Patterns

Read one existing API test file (e.g., `tests/api/test_api_videos.py` or `tests/api/test_api_organizations.py`) to confirm:
- How `APIBase` is imported and used
- How `DataLoader` is used for test data
- How soft assertions (`pytest_check`) are used
- The class and method naming conventions

## Step 3 — Design Test Cases Using the Six-Category Framework

Before writing any code, list the test cases you will write:

1. **Happy path** — valid requests that should succeed
2. **Missing required fields** — omit each required field one at a time
3. **Wrong format** — invalid types, malformed UUIDs, bad date formats
4. **Invalid references** — nonexistent IDs, orphaned relationships
5. **Authorization** — unauthenticated request, wrong-role request (if applicable)
6. **Boundary values** — empty string, zero, negative numbers, max-length strings
7. **State/sequence** — duplicate creation, update nonexistent record

Only include categories that apply to this resource. Skip categories that are not testable given the endpoint's behavior.

## Step 4 — Write the Test File

Create `tests/api/test_api_{resource_name}.py` following this structure:

```python
"""
API tests for the {Resource} endpoint.

Endpoint: {METHOD} {route}
"""
import pytest
from tests.api.api_base import APIBase
from utilities.utils import logger


@pytest.mark.api
@pytest.mark.{resource_marker}
class TestAPI{ResourceName}:
    """{Resource} endpoint tests covering happy path, validation, and edge cases."""

    def test_{resource}_returns_200(self, api_base):
        """Verify the {resource} endpoint returns HTTP 200 with valid input."""
        ...
```

Rules:
- Use `api_base` fixture (already defined in `conftest.py` or `api_base.py`)
- Use `pytest_check` for soft assertions within a test; use `assert` for hard stops
- Include a descriptive failure message in every `assert`: `assert x == y, f"Expected {y}, got {x}"`
- Log test steps with `logger.info()` and failures with `logger.error()`
- Name test methods `test_{what_is_being_tested}_{expected_outcome}` (e.g., `test_create_with_missing_name_returns_400`)
- Add markers: at minimum `@pytest.mark.api` and a feature-area marker

## Step 5 — Register New Markers

If you used a marker that is not already in `pytest.ini`, add it to the `markers =` block with a brief description.

## Step 6 — Verify

After writing, re-read the controller to confirm:
- Route strings match what you tested
- HTTP methods match (`GET` vs `POST` vs `PUT` vs `DELETE`)
- Response shape expectations are consistent with what the DTO defines (remembering camelCase serialization)

Report back with:
- The file(s) created or modified
- A summary of the test cases added and which six-category buckets they cover
- Any gaps (categories that were skipped and why)
- Any markers added to `pytest.ini`
