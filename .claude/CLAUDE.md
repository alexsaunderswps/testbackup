# CLAUDE.md — WildXR.test Repository

## Project Overview

This is a QA test automation repository for the **WildXR web portal**, a wildlife conservation technology platform built by Wildlife Protection Solutions (WPS). The test suite is maintained separately from the application code and runs against Azure-hosted QA environments.

- **Application under test:** WildXR web portal (React frontend, .NET/C# API backend)
- **QA web URL:** `https://wildxr-web-qa.azurewebsites.net/`
- **QA API URL:** `https://wildxr-api-qa.azurewebsites.net/api/`
- **Test repository:** Standalone — not colocated with application source code
- **CI trigger:** GitHub Actions via `repository_dispatch` (triggered when builds are pushed) and `workflow_dispatch` (manual)

## Tech Stack

- **Language:** Python 3.x
- **Test runner:** pytest
- **Browser automation:** Playwright (migrated from Selenium — do NOT introduce Selenium patterns)
- **API testing:** `requests` library with custom `APIBase` class
- **Schema validation:** `jsonschema`
- **Assertions:** `pytest-check` (soft assertions) and standard `assert`
- **Reporting:** `pytest-html`
- **Environment variables:** `python-dotenv` (`.env` file, never committed)
- **Playwright version:** Pinned in `requirements.txt` — keep local and CI versions matched

## Repository Structure

```
wildxr.test/
├── conftest.py                  # Root-level: shared fixtures, browser setup, CLI options
├── pytest.ini                   # Pytest configuration and marker registration
├── requirements.txt             # Pinned dependencies
├── .env                         # Local env vars (NOT in version control)
├── .github/
│   └── workflows/               # GitHub Actions CI workflows
├── page_objects/
│   ├── common/
│   │   └── base_page.py         # BasePage class — all page objects inherit from this
│   ├── authentication/
│   │   └── login_page.py        # LoginPage — handles authentication flows
│   └── dashboard/
│       ├── organizations_page.py
│       ├── videos_page.py
│       ├── map_markers_page.py
│       ├── countries_page.py
│       ├── users_page.py
│       ├── devices_page.py
│       └── ...                  # One file per page of the application
├── tests/
│   ├── api/
│   │   ├── api_base.py          # APIBase class — authentication, session, helpers
│   │   ├── test_api_connection.py
│   │   ├── test_api_videos.py
│   │   ├── test_api_schemas.py
│   │   └── ...
│   ├── ui/
│   │   ├── test_base_page_ui.py # Shared UI element checks (nav, admin, definitions)
│   │   ├── test_organizations_page.py
│   │   ├── test_videos_page.py
│   │   └── ...
│   └── functional/
│       └── test_login_functionality.py
├── test_data/
│   └── api/
│       └── qa/
│           ├── data/            # JSON test data files
│           └── schemas/         # JSON schema files for validation
└── utilities/
    ├── config.py                # Constants, timeouts, locator strings, log config
    ├── utils.py                 # Logger setup, HTMLReportLogger, test capture functions
    ├── data_handling.py         # DataLoader class for test data and schemas
    └── screenshot_manager.py    # Screenshot capture utility
```

## Reference Codebase

Snapshots of both the WildXR frontend and backend live inside `reference/`. These are **not** live application code — they are point-in-time copies kept here as a reference. Treat them as a strong guide, but verify against the running QA environment if anything seems mismatched.

```
reference/
├── wildxr.web/    # React/TypeScript frontend
└── wildxr.api/    # .NET/C# backend API + database schema
```

### Why It Matters

The reference codebase is the primary source of truth for:

- **Locator strategy** — read the JSX components to find exact button labels, ARIA roles, and form field labels before writing `page.get_by_role()` or `page.get_by_text()` calls
- **Column and field names** — table headers and form fields in the UI come directly from the component render output
- **API endpoint routes and HTTP methods** — controllers define the exact URL patterns and accepted verbs
- **Request/response shapes** — DTOs define the precise field names, types, and required vs optional fields for API test payloads and schema validation
- **Database schema and relationships** — entity models and SQL table definitions reveal what data exists and how it relates

### Key Paths — Frontend (`reference/wildxr.web/`)

```
reference/wildxr.web/src/
├── components/          # One folder per feature — maps directly to page objects
│   ├── video/           # VideoManagementPage, AddEditVideo, UploadVideoForm
│   ├── mapMarkers/      # ManageMapMarkersPage, AddEditMapMarker
│   ├── organzations/    # ManageOrganizationsPage, AddEditOrg  (note: typo in folder name)
│   ├── installations/   # ManageAddEditInstallation, InstallationsList
│   ├── devices/         # ManageDevicesPage, AddEditDevice
│   ├── panels/          # ManagePanelsPage, AddEditPanel
│   ├── videoCatalogues/ # VideoCataloguesPage, AddEditCatalogue
│   ├── species/         # ManageSpeciesPage, AddEditSpecies
│   ├── countries/       # ManageCountriesPage
│   ├── iucnStatus/      # ManageIUCNStatusPage
│   └── ...
├── api/                 # Axios wrappers — shows endpoint paths the frontend calls
│   ├── videos/videosApi.tsx
│   ├── mapMarkers/mapMarkersApi.tsx
│   ├── installations/installationApi.tsx
│   ├── devices/deviceApi.tsx
│   └── ...
├── context/             # Global state and data models
└── helpers/             # Auth, org ID resolution, utilities
```

### Key Paths — Backend (`reference/wildxr.api/`)

```
reference/wildxr.api/
├── WildXR.Api/
│   ├── Controllers/     # ASP.NET controllers — authoritative source for routes and HTTP methods
│   │   ├── InstallationsController.cs
│   │   ├── VideosController.cs
│   │   ├── MapMarkerController.cs
│   │   ├── DeviceController.cs
│   │   ├── OrganizationController.cs
│   │   └── ...          # One controller per resource
│   └── Dto/             # Data Transfer Objects — exact field names and types for API payloads
│       ├── InstallationDto.cs
│       ├── VideoDto.cs
│       ├── DeviceDto.cs
│       └── ...          # One DTO per resource (some resources have separate request DTOs)
├── WildXR.Data/
│   ├── Models/          # Entity Framework models — full field list including nullable vs required
│   │   ├── Installation.cs
│   │   ├── Video.cs
│   │   ├── Device.cs
│   │   └── ...
│   └── Context/
│       └── WildXRDbContext.cs  # EF DbContext — shows entity relationships and table mappings
└── WildXR.Data.Database/
    └── dbo/Tables/      # SQL CREATE TABLE definitions — canonical schema source
```

### How to Use It

Before writing a new page object:
1. Open the matching component in `reference/wildxr.web/src/components/` — this gives you exact text for `get_by_text()` and roles for `get_by_role()`
2. If a column name or button label isn't working, the component render output is the first place to check

Before writing a new API test:
1. Open the controller in `reference/wildxr.api/WildXR.Api/Controllers/` to confirm the route, HTTP method, and any authorization requirements
2. Open the corresponding DTO in `WildXR.Api/Dto/` to see exact request field names and types — this drives what goes into test payloads and schema files
3. Open the entity model in `WildXR.Data/Models/` to understand which fields are nullable (optional) vs required and what relationships exist
4. **Do NOT copy C# property names directly as JSON keys.** ASP.NET Core serializes PascalCase C# properties to camelCase JSON automatically (e.g., `VideoCatalogueId` → `videoCatalogueId`). Always verify actual key casing against a real API response before writing field assertions.

## Architecture and Design Patterns

### Page Object Model (POM)

Every page of the WildXR application has a corresponding page object class. All page objects inherit from `BasePage`.

- **BasePage** contains: navigation locators, common element locators (header, logout, pagination), shared verification methods (`verify_all_nav_elements_present`, `verify_page_title_present`), and navigation helper methods.
- **Page-specific classes** contain: page-specific element locators, table column verification, action button methods, and any page-unique functionality.
- **Table elements live in page-specific classes**, NOT in BasePage — because column headers vary per page.
- **Navigation elements live in BasePage** — because the nav bar is consistent across all pages.

### Fixtures over Inheritance for Tests

Tests use **pytest fixtures with dependency injection**, not class inheritance for shared test logic. This was a deliberate architectural decision:

- Common verification routines (nav elements, admin links, definition links) are provided via fixtures in `conftest.py`
- Test classes declare what fixtures they need through function parameter names
- pytest automatically discovers and injects fixtures — no imports needed from `conftest.py`
- Page-specific verification (tables, action buttons) is called directly on page objects

### Playwright Patterns (NOT Selenium)

The codebase has been migrated from Selenium to Playwright. Do NOT reintroduce Selenium patterns.

**Locator strategy:**
- Use Playwright's built-in locator methods: `page.locator()`, `page.get_by_text()`, `page.get_by_role()`
- Use `locator.filter()` with `has_text` for disambiguation
- Use `re.compile(r"^Exact Text$")` for exact text matching when needed
- Prefer CSS selectors over XPath for new code
- XPath is acceptable where existing patterns use it, but prefer modern selectors for new work

**Auto-waiting:**
- Playwright has built-in auto-waiting — do NOT add explicit waits unless there is a specific timing issue
- Timeouts are in milliseconds (not seconds like Selenium)

**Browser contexts:**
- Playwright uses browser contexts for isolation (lightweight, not full browser instances)
- The `conftest.py` manages browser lifecycle: playwright → browser → context → page
- Multiple user roles (admin, org admin) can run in separate contexts within the same browser

**Element verification pattern in page objects:**
```python
def get_some_element(self):
    """Get the element using Playwright locator."""
    return self.page.locator("selector")
```

### API Testing

- `APIBase` class handles authentication (Bearer token via `/Users/Authenticate`) and provides HTTP method wrappers
- Response time measurement is built into `APIBase`
- Tests validate: status codes, response structure, schema compliance, data integrity, pagination, and business rules
- `DataLoader` class loads test data and schemas from JSON files in `test_data/`
- API endpoints follow the pattern: `{QA_BASE_URL}/api/{Resource}`

### Six-Category Framework for API Test Cases

When designing API tests, consider:
1. **Missing information** — required fields omitted
2. **Wrong format** — invalid data types, malformed UUIDs
3. **Invalid references** — nonexistent IDs, orphaned relationships
4. **Authorization issues** — wrong role, expired token, no token
5. **Boundary values** — empty strings, zero, negative numbers, max lengths
6. **State/sequence issues** — duplicate creation, update nonexistent record, concurrency

### Document Gaps — Don't Test Them

**Do not write tests that validate known bugs or design gaps.** If the API accepts invalid data (e.g., missing required fields, no FK validation, nameless records), document the gap in a comment — in the test file header, in CLAUDE.md, or in Todo.md — and move on.

Tests should verify *intended* behavior. A test that passes only because something is broken:
- Provides false confidence (a green test ≠ correct behavior)
- Creates test artifacts that must be cleaned up forever
- Adds noise to CI results
- Must be rewritten when the gap is eventually fixed

When a gap is fixed, the comment is what guides you to write the real test. Until then, leave it out.

**Example:** The Installations API accepts a create request with no `name` (DB column is nullable, zero server-side validation). This is documented in the `test_api_installations.py` file header as a design gap — no test for it exists.

## Code Style and Conventions

### Readability over Cleverness

Write code that is **clear and readable**, not concise but obfuscated. If a one-liner requires mental gymnastics to parse, expand it. The codebase owner is learning — code should teach, not obscure.

### Naming

- **Test files:** `test_{page_name}_{test_type}.py` (e.g., `test_organizations_page.py`, `test_api_videos.py`)
- **Page objects:** `{page_name}_page.py` (e.g., `organizations_page.py`)
- **Classes:** PascalCase (`OrganizationsPage`, `TestAPIVideos`)
- **Methods/functions:** snake_case (`verify_all_nav_elements_present`, `get_video_data`)
- **Locator methods:** `get_{element_name}()` (e.g., `get_map_markers_core_tab()`)
- **Verification methods:** `verify_{what}()` returning `(bool, list)` tuple — success flag and missing items
- **Navigation methods:** `go_{page_name}_page()` (e.g., `go_countries_page()`)

### Docstrings

Every class and method should have a docstring. Use this format:
```python
def verify_page_title_present(self) -> bool:
    """Verify that the page title element is present on the current page.

    Returns:
        bool: True if title is found, False otherwise.
    """
```

Do NOT leave placeholder docstrings (`"""_summary_"""`). Fill them in or remove them.

### Logging

- Use the project's `logger` from `utilities.utils` — do not create new logger instances
- Log at appropriate levels: `logger.info()` for successful checks, `logger.error()` for failures, `logger.debug()` for setup/teardown detail
- Include context in log messages: what element, what page, what was expected vs actual
- Use separator lines (`logger.info("=" * 80)`) sparingly and consistently for test boundaries

### Error Handling

- Use `try/except` blocks in page object verification methods
- Catch specific exceptions, not bare `except:`
- Log errors before returning False
- Take screenshots on element-not-found failures (where applicable)
- In API tests, assert with descriptive failure messages:
  ```python
  assert response.status_code == 200, f"Expected 200, got {response.status_code} for {endpoint}"
  ```

### pytest Markers

Tests are organized with markers. Register new markers in `pytest.ini`. Common markers include:
- `@pytest.mark.UI` — browser-based UI tests
- `@pytest.mark.api` — API tests
- `@pytest.mark.functional` — functional/workflow tests
- `@pytest.mark.github` — tests that run in CI
- Page-specific markers: `@pytest.mark.video`, `@pytest.mark.organizations`, etc.
- `@pytest.mark.schema` — schema validation tests
- `@pytest.mark.connection` — API connectivity tests
- `@pytest.mark.slow` — long-running tests

### DRY Principles

- If a verification pattern is used across multiple pages, it belongs in `BasePage` or a shared fixture
- If it's page-specific (like table columns), it stays in the page object
- Don't duplicate locators — if an element appears on every page, define it once in `BasePage`
- Use `@pytest.mark.parametrize` for testing multiple similar cases (e.g., endpoint connectivity)

## Environment Configuration

### Required Environment Variables (in `.env`)

```
ADMIN_USERNAME=<admin username>
ADMIN_PASSWORD=<admin password>
QA_LOGIN_URL=https://wildxr-web-qa.azurewebsites.net/login
QA_BASE_URL=https://wildxr-api-qa.azurewebsites.net
```

These must also be configured as GitHub Secrets for CI runs.

### pytest CLI Options (defined in conftest.py)

- `--browser` — Browser to test with: `chromium`, `firefox`, `webkit` (default: `chromium`)
- `--headless` — Run headless: `true`/`false` (default: `false`, CI always uses `true`)
- `--private` — Private/incognito mode: `true`/`false`
- `--username` / `--password` — Override credentials (defaults to env vars)

## CI/CD — GitHub Actions

### Workflow Structure

The workflow runs on `ubuntu-latest` and:
1. Checks out the test repository
2. Sets up Python
3. Creates a virtual environment
4. Installs dependencies from `requirements.txt`
5. Runs `playwright install --with-deps chromium` (critical — installs browser binaries AND system deps)
6. Runs pytest with `--browser chromium --headless true`
7. Uploads test results as artifacts

### Key CI Notes

- Always pass `--browser chromium` (not `Chrome` or `chrome`) — Playwright only recognizes `chromium`, `firefox`, `webkit`
- Always include `playwright install --with-deps` after pip install — the Python package and browser binaries are separate
- Pin Playwright version in `requirements.txt` to match local development
- Environment variables (credentials, URLs) come from GitHub Secrets
- The workflow supports `workflow_dispatch` with inputs for markers and browser selection
- Use `-m` flag for marker-based test selection in CI

## Common Tasks

### Adding a New Page Object

1. Create `page_objects/dashboard/{page_name}_page.py`
2. Inherit from `BasePage`
3. Define page-specific locators as methods (`get_{element}()`)
4. Add verification methods (`verify_all_{page}_table_elements_present()`)
5. Add navigation methods if the page has sub-navigation

### Adding Tests for a New Page

1. Create `tests/ui/test_{page_name}_page.py`
2. Create a fixture in `conftest.py` that navigates to the page and returns the page object
3. Use shared fixtures (`verify_ui_elements`) for nav/admin/definition checks
4. Write page-specific tests for table elements, action buttons, page title
5. Register any new markers in `pytest.ini`

### Adding a New API Test

1. Add test class to appropriate file in `tests/api/` (or create new file)
2. Use `APIBase` for authenticated requests
3. Add test data to `test_data/api/qa/data/` if needed
4. Add schema file to `test_data/api/qa/schemas/` if doing schema validation
5. Follow the six-category framework for comprehensive coverage

## Important Warnings

- **Never commit `.env` files** — they contain credentials
- **Never introduce Selenium** — the codebase has been fully migrated to Playwright
- **Always review the full current codebase** before suggesting changes — avoid recreating existing functions or breaking other code
- **QA environment has known cross-environment issues** — the QA API once wrote to production storage containers. Be aware of environment boundaries.
- **DELETE is not implemented** on all API endpoints — use `TEST_` naming prefix for test data that can't be cleaned up
- **JWT tokens have 30-day lifetimes** — this is a known security concern, not a test bug
- **The pagination formula `Math.Abs(count / pageSize) + 1`** is a known bug (WILDXR-1907) in the Panels controller — the correct formula is `Math.Ceiling((double)count / pageSize)`

## Working with the Codebase Owner

The codebase owner (Alex) is a QA engineer transitioning from biology and education into software testing. When suggesting changes:

- Explain the *why* before the *how*
- Break complex changes into logical steps
- Use clear, descriptive variable and method names
- Prefer readable code over clever one-liners
- If making architectural suggestions, explain the tradeoffs
- Connect technical concepts to concrete examples in the codebase
- If something is wrong, say so directly — don't validate incorrect approaches