# element_locator.py

import os
from .config import DEFAULT_TIMEOUT, EXTENED_TIMEOUT
from .utils import logger
from .selenium_utils import wait_for_element, wait_for_elements, wait_for_element_to_disapear
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import Optional, List


class ElementLocator:
    """A class for locating elements
    """
    
    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
    

    def get_element(self, locator: str, locator_type: str = "xpath", condition: str = "presence") -> Optional[WebElement]:
        """_summary_

        Args:
            driver (WebDriver): _description_
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "xpath".

        Returns:
            _type_: _description_
        """
        return wait_for_element(self.driver, locator, locator_type, condition, self.timeout)
        
    
    def is_element_present(self, locator: str, locator_type: str = 'xpath', condition: str = 'presence') -> bool:
        """_summary_

        Args:
            driver (WebDriver): _description_
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to 'xpath'.

        Returns:
            bool: _description_
        """
        element = wait_for_element(self.driver, locator, locator_type, condition, self.timeout)
        if element is not None:
            return True
        return False
        
        
    def check_elements_present(self, locator: str, locator_type: str = "xpath") -> bool:
        """_summary_

        Args:
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "xpath".

        Returns:
            bool: _description_
        """
        logger.info(f"Attempting to find element(s): {locator}")
        return wait_for_elements(self.driver, locator, locator_type, self.timeout)
    
    
    def check_element_has_disappeared(self, locator: str, locator_type: str = "xpath") -> bool:
        """_summary_

        Args:
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "xpath".

        Returns:
            bool: _description_
        """
        return wait_for_element_to_disapear(self.driver, locator, locator_type, self.timeout)