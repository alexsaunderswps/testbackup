# test_api_connection.py is a test file that contains the test cases for the API connection.
import pytest
from .api_base import APIBase
from utilities.utils import logger
from .enpoint_data import ENDPOINT_DATA

# Basic Connection tests

class TestAPIConnection:
    def setup_method(self):
        self.api = APIBase()
    
    # Paramertized test for using valid authorization, valid status code and response time from multiple endpoints
    @pytest.mark.github
    @pytest.mark.api
    @pytest.mark.connection
    @pytest.mark.parametrize("endpoint", ENDPOINT_DATA.ENDPOINTS)
    @pytest.mark.parametrize("auth_type, expected_status_code", [
        ('valid', 200),
        ('invalid', 401),
        ('none', 401)
    ])
    def test_api_connection_parametrized_valid(self, endpoint, auth_type, expected_status_code):
        response = self.api.get(endpoint, auth_type)
        response_time = self.api.measure_response_time(response)
        logger.info('-' * 80)
        logger.info(f"For {endpoint} & {auth_type} - Response time: {response_time:.3f} seconds, Status code: {response.status_code}")
        logger.info('-' * 80)
        threshold = ENDPOINT_DATA.THRESHOLDS.get(endpoint, 0.3) # Default threshold is 0.3 seconds
        assert response.status_code == expected_status_code, (
            f"Unexpected status code for {endpoint} with {auth_type} auth. "
            f"Expected {expected_status_code}, got {response.status_code}"
        )
        assert response_time < threshold, (
            f"Response time for {endpoint} with {auth_type} auth is too high. "
            f"Expected < {threshold}, got {response_time:.3f}"
        )

