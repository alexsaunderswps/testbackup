# WildXR API — Response Shape Evolution: Why Some GET Endpoints Return Different Shapes

**Written:** 2026-02-24
**Context:** Discovered while writing `test_api_organizations.py` and auditing existing API tests

---

## The Pattern at a Glance

Not all GET list endpoints in this API return the same shape. There are two distinct shapes:

| Shape | Example | Starts with |
|---|---|---|
| **Plain array** | `GET /api/Organization`, `GET /api/Device`, `GET /api/Installations` | `[` |
| **ResponseDto wrapper** | `GET /api/Panels`, `GET /api/Videos`, any `/search` endpoint | `{` |

**The rule that holds everywhere:**
- Every `/search` endpoint returns a **ResponseDto wrapper**
- Most basic `GET /{Resource}` list endpoints return a **plain array**
- The exception is `GET /Panels` and `GET /Videos`, which return a ResponseDto from their basic list endpoint too

---

## What Each Shape Actually Looks Like

### Plain array (e.g. GET /api/Organization, GET /api/Device)

The response body starts with `[`. The root of the document **is** the list:

```json
[
  {
    "organizationId": "a1b2c3d4-0000-0000-0000-000000000001",
    "name": "Wildlife Protection Solutions",
    "rowVersion": "AAAAAAAAB+E="
  },
  {
    "organizationId": "e5f6a7b8-0000-0000-0000-000000000002",
    "name": "Test Organization - Used for Automation Tests",
    "rowVersion": "AAAAAAAAB+I="
  }
]
```

There is **no total count**, no page number, no page count. You cannot calculate how many total pages exist from this response alone.

In Python tests, you access data like this:

```python
data = response.json()
first_item = data[0]            # index directly into the list
name = data[0]["name"]
count = len(data)               # how many on THIS page only — not the total
```

### ResponseDto wrapper (e.g. GET /api/Panels, any /search endpoint)

The response body starts with `{`. The root is an object with pagination metadata, and the records live inside a `"results"` key:

```json
{
  "page": 1,
  "pageSize": 10,
  "pageCount": 3,
  "totalCount": 27,
  "orderBy": null,
  "sortOrder": null,
  "results": [
    {
      "panelId": "c3d4e5f6-0000-0000-0000-000000000003",
      "name": "Jaguar Panel",
      "newFlag": false,
      "contents": 5
    }
  ]
}
```

You know the total: `data["totalCount"]` is 27, `data["pageCount"]` is 3. The frontend can render "Page 1 of 3" without making additional requests.

In Python tests:

```python
data = response.json()
results = data["results"]       # must go through "results" key first
first_item = results[0]
total = data["totalCount"]      # pagination metadata available
```

**Common mistake:** If you do `data[0]` on a ResponseDto response, you get a `TypeError: list indices must be integers or slices, not str` — the root is a dict, not a list. Going the other direction (`data["results"]` on a plain array) gives `TypeError: list indices must be integers or slices, not str` for the same reason.

---

## The Full Endpoint Map

| Controller | Endpoint | Response Shape | Notes |
|---|---|---|---|
| Organization | `GET /api/Organization` | **Plain array** | No total count |
| Organization | `GET /api/Organization/search` | ResponseDto | Has total count, name filter |
| Organization | `GET /api/Organization/{id}/Details` | Single object | — |
| Installations | `GET /api/Installations` | **Plain array** | No total count |
| Installations | `GET /api/Installations/search` | ResponseDto | Has total count, name filter |
| Installations | `GET /api/Installations/{id}/details` | Single object | — |
| Device | `GET /api/Device` | **Plain array** | No total count |
| Device | `GET /api/Device/search` | ResponseDto | Has total count, name filter |
| Device | `GET /api/Device/{id}/Details` | Single object | — |
| MapMarker | `GET /api/MapMarker` | **Plain array** | No search endpoint |
| MapMarker | `GET /api/MapMarker/{id}/Details` | Single object | — |
| Users | `GET /api/Users` | **Plain array** | No search endpoint |
| Users | `GET /api/Users/{id}/Details` | Single object | — |
| **Videos** | `GET /api/Videos` | **ResponseDto** | Exception — wraps basic list |
| **Videos** | `GET /api/Videos/search` | ResponseDto | — |
| Videos | `GET /api/Videos/{id}/Details` | Single object | — |
| **Panels** | `GET /api/Panels` | **ResponseDto** | Exception — wraps basic list |
| **Panels** | `GET /api/Panels/search` | ResponseDto | — |
| Panels | `GET /api/Panels/{id}/Details` | Single object | — |

---

## Why the Inconsistency Exists

This is an evolutionary inconsistency, not a deliberate design choice. Here is what most likely happened as the API was developed:

### Stage 1 — Early controllers (Organization, Installations, Device, Users, MapMarkers)

The first controllers were written with the simplest possible approach. `return Ok(result)` where `result` is already a `List<SomeDto>` is one line of code. The frontend could render whatever it received. At this stage, pagination was probably a "nice to have" rather than a requirement — the datasets were small enough that showing everything on one request was acceptable.

```csharp
// Simplest thing that works — just hand the list to the serializer
return Ok(result);
```

No wrapper needed. No total count. The `pageNumber` and `pageSize` query parameters exist on these endpoints, but the response never tells you how many total records exist or how many pages that implies.

### Stage 2 — The /search endpoints are added

When the frontend needed a search bar with working pagination (showing "Page 1 of 3" requires knowing the total count), a plain array was no longer sufficient. The `ResponseDto` class was introduced — or already existed — and the search endpoints were built with it from the start:

```csharp
var responseDto = new ResponseDto<List<OrganizationDto>>
{
    Page    = searchQuery.PageNumber,
    PageCount = (int)Math.Ceiling((double)count / searchQuery.PageSize),
    PageSize  = searchQuery.PageSize,
    TotalCount = count,
    Results   = result
};
return Ok(responseDto);
```

The existing plain-array basic GET endpoints were **not changed** — presumably because the frontend was already depending on them in their current shape, and changing them would have been a breaking change requiring frontend updates too.

### Stage 3 — Newer controllers (Videos, Panels)

By the time Videos and Panels were written, the `ResponseDto` pattern was clearly established in the codebase and had been proven out on the search endpoints. Whoever wrote these controllers applied it to the basic GET list too — there was no reason not to. The result is a cleaner, more consistent interface:

```csharp
// Panels basic GET — returns ResponseDto even without a filter
return Ok(new ResponseDto<List<PanelDto>>
{
    Page      = pageNumber, PageSize = pageSize,
    PageCount = (int)Math.Ceiling((double)count / pageSize),
    TotalCount = count,
    Results   = result
});
```

The older controllers were likely not retroactively updated because doing so would break any frontend or API consumer that was already calling those endpoints and expecting a plain array.

---

## What This Means When Writing Tests

### Always verify the actual response shape before writing assertions

The source of truth is the controller, not the DTO or the test expectation. Check `return Ok(...)` in the relevant controller in `reference/wildxr.api/WildXR.Api/Controllers/`:

- `return Ok(result)` where `result` is a `List<T>` → plain array
- `return Ok(responseDto)` or `return Ok(new ResponseDto<...> { ... })` → ResponseDto wrapper
- `return Ok(someDto)` → single object

### Always test both the basic GET and the /search endpoint separately

They have different shapes, different behaviours, and different failure modes:

| Concern | Basic `GET` | `/search` |
|---|---|---|
| Response shape | Different (plain array vs ResponseDto) | — |
| Total count available | No | Yes |
| Name filtering | No | Yes |
| Auth filtering | Varies | Often yes (e.g. org admins see only their data) |
| Pagination metadata | Not returned | Returned |

A bug on one will not necessarily appear on the other. If a deployment accidentally breaks the search endpoint's ResponseDto wrapping, the basic GET test would still pass. If the search endpoint's name filter stops working, no amount of testing the basic GET will catch it.

For resources that have both, write tests for both — as `test_api_organizations.py` does with `TestAPIOrganizationsGet`.

### The shape assertion is worth keeping explicitly

`test_api_organizations.py` has `test_get_list_returns_array` which asserts `isinstance(data, list)`. This looks like a trivial check but it serves as a sentinel: if the backend team ever wraps the plain-array endpoints in a ResponseDto (a reasonable cleanup they might do), this test will fail immediately and loudly rather than causing a cascade of confusing `KeyError`/`TypeError` failures in downstream tests.

---

## Quick Reference for New API Test Files

```python
# Plain array endpoint (Organization, Installations, Device, MapMarker, Users basic GET)
response = self.api.get("/Organization", params={"pageNumber": 1, "pageSize": 10})
data = response.json()
assert isinstance(data, list)           # root is the list
first = data[0]                         # index directly
name = data[0]["name"]

# ResponseDto endpoint (any /search, Videos, Panels basic GET)
response = self.api.get("/Organization/search", params={"name": "a", ...})
data = response.json()
assert isinstance(data, dict)           # root is the wrapper object
results = data["results"]               # records are inside "results"
total = data["totalCount"]              # pagination metadata available
first = results[0]
```
