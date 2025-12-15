# auth.py
"""
Shared authentication utility for API requests.
Provides token generation and caching during test sessions.
"""
import os
import requests
import json
from typing import Optional
from dotenv import load_dotenv
from utilities.utils import logger

# Load environment variables
load_dotenv()

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL")
SYS_ADMIN_USERNAME = os.getenv("SYS_ADMIN_USERNAME")
SYS_ADMIN_PASSWORD = os.getenv("SYS_ADMIN_PASSWORD")


class TokenCache:
    """
    Singleton class to cache authentication token during test session.
    This prevents repeated authentication calls while ensuring fresh tokens.
    """
    _instance: Optional['TokenCache'] = None
    _token: Optional[str] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenCache, cls).__new__(cls)
        return cls._instance

    def get_token(self) -> str:
        """
        Get cached token or generate a new one if not available.

        Returns:
            str: Valid authentication token

        Raises:
            Exception: If authentication fails
        """
        if self._token is None:
            self._token = self._fetch_new_token()
        return self._token

    def _fetch_new_token(self) -> str:
        """
        Fetch a fresh authentication token from the API.

        Returns:
            str: Authentication token

        Raises:
            Exception: If authentication fails
        """
        auth_endpoint = f"{API_BASE_URL}/Users/Authenticate"
        auth_data = {
            "username": SYS_ADMIN_USERNAME,
            "password": SYS_ADMIN_PASSWORD
        }

        try:
            logger.debug(f"Fetching new authentication token from {auth_endpoint}")
            response = requests.post(
                auth_endpoint,
                headers={"Content-Type": "application/json"},
                data=json.dumps(auth_data),
                timeout=30
            )
            response.raise_for_status()
            token = response.json().get("token")

            if not token:
                raise ValueError("No token returned in authentication response")

            logger.info("Successfully obtained authentication token")
            return token

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to obtain authentication token: {str(e)}")
            raise Exception(f"Authentication failed: {str(e)}")

    def refresh_token(self) -> str:
        """
        Force refresh the cached token.

        Returns:
            str: New authentication token
        """
        logger.info("Refreshing authentication token")
        self._token = self._fetch_new_token()
        return self._token

    def clear_token(self):
        """Clear the cached token."""
        logger.debug("Clearing cached authentication token")
        self._token = None


def get_auth_token() -> str:
    """
    Get a cached authentication token for API requests.

    This is the main function to use in fixtures and tests.
    It returns a cached token if available, or generates a new one.

    Returns:
        str: Valid authentication token

    Example:
        >>> token = get_auth_token()
        >>> headers = {"Authorization": f"Bearer {token}"}
    """
    cache = TokenCache()
    return cache.get_token()


def refresh_auth_token() -> str:
    """
    Force refresh the authentication token.

    Use this when you suspect the token has expired or been invalidated.

    Returns:
        str: New authentication token

    Example:
        >>> token = refresh_auth_token()
    """
    cache = TokenCache()
    return cache.refresh_token()


def get_auth_headers() -> dict:
    """
    Get headers with authentication for API requests.

    Returns:
        dict: Headers dictionary with Authorization and Content-Type

    Example:
        >>> headers = get_auth_headers()
        >>> response = requests.post(url, headers=headers, json=payload)
    """
    token = get_auth_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def clear_token_cache():
    """
    Clear the cached token.

    Useful for testing or when you need to force re-authentication.
    """
    cache = TokenCache()
    cache.clear_token()
