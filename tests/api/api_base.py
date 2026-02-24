import os
import requests
import json
from urllib.parse import urljoin
from dotenv import load_dotenv
from api_test_context import APITestContext
from utilities.utils import logger
from utilities.auth import get_auth_token

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

class APIBase:
    def __init__(self, token: str = None):
        """
        Initialize APIBase with an optional pre-fetched authentication token.

        Args:
            token: A JWT token string. If provided, it is used directly for all
                   requests instead of calling get_auth_token(). Pass this when
                   you need to authenticate as a specific user account (e.g., an
                   org-admin in authorization tests). If None, the shared system
                   admin token is used (see utilities/auth.py get_auth_token()).
        """
        self.base_url = API_BASE_URL
        self.context = APITestContext()
        self.token = token if token is not None else get_auth_token()
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
    
    def post(self, endpoint, auth_type='valid', params=None, body=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers(auth_type)
        self.context.set_current_request("POST", url, headers, params=params, body=body)
        logger.info(f"Sending POST request to {url}")
        
        response = requests.post(url, headers=headers, params=params, json=body)
        
        self.context.set_current_response(response.status_code, response.headers, response.text)
        logger.info(f"Received response with status code {response.status_code}")
        
        return response
        
    def put(self, endpoint, auth_type='valid', params=None, body=None):
        """
        Send a PUT request to the given endpoint.

        NOTE: The WildXR API uses PUT (not POST) for resource creation. This is an
        unconventional but consistent design choice across all controllers — PUT maps to
        "create" and POST maps to "update" throughout this API. Use this method when
        calling any /Create endpoint (e.g., /api/Device/Create, /api/Installations/create).

        Args:
            endpoint (str): The API endpoint path (e.g., '/api/Device/Create').
            auth_type (str, optional): Authentication type ('valid', 'invalid', 'none'). Defaults to 'valid'.
            params (dict, optional): Query string parameters. Defaults to None.
            body (dict, optional): Request body as a dict; serialized to JSON. Defaults to None.

        Returns:
            requests.Response: The HTTP response object.
        """
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers(auth_type)
        self.context.set_current_request("PUT", url, headers, params=params, body=body)
        logger.info(f"Sending PUT request to {url}")

        response = requests.put(url, headers=headers, params=params, json=body)

        self.context.set_current_response(response.status_code, response.headers, response.text)
        logger.info(f"Received response with status code {response.status_code}")

        return response

    def delete(self, endpoint, auth_type='valid', params=None):
        """
        Send a DELETE request to the given endpoint.

        This API passes the record ID as a query parameter rather than in the URL path
        (e.g., DELETE /api/Installations/delete?id=<guid>), so use the params argument
        rather than embedding the ID in the endpoint string.

        Args:
            endpoint (str): The API endpoint path (e.g., '/api/Installations/delete').
            auth_type (str, optional): Authentication type ('valid', 'invalid', 'none'). Defaults to 'valid'.
            params (dict, optional): Query string parameters, typically {'id': '<guid>'}. Defaults to None.

        Returns:
            requests.Response: The HTTP response object.
        """
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers(auth_type)
        self.context.set_current_request("DELETE", url, headers, params=params)
        logger.info(f"Sending DELETE request to {url}")

        response = requests.delete(url, headers=headers, params=params)

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