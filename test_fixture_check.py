# test_fixture_check.py
import pytest
from fixtures.installations import installations_pagination_test_data

def test_pagination_fixture(installations_pagination_test_data):
    """
    Test that the installations pagination fixture creates data correctly.
    
    Args:
        pagination_test_data: The fixture we're testing
    """
    # The fixture value is what was yielded (the installation_ids list)
    installation_ids = installations_pagination_test_data
    
    # Print information about what was created
    print(f"\nCreated {len(installation_ids)} test installations")
    
    if installation_ids:
        print(f"First installation ID: {installation_ids[0]}")
    
    # Basic assertions to verify it worked
    assert installation_ids, "No installations were created"
    assert len(installation_ids) > 0, "Empty list of installation IDs"
    
    # The teardown/cleanup will happen automatically after this test completes