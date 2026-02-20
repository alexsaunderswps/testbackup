# WILDXR-1868 — Installations Panel Collection Field: Test Coverage Summary

Generated: 2026-02-20

---

## Ticket Summary

**WILDXR-1868 (WXRP — Update Installations for Catalogues on Front End)**

Frontend counterpart to the API changes in WILDXR-1867. The Installation management UI
was updated to expose a panel collection selector, allowing admins to view and assign
which panel collection an installation uses. The field defaults to "WildXR Panels."

**Related tickets:** WILDXR-1867 (API backing), WILDXR-1864 (PanelDto), WILDXR-1866 (VideoDatabaseDto), WILDXR-1870 (panels page)

---

## What Was Already in Place

The `installations_page.py` page object already had the panel collection field locators
from a prior session, anchored to the hidden input name rather than fragile `.nth()`
positional indexing:

```python
def get_installations_select_panel_collection_label(self):
    return self.page.get_by_text("Select Panel Collection")

def get_installations_select_panel_collection_dropdown(self):
    return self.page.locator(
        "div:has(> input[name='panelCollectionId']) .css-19bb58m"
    )
```

This locator pattern (`div:has(> input[name='panelCollectionId'])`) is the preferred
approach for all React Select dropdowns on this form — it is immune to index shifts
caused by conditional fields (startup video, favorites) appearing or disappearing.

---

## What Was Added (2026-02-20)

### `page_objects/admin_menu/installations_page.py`

Five new methods added:

| Method | Purpose |
|---|---|
| `get_add_installation_page_title()` | `locator("h1", has_text="Add Installation")` |
| `get_edit_installation_page_title()` | `locator("h1", has_text="Installation Details")` |
| `navigate_to_first_installation_edit()` | Clicks first row + `wait_for(state="visible")` on the heading — SPA-safe navigation |
| `get_panel_collection_selected_value_text()` | Reads displayed React Select value via `[class*='singleValue']` partial class match |
| `verify_panel_collection_field_present()` | `(bool, List[str])` tuple checking label + dropdown |

**Key locator detail — reading the selected value:**

```python
def get_panel_collection_selected_value_text(self):
    return self.page.locator(
        "div:has(> input[name='panelCollectionId'])"
    ).locator("[class*='singleValue']")
```

React Select renders the chosen option in an element whose class contains `singleValue`.
Using `[class*='singleValue']` (partial match) avoids breakage if React Select's
generated class hash changes between library upgrades.

### `tests/ui/adminUI/test_installations_page_ui.py`

Two new tests added at the end of `TestInstallationsPageUI`:

1. **`test_installation_edit_form_panel_collection_field_present`**
   - Navigates to the first installation's edit form
   - Verifies "Select Panel Collection" label and React Select dropdown are both visible
   - Skips (not fails) if no installation rows exist in QA

2. **`test_installation_edit_form_panel_collection_has_selected_value`**
   - Navigates to the first installation's edit form
   - Verifies the dropdown shows a selected value (non-empty `singleValue` element visible)
   - Does not assert the exact name — QA installations may have been updated to a
     non-default collection; the failure message calls out the expected default
     ("WildXR Panels") if the field is found empty
   - Skips if no installation rows exist in QA

### `tests/functional/adminFunctional/test_installations_page_functional.py`

`_create_installation_via_ui` helper updated to explicitly select the panel collection
between the video catalogue and automatic download mode steps:

```python
# Select panel collection (WILDXR-1868)
panel_collection_dropdown = ip.get_installations_select_panel_collection_dropdown()
panel_collection_dropdown.click()
ip.page.get_by_text("Test Panel Collection - Used for Automation Tests", exact=True).click()
```

Previously the helper relied on the form's default population, which obscured
whether the panel collection field was being set at all.

---

## Persistent Test Data Created in QA

> ⚠️ These records must not be deleted — the functional test suite depends on them.

| Name | Type | Organization | Notes |
|---|---|---|---|
| `Test Panel Collection - Used for Automation Tests` | Panel Collection | Test Organization - Used for Automation Tests | Used by `_create_installation_via_ui` |
| `Test Panel - Used for Automation Tests` | Panel | (assigned to above collection) | Required because the Panel Collection form requires at least one panel |

**Existing persistent test data this joins:**

| Name | Type | Used by |
|---|---|---|
| `Test Organization - Used for Automation Tests` | Organization | `_create_installation_via_ui`, `test_add_installation` |
| `Test Organization Catalogue` | Video Catalogue | `_create_installation_via_ui`, `test_add_installation` |

---

## QA Approach Coverage

From the WILDXR-1868 ticket's QA Approach, here is what is covered by automated tests
and what remains manual or deferred:

| QA Approach Item | Status | Notes |
|---|---|---|
| Verify panel collection field is visible on Installations page | ✅ Automated | `test_installation_edit_form_panel_collection_field_present` |
| Confirm default value displays as "WildXR Panels" | ✅ Automated (partial) | `test_installation_edit_form_panel_collection_has_selected_value` verifies non-empty; does not assert exact name |
| Change panel collection, save, refresh, verify persists | ⬜ Not automated | Requires modifying existing QA data; excluded to avoid unintentional side effects |
| Check form validation — empty/invalid panel collection | ⬜ Not automated | WILDXR-1909 established that the API has no server-side validation; UI also does not enforce required; documenting actual behavior is the appropriate response |
| Verify UI label/tooltip communicates clearly | ✅ Manual | Label "Select Panel Collection" is verified by automated test; no tooltip present in component |
| Responsive layout | ⬜ Not automated | Outside current test pattern scope |
| No regression on saving other installation fields | ✅ Automated (indirect) | `test_add_installation` functional test exercises Save with all fields including the panel collection |

---

## Relevant Reference Files

- `reference/wildxr.web/src/components/installations/AddEditInstallation.tsx` — form component; panel collection field at line 328–353
- `reference/wildxr.api/WildXR.Api/Controllers/PanelCollectionsController.cs` — API endpoints (GET, Create, Update, Delete, SetPanels, AddPanel, RemovePanel)
- `reference/wildxr.api/WildXR.Api/Controllers/InstallationsController.cs` — installation API; `ResolvePanelCollectionIdAsync` is defined but not called (see WILDXR-1909)
