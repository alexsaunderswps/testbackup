#utils.py
import os
import logging
from datetime import datetime
from threading import Lock
from .config import LOG_DIR
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
    """_summary_

    Args:
        logging (_type_): _description_
    """
    def __init__(self, name: str, level=logging.NOTSET) -> None:
        """_summary_

        Args:
            name (str): _description_
            level (_type_, optional): _description_. Defaults to logging.NOTSET.
        """
        super().__init__(name, level)
        self.html_logger = HTMLReportLogger()
        
    def log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        """_summary_

        Args:
            level (_type_): _description_
            msg (_type_): _description_
            args (_type_): _description_
            exc_info (_type_, optional): _description_. Defaults to None.
            extra (_type_, optional): _description_. Defaults to None.
            stack_info (bool, optional): _description_. Defaults to False.
        """
        super().log(level, msg, args, exc_info, extra, stack_info)
        self.html_logger.log(logging.getLevelName(level), msg % args if args else msg)

# Set Up logging
def setup_logging():
    """_summary_

    Returns:
        _type_: _description_
    """
    # Ensure the directory exists
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Create a timestamp for the log file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"log_{timestamp}.log")
    
    # Setup logging
    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
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
    
    logger.info(f"Logging initialized. Log file: {log_file}")
    
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