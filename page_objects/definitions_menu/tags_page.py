# tags_page.py (Playwright version)
import os
from typing import Tuple, List
from dotenv import load_dotenv
from page_objects.common.base_page import BasePage
from utilities.utils import logger

load_dotenv()

# Environmental Variables

BASE_URL = os.getenv("QA_BASE_URL")

class TagsPage(BasePage):
    """
    Page object for the Tags page using Playwright.

    This class provides methods to interact with elements on the Tags page,
    following the established pattern of method-based element getters that return
    Playwright locators for reliable element interaction.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.logger = logger
        
    # Element locators - Using method-based approach for consistency
    def get_development_notice(self):
        """Get the development notice element."""
        return self.page.get_by_text("This page is currently in development")

    # Check Page Element presence
    def verify_development_notice(self):
        """Verify the presence of the development notice element."""
        return self.get_development_notice().is_visible()