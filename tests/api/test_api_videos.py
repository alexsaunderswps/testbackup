# test_api_videos.py is a test file that contains the test cases for the API videos endpoints.
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
    
    @pytest.mark.api
    @pytest.mark.connection
    def test_get_video_by_id(self, random_video_data):
        """_summary_

        Args:
            random_video_data (_type_): _description_

        Raises:
            AssertionError: _description_
        """
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
            
            fields_to_check = [
                ("videoId", video_id),
                ("name", expected_video_name),
                ("overview", expected_video_overview)
            ]
            
            for field, expected_value in fields_to_check:
                try:
                    assert json_response[field] == expected_value, f"{field} does not match. Expected: {expected_value}, Actual: {json_response[field]}"
                    logger.info(f"{field}: {json_response[field]}")
                except AssertionError as e:
                    logger.error(str(e))
                    raise
                except KeyError:
                    logger.error(f"Field: {field} not found in response")
                    raise
                
        except requests.exceptions.JSONDecodeError:
            logger.error("Response is not in JSON format")
            raise AssertionError("Response is not in JSON format")
        except Exception as e:
            logger.error(f"Unexpected error occured: {str(e)}")
            raise
    
    @pytest.mark.api
    @pytest.mark.connection
    @pytest.mark.slow
    @pytest.mark.parametrize("video_data", VIDEO_DATA)
    def test_get_all_videos_by_id(self, video_data):
        """_summary_

        Args:
            random_video_data (_type_): _description_

        Raises:
            AssertionError: _description_
        """
        video_id = video_data["ID"]
        expected_video_name = video_data["Name"]
        expected_video_overview = video_data["Overview"]
        
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
            
            fields_to_check = [
                ("videoId", video_id),
                ("name", expected_video_name),
                ("overview", expected_video_overview)
            ]
            
            for field, expected_value in fields_to_check:
                try:
                    assert json_response[field] == expected_value, f"{field} does not match. Expected: {expected_value}, Actual: {json_response[field]}"
                    logger.info(f"{field}: {json_response[field]}")
                except AssertionError as e:
                    logger.error(str(e))
                    raise
                except KeyError:
                    logger.error(f"Field: {field} not found in response")
                    raise
                
        except requests.exceptions.JSONDecodeError:
            logger.error("Response is not in JSON format")
            raise AssertionError("Response is not in JSON format")
        except Exception as e:
            logger.error(f"Unexpected error occured: {str(e)}")
            raise
            
    
