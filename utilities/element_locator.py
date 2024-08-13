# element_locator.py

import os
from .utils import logger
from typing import Otional, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import datetime

class ElementLocator:
    """A class for locating elements
    """
    
    def __init__(self, driver):
        self.driver = driver
        
    @staticmethod
    def get_by_type(locator_type: str ="xpath"):
        """_summary_

        Args:
            locator_type (str, optional): _description_. Defaults to "xpath".

        Returns:
            _type_: _description_
        """
        locator_type = locator_type.lower()
        locator_map = {
            "id": By.ID,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "classname": By.CLASS_NAME,
            "linktext": By.LINK_TEXT,
            "name": By.NAME
        }
        if locator_type not in locator_map:
            logger.error(f"Locator type: {locator_type} is not supported.")
            return None
        return locator_map[locator_type]
    
    @staticmethod
    def get_element(driver: WebDriver, locator: str, locator_type: str = "xpath"):
        """_summary_

        Args:
            driver (WebDriver): _description_
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "xpath".

        Returns:
            _type_: _description_
        """
        try:
            by_type = ElementLocator.get_by_type(locator_type)
            if by_type is None:
                return None
            element = driver.find_element(by_type, locator)
            logger.info(f"Element found with locator: {locator}")
            return element
        except NoSuchElementException:
            logger.error(f"No such element found with locator: {locator}")
            return None
        
    @staticmethod
    def is_element_present(driver: WebDriver, locator: str, locator_type: str = 'xpath') -> bool:
        """_summary_

        Args:
            driver (WebDriver): _description_
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to 'xpath'.

        Returns:
            bool: _description_
        """
        try:
            driver.find_element(locator_type, locator)
            logger.info(f"Element found with locator: {locator}")
            return True
        except NoSuchElementException:
            logger.error(f"No such element found with locator: {locator}")
            return False
        
    @staticmethod
    def check_elements_present(driver: WebDriver, locator: str, locator_type: str = "xpath") -> bool:
        elements = driver.find_elements(locator_type, locator)
        if elements:
            logger.info(f"{len(elements)} element(s) found with locator: {locator}")
            return True
        else:
            logger.error(f"No elements found with locator: {locator}")
            return False