#screenshot_manager.py
import os
import time
from .config import SCREENSHOT_DIR
from utilities.utils import logger
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver

class ScreenshotManager:
    """A class for managing screenshots."""

    @staticmethod
    def take_screenshot(driver: WebDriver, file_name: str, shot_directory: str = SCREENSHOT_DIR ) -> None:
        """
        Take a screenshot of the current page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            file_name (str): Base name for the screenshot file.
            shot_directory (str): Directory to save the screenshot. If None, uses SCREENSHOT_DIR from config
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{file_name}_{timestamp}.png"

        # Use the provided shot_directory or fall back to SCREENSHOT_DIR from config
        screenshot_dir = shot_directory or SCREENSHOT_DIR
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_destination = os.path.join(screenshot_dir, file_name)

        try:
            time.sleep(1)
            driver.save_screenshot(screenshot_destination)
            logger.info(f"Screenshot saved to: {screenshot_destination}")
        except Exception as e:
            logger.error(f"Failed to save screenshot: {str(e)}")