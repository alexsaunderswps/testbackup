# schema_validation.py
import os
import pytest
import requests
from typing import Dict, List, Any, Optional
from utilities.data_loader import DataLoader
from utilities.utils import logger 

class WildXRSchemas:
    """
    Define expected schema for Video endpoint responses
    """
    
    # Schema for single video object
    VIDEO_OBJECT_SCHEMA = {
        "type": "object",
        "required": ["name", "overview", "thumbnailUrl", "country", "videoResolutionId", "species"],
        "properties": {
            "rowVersion": {"type": "string"},
            "videoId": {"type": "string", "format": "uuid"},
            "name": {"type": "string", "minLength": 1},
            "overview": {"type": "string"},
            "dateCreated": {"type": "string", "format": "date-time"},
            "thumbnailUrl": {"type": "string", "format": "uri"},
            "youTubeUrl": {"type": "string", "format": "uri"},
            "totalViews": {"type": "integer", "minimum": 0},
            "totalLikes": {"type": "integer", "minimum": 0},
            "totalDislikes": {"type": "integer", "minimum": 0},
            "rating": {"type": "number", "minimum": 0, "maximum": 5},
            "mapMarkers": {
                "type": "array",
                "items": {"type": "object"}  # Can be more specific if needed
            },
            "startTime": {"type": "string", "format": "time"},
            "endTime": {"type": "string", "format": "time"},
            "countryObtainedId": {"type": "string", "format": "uuid"},
            "tags": {
                "type": "array",
                "items": {"type": "string"}
            },
            "lastEditedBy": {"type": "string"},
            "lastEditedDate": {"type": "string", "format": "date-time"},
            "species": {
                "type": "array",
                "items": {"type": "string", "format": "uuid"}
            },
            "videoFormat": {"type": "integer", "minimum": 0},
            "videoStatusId": {"type": "integer", "minimum": 0},
            "videoResolutionId": {"type": "integer", "minimum": 0}
        }
    }
    
    