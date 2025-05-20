#utils.py
import os
import logging
from datetime import datetime
from threading import Lock
from .config import LOG_DIR, LOG_LEVEL_FILE, LOG_LEVEL_CONSOLE, LOG_LEVEL_OVERALL
from colorlog import ColoredFormatter

class HTMLReportLogger:
    """
    A thread-safe logger for capturing test-specific logs for HTML reporting.

    This class allows for the capture, retrieval, and management of logs
    on a per-test basis, making it suitable for use in concurrent testing
    environments where logs need to be associated with specific tests.
    """
    
    def __init__(self):
        """
        Initialize the HTMLReportLogger.

        Sets up the necessary data structures for log management and
        ensures thread-safety through the use of a lock:
        - test_logs: A dictionary to store logs for each test.
        - current_test: A variable to track the currently running test.
        - lock: A threading Lock to ensure thread-safety in concurrent environments.
        """
        self.test_logs = {}
        self.current_test = None
        self.lock = Lock()
        self.context = None
        
    def set_context(self, context):
        self.context = context
        
    def start_test_capture(self, test_name):
        """
        Start capturing logs for a specific test.

        This method should be called at the beginning of each test. It sets up
        the logging environment for the specified test.

        Args:
            test_name (str): The name of the test for which to start capturing logs.
        """
        with self.lock:
            self.current_test = test_name
            self.test_logs[test_name] = []
    
    def end_test_capture(self, test_name):
        """
        End the log capture for a specific test.

        This method should be called at the end of each test. It resets the
        current test to None, indicating that no test is currently running.

        Args:
            test_name (str): The name of the test for which to end capturing logs.
        """
        with self.lock:
            self.current_test = None
            
    def get_logs_for_test(self, test_name):
        """
        Retrieve the logs for a specific test.

        This method returns all captured logs for the specified test as a single string,
        with each log entry separated by a newline.

        Args:
            test_name (str): The name of the test for which to retrieve logs.

        Returns:
            str: A string containing all log entries for the specified test,
                or an empty string if no logs are found.
        """
        with self.lock:
            return "\n".join(self.test_logs.get(test_name,[]))
    
    def log(self, level, message):
        """
        Add a log entry for the current test.

        This method adds a log entry with the specified level and message to the
        current test's log. If no test is currently set, the log entry is ignored.

        Args:
            level (str): The log level (e.g., 'INFO', 'WARNING', 'ERROR').
            message (str): The log message to be recorded.
        """
        with self.lock:
            if self.current_test:
                self.test_logs[self.current_test].append(f"{level}: {message}")
                
class CustomLogger(logging.Logger):
    """
    A custom logger class that extends the functionality of the standard logging.Logger.

    This logger adds HTML report logging capabilities on top of the standard logging
    functions. It uses an HTMLReportLogger instance to capture logs for HTML reports
    while still maintaining all the functionality of the standard Logger.

    Inherits from:
        logging.Logger: The standard Python logging class.
    """
    def __init__(self, name: str, level: int =logging.NOTSET) -> None:
        """
        Initialize the CustomLogger.

        This constructor sets up both the standard logging capabilities and
        the HTML report logging functionality.

        Args:
            name (str): The name of the logger.
            level (int, optional): The logging level. Defaults to logging.NOTSET.
                This determines the minimum severity of messages that the logger
                will handle.Standard levels are:
            - CRITICAL = 50
            - ERROR = 40
            - WARNING = 30
            - INFO = 20
            - DEBUG = 10
            - NOTSET = 0

        Returns:
            None
        """
        super().__init__(name, level)
        self.html_logger = HTMLReportLogger()
        
    def log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        """
        Log a message with the specified level and additional context.

        This method extends the standard logging functionality by also logging
        the message to the HTML report logger.

        Args:
            level (int): The logging level (e.g., logging.INFO, logging.ERROR).
            msg (str): The message format string.
            args (tuple): Arguments to merge into msg.
            exc_info (tuple, optional): Exception information to be added to the log.
                Can be an exception tuple or a boolean. Defaults to None.
            extra (dict, optional): A dictionary of additional attributes to add to the log record.
                Defaults to None.
            stack_info (bool, optional): If True, stack information is added to the log.
                Defaults to False.

        Note:
            This method first calls the standard logging method and then logs
            the message to the HTML report logger.
        """
        super().log(level, msg, args, exc_info, extra, stack_info)
        level_name = logging.getLevelName(level)
        formatted_msg = msg % args if args else msg
        self.html_logger.log(level_name, formatted_msg)

# Set Up logging
def setup_logging():
    """
    Set up and configure the logging system for the application.

    This function performs the following tasks:
    1. Ensures the log directory exists.
    2. Creates a unique log file with a timestamp.
    3. Configures a CustomLogger as the logger class.
    4. Sets up both file and console logging handlers.
    5. Configures formatters for log messages, including colored output for console.
    6. Sets the logging level to DEBUG for comprehensive logging.

    The log messages will have the following format:
    "timestamp - logger_name - log_level - message"

    Console output will be color-coded based on the log level for better readability.

    Returns:
        logging.Logger: A configured logger instance ready for use in the application.

    Note:
        This function uses a global LOG_DIR variable to determine where log files should be stored.
        Ensure this variable is properly set before calling this function.
    """
    # Ensure the directory exists
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Create a timestamp for the log file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"log_{timestamp}.log")
    
    # Setup logging
    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger(__name__)
    print(f"Effective Log Level: {logging.getLevelName(logger.getEffectiveLevel())}")
    logger.setLevel(LOG_LEVEL_OVERALL)
    
    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(LOG_LEVEL_FILE)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL_CONSOLE)
    
    #Formatters
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    color_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    
    # Apply formatters to handlers
    console_handler.setFormatter(color_formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to Logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized. Log file: {log_file}, Log Levels: Console {logging.getLevelName(LOG_LEVEL_CONSOLE)}, File {logging.getLevelName(LOG_LEVEL_FILE)}")
    
    return logger

# Create Global logger instance
logger = setup_logging()

def start_test_capture(test_name):
    """_summary_

    Args:
        test_name (_type_): _description_
    """
    logger.html_logger.start_test_capture(test_name)

def end_test_capture(test_name):
    """_summary_

    Args:
        test_name (_type_): _description_
    """
    logger.html_logger.end_test_capture(test_name)
    
def get_logs_for_test(test_name):
    """_summary_

    Args:
        test_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    return logger.html_logger.get_logs_for_test(test_name)

def get_browser_name(page):
    """Safely get browser name from a Playwright page object."""
    try:
        return page.context.browser.browser_type.name
    except AttributeError:
        return "unknown browser"