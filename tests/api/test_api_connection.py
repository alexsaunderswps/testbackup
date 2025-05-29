# test_api_connection.py is a test file that contains the test cases for the API connection.
import pytest
from typing import Dict, Any
from .api_base import APIBase
from utilities.data_handling import DataLoader
from utilities.utils import logger

# Get endpoints needed
def get_endpoints():
    """
    Get the list of endpoints to test
    """
    return DataLoader().get_endpoints_list()

# Basic Connection tests

class TestAPIConnection:
    def setup_method(self):
        self.api = APIBase()
        self.data_loader = DataLoader()
    
    # Paramertized test for using valid authorization, valid status code and response time from multiple endpoints
    @pytest.mark.api
    @pytest.mark.connection
    # @pytest.mark.github
    @pytest.mark.parametrize("endpoint", get_endpoints())
    @pytest.mark.parametrize("auth_type, expected_status_code", [
        ('valid', 200),
        ('invalid', (401, 404)),  # 401 for unauthorized, 404 for not found
        ('none', (401, 404)),  # 401 for unauthorized, 404 for not found
    ])
    def test_api_connection_parametrized_valid(self, endpoint: str, auth_type: str, expected_status_code: int):
        """
        Test API connection with valid authorization, valid status code and response time

        Args:
            endpoint (str): The endpoint to test
            auth_type (str): The authorization type to use ('valid', 'invalid', 'none')
            expected_status_code (int): The expected HTTP status code
            
        The test verifies:
        1. Correct status code based on auth type
        2. Response time within threshold
        3. Endpoint is accessible/inaccessible as expected
        """
        # Get endpoint configuration
        endpoint_info = self.data_loader.get_endpoint_info(endpoint)
        threshold = self.data_loader.get_endpoint_threshold(endpoint)
        
        # Make API request
        response = self.api.get(endpoint, auth_type)
        response_time = self.api.measure_response_time(response)
        
        # Log Test details
        logger.info('=' * 80)
        logger.info("API Connection Test Details:")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Description: {endpoint_info['description']}")
        logger.info(f"Auth Type: {auth_type}")
        logger.info(f"Requires Auth: {endpoint_info['requires_auth']}")
        logger.info(f"Allowed Methods: {', '.join(endpoint_info['methods'])}")
        logger.info(f"Response Time: {response_time:.3f} seconds")
        logger.info(f"Threshold: {threshold} seconds")
        logger.info(f"Status Code: {response.status_code} (Expected: {expected_status_code})")
        logger.info('=' * 80)
        
        # Assertions
        try:
            # Check status code
            if isinstance(expected_status_code, (list, tuple)):
                assert response.status_code in expected_status_code, (
                    f"Unexpected status code for {endpoint} with {auth_type} auth. "
                    f"Expected one of {expected_status_code}, got {response.status_code}"
                )
            else:
                assert response.status_code == expected_status_code, (
                    f"Unexpected status code for {endpoint} with {auth_type} auth. "
                    f"Expected {expected_status_code}, got {response.status_code}"
                )
            
            # Check response for only successful requests
            if response.status_code == 200:
                assert response_time < threshold, (
                    f"Response time for {endpoint} with {auth_type} auth is too high. "
                    f"Expected < {threshold}, got {response_time:.3f}"
                )
            
            # Additional checks based on endpoint configuration
            if endpoint_info['requires_auth']:
                if auth_type != 'valid':
                    assert response.status_code == 401 or response.status_code == 404, (
                        f"Protected endpoint {endpoint} allowed access with {auth_type} auth-type. "
                    )
            logger.info("\nAPI Connection Test Summary:")
            logger.info(f"✓ All assertions passed for {endpoint} with {auth_type} auth")
            
        except AssertionError as e:
            logger.error(f"✗ Test failed: {str(e)}")
            raise
    
    @pytest.mark.api
    @pytest.mark.connection
    @pytest.mark.bulk
    # @pytest.mark.github
    def test_api_connection_bulk(self):
            """
            Alternative approach: Test all endpoints in a single test for better reporting
            """
            results = []
            endpoints = self.data_loader.get_endpoints_list()
            auth_scenarios = [
                ('valid', 200),
                ('invalid', (401, 404)),  # 401 for unauthorized, 404 for not found
                ('none', (401, 404)) # 401 for unauthorized, 404 for not found
            ]

            for endpoint in endpoints:
                endpoint_info = self.data_loader.get_endpoint_info(endpoint)
                threshold = self.data_loader.get_endpoint_threshold(endpoint)

                for auth_type, expected_status_code in auth_scenarios:
                    try:
                        response = self.api.get(endpoint, auth_type)
                        response_time = self.api.measure_response_time(response)

                        result = {
                            'endpoint': endpoint,
                            'auth_type': auth_type,
                            'status_code': response.status_code,
                            'expected_status_code': expected_status_code,
                            'response_time': response_time,
                            'threshold': threshold,
                            'passed': True,
                            'error': None
                        }

                        # Run assertions - handle both single values and collections
                        if isinstance(expected_status_code, (list, tuple)):
                            assert response.status_code in expected_status_code
                        else:
                            assert response.status_code == expected_status_code
                            
                        if response.status_code == 200:
                            assert response_time < threshold

                    except Exception as e:
                        result = {
                            'endpoint': endpoint,
                            'auth_type': auth_type,
                            'status_code': getattr(response, 'status_code', None),
                            'expected_status_code': expected_status_code,
                            'response_time': getattr(response, 'elapsed', None),
                            'threshold': threshold,
                            'passed': False,
                            'error': str(e)
                        }

                    results.append(result)

            # Log summary
            logger.info(f"\nAPI Connection Test for: {endpoint}")
            logger.info("=" * 80)
            
            total_tests = len(results)
            passed_tests = sum(1 for r in results if r['passed'])
            failed_tests = total_tests - passed_tests

            logger.info(f"Total Tests: {total_tests}")
            logger.info(f"Passed: {passed_tests}")
            logger.info(f"Failed: {failed_tests}")
            logger.info("=" * 80)

            # Log failures in detail
            if failed_tests > 0:
                logger.error("\nFailed Tests:")
                for result in results:
                    if not result['passed']:
                        logger.error(f"""
                        Endpoint: {result['endpoint']}
                        Auth Type: {result['auth_type']}
                        Status Code: {result['status_code']} (Expected: {result['expected_status_code']})
                        Error: {result['error']}
                        """)

            # Final assertion
            assert failed_tests == 0, f"{failed_tests} tests failed. See log for details."