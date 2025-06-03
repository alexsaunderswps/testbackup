#utilities/search_mixins.py
"""
Search testing mixin for consistent, robust search functionality testing.

This module provides reusable components for testing search functionality across
different pages of the application. Thie mixins focus on timing and state management
rather than content validation, making them robust and maintainable.
"""

import time
from typing import Callable, Optional
from utilities.utils import logger

class SimpleSearchMixin:
    """
    Mixin providubg robust simple serch testing capabilities.
    
    This mixin is designed for pages that have a simple search pattern:
    - One search input field
    - One search button
    - Results displayed in a table or list
    
    The mixin focuses on proper timing and state management rather than
    content validation, making test more reliable and maintainable.
    
    Useage:
        class TestMyPageSearch(SimpleSearchMixin):
            def test_my_search(self, my_page):
                search_config = {
                    'search_input_getter': my_page.get_search_input,
                    'search_button_getter': my_page.get_search_button,
                    'results_container_getter': my_page.get_results_container,
                    'results_selector': 'table tbody tr:has(td:not(:empty))'
                }
            
                self.execute_simple_search_test(my_page, search_config, test cases)    
    """
    
    def execute_simple_search_test(self, page_object, search_config, test_cases):
        """
        Execute a complete simple search test suite.

        Args:
            page_object: The page object instance (e.g., InstallationsPage).
            serch_config: Dictionary containing search element getters and selectors
            test_cases: List of test case dictionaries
            
        search_config format:
        {
            'search_input_getter': Callable,  # Function to get the search input element
            'search_button_getter': Callable,  # Function to get the search button element
            'results_container_getter': Callable,  # Function to get the results container element
            'results_selector': str  # CSS selector for results in the container
        }
        
        test_cases format:
        [
            {
                'name': 'exact_match',  # Name of the test case
                'search_term': str,  # Term to search for
                'expected_min_results': int,  # Expected number of results
                'description': 'Should find the specific installation'
            },
            {
                'name': 'no_results', 
                'search_term': 'NONEXISTENT',
                'expected_exact_results': 0,
                'description': 'Should return no results for non-existent item'
            }
        ]
        """
        logger.info(f"Starting simple search test suite with {len(test_cases)} cases")
        
        # Establish clean baseline for all tests
        self._establish_clean_baseline(page_object, search_config)
        
        # Execute each test case
        for test_case in test_cases:
            logger.info(f"=== Executing: {test_case['name']} ===")
            logger.info(f"Description: {test_case.get('description', 'No description provided')}")
            
            # Execute the search
            result_count = self._execute_simple_search(
                page_object,
                search_config,
                test_case['search_term']
            )
            
            # Validate expectations
            self._validate_search_expectations(test_case, result_count)
            
            # Reset state for the next test case (ensures test isolation)
            self._reset_simple_search_state(page_object, search_config)
            
        logger.info("All simple search tests completed successfully")
        
    def _establish_clean_baseline(self, page_object, search_config):
        """
        Establish a clean baseline state before running tests.
        
        This method ensures that the search input is empty and no results are displayed.
        """
        logger.info("Establishing clean search baseline state")
        
        # Start with a completely fresh page state
        page_object.page.reload()
        page_object.page.wait_for_load_state('networkidle')
        
        # Wait for the results container to be ready with data
        try:
            page_object.page.wait_for_selector(
                search_config['results_selector'],
                timeout=10000
            )
            # Additional stabilization time for any client-side rendering
            page_object.page.wait_for_timeout(1000)
            logger.info("Results container is ready with data")
        except Exception as e:
            logger.warning(f"Results container readiness check failed: {str(e)}")
            # Continue with the test, but note the issues
            
        # Ensure seach input is clear and ready
        search_input = search_config['search_input_getter']()
        current_value = search_input.input_value()
        if current_value:
            logger.info(f"Clearing existing search value: '{current_value}'")
            search_input.clear()
            search_config['search_button_getter']().click()
            self._wait_for_search_completion(page_object, search_config)
            
        logger.info("Search baseline established")
        
    def _execute_simple_search(self, page_object, search_config, search_term):
        """
        Execute a single search operation with comprehensive timing.

        This method handles the complete lifecycle of a search:
        1. Record current state
        2. Input the search term
        3. Execute the searach
        4. Wait for the completion
        5. Return result count
        """
        logger.info(f"Executing searach for: '{search_term}'")
        
        # Record baselline state for comparison
        baseline_count = self._get_results_count(search_config)
        logger.info(f"Baseline results count: {baseline_count}")
        
        # Get search elements
        search_input = search_config['search_input_getter']()
        search_button = search_config['search_button_getter']()
        
        # Clear any exisiting content and enter the search term
        search_input.clear()
        page_object.page.wait_for_timeout(500)  # Ensure input is ready
        search_input.fill(search_term)
        
        # Verify the search term was entered correctly
        entered_value = search_input.input_value()
        if entered_value != search_term:
            raise Exception(f"Search term entry fialed. Expected '{search_term}', got '{entered_value}'")
        
        # Execute the search
        search_button.click()
        
        # Wait for the seaach to complete
        self._wait_for_search_completion(page_object, search_config, baseline_count)
        
        # Get and return final result count
        final_count = self._get_results_count(search_config)
        logger.info(f"Search completed. Result count: {final_count}")
        
        return final_count

    def _wait_for_search_completion(self, page_object, search_config, baseline_count=None):
        """
        Wait for sarch completion using multi-layered timing strategy.
        
        Different web applications implement search differently.
        - Some make server requests (detected by network activity)
        - Some filter client-side (determined by DOM changes)
        - some use debouncing (requires patience)
        """
        logger.info("Waiting for serach completion")
        
        # Layer 1: Network activity (handles server-side searches)
        try:
            page_object.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception as e:
            # Timeout is acceptable - might be client-side search
            logger.warning(f"Network idle wait failed: {str(e)}")
            pass
        
        # Layer 2: DOM changes (handles client-side filtering)
        page_object.page.wait_for_timeout(1500) # Generous wait for debounced inputs
        
        # Layer 3: Result count change detection (if baseline provided)
        if baseline_count is not None:
            try:
                # Give extra time if results haven't changed yet.
                current_count = self._get_results_count(search_config)
                if current_count == baseline_count:
                    logger.warning("Result count unchanged, wiating loner for search processing")
                    page_object.page.wait_for_timeout(2000)
            except Exception as e:
                logger.warning(f"Result count check failed: {str(e)}")
                logger.warning("Waiting longer for search processing")
                page_object.page.wait_for_timeout(2000)
                
        # Layer 4: Final stabliazation
        page_object.page.wait_for_timeout(1000)
        
        logger.info("Search completion wait finished")
        
    def _get_results_count(self, search_config):
        """
            Get the current number of search results.
            
            This abstracts the counting logic so it can work with different
            result container types (tables, lists, grids, etc.).
        """
        try:
            results_container = search_config['results_container_getter']()
            return results_container.count()
        except Exception as e:
            logger.error(f"Failed to get results count: {str(e)}")
            return 0
        
    def _validate_search_expectations(self, test_case, actual_count):
        """
            Validate that search results meet expectations.
            
            This uses pytest-check for soft assertions, allowing multiple
            validations to run even if some fail.
        """
        from pytest_check import check
        
        test_name = test_case['name']
        search_term = test_case['search_term']
        
        if 'expected_min_results' in test_case:
            expected_min = test_case['expected_min_results']
            check.greater_equal(actual_count, expected_min,
                                f"{test_name}; Expected at least {expected_min} results for '{search_term}', got {actual_count}")
        
        if 'expected_max_results' in test_case:
            expected_max = test_case['expected_max_results']
            check.less_equal(actual_count, expected_max,
                            f"{test_name}; Expected at most {expected_max} results for '{search_term}', got {actual_count}")
            
        if 'expected_exact_results' in test_case:
            expected_exact = test_case['expected_exact_results']
            check.equal(actual_count, expected_exact,
                        f"{test_name}; Expected exactly {expected_exact} results for '{search_term}', got {actual_count}")
            
    def _reset_simple_search_state(self, page_object, search_config):
        """
            Reset search state to prepare for the next test case.
            
            This ensures test isolation - each search test starts from
            the same clean state regardless of what previous tests did.
        """
        logger.info("Restting search state for the next test case")
        
        # Clear the search input
        search_input = search_config['search_input_getter']()
        search_input.clear()
        
        # Execute the clear operations (should show all results)
        search_button = search_config['search_button_getter']()
        search_button.click()
        
        # Wait for reset to cpomplete
        self._wait_for_search_completion(page_object, search_config)
        
        # Verify the saerch input is acutally empty
        remaining_value = search_input.input_value()
        if remaining_value:
            logger.warning(f"Search input still contains '{remaining_value}' after reset")
            # Try one more time
            search_input.clear()
            page_object.page.wait_for_timeout(500)
            search_button.click()
            
        logger.info("Search state reset complete")