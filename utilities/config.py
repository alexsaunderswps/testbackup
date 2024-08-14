#config.py

import os
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
FILE_UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# URLs
QA_BASE_URL = "https://wildxr-cm-qa.azurewebsites.net/"
QA_LOGIN_URL = f"{QA_BASE_URL}/login"

# Constant Element Paths
LOGOUT_BUTTON = "//section//button[text()='LOG OUT']"
LOGIN_BUTTON = "//section//button[text()='LOG IN']"

# Timeouts
DEFAULT_TIMEOUT = 10
EXTENED_TIMEOUT = 30

# Other constants
MAX_RETRIES = 3