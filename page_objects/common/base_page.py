#base_page.py
from utilities.config import DEFAULT_TIMEOUT, SCREENSHOT_DIR
from utilities import ElementInteractor
from utilities import ElementLocator
from utilities import ScreenshotManager
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
        self.locator = ElementLocator()
        self.interactor = ElementInteractor()
        self.screenshot = ScreenshotManager()
        
    class CommonLocators:
        
        HEADER_LOGO = ("//section//img[@alt='logo']", "xpath")
        # FOOTER =
        LOGIN_LINK = ("//section//button[text()='LOG IN']", "xpath")
        LOGOUT_BUTTON = ("//section//button[text()='LOG OUT']", "xpath")
        
    def find_logo(self):
        return self.locator.is_element_present(*self.CommonLocators.HEADER_LOGO)
    
    def find_login_link(self):
        return self.locator.is_element_present(*self.CommonLocators.LOGIN_LINK)
    
    def find_logout(self):
        return self.locator.is_element_present(*self.CommonLocators.LOGOUT_BUTTON)
    
    def logout_site(self):
        self.interactor.element_click(*self.CommonLocators.LOGOUT_BUTTON)
        
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