# Defines functions for use across test files in pytest

import os
import pytest
import time
from datetime import datetime
from dotenv import load_dotenv
from page_objects.authentication.login_page import LoginPage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from typing import Union, List, Tuple
from utilities.config import LOGIN_BUTTON, LOGOUT_BUTTON
from utilities.utils import logger, start_test_capture, end_test_capture, get_logs_for_test
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT
from utilities.element_locator import ElementLocator

# Load and define environmental variables
load_dotenv()
ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")
LOGIN_URL = os.getenv("QA_LOGIN_URL")

# Initialize ElementLocator
locator = ElementLocator()

# Define pytest addoption for Command Line running of Pytest with options
def pytest_addoption(parser):
    """
    Add custom command line options to pytest.
    
    This function is called by pytest to add custom options to the command line parser.
    It defines options for browser selection, test setup type, headless and private mode,
    and login credentials
    
    Args:
        parser (argparse.Parser): The pytest command line parser.
        
    Example:
        pytest --browser firefox --headless True
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Specify the browser, chrome, edge, firefox, or all."
    )
    parser.addoption(
        "--setup-type",
        action="store",
        default="isolated",
        help="Specify the session type: isolated or continuous" # Isolated setsup and tearsdown each test, continuous setsup and tearsdown at start and end of run
    )
    parser.addoption(
        "--headless",
        action="store",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--private",
        action="store",
        default=False,
        help="Run tests in private or incognito mode"
    )
    parser.addoption(
        "--username",
        action="store",
        default=ADMIN_USER,
        help="Username for login"
    )
    parser.addoption(
        "--password",
        action="store",
        default=ADMIN_PASS,
        help="Password for login"
    )


# Define Setup and Teardown steps
def chrome_setup(headless: bool, private: bool) -> webdriver:
    """
    Sets up a Chrome WebDriver with specified options.
    """
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless")
    if private:
        options.add_argument("--incognito")
    return webdriver.Chrome(options=options)

def edge_setup(headless:bool, private: bool) -> webdriver:
    """
    Sets up an Edge WebDriver with specified options
    """
    options = EdgeOptions()
    if headless:
        options.add_argument("--headless")
    if private:
        options.add_argument("--inprivate")
    return webdriver.Edge(options=options)

def firefox_setup(headless:bool, private:bool) -> webdriver:
    """
    Sets up a Firefox WebDriver with specified options
    """
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    if private:
        options.add_argument("--private")
    return webdriver.Firefox(options=options)

def perform_setup(browser_name: str, headless: bool, private: bool) -> webdriver:
    """
    Sets up WebDriver instance(s) for the specified browser with given options.
    
    This function initializes WebDriver(s) for Chrome, Edge, or Firefox browsers.
    It configures the browser(s) according to the headless and private browsing options,
    maximizes the window(s), sets up a WebDriverWait instance(s), and prepares for test capture.

    Args:
        browser_name (str): The name of the browser to set up.
                            Must be one of "chrome", "edge", "firefox", or "all".
        headless (bool): If True, the browser will run in headless mode.
        private (bool): If True, the browser will run in private/incognito mode.

    Raises:
        ValueError: If an unsupported browser name is provided.

    Returns:
        Union[Tuple[WebDriver, WebDriverWait], List[Tuple[WebDriver, WebDriverWait]]]:
            - If browser_name is not "all": A tuple containing the WebDriver and WebDriverWait instances.
            - If browser_name is "all": A list of tuples, each containing WebDriver and WebDriverWait instances
            for each supported browser.
    
    Example:
        # Set up a single browser
        driver, wait = perform_setup("chrome", headless=True, private=False)

        # Set up all supported browsers
        all_browsers = perform_setup("all", headless=False, private=True)
        for driver, wait in all_browsers:
            # Use each driver and wait instance
    """
    logger.info("*" * 80)
    logger.info(f"Setting up {browser_name} browser in setup")
    logger.info("*" * 80)
    setup_functions = {
        "chrome": chrome_setup,
        "edge": edge_setup,
        "firefox": firefox_setup
    }
    if browser_name.lower() == "all":
        return [setup_single_browser(browser, setup_functions[browser], headless, private) 
                for browser in setup_functions.keys()]

    setup_func = setup_functions.get(browser_name.lower())
    if not setup_func:
        raise ValueError(f"Unsupported browser requrest: {browser_name}")
    
    return setup_single_browser(browser_name, setup_func, headless, private)

def setup_single_browser(browser_name: str, setup_func, headless: bool, private: bool) -> webdriver:
    """
    Sets up a single browser instance and works with perform_setup to allow multiple browser instances

    Args:
        browser_name (str): The name of the browser to set up.
            Must be one of "chrome", "edge", "firefox", or "all".
        setup_func (function): passed from perform_setup
        headless (bool): If True, the browser will run in headless mode.
        private (bool): If True, the browser will run in private/incognito mode.

    Returns:
        Tuple: A tuple containing the WebDriver and WebDriverWait instances.
        
    Note:
    - The function starts with a blank page (about:blank) after setup.
    - Attempts to delete all cookies and, if not a Firefox instances, clears local storage.
    Firefox throws a security warning.
    - Test capture is initiated using the driver's session ID.
    - The WebDriver window is maximized by default.
    
    """
    driver = setup_func(headless, private)
    driver.maximize_window()
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    
    # Navigate to a blank website before clearing data
    driver.get("about:blank")
    
    # Clear cookies and cache just in case
    logger.debug("Clearing browser data.")
    try:
        driver.delete_all_cookies()
        if browser_name != 'firefox':
            logger.debug("Attempting to clear local and session storage")
            driver.get(LOGIN_URL)
            driver.execute_script("localStorage.clear();")
            driver.execute_script("sessionStorage.clear();")
    except Exception as e:
        logger.error(f"Error clearing browser data: {str(e)}")
    finally:
        driver.get("about:blank")
    
    start_test_capture(driver.session_id)
    
    return driver, wait

@pytest.fixture(scope="function")
def setup_isolated(request):
    """
    Sets up an isolated test environment for each test function
    
    This fixture creates a new browser instance for each test, configured according
    to the command line options. It handles the setup before the test and 
    ensures proper teardown after the test is complete.

    Args:
        request (FixtureRequest): The pytest request object, containing information
                                    about the requesting test function.

    Yields:
        tuple or list of tuples: A tuple containing (WebDriver, WebDriverWait) if
                                    a single browser is configured, or a list of 
                                    such tuples if multiple browsers are set up.
                                    
    Notes:
        - After yielding the driver(s), the fixture performs cleanup operations.
        
    Example:
        def test_example(setup_isolated):
            test_pages = []
            for driver, wait in setup_isolated:
                test_pages.append(TestPage(driver))
            yield test_pages
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    private = request.config.getoption("--private")
    result = perform_setup(browser, headless, private)
    
    if not isinstance(result, list):
        result = [result]
    
    logger.debug(f"setup_isolated fixture: yielding {len(result)} browser(s)")
    yield result
    
    logger.debug("setup_isolated fixture: starting teardown")
    
    # Teardown
    for driver, wait in result:
        logger.info(f"Performing teardown of isolated test for {driver.name}")
        perform_teardown(driver, wait)
    logger.debug("setup_isolated fixture: teardown complete")

@pytest.fixture
def logged_in_browser(setup_isolated, request):
    """
    Fixture that provides logged-in browser instance(s) for tests that require pre-authenitcation.

    Args:
        setup_isolated (fixture): A pytest fixture that provides a list of tuples,
                                    each containing a WebDriver and WebDriverWait instance.
        request (FixtureRequest): The pytest request object, containing information
                                    about the requesting test function, including test configuration.

    Yields:
        List[LoginPage]: A list of LoginPage objects, one for each logged-in browser session.
                            Each LoginPage object represents a logged-in browser state and
                            can be used to interact with the authenticated application.
    
    Note:
        - This fixture uses the username and password specified in the pytest command-lie options
            (--username and --password), falling back to default admin credentials if not provided.
        - The fixture logs the start and end of its execution, as well as login attempts for each browser.
        - After yielding the logged-in pages, any necessary teardown could be performed here,
            but is currently included in the setup_isolated fixture.
    """
    logger.info("Starting logged_in_browser fixture")
    login_pages = []
    for driver, wait in setup_isolated:
        logger.info("=" * 80)
        logger.info(f"Logging in on {driver.name}")
        logger.info("=" * 80)
        driver.get(LOGIN_URL)
        login_page = LoginPage(driver)
        username = request.config.getoption("--username", default=ADMIN_USER)
        password = request.config.getoption("--password", default=ADMIN_PASS)
        login_page.login(username, password)
        login_pages.append(login_page)
    logger.debug(f"logged_in_browser fixture: yielding {len(login_pages)} logged-in page(s)")
    yield login_pages
    logger.debug("logged_in_browser fixture: finished")

def logout(driver, wait):
    """
    Attempt to log out of the website and verify logout success
    """
    logger.debug("Attemping to log out of website")
    locator.set_driver(driver)
    try:
        # Check for the logout button before attempting to log out
        if locator.is_element_present(LOGOUT_BUTTON):
            logout_button = locator.get_element(LOGOUT_BUTTON)
            logout_button.click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON)))
            logger.debug("Successfully logged out, login button is present")
        else:
            logger.warning("Logout button not found. User might not be logged in.")
    except TimeoutException:
        logger.error("Timeout while waiting for login button to appear after logout.")
    except Exception as e:
        logger.error(f"Unexpected error during logout: {str(e)}")
    
def close_browser(driver):
    """
    Attempt to fully close the browser and end the WebDriver session
    """
    try:
        driver.quit()
        logger.debug("WebDriver session ended successfully")
    except WebDriverException as e:
        logger.error(f"Error while quitting WebDriver: {str(e)}")

def perform_teardown(driver, wait):
    """
    Performs the teardown of a WebDriver instance after a test case is complete.
    
    This function attempts to log out of the website, verify the logout was successful, 
    and then close the browser. It handles various exceptions that might occur during this
    process and logs appropriate messages

    Args:
        driver (WebDriver): The WebDriver instance to be torn down.
        wait (_type_): The WebDriverWait instance associated with the driver.
    """
    try:
        logout(driver, wait)
    except Exception as e:
        logger.error(f"Error while logout process: {str(e)}")
    finally:
        close_browser(driver)

# Define pytest configuration and reporting

def pytest_configure(config):
    """
    Configure pytest reporting structure.
    
    This function sets up the HTML report configuration for pytest. It performs the following actions:
        1. Determines the test suite name.
        2. Generates a timestamp for the report.
        3. Constructs a unqiue report name.
        4. Creates a 'reports' directory if one does not exist.
        5. Sets the HTML report path

    Args:
        config (pytest.Config): The pytest configuration object.
    
    Note:
        - If a directory named 'pytestpackage' exists in the root directory, it is used as the suite name.
        - Otherwise, the name of the root directory is used as the suite name.
        - The report name format is: "{suitname}_{timestamp}_report.html".
        - The function only modifies the htmlpath if it is already set in the pytest configuration.
    """
    # Get the test suite name
    suite_name = "pytestpackage"
    
    if not os.path.isdir(os.path.join(config.rootdir, suite_name)):
        suite_name = os.path.basename(config.rootdir)
        
    # Get current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Contruct the report name
    report_name = f"{suite_name}_{timestamp}_report.html"
    
    reports_dir = os.path.join(config.rootdir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    report_path = os.path.join(reports_dir, report_name)
    
    if config.option.htmlpath:
        config.option.htmlpath = report_path

def pytest_html_report_title(report):
    """
    Customize the title of the pytest HTML report.

    This function is a pytest hook that sets a custom title for the HTML report,
    including the current date and time.

    Args:
        report (pytest.HTMLReport): The HTML report object.

    Note:
        The title is set using the `title` attribute of the `report` object.
    """
    current_time = datetime.now()
    datestamp = current_time.strftime("%A - %B %Y")
    timestamp = current_time.strftime("%H:%M:%S")
    report.title = f"Testing WildXR Website on - {datestamp} @ {timestamp}"
    
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook for customizing test reports.

    This function captures logs for each test and adds them to the HTML report.
    It only operates during the 'call' phase of testing (the actual test execution).

    Args:
        item (pytest.Item): The test item object, representing a single test.
        call (pytest.CallInfo): Object containing information about the test function call.

    Yields:
        Generator: Yields control back to pytest to generate the report.

    Note:
        - This function is a hookwrapper, allowing it to modify pytest's report generation behavior.
        - Logs are captured using a custom 'get_logs_for_test' function.
        - Logs are added to the report's 'extra' section, which appears in the HTML report.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == call:
        # Captures logs for the test
        logs = get_logs_for_test(item.name)
        
        # Adds logs to the report
        extra = getattr(report, "extra", [])
        extra.append(pytest.html.extras.text(logs, name="Log"))
        report.extra = extra
        
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    """
    Pytest hook that runs before the setup of each test.

    This function initializes the log capture for a test before it runs.
    It's set to run before other plugins and wrap around the actual setup process.

    Args:
        item (pytest.Item): The test item object, representing a single test.

    Yields:
        None: Control is yielded back to pytest to perform the actual test setup.

    Note:
        - This hook uses 'tryfirst=True' to attempt to run before other plugins.
        - It's a hookwrapper, allowing it to wrap around the actual setup process.
        - The log capture is started using the test item's name.
        - After yielding, the actual test setup occurs, but this hook doesn't do anything post-setup.
    """
    # Clear the log capture for this test
    start_test_capture(item.name)
    yield
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_teardown(item):
    """
    Pytest hook that runs after the teardown of each test.

    This function finalizes the log capture for a test after it has run.
    It's set to run before other plugins and wrap around the actual teardown process.

    Args:
        item (pytest.Item): The test item object, representing a single test.

    Yields:
        None: Control is yielded back to pytest to perform the actual test teardown.

    Note:
        - This hook uses 'tryfirst=True' to attempt to run before other plugins.
        - It's a hookwrapper, allowing it to wrap around the actual teardown process.
        - The log capture is ended using the test item's name.
        - After calling end_test_capture, it yields control for the actual teardown, 
          but doesn't perform any actions post-teardown.
    """
    end_test_capture(item.name)
    yield
    
# TODO eventually used in tests to allow either isolated or continuous testing
# @pytest.fixture(scope="function")
# def setup(request):
#     """_summary_

#     Args:
#         request (_type_): _description_

#     Raises:
#         ValueError: _description_

#     Yields:
#         _type_: _description_
#     """
#     setup_type = request.config.getoption("--setup_type")
#     if setup_type == "isolated":
#         yield from setup_isolated(request)
#     elif setup_type == "continuous":
#         yield from setup_continuous(request)
#     else:
#         raise ValueError(f"Invalid setup type: {setup_type}. Should be either isolated or continuous.")
    
# TODO eventually to be used to allow multiple tests on one browser instance.
# @pytest.fixture(scope="class")
# def setup_continuous(request):
#     """_summary_

#     Args:
#         request (_type_): _description_

#     Yields:
#         _type_: _description_
#     """
#     browser = request.config.getoption("--browser")
#     headless = request.config.getoption("--headless")
#     private = request.config.getoption("--private")
    
#     drivers = []
#     for browser_name in (browser if isinstance(browser,list) else [browser]):
#         driver, wait = perform_setup(browser_name, headless, private)
#         drivers.append((driver,wait))
    
#     logger.info("Setting up a continuous test environment.")
    
#     driver, wait = drivers[0] if len(drivers) == 1 else drivers
#     request.cls.driver = driver
#     request.cls.wait = wait
#     yield driver, wait