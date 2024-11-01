# test_api_videos.py is a test file that contains the test cases for the API videos endpoints.
import pytest
import random
import requests
from .api_base import APIBase
from utilities.utils import logger
from utilities.data_loader import DataLoader
from test_data.api.qa.api_endpoints import EndpointManager

# Create module level dataloader instance for fixtures
data_loader = DataLoader()

@pytest.fixture(scope="session")
def random_video_data():
    return data_loader.get_random_video()

class TestAPIVideos:
    def setup_method(self):
        """
        Setup method to initialize the APIBase and DataLoader objects
        """
        self.api = APIBase()
        self.data_loader = DataLoader()

    @pytest.mark.api
    @pytest.mark.video
    @pytest.mark.github
    def test_get_video_collection_size(self):
        """
        Test to verify the total number of videos in the collection
        Raises:
            AssertionError: If the total number of videos in the collection does not match the expected value
        """
        response = self.api.get("/Videos", params={"pageNumber":1, "pageSize":25})
        
        try:
            json_response = response.json()
            endpoint_manager = self.data_loader.endpoint_manager
            expected_pages = self.data_loader.get_total_pages()
            expected_videos = self.data_loader.get_total_videos()
            
            fields_to_check = [
                ("pageCount", expected_pages),
                ("totalCount", expected_videos)
            ]
            
            for field, expected_value in fields_to_check:
                try:
                    assert json_response[field] == expected_value, (f"{field} does not match."
                                                                    f"Expected: {expected_value}, " 
                                                                    f"Actual: {json_response[field]}"
                                                                    )
                    logger.info("\nAPI Video Collection Size Test Summary:")
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
        """
        Test to verify the number of videos per page
        """
        errors = []
        page_size = self.data_loader.get_max_page_size()
        total_pages = self.data_loader.get_total_pages()
        total_videos = self.data_loader.get_total_videos()
        for page in range(1, total_pages + 1):
            response = self.api.get(
                "/Videos",
                params={"pageNumber": page, "pageSize": page_size}
            )

            if response.status_code == 200:
                data = response.json()
                actual_page_size = len(data['results'])
                
                # Calculate the expected page size(handle last page differently)
                expected_page_size = (
                    page_size if page < total_pages 
                    else total_videos % page_size
                )
            
                if actual_page_size != expected_page_size:
                    errors.append(
                        f"Page {page} has {actual_page_size} videos, "
                        f"expected {expected_page_size} videos"
                    )
                
                if data['page'] != page:
                    errors.append(
                        f"Page number mismatch."
                        f"Expected: {page}, Actual {data['page']} "
                    )
                    
                if data['pageSize'] != page_size:
                    errors.append(
                        f"Page size mismatch."
                        f"Expected: {page_size}, Actual {data['pageSize']} "
                    )
                
                if data['totalCount'] != total_videos:
                    errors.append(
                        f"Total video count mismatch."
                        f"Expected: {total_videos}, Actual {data['totalCount']} "
                    )
            else:
                errors.append(
                    f"Failed to get page {page}."
                    f"Status code: {response.status_code}"
                )
        # Log results
        if errors:
            logger.warning(f"Errors found in video count per page: {errors}")
        else:
            logger.info("\nAPI Video Count Per Page Test Summary:")
            logger.info('+' * 60)
            logger.info("No errors found in video count per page")
            logger.info('+' * 60)
        
        # Final assertion
        assert not errors, f"Errors found in video count per page: {errors}"
    
    @pytest.mark.api
    @pytest.mark.video
    def test_get_video_by_id(self, random_video_data):
        """
        Test to verify the details of a video by ID

        Args:
            random_video_data (_type_): Random video data to be used for the test 

        Raises:
            AssertionError: If the response status code is not 200
        """
        video_id = random_video_data["ID"]
        expected_video_name = random_video_data["Name"]
        expected_video_overview = random_video_data["Overview"]
        
        # Get endpoint info from data_loader
        
        enpoint_info = self.data_loader.get_endpoint_info("/Videos")
        threshold = enpoint_info["threshold"]
        
        response = self.api.get(f"/Videos/{video_id}/Details")
        response_time = self.api.measure_response_time(response)
        
        logger.info('*' * 80)
        logger.info(f"Testing Video ID: {video_id}")
        logger.info(f"Response time: {response_time:.3f} seconds")
        logger.info('*' * 80)
        assert response.status_code == 200, (
            f"Failed to get video by ID." 
            f"Status code: {response.status_code}"
        )
        assert response_time < threshold, f"Response time is too high: {response_time}"
        
        content_type = response.headers.get("Content-Type")
        assert 'application/json' in content_type, (
            f"Content-Type is not application/json." 
            f"Content-Type: {content_type}"
        )
        
        try:
            json_response = response.json()
            
            fields_to_check = [
                ("videoId", video_id),
                ("name", expected_video_name),
                ("overview", expected_video_overview)
            ]
            
            for field, expected_value in fields_to_check:
                try:
                    assert json_response[field] == expected_value, (
                        f"{field} does not match. "
                        f"Expected: {expected_value}, "
                        f"Actual: {json_response[field]}"
                    )
                    logger.info("\nAPI Video Random ID Test Summary:")
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
    def test_get_all_videos_by_id(self):
        """
        Test to verify the details of all videos by ID
        """
        logger.info("\nAPI Test All Videos by ID:")
        video_data_list = self.data_loader.get_video_data()
        endpoint_info = self.data_loader.get_endpoint_info("/Videos")
        threshold = endpoint_info["threshold"]
        
        validation_errors = []
        
        for video_data in video_data_list:
            video_id = video_data["ID"]
            expected_video_name = video_data["Name"]
            expected_video_overview = video_data["Overview"]
            
            logger.info('-' * 80)
            logger.info(f"Testing Video ID: {video_id}")
            logger.info(f"Expected Name: {expected_video_name}")
            logger.info(f"Expected Overview: {expected_video_overview}")
            logger.info('-' * 80)
            
            try:
                # Make API request
                response = self.api.get(f"/Videos/{video_id}/Details")
                response_time = self.api.measure_response_time(response)
        
                # Log response details
                logger.info(f"Response time: {response_time:.3f} seconds")
                logger.info(f"Status Code: {response.status_code}")
        
                # Validate response code
                if response_time >= threshold:
                    validation_errors.append(
                        f"Video {video_id}: Response time is too high: {response_time:.3f}"
                    )
                
                # Validate content tyoe
                content_type = response.headers.get("Content-Type")
                if 'application/json' not in content_type: 
                    validation_errors.append(
                    f"Content-Type is not application/json for Video {video_id}." 
                    f"Content-Type: {content_type}"
                    )
                    continue
            
                # Validate response data
                json_response = response.json()
                
                # Check each field
                fields_to_check = [
                    ("videoId", video_id),
                    ("name", expected_video_name),
                    ("overview", expected_video_overview)
                ]
                
                for field, expected_value in fields_to_check:
                    actual_value = json_response.get(field)
                    if actual_value != expected_value:
                        validation_errors.append(
                            f"Video {video_id}: {field} does not match. "
                            f"Expected: {expected_value}, Actual: {actual_value}"
                        )
                    else:
                        logger.info(f"✓ {field}: matches {json_response[field]}")
        
            except Exception as e:
                validation_errors.append(f"Video {video_id}: Error during validation: {str(e)}")
                logger.error(f"Error during validation: {str(e)} of Video: {video_id}")
                
        # After all videos are processed, report results
        total_videos = len(video_data_list)
        failed_videos = len(validation_errors)
        
        logger.info("\n ")
        logger.info("\nValidation Summary:")
        logger.info(f"Total Videos: {total_videos}")
        logger.info(f"Failed Videos: {failed_videos}")
        logger.info("\n ")
        
        if validation_errors:
            logger.error("\nFailed Videos:")
            for error in validation_errors:
                logger.error(error)
            raise AssertionError(f"Failed Videos: {failed_videos}")    
            