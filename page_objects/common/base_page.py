#base_page.py
from utilities.config import DEFAULT_TIMEOUT, SCREENSHOT_DIR
from utilities.element_interactor import ElementInteractor
from utilities.element_locator import ElementLocator
from utilities.screenshot_manager import ScreenshotManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """_summary_
    """
    def __init__(self, driver):
        """_summary_

        Args:
            driver (_type_): _description_
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.locator = ElementLocator(driver)
        self.interactor = ElementInteractor(driver)
        self.screenshot = ScreenshotManager()
        
    class CommonLocators:
        
        HEADER_LOGO = "//section//img[@alt='logo']"
        # FOOTER =
        LOGIN_LINK = "//section//button[text()='LOG IN']"
        LOGOUT_BUTTON = "//section//button[text()='LOG OUT']"
    
    class NavigationLocators:
        VIDEOS_LINK = "//li//a[contains(@href,'/') and contains(text(), 'Videos')]"
        COLLECTIONS_LINK = "//li//a[@href='/videoCollections']"
        PORTALS_LINK = "//li//a[@href='/portals']"
        # Needs update once development has started
        USERS_LINK = "//li//a[text()='Users']"
        # Definitiions is a button not a link
        DEFINITIONS_BUTTON = "//li//button[text()='Definitions']"
        ORGS_LINK = "//li//a[@href='/organizations']"
        # Needs update once development has started
        INSTA_LINK = "//li//a[text()='Installations']"

        
    # Basic methods
    def find_logo(self):
        return self.locator.is_element_present(self.CommonLocators.HEADER_LOGO)
    
    def find_login_link(self):
        return self.locator.is_element_present(self.CommonLocators.LOGIN_LINK)
    
    def find_logout(self):
        return self.locator.is_element_present(self.CommonLocators.LOGOUT_BUTTON)
    
    def logout_site(self):
        self.interactor.element_click(self.CommonLocators.LOGOUT_BUTTON)
        
    def get_page_title(self):
        return self.driver.title
    
    def get_current_url(self):
        return self.driver.current_url
    
    def navitate_to(self, url: str):
        self.driver.get(url)
    
    def refresh_page(self):
        self.driver.refresh()
        
    def go_back(self):
        self.driver.back()
        
    def go_forward(self):
        self.driver.forward()
        
    def swtich_to_frame(self, frame_reference: str):
        self.driver.switch_to.frame(frame_reference)
    
    def swtich_to_default_content(self):
        self.driver.swtich_to.default_content()
        
    def accept_alert(self):
        self.driver.swtich_to.alert.accept()
    
    def dismiss_alert(self):
        self.driver.switch_to.alert.dismiss()
    
    def get_alert_text(self) -> str:
        return self.driver.switch_to.alert.text
    
    # Navigation methods
    
    def find_videos_button(self):
        return self.locator.is_element_present(self.NavigationLocators.VIDEOS_LINK)
    
    def go_videos_page(self):
        self.interactor.element_click(self.NavigationLocators.VIDEOS_LINK)
        
    def find_collections_button(self):
        return self.locator.is_element_present(self.NavigationLocators.COLLECTIONS_LINK)
    
    def go_collections_page(self):
        self.interactor.element_click(self.NavigationLocators.COLLECTIONS_LINK)
        
    def find_portals_button(self):
        return self.locator.is_element_present(self.NavigationLocators.PORTALS_LINK)
    
    def go_portals_page(self):
        self.interactor.element_click(self.NavigationLocators.PORTALS_LINK)
    
    def find_users_button(self):
        return self.locator.is_element_present(self.NavigationLocators.USERS_LINK)
    
    def go_users_page(self):
        self.interactor.element_click(self.NavigationLocators.USERS_LINK)

    def find_organizations_button(self):
        return self.locator.is_element_present(self.NavigationLocators.ORGS_LINK)
    
    def go_organizations_page(self):
        self.interactor.element_click(self.NavigationLocators.ORGS_LINK)
        
    def find_installations_button(self):
        return self.locator.is_element_present(self.NavigationLocators.INSTA_LINK)
    
    def go_installations_page(self):
        self.interactor.element_click(self.NavigationLocators.INSTA_LINK)
        
    # Handle Definitions as it is a dropdown list
    
    def find_definitions_buttons(self):
        self.locator.is_element_present(self.NavigationLocators.DEFINITIONS_BUTTON)