# test_api_videos.py is a test file that contains the test cases for the API videos endpoints.
import pytest
import random
import math
import requests
from .api_base import APIBase
from utilities.utils import logger
from utilities.data_handling import DataLoader

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
    # @pytest.mark.github
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
        video_id = random_video_data["guid"]
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
    @pytest.mark.github
    def test_video_data_integrity(self):
        """
        Test video data meets both schema requirements and business rules.
        
        This test verifies:
        1. API response structure matches defined schema
        2. Response metadata is consistent (page counts, totals)
        3. Video objects contain valid data
        4. Required relationships are present (species, countries)
        5. Geographical data is valid
        """
        logger.info("\nTesting Video Data Integrity")
        
        # Test multiple pages to ensure consistent data quality
        page_size = 25
        pages_to_test = 2  # Test first two pages
        
        for page in range(1, pages_to_test + 1):
            response = self.api.get("/Videos", params={
                "pageNumber": page,
                "pageSize": page_size
            })
            
            assert response.status_code == 200, f"Failed to get page {page}"
            data = response.json()
            
            # 1. Schema Validation
            assert self.data_loader.validate_response(
                "video_list_response", 
                data
            ), "Response failed schema validation"
            
            # 2. Metadata Validation
            self._validate_pagination_metadata(data, page, page_size)
            
            # 3. Video Content Validation
            validation_errors = []
            for video in data["results"]:
                errors = self._validate_video_content(video)
                if errors:
                    validation_errors.extend(errors)

            # Report Results
            total_videos = len(data["results"])
            logger.info(f"\nValidated {total_videos} videos on page {page}")
            
            if validation_errors:
                logger.error("\nValidation Errors:")
                for error in validation_errors:
                    logger.error(error)
                pytest.fail(f"Found {len(validation_errors)} validation errors")
            else:
                logger.info("All videos passed validation")

    def _validate_pagination_metadata(self, data: dict, expected_page: int, expected_page_size: int) -> None:
        """
        Validate pagination metadata is consistent.
        
        Args:
            data: API response data
            expected_page: Expected page number
            expected_page_size: Expected page size
        """
        assert data["page"] == expected_page, \
            f"Wrong page number. Expected {expected_page}, got {data['page']}"
        
        assert data["pageSize"] == expected_page_size, \
            f"Wrong page size. Expected {expected_page_size}, got {data['pageSize']}"
        
        assert data["totalCount"] >= 0, \
            f"Invalid total count: {data['totalCount']}"
        
        assert data["pageCount"] == math.ceil(data["totalCount"] / data["pageSize"]), \
            "Page count doesn't match total records and page size"

    def _validate_video_content(self, video: dict) -> list[str]:
        """
        Validate individual video object content.
        
        Args:
            video: Video object to validate
            
        Returns:
            list[str]: List of validation error messages, empty if no errors
        """
        errors = []
        video_id = video.get('videoId', 'unknown')

        # Required Fields Validation
        required_fields = {
            'videoId': str,
            'name': str,
            'overview': str
        }
        
        for field, expected_type in required_fields.items():
            value = video.get(field)
            if not value:
                errors.append(f"Missing required field '{field}' for video {video_id}")
            elif not isinstance(value, expected_type):
                errors.append(
                    f"Invalid type for '{field}' in video {video_id}. "
                    f"Expected {expected_type.__name__}, got {type(value).__name__}"
                )

        # Video Status-based Validation
        if video.get('videoStatusId') == 2:  # Assuming 2 is "Published" status
            if not video.get('thumbnailUrl'):
                errors.append(f"Published video {video_id} missing thumbnail URL")
            
            if not video.get('species'):
                errors.append(f"Published video {video_id} missing species information")
            
            if not video.get('countryObtainedId'):
                errors.append(f"Published video {video_id} missing country information")

        # Map Marker Validation
        if video.get('mapMarkers'):
            marker_errors = self._validate_map_markers(video['mapMarkers'], video_id)
            errors.extend(marker_errors)

        # Species Validation
        if video.get('species'):
            species_errors = self._validate_species(video['species'], video_id)
            errors.extend(species_errors)

        return errors

    def _validate_map_markers(self, markers: list, video_id: str) -> list[str]:
        """
        Validate map marker data.
        
        Args:
            markers: List of map markers to validate
            video_id: ID of video containing markers
            
        Returns:
            list[str]: List of validation error messages
        """
        errors = []
        
        for idx, marker in enumerate(markers):
            # Required fields check
            if not marker.get('mapMarkerId'):
                errors.append(f"Map marker {idx} missing ID in video {video_id}")
            
            if not marker.get('name'):
                errors.append(f"Map marker {idx} missing name in video {video_id}")
                
            # Coordinate validation
            try:
                lat = float(marker.get('latitude', 0))
                lon = float(marker.get('longitude', 0))
                
                if not (-90 <= lat <= 90):
                    errors.append(
                        f"Invalid latitude {lat} in marker {idx} of video {video_id}"
                    )
                
                if not (-180 <= lon <= 180):
                    errors.append(
                        f"Invalid longitude {lon} in marker {idx} of video {video_id}"
                    )
            except (TypeError, ValueError):
                errors.append(
                    f"Invalid coordinate format in marker {idx} of video {video_id}"
                )
                
        return errors

    def _validate_species(self, species_list: list, video_id: str) -> list[str]:
        """
        Validate species data.
        
        Args:
            species_list: List of species to validate
            video_id: ID of video containing species
            
        Returns:
            list[str]: List of validation error messages
        """
        errors = []
        
        for idx, species in enumerate(species_list):
            # Required fields check
            required_fields = ['speciesId', 'name', 'scientificName']
            
            for field in required_fields:
                if not species.get(field):
                    errors.append(
                        f"Species {idx} missing {field} in video {video_id}"
                    )
            
            # Validate relationships
            if not species.get('iucnStatusId'):
                errors.append(
                    f"Species {idx} missing IUCN status in video {video_id}"
                )
                
            if not species.get('populationTrendId'):
                errors.append(
                    f"Species {idx} missing population trend in video {video_id}"
                )
                
            if not species.get('speciesCategoryId'):
                errors.append(
                    f"Species {idx} missing category in video {video_id}"
                )
        
        return errors
                
    @pytest.mark.api
    @pytest.mark.video
    def test_get_video_list(self):
        """
        Test the paginated video endpoint
        """
        response = self.api.get("/Videos", params={"pageNumber": 1, "pageSize": 25})
        
        # Validate response structure
        assert self.data_loader.validate_response(
            "video_list_response",
            response.json()
        ), "Response does not match expected schema"
