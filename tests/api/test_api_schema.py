import pytest
import random
import requests
from jsonschema import validate, ValidationError
from utilities.utils import logger
from utilities.data_loader import DataLoader
from test_data.api.qa.api_endpoints import EndpointManager

# Create module level dataloader instance for fixtures
data_loader = DataLoader()

@pytest.fixture(scope='session')
def video_schema_data():
    return data_loader.get_video_schema_data()

@pytest.fixture(scope='session')
def random_video_data():
    return data_loader.get_random_video()

class TestAPISchemas:
    def setup_method(self):
        """_summary_
        """
        self.api = APIBase()
        self.data_loader = DataLoader()
        
    @pytest.mark.api
    @pytest.mark.schema
    def test_video_get_schema(self, video_schema_data, random_video_data):
        """_summary_
        """
        video_id = random_video_data['id']

        # Get video data using random video id
        response = self.api.get(f"/Videos/{video_id}/Details")
        
        try:
            json_response = response.json()
        except requests.exceptions.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {str(e)}")
            
        # Validate against schema
        try:
            validate(instance=json_response, schema=video_schema_data)
            logger.info(f"Schema validation passed for video id: {video_id}")
        except ValidationError as e:
            logger.error(f"Schema validation failed for video id: {video_id}: {str(e)}")
            raise