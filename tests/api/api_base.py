import os
import requests
import json
from urllib.parse import urljoin
from dotenv import load_dotenv
from api_test_context import APITestContext
from utilities.utils import logger

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

class APIBase:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.auth_endpoint = "api/Users/Authenticate"
        self.context = APITestContext()
        self.token = self._get_auth_token()
        logger.html_logger.set_context(self.context)
        
    def _get_auth_token(self):
        """Fetch authentication token from the API.
        """
        auth_url = urljoin(self.base_url, self.auth_endpoint)
        auth_data = {
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
        
        try:
            response = requests.post(
                auth_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(auth_data)
            )
            response.raise_for_status()
            return response.json().get("token")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to obtain authentication token: {str(e)}")
            raise
        
    def get_headers(self, auth_type='valid'):
        """
        Get headers for API requests.
        
        Args:
            auth_type (str, optional): Type of authentication ('valid', 'invalid', or 'none'). Defaults to 'valid'.

        Returns:
            dict: Headers for the API request
        """
        base_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if auth_type == 'valid':
            base_headers["Authorization"] = f"Bearer {self.token}"
        if auth_type == 'invalid':
            base_headers["Authorization"] = "Bearer invalid_token"
        # For auth_type == 'none', no Authorization header is added
        return base_headers
    
    # def get_valid_headers(self):
    #     return self.get_headers('valid')
    
    # def get_invalid_headers(self):
    #     return self.get_headers('invalid')
    
    # def get_no_auth_headers(self):
    #     return self.get_headers('none')
        
    def get(self, endpoint, auth_type='valid', params=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers(auth_type)
        self.context.set_current_request("GET", url, headers, params)
        logger.info(f"Sending GET request to {url}")
        
        response = requests.get(url, headers=headers, params=params)
        
        self.context.set_current_response(response.status_code, response.headers, response.text)
        logger.info(f"Received response with status code {response.status_code}")

        return response
    
    def post(self, endpoint, auth_type='valid', params=None, body=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers(auth_type)
        self.context.set_current_request("POST", url, headers, params=params, body=body)
        logger.info(f"Sending POST request to {url}")
        
        response = requests.post(url, headers=headers, params=params, json=body)
        
        self.context.set_current_response(response.status_code, response.headers, response.text)
        logger.info(f"Received response with status code {response.status_code}")
        
        return response
        
    def measure_response_time(self, response):
        return response.elapsed.total_seconds()
    
    @property
    def total_videos(self):
        """_summary_
        """
        url = "/Videos/Query"
        body = {
            "page": 0,
            "pageSize": 0,
            "pageCount": 0,
            "orderBy": "string",
            "sortOrder": "string",
            "name": "",
            "overview": "string"
            }
        
        try:
            response = self.post(url, 'valid', None, body=body)
            response.raise_for_status()
            return response.json().get("totalCount")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch total video count: {str(e)}")