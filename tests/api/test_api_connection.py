# test_api_connection.py is a test file that contains the test cases for the API connection.
import pytest
import random
import requests
from pytest_check import check
from .api_base import APIBase
from utilities.utils import logger
from .test_data import VIDEO_DATA

# Basic Connection tests

class TestAPIConnection:
    def setup_method(self):
        self.api = APIBase()
    
    @pytest.fixture(scope="class")
    def random_video_data(self):
        return random.choice(VIDEO_DATA)
    
    # Paramertized test for valid status code and response time from multiple endpoints
    @pytest.mark.api
    @pytest.mark.connection
    @pytest.mark.parametrize("endpoint, threshold", [
    ("/Videos", 0.4),
    ("/VideoCatalogue", 0.3),
    ("/MapMarker", 0.3),
    ("/Countries", 0.3),
    ("/IUCNStatus", 0.3),
    ("/Organization", 0.3),
    ("/PopulationTrend", 0.3),
    ("/Species", 0.3),
    ("/Site", 0.3),
    ("/SpeciesCategory", 0.3),
    ("/Tag", 0.3),
    ("/Users", 0.3),
    ("/Organization", 0.3),
    ])
    def test_api_connection_parametrized(self, endpoint, threshold):
        response = self.api.get(endpoint)
        response_time = self.api.measure_response_time(response)
        logger.info('-' * 80)
        logger.info(f"For {endpoint} - Response time: {response_time}, Status code: {response.status_code}")
        logger.info('-' * 80)
        assert response.status_code == 200, f"Failed to get response from {endpoint}. Status code: {response.status_code}"
        assert response_time < threshold, f"Response time is too high: {response_time}"
        logger.info(f"{endpoint} response time: {response_time:.3f} seconds")
