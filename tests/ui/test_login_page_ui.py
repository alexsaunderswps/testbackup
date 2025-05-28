#test_login_page_ui.py
import os
import pytest
from faker import Faker
from dotenv import load_dotenv
from pytest_check import check
from fixtures.login_fixtures import login_page
from utilities.utils import get_browser_name, logger

# Initialize Faker
fake = Faker()

# Load environmental variables
load_dotenv()
QA_LOGIN_URL = os.getenv("QA_LOGIN_URL").replace("\\x3a", ":")
SYS_ADMIN_USER = os.getenv("SYS_ADMIN_USERNAME")
SYS_ADMIN_PASS = os.getenv("SYS_ADMIN_PASSWORD")
ORG_WPS_USER = os.getenv("ORG_ADMIN_WPS_USERNAME")
ORG_WPS_PASS = os.getenv("ORG_ADMIN_WPS_PASSWORD")

class TestLoginPageUI:
    """
    Test suite for the Login page UI elements using Playwright.
    
    This class focuses on verifying that users can see and interact with
    login interface elements. It follows the established pattern for 
    Playwright-based UI testing, ensuring consistent user experience
    across different browsers and scenarios.
    
    The login page is unique because it's the entry point to the application,
    so these tests verify the fundamental interface elements that every user
    must successfully interact with to access the system.
    """
    
    @pytest.mark.UI
    @pytest.mark.login
    def test_login_page_essential_elements(self, login_page):
        """
        Test that all essential login elements are present and accessible.
        
        This test verifies the core elements that users need to authenticate:
        username field, password field, and login button. These elements form
        the fundamental interface for system access.
        
        The test ensures that each element is not only present in the DOM but
        also properly rendered and accessible to users, which is critical for
        both usability and accessibility compliance.
        
        Args:
            login_page: The LoginPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_login_page_essential_elements")
        for lp in login_page:
            browser_name = get_browser_name(lp.page)
            logger.info(f"Testing essential login elements on {browser_name}")
            
            # Test username input field presence and accessibility
            username_input = lp.get_username_input()
            check.is_true(username_input.count() > 0, 
                f"Username input field not found on {browser_name}")
            
            if username_input.count() > 0:
                # Verify the field is actually interactable
                check.is_true(username_input.is_visible(), 
                    f"Username input field not visible on {browser_name}")
                check.is_true(username_input.is_enabled(), 
                    f"Username input field not enabled on {browser_name}")
            
            # Test password input field presence and accessibility  
            password_input = lp.get_password_input()
            check.is_true(password_input.count() > 0, 
                f"Password input field not found on {browser_name}")
            
            if password_input.count() > 0:
                # Verify the field is actually interactable
                check.is_true(password_input.is_visible(), 
                    f"Password input field not visible on {browser_name}")
                check.is_true(password_input.is_enabled(), 
                    f"Password input field not enabled on {browser_name}")
            
            # Test login button presence and accessibility
            login_button = lp.get_login_button()
            check.is_true(login_button.count() > 0, 
                f"Login button not found on {browser_name}")
            
            if login_button.count() > 0:
                # Verify the button is actually clickable
                check.is_true(login_button.is_visible(), 
                    f"Login button not visible on {browser_name}")
                check.is_true(login_button.is_enabled(), 
                    f"Login button not enabled on {browser_name}")
            
            logger.info(f"Verification Successful :: All essential login elements found and accessible on {browser_name}")
    
    @pytest.mark.UI
    @pytest.mark.login
    def test_login_form_interaction_capability(self, login_page):
        """
        Test that login form elements can be interacted with properly.
        
        Beyond just being present, form elements need to accept user input
        correctly. This test verifies that users can actually type in the
        input fields and that the form behaves as expected during interaction.
        
        This is particularly important for login forms because any interaction
        issues here prevent users from accessing the entire application.
        
        Args:
            login_page: The LoginPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_login_form_interaction_capability")
        test_username = "test_user_input"
        test_password = "test_pass_input"
        
        for lp in login_page:
            browser_name = get_browser_name(lp.page)
            logger.info(f"Testing form interaction capability on {browser_name}")
            
            try:
                # Test username field accepts input
                username_input = lp.get_username_input()
                if username_input.count() > 0:
                    username_input.fill(test_username)
                    entered_username = username_input.input_value()
                    check.equal(entered_username, test_username, 
                        f"Username field did not accept input correctly on {browser_name}")
                    
                    # Clear the field to clean up
                    username_input.clear()
                
                # Test password field accepts input
                password_input = lp.get_password_input()
                if password_input.count() > 0:
                    password_input.fill(test_password)
                    entered_password = password_input.input_value()
                    check.equal(entered_password, test_password, 
                        f"Password field did not accept input correctly on {browser_name}")
                    
                    # Clear the field to clean up
                    password_input.clear()
                
                logger.info(f"Verification Successful :: Form interaction works correctly on {browser_name}")
                
            except Exception as e:
                logger.error(f"Error during form interaction test on {browser_name}: {str(e)}")
                check.fail(f"Form interaction test failed on {browser_name}: {str(e)}")
    
    @pytest.mark.UI
    @pytest.mark.login
    def test_login_page_accessibility_attributes(self, login_page):
        """
        Test that login form elements have proper accessibility attributes.
        
        Accessibility is crucial for login forms since they're the gateway to
        the application. This test verifies that form elements have appropriate
        labels, roles, and other attributes that screen readers and other
        assistive technologies need to help users navigate the interface.
        
        This testing ensures that the application is usable by people with
        disabilities, which is both an ethical imperative and often a legal
        requirement for many organizations.
        
        Args:
            login_page: The LoginPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_login_page_accessibility_attributes")
        
        for lp in login_page:
            browser_name = get_browser_name(lp.page)
            logger.info(f"Testing accessibility attributes on {browser_name}")
            
            # Test username field accessibility
            username_input = lp.get_username_input()
            if username_input.count() > 0:
                # Check for proper input type or role
                input_role = username_input.get_attribute("role")
                input_type = username_input.get_attribute("type")
                aria_label = username_input.get_attribute("aria-label")
                placeholder = username_input.get_attribute("placeholder")
                
                # At least one method of labeling should be present
                has_labeling = any([
                    input_role == "textbox",
                    input_type in ["text", "email"],
                    aria_label and "username" in aria_label.lower(),
                    placeholder and "username" in placeholder.lower()
                ])
                
                check.is_true(has_labeling, 
                    f"Username field lacks proper accessibility labeling on {browser_name}")
            
            # Test password field accessibility  
            password_input = lp.get_password_input()
            if password_input.count() > 0:
                # Password fields should have type="password"
                input_type = password_input.get_attribute("type")
                check.equal(input_type, "password", 
                    f"Password field should have type='password' on {browser_name}")
                
                # Check for labeling
                aria_label = password_input.get_attribute("aria-label")
                placeholder = password_input.get_attribute("placeholder")
                
                has_labeling = any([
                    aria_label and "password" in aria_label.lower(),
                    placeholder and "password" in placeholder.lower()
                ])
                
                check.is_true(has_labeling, 
                    f"Password field lacks proper accessibility labeling on {browser_name}")
            
            # Test login button accessibility
            login_button = lp.get_login_button()
            if login_button.count() > 0:
                button_text = login_button.inner_text()
                button_role = login_button.get_attribute("role")
                button_type = login_button.get_attribute("type")
                
                # Button should have clear purpose indication
                has_clear_purpose = any([
                    button_text and "log" in button_text.lower(),
                    button_role == "button",
                    button_type == "submit"
                ])
                
                check.is_true(has_clear_purpose, 
                    f"Login button lacks clear purpose indication on {browser_name}")
            
            logger.info(f"Verification Successful :: Accessibility attributes properly configured on {browser_name}")
    
    @pytest.mark.UI
    @pytest.mark.login
    def test_login_page_responsive_layout(self, login_page):
        """
        Test that login page elements maintain proper layout across different viewport sizes.
        
        Users access applications from various devices with different screen sizes.
        The login page must be usable on mobile phones, tablets, and desktop computers.
        This test verifies that essential elements remain visible and accessible
        when the viewport size changes.
        
        Responsive design for login pages is particularly critical because users
        often need to access applications urgently from whatever device is available.
        
        Args:
            login_page: The LoginPage fixture providing page objects for each browser
        """
        logger.debug("Starting test_login_page_responsive_layout")
        
        # Define test viewport sizes: mobile, tablet, desktop
        viewport_sizes = [
            {"width": 375, "height": 667, "name": "Mobile"},
            {"width": 768, "height": 1024, "name": "Tablet"}, 
            {"width": 1920, "height": 1080, "name": "Desktop"}
        ]
        
        for lp in login_page:
            browser_name = get_browser_name(lp.page)
            logger.info(f"Testing responsive layout on {browser_name}")
            
            for viewport in viewport_sizes:
                logger.info(f"Testing {viewport['name']} viewport ({viewport['width']}x{viewport['height']}) on {browser_name}")
                
                # Set the viewport size
                lp.page.set_viewport_size({"width": viewport["width"], "height": viewport["height"]})
                
                # Wait for layout to adjust
                lp.page.wait_for_timeout(500)
                
                # Test that essential elements are still visible
                username_input = lp.get_username_input()
                if username_input.count() > 0:
                    check.is_true(username_input.is_visible(), 
                        f"Username input not visible on {viewport['name']} viewport on {browser_name}")
                
                password_input = lp.get_password_input()
                if password_input.count() > 0:
                    check.is_true(password_input.is_visible(), 
                        f"Password input not visible on {viewport['name']} viewport on {browser_name}")
                
                login_button = lp.get_login_button()
                if login_button.count() > 0:
                    check.is_true(login_button.is_visible(), 
                        f"Login button not visible on {viewport['name']} viewport on {browser_name}")
                
                logger.info(f"Verification Successful :: Elements visible on {viewport['name']} viewport on {browser_name}")
        
        logger.info("Responsive layout testing completed")
    