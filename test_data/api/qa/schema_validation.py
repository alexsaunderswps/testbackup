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
        "rowVersion": str,
        "videoId": str,
        "name": str,
        "overview": str,
        "dateCreated": str,
        "thumbnailUrl": str,
        "youTubeUrl" : str,
        "totalViews": int,
        "totalLikes": int,
        "totalDislikes": int,
        "rating": float,
        "mapMarkers": list,
        "startTime": str,
        "endTime": str,
        "countryObtainedId": str,
        "tags": list,
        "lastEditedBy": str,
        "lastEditedDate": str,
        "species": list,
        "videoFormat": int,
        "videoStatusId": int,
        "videoResolutionId": int
    }
    
    