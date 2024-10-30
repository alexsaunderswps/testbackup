# test_api_videos.py is a test file that contains the test cases for the API videos endpoints.
import pytest
import random
import requests
from .api_base import APIBase
from utilities.utils import logger
from .test_data import VIDEO_DATA
from .endpoint_data import ENDPOINT_DATA

# Basic Connection tests

class TestAPIConnection:
    def setup_method(self):
        self.api = APIBase()
    
    @pytest.fixture(scope="class")
    def random_video_data(self):
        return random.choice(VIDEO_DATA)
    
    @pytest.mark.api
    @pytest.mark.video
    @pytest.mark.debug
    def test_get_video_collection_size(self):
        response = self.api.get("/Videos", params={"pageNumber":1, "pageSize":25})
        try:
            json_response = response.json()
            fields_to_check = [
                ("pageCount", ENDPOINT_DATA.TOTAL_PAGES),
                ("totalCount", ENDPOINT_DATA.TOTAL_VIDEOS)
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
    @pytest.mark.video
    def test_video_count_per_page(self):
        errors = self.verify_video_count_per_page()
        assert not errors, f"Errors found in video count per page: {errors}"
    
    @pytest.mark.api
    @pytest.mark.video
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
        
        logger.info('*' * 80)
        logger.info(f"Testing Video ID: {video_id}")
        logger.info(f"Response time: {response_time:.3f} seconds")
        logger.info('*' * 80)
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
    @pytest.mark.video
    @pytest.mark.slow
    @pytest.mark.github
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
            
    def verify_video_count_per_page(self):
        errors = []
        page_size = ENDPOINT_DATA.MAX_PAGE_SIZE
        for page in range(1, ENDPOINT_DATA.TOTAL_PAGES + 1):
            response = self.api.get("/Videos", params={"pageNumber": page, "pageSize": page_size})
            
            if response.status_code == 200:
                data = response.json()
                actual_page_size = len(data['results'])
                expected_page_size = page_size if page < ENDPOINT_DATA.TOTAL_PAGES else ENDPOINT_DATA.TOTAL_VIDEOS % page_size

                if actual_page_size != expected_page_size:
                    errors.append(f"Page {page} has {actual_page_size} videos, expected {expected_page_size} videos")
                    
                if data['page'] != page:
                    errors.append(f"Page number mismatch. Expected: {page}, Actual: {data['page']}")
                
                if data['pageSize'] != page_size:
                    errors.append(f"Page size mismatch. Expected: {page_size}, Actual: {data['pageSize']}")
                
                if data['totalCount'] != ENDPOINT_DATA.TOTAL_VIDEOS:
                    errors.append(f"Total video count mismatch. Expected: {ENDPOINT_DATA.TOTAL_VIDEOS}, Actual: {data['totalCount']}")
            else:
                errors.append(f"Failed to get page {page}. Status code: {response.status_code}")
        if errors:
            logger.warning(f"Errors found in video count per page: {errors}")
        else:
            logger.info('=== ' * 20)
            logger.warning("No errors found in video count per page")
            logger.info('=== ' * 20)
        return errors