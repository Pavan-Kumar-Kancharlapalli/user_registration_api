import logging
import os

# Log directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create loggers
logger = logging.getLogger("user_logger")
logger.setLevel(logging.DEBUG)  # capture all levels

# Format for all logs
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Success log handler (INFO, DEBUG)
success_handler = logging.FileHandler(os.path.join(LOG_DIR, "success.log"))
success_handler.setLevel(logging.INFO)
success_handler.setFormatter(formatter)

# Error log handler (ERROR and above)
error_handler = logging.FileHandler(os.path.join(LOG_DIR, "error.log"))
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# Add handlers only once
if not logger.handlers:
    logger.addHandler(success_handler)
    logger.addHandler(error_handler)
