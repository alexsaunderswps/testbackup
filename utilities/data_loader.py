# utilities/data_loader.py is a utility file that contains the data loader class.
import json
import os
import random
import importlib.util
from jsonschema import validate, ValidationError # type: ignore
from typing import Any, Dict, List, Optional, Union
from utilities.utils import logger

class DataLoader:
    """
    Handles loading and managing test data for the test cases.
    
    This class provides centralized access to test data files, with features for:
    - Loading test data from JSON files and Python modules
    - Environment-specific data loading
    - Data validation
    - Caching for performance
    - Error handling and logging
    """
    def __init__(self, env: str = "qa"):
        """
        Initialize the TestDataLoader class.
        
        Args:
        - env (str): The environment to load the test data for. Default is "qa".
        """
        self.env = env
        project_root = os.path.dirname(os.path.dirname(__file__))
        self.base_path = os.path.join(project_root, "test_data", "api", self.env)
        self.data_cache: Dict[str, Any] = {}
        self._endpoint_manager = None
        
        logger.debug(f"TestDataLoader initialized with base path: {self.base_path}")
        # Verify directory structure
        if not os.path.exists(self.base_path):
            logger.error(f"Test data directory not found: {self.base_path}")
            logger.debug("Available directories:")
            test_data_dir = os.path.join(project_root, "test_data")
            if os.path.exists(test_data_dir):
                for root, dirs, files in os.walk(test_data_dir):
                    logger.debug(f"Directory: {root}")
                    for d in dirs:
                        logger.debug(f"  - {d}/")
                    for f in files:
                        logger.debug(f"  - {f}")
        
    def _load_python_module(self, module_path: str) -> Any:
        """
        Load a Python module from a file path dynamically.

        Args:
            module_path (str): file path to the module.

        Returns:
            Any: _description_
        """
        try:
            spec = importlib.util.spec_from_file_location("module", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            logger.error(f"Failed to load python module at: {module_path}: {str(e)}")
            raise
        
    def _load_json_file(self, file_path:str) -> Dict[str, Any]:
        """
        Load and parse a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            Dict[str, Any]: Parsed JSON data.
        
        Raises:
            FileNotFoundError: If the file is not found.
            json.JSONDecodeError: If the file is not in JSON format.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"Test data file not found at: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Test data is in invalid JSON format at: {file_path} - {str(e)}")
            raise
    
    def get_data_path(self, data_type:str) -> str:
        """
        Get the appropriate file path for the requested data type.

        Args:
            data_type (str): Type of data to load (e.g., "videos", "endpoints").

        Returns:
            str: Full file path
        """
        # First try environment_specific path
        env_path = os.path.join(self.base_path, self.env, f"{data_type}.json")
        if os.path.exists(env_path):
            return env_path
        
        # Fall back to default path
        default_path = os.path.join(self.base_path, f"{data_type}.json")
        if os.path.exists(default_path):
            return default_path
        
        raise FileNotFoundError(f"No data file found for {data_type} in {self.env} or default")
    
    def _validate_video_data(self, data: Dict[str, Any]) -> bool:
        """
        Validates the video data structure.

        Args:
            data (Dict[str, Any]): Video data to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        # required_fields needs to be fleshed out to include the whole structure
        # this will require an update to the video_data.py file
        try:
            # Get videos list either from module.VIDEO_DATA or direct data
            videos = data.VIDEO_DATA if hasattr(data, "VIDEO_DATA") else data
            required_fields = ["ID", "Name", "Overview"]
            
            if not isinstance(videos, list):
                return False
            
            return all(
                isinstance(video, dict) and 
                all(field in video for field in required_fields)
                for video in videos
            )
        except (AttributeError, TypeError) as e:
            logger.debug(f"Failed to validate video data: {str(e)}")
            return False
    
    def _validate_endpoint_data(self, data: Dict[str, Any]) -> bool:
        """
        Validates the endpoint data structure.

        Args:
            data (Dict[str, Any]): Endpoint data to validate.

        Returns:
            bool: True if valid, False if otherwise.
        """
        if not isinstance(data, dict):
            return False
        
        required_keys = ["DEFAULT_THRESHOLD", "ENDPOINTS"]
        required_fields = ["threshold", "description", "methods", "requires_auth"]
        
        # Check required top-level keys
        if not all(key in data for key in required_keys):
            return False
        
        # Check endpoint data structure
        for endpoint, config in data["ENDPOINTS"].items():
            if not all(field in config for field in required_fields):
                return False
            
            # Validate field types
            if not isinstance(config["threshold"], (int, float)):
                return False
            if not isinstance(config["methods"], list):
                return False
            if not isinstance(config["requires_auth"], bool):
                return False
            
        return True
    
    def get_endpoint_data(self, cache: bool = True) -> Dict[str, Any]:
        """
        Get endpoint test data.

        Args:
            cache (bool, optional): Whether to cache the data or not. Defaults to True.

        Returns:
            Dict[str, Any]: Complete endpoint configuration.
        """
        if cache and "endpoints" in self.data_cache:
            return self.data_cache["endpoints"]
        
        # Load from Python module
        try:
            module_path = self._get_module_path("api_endpoints")
            logger.debug(f"Attempting to load endpoint data from: {module_path}")
            
            if not os.path.exists(module_path):
                logger.error(f"Endpoint data file not found at: {module_path}")
                # Log directory contents for debugging
                parent_dir = os.path.dirname(module_path)
                if os.path.exists(parent_dir):
                    logger.debug(f"Contents of {parent_dir}:")
                    for item in os.listdir(parent_dir):
                        logger.debug(f"  - {item}")
                raise FileNotFoundError(f"Endpoint data file not found at: {module_path}")
        
            module = self._load_python_module(module_path)
            data = module.ENDPOINT_CONFIG
            
            if not self._validate_endpoint_data(data):
                raise ValueError("Invalid endpoint data format")
            
            if cache:
                self.data_cache["endpoints"] = data
            return data
        except Exception as e:
            logger.error(f"Failed to load endpoint data: {str(e)}")
            logger.error(f"Searched path: {module_path}")
            raise
        
    def get_endpoints_list(self) -> List[str]:
        """
        Get just the list of endpoint paths

        Returns:
            List[str]: List of endpoint paths.
        """
        endpoint_data = self.get_endpoint_data()
        return list(endpoint_data["ENDPOINTS"].keys())
    
    def get_endpoint_threshold(self, endpoint: str) -> float:
        """
        Get threshold for a specific endpoint.

        Args:
            endpoint (str): Endpoint path.

        Returns:
            float: Threshold value.
        """
        endpoint_data = self.get_endpoint_data()
        return (endpoint_data["ENDPOINTS"].get(endpoint, {}).get("threshold") or
                endpoint_data["DEFAULT_THRESHOLD"])
        
    def get_endpoint_info(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about an endpoint.

        Args:
            endpoint (str): Endpoint path.

        Returns:
            Optional[Dict[str, Any]]: Detailed endpoint information.
        """
        endpoint_data = self.get_endpoint_data()
        return endpoint_data["ENDPOINTS"].get(endpoint)
        
    def get_video_data(self, cache: bool = True) -> List[Dict[str, Any]]:
        """
        Gets the video test data.

        Args:
            cache (bool, optional): Whether to cache the data or not. Defaults to True.

        Returns:
            List[Dict[str, Any]]: List of video data dictionaries.
        """
        if cache and "videos" in self.data_cache:
            return self.data_cache["videos"]
        
        # Load from Python module
        module_path = self._get_module_path("video_data")
        logger.debug(f"Attempting to load video data from: {module_path}")
        
        try:
            module = self._load_python_module(module_path)
            videos = module.VIDEO_DATA
        
            if not self._validate_video_data(module):
                raise ValueError("Invalid video data format")
        
            if cache:
                self.data_cache["videos"] = module.VIDEO_DATA
            return videos
        except Exception as e:
            logger.error(f"Failed to load video data: {str(e)}")
            logger.error(f"Searched path: {module_path}")
            raise
    
    def get_random_video(self) -> Dict[str, Any]:
        """
        Get a random video from the video test data.

        Returns:
            Dict[str, Any]: Random video data.
        """
        videos = self.get_video_data()
        return random.choice(videos)
    
    def get_video_subset(self, count: int) -> List[Dict[str, Any]]:
        """
        Get a random subset of video data.

        Args:
            count (int): Number of videos to return.

        Returns:
            List[Dict[str, Any]]: Random subset of video data.
        """
        videos = self.get_video_data()
        return random.sample(videos, min(count, len(videos)))
    
    def clear_cache(self) -> None:
        """
        Clear the data cache.
        """
        self.data_cache.clear()
        logger.info("Test data cache cleared")
        
    def get_video_schema_data(self, cache: bool = True) -> Dict[str, Any]:
        """
        Get video schema data.

        Args:
            cache (bool, optional): Whether to cache the data or not. Defaults to True.

        Returns:
            Dict[str, Any]: Complete video endpoint schema.
        """
        if cache and "video_schema" in self.data_cache:
            return self.data_cache["video_schema"]
        
        # Load from Python module
        try:
            module_path = self._get_module_path("schema_validation")
            logger.debug(f"Attempting to load endpoint data from: {module_path}")
            
            if not os.path.exists(module_path):
                logger.error(f"Endpoint data file not found at: {module_path}")
                # Log directory contents for debugging
                parent_dir = os.path.dirname(module_path)
                if os.path.exists(parent_dir):
                    logger.debug(f"Contents of {parent_dir}:")
                    for item in os.listdir(parent_dir):
                        logger.debug(f"  - {item}")
                raise FileNotFoundError(f"Schema data file not found at: {module_path}")
        
            module = self._load_python_module(module_path)
            data = module.VIDEO_OBJECT_SCHEMA
            
            # Need to write _validate_video_schema_data method
            if not self._validate_video_schema_data(data):
                raise ValueError("Invalid video schema data format")
            
            if cache:
                self.data_cache["video_schema"] = data
            return data
        except Exception as e:
            logger.error(f"Failed to load video_schema data: {str(e)}")
            logger.error(f"Searched path: {module_path}")
            raise

    def _validate_video_schema_data(self, data: Dict[str, Any]) -> bool:
        """
        Validates the video_schema data structure.

        Args:
            data (Dict[str, Any]): Video Schema to validate.

        Returns:
            bool: True if valid, False if otherwise.
        """
        try:
            # Check if data is a dictionary and has expected structure
            if not isinstance(data, dict):
                logger.error("Video schema data is not a dictionary")
                return False
        
            # Extract schema if it is nested under VIDEO_OBJECT_SCHEMA
            schema = data.get("VIDEO_OBJECT_SCHEMA", data)

            # Validate schema structure
            required_top_level_keys = ["type", "required", "properties"]
            if not all(key in schema for key in required_top_level_keys):
                logger.error("Video schema data is missing required top-level keys: {required_top_level_keys}")
                return False
            
            # Try to use it as a JSON schema
            try:
                # Validate against a simple test object to verify schema validity
                test_object = {
                    "name": "Test Video",
                    "overview": "This is a test video",
                    "thumbnailUrl": "https://test.com/thumbnail.jpg",
                    "country": "USb4e7c055-2f2a-4626-8224-f0a263f16963",
                    "videoResolutionId": 1,
                    "species": ["Lionf8a87a6b-f4e4-4e90-bb61-76aeff840a82"]
                } 
                validate(instace=test_object, schema=schema)
                return True
            except ValidationError as e:
                logger.error(f"Video schema data is not a valid JSON schema: {str(e)}")
                return False
        except Exception as e:
            logger.error(f"Failed to validate video schema data: {str(e)}")
            return False

# Endpoint Manager
    @property
    def endpoint_manager(self):
        """
        Get an instance of the EndpointManager class.

        Returns:
            EndpointManager: _description_
        """
        if self._endpoint_manager is None:
            try:
                module_path = os.path.join(self.base_path,"api_endpoints.py")
                module = self._load_python_module(module_path)
                self._endpoint_manager = module.EndpointManager()
            except Exception as e:
                logger.error(f"Failed to load endpoint manager: {str(e)}")
                raise
        return self._endpoint_manager
    
    # Helper methods for endpoint manager functionality
    def get_total_videos(self) -> int:
        """
        Get the total number of videos.

        Returns:
            int: Total number of videos.
        """
        return self.endpoint_manager.total_videos
    
    def get_max_page_size(self) -> int:
        """
        Get the maximum page size for videos.

        Returns:
            int: Maximum page size.
        """
        return self.endpoint_manager.max_page_size
    
    def get_total_pages(self) -> int:
        """
        Get the total number of pages for videos.

        Returns:
            int: Total number of pages.
        """
        return self.endpoint_manager.total_pages
    
    def _get_module_path(self, module_name: str) -> str:
        """
        Get the full file path for a Python module.

        Args:
            module_name (str): Name of the module.

        Returns:
            str: Full file path.
        """
        return os.path.join(self.base_path, f"{module_name}.py")