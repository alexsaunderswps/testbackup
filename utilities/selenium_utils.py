# selenium_utils.py
from .config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT
from utilities.utils import logger
from typing import Optional, Tuple, Any
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_by_type(locator_type: str ="xpath"):
    """Convert string locator type to Selenium's By class attribute

    Args:
        locator_type (str, optional): The locator type used to find an element with the By method. Defaults to "xpath".

    Returns:
        dictionary string: the By.Locator_Type to be used to find an element.
    """
    from selenium.webdriver.common.by import By # Imported here to avoid circular imports

    locator_type = locator_type.lower()
    locator_map = {
        "id": By.ID,
        "xpath": By.XPATH,
        "css": By.CSS_SELECTOR,
        "classname": By.CLASS_NAME,
        "linktext": By.LINK_TEXT,
        "name": By.NAME,
        "tag": By.TAG_NAME,
        "partiallinktext": By.PARTIAL_LINK_TEXT
    }
    if locator_type not in locator_map:
        logger.error(f"Locator type: {locator_type} is not supported.")
        return None
    return locator_map[locator_type]

def wait_for_element(driver: WebDriver, locator: str, locator_type: str = "xpath", condition: str = "presence", timeout: int = DEFAULT_TIMEOUT) -> Optional[WebElement]:
    """Wait for an element to be in a certain condition

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (str): The locator of the element.
        locator_type (str, optional): The type of locator used by the By. statement to find the locator (xpath, id, css, etc). Defaults to "xpath".
        condition (str, optional): The condition to wait for ("presence", "clickable", "visible"). Defaults to "presence".
        timeout (int, optional): Maximum amount of time to wait for the element to statisfy the condition. Defaults to DEFAULT_TIMEOUT.

    Returns:
        Optional[WebElement]: The WebElement if found, None if otherwise
    """
    by_type = get_by_type(locator_type)
    if by_type is None:
        logger.error(f"By statement not a valid by_type: {by_type}")
        return None
    wait = WebDriverWait(driver, timeout)
    try:
        logger.info(f"Attempting to get locator: {locator} with condition: {condition}")
        if condition == "presence":
            return wait.until(EC.presence_of_element_located((by_type, locator)))
        elif condition == "clickable":
            return wait.until(EC.element_to_be_clickable((by_type, locator)))
        elif condition == "visible":
            return wait.until(EC.visibility_of_element_located((by_type, locator)))
        else: 
            logger.error(f"Unsupported wait conition: {condition}")
    except TimeoutException:
        logger.error(f"Element not found with locator: {locator}, condition: {condition}")
        return None
    except NoSuchElementException:
        logger.error(f"Not such element found with locator: {locator}, and condition: {condition}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in wait_for_element: {str(e)}")
        return None

def wait_for_elements(driver: WebDriver, locator: str, locator_type: str = "xpath", timeout: int = DEFAULT_TIMEOUT) -> list[WebElement]:
    """Wait for multiple elements to be in a certain present

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (str): The locator of the elements.
        locator_type (str, optional): The type of locator used by the By. statement to find the locator (xpath, id, css, etc).  Defaults to "xpath".
        timeout (int, optional): Maximum amount of time to wait for the element to statisfy the condition. Defaults to DEFAULT_TIMEOUT.

    Returns:
        Optional[WebElement]: A list of WebElement if found, empty if otherwise
    """
    by_type = get_by_type(locator_type)
    if by_type is None:
        logger.error(f"By statement not a valid by_type: {by_type}")
        return None
    
    wait = WebDriverWait(driver, timeout)
    try:
        elements = wait.until(EC.presence_of_all_elements_located((by_type, locator)))
        logger.info(f"{len(elements)} element(s) found with locator: {locator}")
        return elements
    except TimeoutException:
        logger.error(f"No elements found with locator: {locator}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in wait_for_elements: {str(e)}")
        return []
    
def wait_for_element_to_disapear(driver: WebDriver, locator: str, locator_type: str = "xpath", timeout: int = DEFAULT_TIMEOUT) -> bool:
    """Wait for an element to become invisible or to be removed from the DOM

    Args:
        driver (WebDriver): Selenium WebDriver instance
        locator (str): The locator of the element.
        locator_type (str, optional): The type of locator used by the By. statement to find the locator (xpath, id, css, etc.). Defaults to "xpath".
        timeout (int, optional): Maximum time to wait for the element to disappear. Defaults to DEFAULT_TIMEOUT.

    Returns:
        bool: True if the element has disappeared, False otherwise
    """
    by_type = get_by_type(locator_type)
    if by_type is None:
        logger.error(f"By statement not a valid by_type: {by_type}")
        return False
    
    wait = WebDriverWait(driver, timeout)
    try:
        logger.info(f"Waiting until the element disappears.")
        return wait.until(EC.invisibility_of_element_located((by_type, locator)))
    except TimeoutException:
        logger.error(f"Element with locator: {locator} did not disappear within the timeout period.")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in wait_for_element_to_disappear: {str(e)}")
        return False
    