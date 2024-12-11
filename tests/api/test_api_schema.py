import pytest
import requests
from jsonschema import validate, ValidationError # type: ignore
from .api_base import APIBase
from utilities.utils import logger
from utilities.data_handling import DataLoader


# Create module level dataloader instance for fixtures
data_loader = DataLoader()

@pytest.fixture(scope='session')
def video_schema_data():
    schema_file = data_loader.schema_path / "data_schemas" / "video_data.json"
    try:
        return data_loader._load_json_file(schema_file)
    except Exception as e:
        logger.error(f"Failed to load video schema: {str(e)}")
        raise

@pytest.fixture(scope='session')
def random_video_data():
    return data_loader.get_random_video()

class TestAPISchemas:
    def setup_method(self):
        """_summary_
        """
        self.api = APIBase()
        self.data_loader = DataLoader()
        
        
    @pytest.mark.schema
    def test_video_get_schema(self, video_schema_data, random_video_data):
        """_summary_
        """
        video_id = random_video_data['guid']

        # Get video data using random video id
        response = self.api.get(f"/Videos/{video_id}/Details")
        assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}"
        
        try:
            json_response = response.json()
        except requests.exceptions.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {str(e)}")
            raise
            
        # Validate against schema
        try:
            validate(instance=json_response, schema=video_schema_data)
            logger.info(f"Schema validation passed for video id: {video_id}")
        except ValidationError as e:
            logger.error(f"Schema validation failed for video id: {video_id}: {str(e)}")
            raise