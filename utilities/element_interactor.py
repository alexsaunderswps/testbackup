# element_interactor.py

import os
from .config import FILE_UPLOAD_DIR
from .utils import logger
from .selenium_utils import wait_for_element, wait_for_elements, wait_for_element_to_disapear
from typing import Optional
from utilities.config import DEFAULT_TIMEOUT, EXTENED_TIMEOUT
from utilities.element_locator import ElementLocator
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ElementInteractor:
    
    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.locator = ElementLocator()
        self.timeout = timeout
        
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
        except NoSuchElementException:
            logger.error(f"Element could not be found with {element}")
        
    @staticmethod
    def upload_file(file_input: WebElement, file_name: str) -> bool:
        """Uploads a file using a pre-located file input element

        Args:
            file_input (WebElement): the file input element
            file_name (str): the name of the file to be uploaded

        Returns:
            bool: _description_
        """
        try:
            file_path = os.path.join(FILE_UPLOAD_DIR, file_name)
            abs_file_path = os.path.abspath(file_path)
            logger.info(f"Attempting to upload {file_name} from {file_path}")
            file_input.send_keys(abs_file_path)
            logger.info(f"Successfully uploaded {file_name} found at {file_path}")
            return True
        except Exception as e:
            logger.error(f"Could not upload {file_name} from {file_path}")
            logger.error(f"Error with file uploadL: {str(e)}")
            return False
            
    def element_click(self, locator: str, locator_type: str = "XPATH") -> bool:
        """_summary_

        Args:
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "XPATH".

        Returns:
            bool: _description_
        """
        element = wait_for_element(self.driver, locator, locator_type, "clickable", self.timeout)
        if element:
            element.click()
            logger.info(f"Element clicked successfully: {element.text}")
            return True
        return False
            
    def element_send_input(self, data: str, locator: str, locator_type: str ="XPATH") -> None:

        try:
            element = self.locator.get_element(self.driver, locator, locator_type)
            element.send_keys(data)
            logger.info(f"Successfully sent {data} to {locator}")
        except Exception as e:
            logger.error(f"Failed to send {data} to {locator}")
            logger.error(f"Error sending data: {str(e)}")