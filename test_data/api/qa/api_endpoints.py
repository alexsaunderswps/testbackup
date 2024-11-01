# endpoints_data.py
import math
from tests.api.api_base import APIBase
from typing import Dict, List



class EndpointManager:
    """
    Manages endpoint-related functionality and calculations
    """

    @staticmethod
    def get_total_videos() -> int:
        return APIBase().total_videos
    
    @property
    def total_videos(self) -> int:
        if not hasattr(self, '_total_videos'):
            self._total_videos = self.get_total_videos()
        return self._total_videos
    
    @property
    def max_page_size(self) -> int:
        return 25
    
    @property
    def total_pages(self) -> int:
        return math.ceil(self.total_videos / self.max_page_size)

# Endpoint configuration with combined data structure
ENDPOINT_CONFIG = {
    "DEFAULT_THRESHOLD": 2,
    "ENDPOINTS": {
        "/Videos": {
            "threshold": 2,
            "description": "Video management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/VideoCatalogue": {
            "threshold": 2,
            "description": "Video catalogue management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/MapMarker": {
            "threshold": 2,
            "description": "Map marker management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/Countries": {
            "threshold": 2,
            "description": "Countries management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/IUCNStatus": {
            "threshold": 2,
            "description": "IUCN status management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/Organization": {
            "threshold": 2,
            "description": "Organization management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/PopulationTrend": {
            "threshold": 2,
            "description": "Population trend management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/Species": {
            "threshold": 2,
            "description": "Species management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/Site": {
            "threshold": 2,
            "description": "Site management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/SpeciesCategory": {
            "threshold": 2,
            "description": "Species category management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/Tag": {
            "threshold": 2,
            "description": "Tag management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/Users": {
            "threshold": 2,
            "description": "Users management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        },
        "/Organization": {
            "threshold": 2,
            "description": "Organization management endpoint",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "requires_auth": True
        }
    }
}