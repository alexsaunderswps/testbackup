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
        
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        self.context.set_current_request("GET", url, headers, params)
        logger.info(f"Sending GET request to {url}")
        
        response = requests.get(url, headers=headers, params=params)
        
        self.context.set_current_response(response.status_code, response.headers, response.text)
        logger.info(f"Received response with status code {response.status_code}")

        return response
    
    def post(self, endpoint, data):
        return requests.post(f"{self.base_url}{endpoint}", headers=self.get_headers(), json=data)