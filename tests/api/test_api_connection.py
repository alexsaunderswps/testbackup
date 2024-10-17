# test_api_connection.py is a test file that contains the test cases for the API connection.
import pytest
import requests
from pytest_check import check
from .api_base import APIBase
from utilities.utils import logger

# Basic Connection tests

class TestAPIConnection:
    def setup_method(self):
        self.api = APIBase()
    
    @pytest.mark.api
    @pytest.mark.connection
    def test_api_connection_videos(self):
        response = self.api.get("/api/Videos")
        response_time = self.api.measure_response_time(response)
        logger.info('-' * 80)
        logger.info(f"Response time: {response_time}")
        logger.info('-' * 80)
        assert response.status_code == 200
        assert response_time < 0.5, f"Response time is too high: {response_time}"
    
    @pytest.mark.api
    @pytest.mark.connection
    def test_api_connection(self):
        response = self.api.get("/api/VideoCatalogue")
        response_time = self.api.measure_response_time(response)
        logger.info('-' * 80)
        logger.info(f"Response time: {response_time}")
        logger.info('-' * 80)
        assert response.status_code == 200
        assert response_time < 0.5, f"Response time is too high: {response_time}"
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.connection
    def test_get_video_by_id(self, video_id="5a618fcb-f36b-4a6d-976b-276b8714e354"):
        response = self.api.get(f"/api/Videos/{video_id}/Details")
        response_time = self.api.measure_response_time(response)
        logger.info('-' * 80)
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
            assert json_response["name"] == "#01 Test Video"
            logger.info(f"Video Name: {json_response['name']}")
            assert "overview" in json_response
            logger.info(f"Video Overview: {json_response['overview']}")
        except requests.exceptions.JSONDecodeError:
            assert False, "Response is not in JSON format"