# endpoints_data.py
import math

class ENDPOINT_DATA:

    ENDPOINTS = [
        "/Videos", "/VideoCatalogue", "/MapMarker", "/Countries", "/IUCNStatus",
        "/Organization", "/PopulationTrend", "/Species", "/Site", "/SpeciesCategory",
        "/Tag", "/Users", "/Organization"
    ]

    THRESHOLDS = {
        "/Videos": 2,
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

    # Video collection size data
    TOTAL_VIDEOS = 296
    MAX_PAGE_SIZE = 25
    TOTAL_PAGES = math.ceil(TOTAL_VIDEOS / MAX_PAGE_SIZE)
