import json
import jsonschema # type: ignore
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from utilities.utils import logger

@dataclass
class BaseEndpointConfig:
    """
    Base class for endpoint configuration, all endpoint configurations should inherit from this class
    """
    threshold: float
    description: str 
    methods: List[str]
    requires_auth: bool

@dataclass
class PaginatedEndpointConfig(BaseEndpointConfig):
    """
    Paginated endpoint configuration
    """
    max_page_size: int = 25

@dataclass
class VideoEndpointConfig(BaseEndpointConfig):
    """
    Video endpoint configuration
    """
    video_id: int
    video_name: str


class DataLoader:
    """Enhanced data loader maintaining compatibility with existing test suite"""
    
    def __init__(self, env: str = "qa"):
        self.base_path = Path(__file__).parent.parent / "test_data" / "api" / env
        self.data_path = self.base_path / "data"
        self.schema_path = self.base_path / "schemas"
        self.cache = {}
        
    def _load_json_file(self, file_path: Path) -> Dict:
        """Load and cache JSON file"""
        cache_key = str(file_path)
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.cache[cache_key] = data
            return data

    def get_video_data(self) -> List[Dict[str, Any]]:
        """Get all video test data"""
        data = self._load_json_file(self.data_path / "videos.json")
        return data["data"]
    
    def get_random_video(self) -> Dict[str, Any]:
        """Get a random video for testing"""
        import random
        videos = self.get_video_data()
        return random.choice(videos)

    def get_endpoint_info(self, endpoint: str) -> Dict[str, Any]:
        """Get endpoint configuration"""
        data = self._load_json_file(self.data_path / "endpoints.json")
        return data["ENDPOINTS"].get(endpoint, {})

    def get_endpoint_threshold(self, endpoint: str) -> float:
        """Get endpoint threshold"""
        endpoint_data = self.get_endpoint_info(endpoint)
        return endpoint_data.get("threshold") or self._load_json_file(
            self.data_path / "endpoints.json"
        )["DEFAULT_THRESHOLD"]

    def get_endpoints_list(self) -> List[str]:
        """Get list of all endpoints"""
        data = self._load_json_file(self.data_path / "endpoints.json")
        return list(data["ENDPOINTS"].keys())

    def validate_response(self, schema_name: str, response_data: Dict) -> bool:
        """Validate API response against schema"""
        schema_file = self.schema_path / "response_schemas" / f"{schema_name}.json"
        if not schema_file.exists():
            logger.warning(f"Schema file not found: {schema_file}")
            return True  # No schema defined = no validation needed
        try:
            schema = self._load_json_file(schema_file)
            jsonschema.validate(instance=response_data, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Schema validation failed: {str(e)}")
            return False
        
    def get_total_pages(self) -> int:
        """
        Get the total number of pages based on the total number of videos and the max page size
        Returns:
            int: Total number of pages
        """
        return self.endpoint_manager.total_pages
    
    def get_max_page_size(self) -> int:
        """
        Get the maximum page size for videos
        Returns:
            int: Maximum page size
        """
        return self.endpoint_manager.max_page_size
    
    def get_total_videos(self) -> int:
        """
        Get the total number of videos
        Returns:
            int: Total number of videos
        """
        return self.endpoint_manager.total_videos

    # Compatibility with existing endpoint manager functionality
    @property
    def endpoint_manager(self):
        """Legacy endpoint manager compatibility"""
        class EndpointManager:
            def __init__(self, loader):
                self.loader = loader
                self._config = loader._load_json_file(
                    loader.data_path / "endpoints.json"
                )

            @property
            def total_videos(self) -> int:
                return len(self.loader.get_video_data())

            @property
            def max_page_size(self) -> int:
                return self._config["ENDPOINTS"]["/Videos"].get("max_page_size", 25)

            @property
            def total_pages(self) -> int:
                import math
                return math.ceil(self.total_videos / self.max_page_size)

        return EndpointManager(self)

    def clear_cache(self):
        """Clear the data cache"""
        self.cache.clear()