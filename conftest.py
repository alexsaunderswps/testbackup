# Defines functions for use across test files in pytest

import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from utilities.config import LOGIN_BUTTON, LOGOUT_BUTTON
from utilities.utils import logger, start_test_capture, end_test_capture, get_logs_for_tests
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT
from utilities import ElementLocator

# Initialize ElementLocator
locator = ElementLocator()


# Define pytest addoption for Command Line running of Pytest with options
def pytest_addoption(parser):
    """_summary_

    Args:
        parser (_type_): _description_
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

@pytest.fixture(params=["chrome", "edge", "firefox"])
def all_browsers(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return request.param

@pytest.fixture(scope="class")
def browser(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    browser_option = request.config.getoption("--browser")
    if browser_option == "all":
        return ["chrome", "edge", "firefox"]
    else:
        return browser_option

def perform_setup(browser_name, headless, private):
    """_summary_

    Args:
        browser_name (_type_): _description_
        headless (_type_): _description_
        private (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    logger.info(f"Setting up {browser_name} browser in setup")
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.add_argument("--private")
        driver = webdriver.Edge(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.add_argument("--inprivate")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser request: {browser_name}")
    
    driver.maximize_window()
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    
    # Clear cookies and cache just in case
    driver.delete_all_cookies()
    driver.execute_script("localStorage.clear();")
    driver.execute_script("sessionStorage.clear();")
    
    start_test_capture(driver.session_id)
    
    return driver, wait

@pytest.fixture(scope="function")
def setup(request):
    """_summary_

    Args:
        request (_type_): _description_

    Raises:
        ValueError: _description_

    Yields:
        _type_: _description_
    """
    setup_type = request.config.getoption("--setup_type")
    if setup_type == "isolated":
        yield from setup_isolated(request)
    elif setup_type == "continuous":
        yield from setup_continuous(request)
    else:
        raise ValueError(f"Invalid setup type: {setup_type}. Should be either isolated or continuous.")
    
@pytest.fixture(scope="function")
def setup_isolated(request):
    """_summary_

    Args:
        request (_type_): _description_

    Yields:
        _type_: _description_
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    private = request.config.getoption("--private")
    
    drivers = []
    for browser_name in (browser if isinstance(browser,list) else [browser]):
        driver, wait = perform_setup(browser_name, headless, private)
        drivers.append((driver,wait))
    
    logger.info("Setting up an isolated test.")
    if len(drivers) == 1:
        driver, wait = driver[0]
    else:
        driver, wait = drivers
        request.node.driver = driver # Attach driver to the test node for teardown
        
    yield driver, wait
    
    logger.info(f"Performing teardown of isolated test")
    perform_teardown(driver)
    
@pytest.fixture(scope="class")
def setup_continuous(request):
    """_summary_

    Args:
        request (_type_): _description_

    Yields:
        _type_: _description_
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    private = request.config.getoption("--private")
    
    drivers = []
    for browser_name in (browser if isinstance(browser,list) else [browser]):
        driver, wait = perform_setup(browser_name, headless, private)
        drivers.append((driver,wait))
    
    logger.info("Setting up a continuous test environment.")
    
    driver, wait = drivers[0] if len(drivers) == 1 else drivers
    request.cls.driver = driver
    request.cls.wait = wait
    yield driver, wait
    
def perform_teardown(driver, wait):
    """_summary_

    Args:
        driver (_type_): _description_
        wait (_type_): _description_
    """
    try:
        logger.info(f"Attempting teardown with perform_teardown.")
        try:
            logger.info(f"Attempting to log out of website")
            logout_button = locator.get_element(LOGOUT_BUTTON)
            logout_button.click()
            try:
                login_present = wait.until(EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON)))
                logger.info(f"Successfully logged out, loing button is present.")
            except TimeoutException:
                logger.error("Timeout while waiting for login button to appear after logout.")
            except Exception as e:
                logger.error(f"Unexpected error while waiting for login button to appear: {str(e)}")
        except Exception as e:
                logger.error(f"Error during logout process: {str(e)}")
        finally:
            try:
                driver.quit()
                logger.info("Driver quit successfully.")
            except WebDriverException as e:
                logger.error(f"Error while quitting driver: {str(e)}")
    except Exception as e:
        logger.error(f"Unexcepted error while executing perform_teardown: {str(e)}")
        
def pytest_configure(config):
    """_summary_

    Args:
        config (_type_): _description_
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
    """_summary_

    Args:
        report (_type_): _description_
    """
    datestamp = datetime.now().strftime("%A - %m%Y")
    timestamp = datetime.now().strftime("%H:%M:%S")
    report_title = f"Tesing WildXR Website on - {datestamp} @ {timestamp}"
    
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """_summary_

    Args:
        item (_type_): _description_
        call (_type_): _description_
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == call:
        # Captures logs for the test
        logs = get_logs_for_tests(item.name)
        
        # Adds logs to the report
        extra = getattr(report, "extra", [])
        extra.append(pytest.html.extras.text(logs, name="Log"))
        report.extra = extra
        
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    """_summary_

    Args:
        item (_type_): _description_
    """
    # Clear the log capture for this test
    start_test_capture(item.name)
    yield
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_teardown(item):
    """_summary_

    Args:
        item (_type_): _description_
    """
    end_test_capture(item.name)
    yield