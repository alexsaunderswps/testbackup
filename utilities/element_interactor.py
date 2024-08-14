# element_interactor.py

import os
from .utils import logger
from datetime import datetime
from traceback import print_stack
from typing import Optional, List
from utilities.config import DEFAULT_TIMEOUT, EXTENED_TIMEOUT
from utilities.element_locator import ElementLocator
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ElementInteractor:
    
    def __init__(self, driver):
        self.driver = driver
        self.locator = ElementLocator()
        
    @staticmethod
    def scroll_to_element(driver: WebDriver, element: WebElement, timeout: int = DEFAULT_TIMEOUT) -> Optional[WebElement]:
        """_summary_

        Args:
            driver (WebDriver): _description_
            element (WebElement): _description_
            timeout (int, optional): _description_. Defaults to DEFAULT_TIMEOUT.

        Returns:
            Optional[WebElement]: _description_
        """
        try:
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            WebDriverWait(driver, timeout).until(EC.visibility_of(element))
            logger.info(f"Scrolled to {element}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible after scrolling within {timeout} seconds")
            return None
        
    @staticmethod
    def upload_file(file_input: WebElement, file_path: str) -> None:
        """_summary_

        Args:
            file_input (WebElement): _description_
            file_path (str): _description_
        """
        try:
            logger.info(f"Attempting to upload {file_input} from {file_path}")
            abs_file_path = os.path.abspath(file_path)
            file_input.send_keys(abs_file_path)
            logger.info(f"Successfully uploaded {file_input} found at {file_path}")
        except Exception as e:
            logger.error(f"Could not upload {file_input} from {file_path}")
            logger.error(f"Error with file uploadL: {str(e)}")
            
    def element_click(self, locator: str, locator_type: str = "XPATH") -> None:
        """_summary_

        Args:
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "XPATH".
        """
        try:
            element = self.locator.get_element(self.driver, locator, locator_type)
            element.click()
            logger.info(f"Element clicked successfully: {element.text}")
        except Exception as e:
            logger.error(f"Could not click {locator} with {locator_type}")
            logger.error(f"Error clicking element: {str(e)}")
            
    def element_send_input(self, data: str, locator: str, locator_type: str ="XPATH") -> None:
        """_summary_

        Args:
            data (str): _description_
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "XPATH".
        """
        try:
            element = self.locator.get_element(self.driver, locator, locator_type)
            element.send_keys(data)
            logger.info(f"Successfully sent {data} to {locator}")
        except Exception as e:
            logger.error(f"Failed to send {data} to {locator}")
            logger.error(f"Error sending data: {str(e)}")