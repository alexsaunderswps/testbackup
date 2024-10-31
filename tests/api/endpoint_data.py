# endpoints_data.py
import math
from .api_base import APIBase


class ENDPOINT_DATA:

    ENDPOINTS = [
        "/Videos",
        "/VideoCatalogue",
        "/MapMarker",
        "/Countries",
        "/IUCNStatus",
        "/Organization",
        "/PopulationTrend",
        "/Species",
        "/Site",
        "/SpeciesCategory",
        "/Tag",
        "/Users",
        "/Organization",
    ]
    
    DEFAULT_THRESHOLD = 2
    
    THRESHOLDS = {
        "/Videos": 2, # Sets both the /Videos and the /Videos/{video_id}/Details thresholds
        "/VideoCatalogue": 2,
        "/MapMarker": 2,
        "/Countries": 2,
        "/IUCNStatus": 2,
        "/Organization": 2,
        "/PopulationTrend": 2,
        "/Species": 2,
        "/Site": 2,
        "/SpeciesCategory": 2,
        "/Tag": 2,
        "/Users": 2,
    }

    def get_total_videos():
        return APIBase().total_videos

    # Video collection size data
    TOTAL_VIDEOS = get_total_videos()
    MAX_PAGE_SIZE = 25
    TOTAL_PAGES = math.ceil(TOTAL_VIDEOS / MAX_PAGE_SIZE)
