#endpoints_data.py
import math

class ENDPOINT_DATA:
    
    ENDPOINTS = [
        "/Videos", "/VideoCatalogue", "/MapMarker", "/Countries", "/IUCNStatus",
        "/Organization", "/PopulationTrend", "/Species", "/Site", "/SpeciesCategory",
        "/Tag", "/Users", "/Organization"
    ]

    THRESHOLDS = {
        "/Videos": 0.4,
        "/VideoCatalogue": 0.3,
        "/MapMarker": 0.3,
        "/Countries": 0.3,
        "/IUCNStatus": 0.3,
        "/Organization": 0.3,
        "/PopulationTrend": 0.3,
        "/Species": 0.3,
        "/Site": 0.3,
        "/SpeciesCategory": 0.3,
        "/Tag": 0.3,
        "/Users": 0.3,
    }
    
    # Video collection size data
    TOTAL_VIDEOS = 296
    MAX_PAGE_SIZE = 25
    TOTAL_PAGES = math.ceil(TOTAL_VIDEOS / MAX_PAGE_SIZE)