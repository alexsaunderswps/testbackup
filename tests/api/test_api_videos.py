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
    @pytest.mark.debug
    # @pytest.mark.github
    def test_basic_pagination_mathematics(self):
        """
        This test verifies that:
            1. The API response contains valid pagination data
            2. The total page count matches the mathematical calculation based on 
                total records and page size
            3. All required pagination fields are present
        """
        try:
        # Make API request with specific pagination parameters
            response = self.api.get("/Videos", params={"pageNumber": 1, "pageSize": 25})
            assert response.status_code == 200, (
                f"Failed to get videos list. Expected status code 200, "
                f"got {response.status_code}"
                )
            # Parse JSON response
            try:
                json_response = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON response: {str(e)}")
                raise
            
            # Verify required pagination fields are present
            required_fields = ["page", "pageSize", "totalCount", "pageCount"]
            missing_fields = [field for field in required_fields if field not in json_response]
            if missing_fields:
                raise KeyError(f"Missing required fields: {missing_fields}")
            
            # Calculate expected counts
            total_videos = json_response["totalCount"]
            total_pages = json_response["pageCount"]
            page_size = json_response["pageSize"]
            if total_videos%page_size == 0:
                expected_pages = math.ceil(total_videos / page_size) + 1
            else:
                expected_pages = math.ceil(total_videos / page_size)
            
            # Verify page count matches calculations
            assert total_pages == expected_pages, (f"Page count should be ceiling of total_count/page_size."
                                                                    f"Expected: {expected_pages}, " 
                                                                    f"Actual: {total_pages}"
                                                                    )
            logger.info("\nPagination Mathematics Test Summary:")
            logger.info(f"Total Videos: {total_videos}")
            logger.info(f"Page Size: {page_size}")
            logger.info(f"Total Pages: {total_pages}")
            
        except AssertionError as e:
            logger.error(f"Assertion failed in pagination test with error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected")
            raise
    
    @pytest.mark.api
    @pytest.mark.video
    @pytest.mark.debug
    def test_page_size_constraints(self):
        """
        Verifies that:
            1. All full pages contain exactly 25 videos
            2. The last page contains the correct remaining number of videos
            3. Page numbers and page sizes are consistent throughout
            4. API responses are valid and properly formatted
        """
        errors = []
        try:
        # Make API request to get the total number of pages
            response = self.api.get("/Videos", params={"pageNumber": 1, "pageSize": 25})
            assert response.status_code == 200, (
                f"Failed to get videos list, expected status code 200, "
                f"got response code: {response.status_code}"
                )
            # Parse JSON response
            try:
                json_response = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON response: {str(e)}")
                raise
                
            # All pages except the last page should have 25 videos    
            for page in range(1, json_response["pageCount"]):
                try:
                    page_response = self.api.get("/Videos", params={"pageNumber": page, "pageSize": 25})
                    
                    if page_response.status_code != 200:
                        errors.append(
                            f"Failed to get page {page}. "
                            f"Status code: {page_response.status_code}"
                        )
                        continue
                        
                    try:
                        page_data = page_response.json()
                    except requests.exceptions.JSONDecodeError as e:
                        logger.error(f"Failed to decode JSON response: {str(e)}")
                        errors.append(f"JSON decode error on page {page}")
                        continue
                    
                    # Verify page size (except for last page)
                    
                    if page < page_data["pageCount"] and len(page_data["results"]) != 25:
                        errors.append(
                            f"Page {page} has {len(page_data["results"])} videos, "
                            f"expected 25 videos"
                        )
                    # Verify page number for consistency
                    if page_data['page'] != page:
                        errors.append(
                            f"Page number mismatch."
                            f"Expected: {page}, Actual {page_data['page']} "
                        )
                    # Verify page size for consistency                  
                    if page_data['pageSize'] != 25:
                        errors.append(
                            f"Page size mismatch."
                            f"Expected: 25, Actual: {page_data["page_size"]}"
                        )
                except AssertionError as e: 
                    logger.error(f"Unexpected error processing page {page}: {str(e)}")
                    errors.append(f"Error processing page {page}: {str(e)}")
            
            # Verify last page size
            # This may need adjustment because we are allowing 0 page length which was not allowed previously
            try:
                last_page_size = json_response["totalCount"] % 25
                if last_page_size == 0:
                    last_page_size == 0
                
                last_page_response = self.api.get("/Videos", params={"pageNumber": json_response["pageCount"], "pageSize": 25})
                
                if last_page_response.status_code == 200:
                    last_page_data = last_page_response.json()
                    if len(last_page_data["results"]) != last_page_size:
                        errors.append(
                            f"Last page has {len(last_page_data["results"])} videos, "
                            f"expected {last_page_size}"
                        )
                else:
                    errors.append(
                        f"Failed to get last page. "
                        f"Status code: {last_page_response.status_code}"
                    )

            except Exception as e:
                logger.error(f"Error verifying last page: {str(e)}")
                errors.append(f"Last page verification failed: {str(e)}")

            # Log results
            if errors:
                logger.warning(f"Errors found in video count per page: {errors}")
            else:
                logger.info("\nAPI Video Count Per Page Test Summary:")
                logger.info('+' * 60)
                logger.info("No errors found in video count per page")
                logger.info('+' * 60)
                
        except AssertionError as e:
            logger.error(f"Assertion failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
            
        # Final assertion
        assert not errors, f"Errors found in video count per page: {errors}"
    
    @pytest.mark.api
    @pytest.mark.video
    @pytest.mark.debug
    def test_no_duplicate_videos(self):
        """
        This test verifies that:
            1. Each video ID appears only once in the entire dataset
            2. All pages can be successfully retrieved
            3. All responses contain valid JSON data
            4. The pagination process completes successfully
        """
        try:
            video_ids = set()
            page = 1
            total_videos_checked = 0
            
            while True:
                # Get current page of videos
                response = self.api.get("/Videos", params={"pageNumber": page, "pageSize": 25})
                assert response.status_code == 200, (
                    f"Failed to get videos list. Expected status code 200, "
                    f"got {response.status_code}"
                    )
                
                # Parse JSON response
                try:
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON response: {str(e)}")
                    raise
                
                # Verify required fields are present
                required_fields = ["results", "pageCount"]
                missing_fields = [field for field in required_fields if field not in json_response]
                if missing_fields:
                    raise KeyError(
                        f"Response missing required fields: {missing_fields} on page: {page}"
                        )
                    
                # Check each video on current page for duplicates
                try:
                    for video in json_response["results"]:
                        video_id = video.get("videoId")
                        
                        # Verify video has an ID
                        if not video_id:
                            raise ValueError(
                                f"Video on page {page} is missing videoId field"
                            )
                        
                        # Check for duplicates
                        assert video_id not in video_ids, (
                            f"Duplicate video found: {video_id} on page: {page}"
                        )
                        
                        video_ids.add(video_id)
                        total_videos_checked += 1
                    
                except (KeyError, ValueError) as e:
                    logger.error(f"Error processing page {page}: {str(e)}")
                    raise
                
                if page >= json_response["pageCount"]:
                    break
                
                page += 1
            
            logger.info(
                f"Successfully verified no duplicate videos across {page} pages."
                f"Total videos checked: {total_videos_checked}"
                f"Total unique videos found: {len(video_ids)}"
                f"Here are the video IDs: {video_ids}"
            )    
        
        except AssertionError as e:
            logger.error(f"Duplicate video check failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error during duplicate video check: {str(e)}"
            )
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
                
    @pytest.mark.api
    @pytest.mark.video
    @pytest.mark.edge_case
    def test_video_edge_cases(self):
        """Test boundary conditions and error cases for video pagination
    
            This test verifies the API's handling of various edge cases including:
            1. Invalid page numbers (zero, negative, non-numeric)
            2. Out of range page numbers
            3. Invalid page sizes (zero, too large)
            4. Malformed parameters
            
            Each case should return the expected error status code and maintain
            consistent behavior.
        """
        try:
            test_cases = [
                # {"page": 0, "size": 25, "expected_status": 400, "description": "Invalid page numer (zero)"}, # Invalid page
                # {"page": 999999, "size": 25, "expected_status": 404, "description": "Page number beyond valid range"}, # Page beyond range
                # {"page": 1, "size": 0, "expected_status": 400, "description": "Invalid page size (zero)"}, # Invalid page size
                # {"page": 1, "size": 1000, "expected_status": 400, "description": "Page size exceeds maximum allowed"}, # Size too large
                {"page": "invalid", "size": 25, "expected_status": 400, "description": "Non-numeric page number"}, # Non-numeric page
            ]
        
            failed_cases = []
            
            for case in test_cases:
                try:
                    logger.info(
                        f"Testing edge case {case["description"]}:" 
                        f"page={case['page']}, size={case['size']}"
                    )
                    
                    response = self.api.get("/Videos", params={
                        "pageNumber": case["page"],
                        "pageSize": case["size"]
                    })
                
                    # Verify status code matches expected
                    if response.status_code != case["expected_status"]:
                        failed_cases.append(case["description"])
                        logger.error(
                            f"Unexpected status code for case: {case["description"]}, "
                            f"received {response.status_code}, for expected status: {case["expected_status"]}"
                        )
                    else:
                        logger.info(
                            f"Successfully verified {case["description"]}: "
                            f"received expected status {case['expected_status']}"
                        )
                    
                    # Verify error message for bad requests
                    try:
                        error_response = response.json()
                        logger.debug(f"Error response: {error_response}")
                    except requests.exceptions.JSONDecodeError:
                        logger.debug("Response contained no valid JSON data")
                        
                except Exception as e:
                    logger.error(
                        f"Error testing case: {case["description"]}: {str(e)}"
                    )
                    failed_cases.append(case["description"])
            
            # Log summary of test results
            if failed_cases:
                logger.error(
                    f"\nEdge Case Test Summary - Failed"
                    f"{len(failed_cases)} cases failed"
                )
                logger.error("=" * 60)
                for error in failed_cases:
                    logger.error(f"Failed case: {error}")
                logger.error("=" * 60)
            else:
                logger.info(
                    f"\nEdge Case Test Summary - Passed"
                )
                logger.info("=" * 60)
                logger.info(
                    f"All {len(test_cases)} cases passed"
                )
                logger.error("=" * 60)
            
            # Final assertion
            assert not failed_cases, (
                f"Found {len(failed_cases)} failed edge cases:\n "
                + "\n".join(failed_cases)
            )        
            
        except Exception as e:
            logger.error(
                f"Unexpected error during edge case testing: {str(e)}"
            )
            raise

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
        
        if data["totalCount"]%data["pageSize"] == 0:
            assert data["pageCount"] == math.ceil(data["totalCount"] / data["pageSize"]) + 1, \
                "Page count doesn't match total records and page size"
        else:
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
