# Authentication Refactor Summary

## Problem
The test suite was experiencing 401 authentication errors because:
- Fixtures were using a **hardcoded bearer token** from the `.env` file
- The hardcoded token was invalid/expired
- This caused all API calls in fixtures to fail with 401 errors

## Solution
Refactored authentication to use **dynamic token generation with session caching**:

### 1. Created Shared Authentication Utility
**File:** `utilities/auth.py`

New utility provides:
- `get_auth_token()` - Get cached or generate new token
- `get_auth_headers()` - Get headers with Authorization Bearer token
- `refresh_auth_token()` - Force refresh the token
- `clear_token_cache()` - Clear cached token
- `TokenCache` - Singleton class that caches token during test session

**Benefits:**
- Token generated once per test session (cached)
- Automatic authentication on first use
- Reduces API auth calls
- Consistent across all tests

### 2. Updated All Fixtures
Updated the following fixtures to use dynamic tokens:

**Admin Menu Fixtures:**
- `fixtures/admin_menu/installations_fixtures.py`
- `fixtures/admin_menu/organizations_fixtures.py`

**Dashboard Fixtures:**
- `fixtures/dashboard/videocatalogues_fixtures.py`
- `fixtures/dashboard/mapmarkers_fixtures.py`
- `fixtures/dashboard/videos_fixtures.py`
- `fixtures/dashboard/species_fixtures.py`

**Changes Made:**
```python
# OLD - Hardcoded token from .env
api_token = os.getenv("API_TOKEN")
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# NEW - Dynamic token with caching
from utilities.auth import get_auth_headers
headers = get_auth_headers()
```

### 3. Updated Functional Tests
**File:** `tests/functional/adminFunctional/test_installations_page_functional.py`

- Removed all references to hardcoded `API_TOKEN`
- Updated to use `get_auth_headers()` and `get_auth_token()`
- Consistent authentication across all test methods

### 4. Updated API Test Base
**File:** `tests/api/api_base.py`

- Simplified to use shared `get_auth_token()` utility
- Removed duplicate authentication logic
- Now uses the same cached token as fixtures

## Token Caching Behavior
- **First call:** Token is generated via API authentication
- **Subsequent calls:** Cached token is reused (within same test session)
- **Benefits:** Faster tests, fewer auth API calls, consistent tokens

## Environment Variables
The following .env variables are still used but differently:
- `API_BASE_URL` - API endpoint (still required)
- `SYS_ADMIN_USERNAME` - For dynamic token generation (still required)
- `SYS_ADMIN_PASSWORD` - For dynamic token generation (still required)
- `API_TOKEN` - **NO LONGER USED** (can be removed or kept for reference)

## Testing the Changes
Run your tests as normal:
```bash
pytest tests/ -v
```

The authentication will happen automatically on the first API call, and the token will be cached for the duration of the test session.

## If Token Expires Mid-Session
If you encounter 401 errors mid-session (unlikely but possible):
```python
from utilities.auth import refresh_auth_token

# Force refresh the token
token = refresh_auth_token()
```

## Files Modified
1. ✅ `utilities/auth.py` - NEW FILE
2. ✅ `fixtures/admin_menu/installations_fixtures.py`
3. ✅ `fixtures/admin_menu/organizations_fixtures.py`
4. ✅ `fixtures/dashboard/videocatalogues_fixtures.py`
5. ✅ `fixtures/dashboard/mapmarkers_fixtures.py`
6. ✅ `fixtures/dashboard/videos_fixtures.py`
7. ✅ `fixtures/dashboard/species_fixtures.py`
8. ✅ `tests/functional/adminFunctional/test_installations_page_functional.py`
9. ✅ `tests/api/api_base.py`

## Migration Complete
All authentication now uses dynamic token generation with session caching. No more 401 errors from expired hardcoded tokens!
