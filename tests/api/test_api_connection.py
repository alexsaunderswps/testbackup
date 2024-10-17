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

    @pytest.mark.api
    @pytest.mark.connection
    def test_get_video_by_id(self, random_video_data):
        video_id = random_video_data["ID"]
        expected_video_name = random_video_data["Name"]
        expected_video_overview = random_video_data["Overview"]
        
        response = self.api.get(f"/Videos/{video_id}/Details")
        response_time = self.api.measure_response_time(response)
        
        logger.info('-' * 80)
        logger.info(f"Testing Video ID: {video_id}")
        logger.info(f"Response time: {response_time}")
        logger.info('-' * 80)
        assert response.status_code == 200, f"Failed to get video by ID. Status code: {response.status_code}"
        assert response_time < 0.5, f"Response time is too high: {response_time}"
        
        content_type = response.headers.get("Content-Type")
        assert 'application/json' in content_type, f"Content-Type is not application/json. Content-Type: {content_type}"
        
        try:
            json_response = response.json()
            assert json_response["videoId"] == video_id
            logger.info(f"Video ID: {json_response['videoId']}")
            assert json_response["name"] == expected_video_name
            logger.info(f"Video Name: {json_response['name']}")
            assert json_response["overview"] == expected_video_overview
            logger.info(f"Video Overview: {json_response['overview']}")
        except requests.exceptions.JSONDecodeError:
            assert False, "Response is not in JSON format"
    
