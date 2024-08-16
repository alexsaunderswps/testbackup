# element_interactor.py

import os
from .config import FILE_UPLOAD_DIR
from utilities.utils import logger
from .selenium_utils import wait_for_element
from typing import Optional
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT, MAX_RETRIES
from utilities.element_locator import ElementLocator
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ElementInteractor:
    
    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.locator = ElementLocator(driver)
        self.logger = logger
    
        

    def scroll_to_element(self, driver: WebDriver, element: WebElement, timeout: int = DEFAULT_TIMEOUT) -> Optional[WebElement]:
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
            self.logger.info(f"Scrolled to {element}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible after scrolling within {timeout} seconds")
            return None
        except NoSuchElementException:
            self.logger.error(f"Element could not be found with {element}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error with scroll_to_element: {str(e)}")
            return None
        
        

    def upload_file(self, file_input: WebElement, file_name: str) -> bool:
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
            self.logger.info(f"Attempting to upload {file_name} from {file_path}")
            file_input.send_keys(abs_file_path)
            self.logger.info(f"Successfully uploaded {file_name} found at {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Could not upload {file_name} from {file_path}")
            self.logger.error(f"Error with file uploadL: {str(e)}")
            return False
    
    
    def clear_element_input(self, locator: str, locator_type: str = "xpath", condition: str = "presence", max_retries: int = MAX_RETRIES) -> bool:
        """_summary_

        Args:
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "xpath".
            condition (str, optional): _description_. Defaults to "presence".
            max_retries (int, optional): _description_. Defaults to MAX_RETRIES.

        Returns:
            bool: _description_
        """
        for attempt in range(max_retries):
            try:
                element = wait_for_element(self.driver, locator, locator_type, condition, self.timeout)
                if element:
                    element.clear()
                    self.logger.info(f"Element with locator: {locator}, cleared.")
                    return True
                else:
                    self.logger.warning(f"Element not found with locator: {locator}. Retry attempt {attempt + 1} of {MAX_RETRIES}.")     
            except StaleElementReferenceException:
                self.logger.warning(f"StaleElementReferenceException occured. Retry attempt {attempt + 1} of {MAX_RETRIES}.")
            except Exception as e:
                self.logger.error(f"Unexpected exception: {str(e)}. Retry attempt {attempt + 1} of {MAX_RETRIES}.")
                    
        self.logger.error(f"Failed to clear {locator} in {MAX_RETRIES} attempts.")
        return False
        
    
    def element_click(self, locator: str, locator_type: str = "xpath") -> bool:
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
            self.logger.info(f"Element clicked successfully: {element.text}")
            return True
        return False
            
            
    def element_send_input(self, data: str, locator: str, locator_type: str ="xpath", clear_first: bool = False) -> None:
        """_summary_

        Args:
            data (str): _description_
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "xpath".
            clear_first (bool, optional): _description_. Defaults to True.
        """
        element = wait_for_element(self.driver, locator, locator_type, "presence", self.timeout)
        if element:
            try:
                if clear_first:
                    self.clear_element_input(locator, locator_type)
                    element.send_keys(data)
                    self.logger.info(f"Successfully sent {data} to {locator}")
                else: 
                    element.send_keys(data)
                    self.logger.info(f"Successfully sent {data} to {locator}")
            except Exception as e:
                self.logger.error(f"Unexpected error sending input: {str(e)}")
                
                
    def element_get_text(self, locator: str, locator_type: str = "xpath", max_retries: int = MAX_RETRIES) -> Optional[str]:
        """_summary_

        Args:
            locator (str): _description_
            locator_type (str, optional): _description_. Defaults to "xpath".
            max_retries (int, optional): _description_. Defaults to MAX_RETRIES.

        Returns:
            Optional[str]: _description_
        """
        for attempt in range(max_retries):
            try:
                element = wait_for_element(self.driver, locator, locator_type, "visible", self.timeout)
                if element:
                        text = element.text
                        self.logger.info(f"Got text: {text} from element with locator: {locator}")
                        return text
                else:
                    self.logger.warning(f"Element not found with locator {locator}: Retry attempt {attempt + 1} of {MAX_RETRIES}")
            except StaleElementReferenceException:
                self.logger.warning(f"StaleElementReferenceException occured. Retry attempt {attempt + 1} of {MAX_RETRIES}")
            except Exception as e:
                
                self.logger.error(f"Unexpected error: {str(e)}. Retry attempt {attempt + 1} of {MAX_RETRIES}")
        self.logger.error(f"No text found with locator: {locator}")
        return None