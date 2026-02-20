"""
cleanup_test_data.py — one-shot script to delete orphaned test records from the QA environment.

Deletes any Installations or Organizations whose name starts with a known
test prefix (AUTOTEST_, AUTO_, DEL_). Run from the repo root:

    python cleanup_test_data.py

Dry-run mode (lists what would be deleted without deleting):

    python cleanup_test_data.py --dry-run
"""
import sys
import requests
from dotenv import load_dotenv
from utilities.auth import get_auth_headers

load_dotenv()

# Standard automated test prefixes used by conftest.py helpers.
# "Test Organization UI" is a legacy prefix from test_add_organization before it
# was updated to use AUTOTEST_. Include it here for the one-time cleanup.
TEST_PREFIXES = ("AUTOTEST_", "AUTO_", "DEL_", "Test Organization UI")

RESOURCES = [
    {
        "label": "Installations",
        # pageNumber=1&pageSize=500 is required — without params the API returns only 1 record.
        # Sysadmin token bypasses org filtering and returns all installations.
        "list_url": "{api}/Installations?pageNumber=1&pageSize=500",
        "delete_url": "{api}/Installations/delete?id={id}",
        "id_field": "installationId",
        "name_field": "name",
    },
    {
        "label": "Organizations",
        # Endpoint is /Organization (singular) — /Organizations returns 404.
        "list_url": "{api}/Organization?pageNumber=1&pageSize=500",
        "delete_url": "{api}/Organization/Delete?id={id}",
        "id_field": "organizationId",
        "name_field": "name",
    },
]

import os
API_BASE_URL = os.getenv("API_BASE_URL", "").replace("\\x3a", ":")


def is_test_record(name: str) -> bool:
    return any(name.startswith(prefix) for prefix in TEST_PREFIXES)


def run_cleanup(dry_run: bool = False):
    headers = get_auth_headers()
    mode = "DRY RUN — nothing will be deleted" if dry_run else "LIVE — records will be deleted"
    print(f"\n{'=' * 60}")
    print(f"  WildXR QA Test Data Cleanup  ({mode})")
    print(f"{'=' * 60}\n")

    total_deleted = 0
    total_failed = 0

    for resource in RESOURCES:
        label = resource["label"]
        list_url = resource["list_url"].format(api=API_BASE_URL)
        delete_url_template = resource["delete_url"]
        id_field = resource["id_field"]
        name_field = resource["name_field"]

        print(f"--- {label} ---")

        try:
            response = requests.get(list_url, headers=headers, timeout=30)
            response.raise_for_status()
            all_records = response.json()
        except Exception as e:
            print(f"  ERROR fetching {label}: {e}")
            continue

        targets = [
            r for r in all_records
            if isinstance(r, dict) and is_test_record(r.get(name_field, ""))
        ]

        if not targets:
            print(f"  No test records found.\n")
            continue

        print(f"  Found {len(targets)} test record(s) to delete:")
        for record in targets:
            name = record.get(name_field, "(no name)")
            record_id = record.get(id_field)
            print(f"    {name}  [{record_id}]")

            if dry_run:
                continue

            delete_url = delete_url_template.format(api=API_BASE_URL, id=record_id)
            try:
                del_response = requests.delete(delete_url, headers=headers, timeout=30)
                if del_response.status_code in (200, 204):
                    print(f"      ✓ deleted")
                    total_deleted += 1
                else:
                    print(f"      ✗ failed ({del_response.status_code}): {del_response.text[:120]}")
                    total_failed += 1
            except Exception as e:
                print(f"      ✗ error: {e}")
                total_failed += 1

        print()

    if not dry_run:
        print(f"{'=' * 60}")
        print(f"  Done. Deleted: {total_deleted}   Failed: {total_failed}")
        print(f"{'=' * 60}\n")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    run_cleanup(dry_run=dry_run)
