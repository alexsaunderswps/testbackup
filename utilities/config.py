#config.py
import os
import logging
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
FILE_UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# Constant Element Paths
LOGOUT_BUTTON = "//section//button[text()='LOG OUT']"
LOGIN_BUTTON = "//section//button[text()='LOG IN']"

# Timeouts
DEFAULT_TIMEOUT = 10
EXTENDED_TIMEOUT = 30

# Log Levels
LOG_LEVEL_FILE = logging.DEBUG
LOG_LEVEL_CONSOLE = logging.INFO
LOG_LEVEL_OVERALL = min(LOG_LEVEL_FILE, LOG_LEVEL_CONSOLE)

# Other constants
MAX_RETRIES = 3