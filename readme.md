# WildXR Test Suite

Automated test suite for the WildXR web portal — a wildlife conservation platform by Wildlife Protection Solutions (WPS). Tests run against Azure-hosted QA environments.

- **Web QA URL:** `https://wildxr-web-qa.azurewebsites.net/`
- **API QA URL:** `https://wildxr-api-qa.azurewebsites.net/api/`
- **Tech stack:** Python · pytest · Playwright (UI) · requests (API)

---

## Setup

### Prerequisites

- Python 3.x
- A `.env` file in the repository root (see below — never commit this file)

### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install --with-deps chromium
```

> **Note:** `playwright install --with-deps` is required separately from `pip install` — it installs browser binaries and system-level dependencies that the Python package alone does not provide.

### Environment Variables (`.env`)

```
SYS_ADMIN_USERNAME=<admin username>
SYS_ADMIN_PASSWORD=<admin password>
ORG_WPS_USERNAME=<WPS org admin username>
ORG_WPS_PASSWORD=<WPS org admin password>
QA_LOGIN_URL=https://wildxr-web-qa.azurewebsites.net/login
QA_WEB_BASE_URL=https://wildxr-web-qa.azurewebsites.net
API_BASE_URL=https://wildxr-api-qa.azurewebsites.net/api
API_TOKEN=<bearer token for API tests>
```

---

## Running Tests

### Basic Run

Run the entire test suite with default settings:

```bash
pytest
```

### CLI Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--browser` | `chromium`, `firefox`, `webkit` | `chromium` | Browser to run UI tests with |
| `--headless` | `true`, `false` | `false` | Run browser in headless mode |
| `--private` | `true`, `false` | `false` | Run in private/incognito mode |
| `--username` | string | env var | Override admin username |
| `--password` | string | env var | Override admin password |

Example with overrides:

```bash
pytest --browser firefox --headless true --username "testuser@example.com"
```

### Running by Marker

Use `-m` to target specific test categories. Surround compound expressions in quotes:

```bash
pytest -m api                         # All API tests
pytest -m UI                          # All UI tests
pytest -m "api and not slow"          # API tests, skipping slow ones
pytest -m "organizations or panels"   # Multiple feature areas
pytest -m debug                       # Tests tagged for debugging
```

### Parallel Execution (pytest-xdist)

The suite supports parallel execution via `pytest-xdist`. This is the recommended way to run large test sets — both locally and in CI.

```bash
# Use all available CPU cores
pytest -m api -n auto

# Use a specific number of workers (2 is a safe starting point)
pytest -m api -n 2

# Recommended: combine with --dist=loadfile
# This keeps all tests in the same file on the same worker,
# which prevents test-order-sensitive tests (pagination, data creation)
# from interfering with each other across workers.
pytest -m api -n auto --dist=loadfile
pytest -m UI --browser chromium --headless true -n auto --dist=loadfile
```

**How auth works under xdist:** The suite fetches exactly one JWT token per run regardless of how many parallel workers are used. The controller process acquires the token and distributes it to all worker nodes via `pytest_configure_node` — workers read it from a shared cache at startup. This means `-n 8` produces the same number of auth calls as `-n 1`.

**`--dist` strategy notes:**

| Strategy | Behaviour | When to use |
|----------|-----------|-------------|
| `loadfile` | All tests from the same file run on the same worker | Default recommendation — prevents cross-worker interference |
| `load` | Tests distributed freely across workers | Only if all tests are fully independent |
| `no` | No distribution (disables xdist) | Debugging parallel issues |

---

## Test Markers Reference

Markers are registered in `pytest.ini`. Use `-m <marker>` to select tests.

### Test Type

| Marker | Description |
|--------|-------------|
| `api` | API-focused tests |
| `UI` | Browser-based UI tests |
| `functional` | Functional / workflow tests |
| `integration` | Integration tests |
| `e2e` | End-to-end tests |
| `smoke` | Smoke tests |
| `regression` | Regression tests |
| `performance` | Performance-focused tests |

### Feature Area

| Marker | Description |
|--------|-------------|
| `video` | Video management page |
| `catalogue` | Video catalogues page |
| `map_markers` | Map markers page |
| `species` | Species page |
| `organizations` | Organizations page |
| `installations` | Installations page |
| `devices` | Devices page |
| `users` | Users page |
| `panels` | Panels endpoint/page |
| `panel_collections` | Panel collections page |
| `countries` | Countries page |
| `iucn_status` | IUCN Status page |
| `population_trend` | Population Trend page |
| `tags` | Tags page |

### Test Attribute

| Marker | Description |
|--------|-------------|
| `action` | Tests that find action elements (buttons, links) |
| `authentication` | Authentication-focused tests |
| `base` | Base page tests |
| `bulk` | Bulk operation tests |
| `conditional_data` | Tests that conditionally create test data |
| `connection` | API endpoint connectivity tests |
| `debug` | Tests tagged for active debugging |
| `edge_case` | Edge case and boundary tests |
| `grid` | Tests involving grid/card elements |
| `login` | Login flow tests |
| `navigation` | Navigation element tests |
| `page` | Page element tests |
| `pagination` | Pagination tests |
| `schema` | Schema validation tests |
| `search` | Search element tests |
| `security` | Authorization / security tests |
| `table` | Table manipulation tests |
| `verification` | Data verification tests |

### Credential / Data

| Marker | Description |
|--------|-------------|
| `valid_credentials` | Tests using valid credentials |
| `invalid_credentials` | Tests using invalid credentials |
| `succeeds` | Tests expected to succeed (used for positive-path assertions) |

### Browser-Specific

| Marker | Description |
|--------|-------------|
| `chrome` | Tests targeting Chrome-specific behaviour |
| `firefox` | Tests targeting Firefox-specific behaviour |
| `edge` | Tests targeting Edge-specific behaviour |

### Other

| Marker | Description |
|--------|-------------|
| `github` | Tests related to GitHub integration |
| `slow` | Long-running tests (exclude with `-m "not slow"`) |

---

## Project Structure

```
wildxr.test/
├── conftest.py                  # Shared fixtures, browser setup, CLI options, xdist auth hooks
├── pytest.ini                   # Pytest config, marker registration, xdist defaults
├── requirements.txt             # Pinned dependencies
├── .env                         # Local credentials (never committed)
├── .github/
│   └── workflows/
│       └── run-tests.yml        # GitHub Actions CI workflow
├── fixtures/                    # Page-specific pytest fixtures (one file per page)
│   ├── login_fixtures.py
│   ├── videos_fixtures.py
│   ├── organizations_fixtures.py
│   └── ...
├── page_objects/
│   ├── common/
│   │   └── base_page.py         # BasePage — all page objects inherit from this
│   ├── authentication/
│   │   └── login_page.py
│   ├── admin_menu/              # Organizations, Installations, Devices, Users, Panels, Panel Collections
│   ├── dashboard/               # Videos, Video Catalogues, Map Markers, Species
│   └── definitions_menu/        # Countries, IUCN Status, Population Trend, Tags
├── tests/
│   ├── api/
│   │   ├── api_base.py          # APIBase class (auth, session, HTTP helpers)
│   │   ├── test_api_connection.py
│   │   ├── test_api_videos.py
│   │   ├── test_api_organizations.py
│   │   ├── test_api_panels.py
│   │   ├── test_api_schema.py
│   │   └── test_api_authorization.py
│   ├── ui/
│   │   ├── dashboardUI/         # Videos, Video Catalogues, Map Markers, Species
│   │   ├── adminUI/             # Organizations, Installations, Devices, Users
│   │   └── definitionsUI/       # Countries, IUCN Status, Population Trend, Tags
│   └── functional/
│       ├── test_login_functionality.py
│       ├── test_organizations_page_functional.py
│       └── test_installations_page_functional.py
├── test_data/
│   └── api/qa/
│       ├── data/                # JSON test data (endpoints, videos)
│       └── schemas/             # JSON schema files for API response validation
├── utilities/
│   ├── auth.py                  # TokenCache singleton, get_auth_token(), get_auth_headers()
│   ├── config.py                # Timeouts, page sizes, locator strings, log config
│   ├── utils.py                 # Logger, HTMLReportLogger, test capture functions
│   ├── data_handling.py         # DataLoader — loads test data and schemas from JSON
│   └── search_mixins.py         # Mixins for search functionality
└── reference/
    ├── wildxr.web/              # Point-in-time snapshot of React/TypeScript frontend
    └── wildxr.api/              # Point-in-time snapshot of .NET/C# backend API
```

---

## CI/CD

Tests run automatically via GitHub Actions on `repository_dispatch` (triggered by application builds) and can be triggered manually via `workflow_dispatch`.

The CI workflow:
1. Checks out this repository
2. Sets up Python 3.x and installs dependencies
3. Runs `playwright install --with-deps chromium`
4. Runs API tests: `pytest -m api -n auto --dist=loadfile`
5. Runs UI tests: `pytest --browser chromium --headless true -m UI -n auto --dist=loadfile`

Credentials and environment variables are injected from GitHub Secrets. See `.github/workflows/run-tests.yml` for the full configuration.

---

## Reference Codebase

`reference/wildxr.web/` and `reference/wildxr.api/` contain point-in-time snapshots of the frontend and backend. These are the primary source for:

- **Locator strategy** — exact button labels and ARIA roles from JSX components
- **API routes and HTTP methods** — from ASP.NET controllers
- **Request/response field names** — from C# DTOs (note: PascalCase C# properties serialize to camelCase JSON automatically)
- **Database schema** — from Entity Framework models and SQL table definitions

Always verify against the live QA environment if a reference file seems out of date.
