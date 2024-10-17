import os
import requests
from dotenv import load_dotenv
from api_test_context import APITestContext
from utilities.utils import logger

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_TOKEN = os.getenv("API_TOKEN")

class APIBase:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = API_TOKEN
        self.context = APITestContext()
        logger.html_logger.set_context(self.context)
        
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
    
    def post(self, endpoint, auth_type='valid', params=None, data=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers(auth_type)
        self.context.set_current_request("POST", url, headers, params, data)
        logger.info(f"Sending POST request to {url}")
        
        response = requests.post(url, headers=headers, params=params, json=data)
        
        self.context.set_current_response(response.status_code, response.headers, response.text)
        logger.info(f"Received response with status code {response.status_code}")
        
        return response
        
    def measure_response_time(self, response):
        return response.elapsed.total_seconds()