Scaffold a new page object, fixture, and UI test file for the page named: $ARGUMENTS

Follow these steps exactly, in order:

## Step 1 — Identify the Route

1. Open `reference/wildxr.web/src/App.tsx`. Find the route for this page.
   - **Warning:** The URL path is NOT always predictable from the page name. Example: the Videos page is at `path="/"`, not `/videos`. Check the actual `path=` value.
2. Open `reference/wildxr.web/src/components/common/Nav.tsx`. Find the nav link `href` for this page.
   - The fixture `goto()` URL must match the nav link href, not the page name.

Record:
- `path=` value from App.tsx
- `href=` from Nav.tsx
- Full fixture URL: `os.environ["QA_WEB_BASE_URL"] + "{path}"`

## Step 2 — Read the React Component

Find the component file in `reference/wildxr.web/src/components/{feature}/`. Read it.

Extract:
- The exact text of the page title (for `verify_page_title_present`)
- The exact text of all column headers in any tables (for `verify_all_{page}_table_elements_present`)
- The exact text of all action buttons (Add, Edit, Delete, etc.)
- Any tab labels if the page has tabs
- ARIA roles used on key elements

These exact strings go into your page object locators — do not guess or paraphrase them.

## Step 3 — Check Where the Page Belongs

Determine which section the page belongs to:
- **Dashboard** → `page_objects/dashboard/` and `tests/ui/dashboardUI/`
- **Admin menu** → `page_objects/admin_menu/` and `tests/ui/adminUI/`
- **Definitions menu** → `page_objects/definitions_menu/` and `tests/ui/definitionsUI/`

Check `page_objects/common/base_page.py` to see if this page's nav link is already defined as a locator. If not, you will need to add it.

## Step 4 — Review Existing Patterns

Read one existing page object from the same section (e.g., `page_objects/admin_menu/organizations_page.py`) to confirm:
- Class structure and BasePage inheritance
- How locator methods are named (`get_{element}()`)
- How verification methods return `(bool, list)` tuples
- How navigation methods work (`go_{page}_page()`)

Read the corresponding fixture file (e.g., `fixtures/organizations_fixtures.py`) to confirm the fixture pattern.

Read the corresponding test file (e.g., `tests/ui/adminUI/test_organizations_page_ui.py`) to confirm the test class structure.

## Step 5 — Create the Page Object

Create `page_objects/{section}/{page_name}_page.py`:

```python
"""Page object for the {Page Name} page."""
import re
from page_objects.common.base_page import BasePage
from utilities.utils import logger


class {PageName}Page(BasePage):
    """{Page Name} page — {brief description}."""

    # -----------------------------------------------------------------
    # Locators
    # -----------------------------------------------------------------

    def get_page_title(self):
        """Get the page title element."""
        return self.page.get_by_role("heading", name="{Exact Title Text}")

    def get_{column}_column(self):
        """Get the {column} column header."""
        return self.page.get_by_role("columnheader", name="{Exact Column Text}")

    # -----------------------------------------------------------------
    # Verification
    # -----------------------------------------------------------------

    def verify_all_{page}_table_elements_present(self) -> tuple[bool, list]:
        """Verify all expected table column headers are present.

        Returns:
            tuple[bool, list]: (True if all found, list of missing element names)
        """
        missing = []
        elements = {
            "{Column Name}": self.get_{column}_column(),
            # ... one entry per column
        }
        for name, locator in elements.items():
            try:
                locator.wait_for(state="visible", timeout=5000)
                logger.info(f"Found table element: {name}")
            except Exception:
                logger.error(f"Missing table element: {name}")
                missing.append(name)
        return len(missing) == 0, missing
```

Rules:
- Every locator method must have a docstring
- Use exact strings from the React component (Step 2)
- Use `page.get_by_role()` and `page.get_by_text()` over CSS selectors where possible
- Use `re.compile(r"^Exact Text$")` for exact text matching when needed

## Step 6 — Add Nav Locator to BasePage (if missing)

If the page's nav link is not already in `page_objects/common/base_page.py`, add:
- A locator method `get_{page}_nav_link()` in the appropriate nav section
- A `go_{page}_page()` navigation method

Read `base_page.py` first to understand where to insert without breaking existing patterns.

## Step 7 — Create the Fixture File

Create `fixtures/{page_name}_fixtures.py`:

```python
"""Fixtures for the {Page Name} page tests."""
import os
import pytest
from page_objects.{section}.{page_name}_page import {PageName}Page
from utilities.utils import logger


@pytest.fixture
def {page_name}_page(logged_in_page):
    """{Page Name} page fixture — navigates to page and returns page object(s).

    Args:
        logged_in_page: Pre-authenticated Playwright page(s) from conftest.

    Returns:
        List[{PageName}Page]: Page object(s) for the {Page Name} page.
    """
    pages = []
    base_url = os.environ.get("QA_WEB_BASE_URL", "")
    for page in logged_in_page:
        page.goto(base_url + "{path from Step 1}", wait_until="networkidle")
        pages.append({PageName}Page(page))
        logger.info(f"Navigated to {Page Name} page")
    return pages
```

## Step 8 — Create the Test File

Create `tests/ui/{section}/test_{page_name}_page_ui.py`:

```python
"""UI tests for the {Page Name} page."""
import pytest
from utilities.utils import logger


@pytest.mark.UI
@pytest.mark.{feature_marker}
class Test{PageName}PageUI:
    """UI tests for the {Page Name} page — nav, title, table elements, action buttons."""

    def test_nav_elements_present(self, {page_name}_page, verify_ui_elements):
        """Verify all navigation elements are present on the {Page Name} page."""
        verify_ui_elements.verify_nav_elements({page_name}_page)

    def test_page_title_present(self, {page_name}_page):
        """Verify the {Page Name} page title is present."""
        for page in {page_name}_page:
            assert page.verify_page_title_present(), "{Page Name} page title not found"

    def test_table_elements_present(self, {page_name}_page):
        """Verify all expected table columns are present on the {Page Name} page."""
        for page in {page_name}_page:
            success, missing = page.verify_all_{page_name}_table_elements_present()
            assert success, f"Missing table elements: {missing}"
```

Add additional tests for:
- Admin section links (if applicable): `verify_ui_elements.verify_admin_elements(...)`
- Definition section links (if applicable): `verify_ui_elements.verify_definition_elements(...)`
- Action buttons (Add, Edit, Delete)
- Any tabs or secondary navigation

## Step 9 — Register New Markers

If you used a marker not already in `pytest.ini`, add it to the `markers =` block.

## Step 10 — Verify

Check your work:
- Page object file exists and inherits from BasePage
- Fixture file exists and uses `logged_in_page`
- Test file exists and imports from the fixture file's path
- All exact strings match what's in the React component (not paraphrased)
- The `goto()` URL uses the path from App.tsx, not a guessed URL

Report back with:
- Files created or modified
- The exact page title and column names extracted from the component
- The route and fixture URL used
- Any additions to `base_page.py`
- Any markers added to `pytest.ini`
