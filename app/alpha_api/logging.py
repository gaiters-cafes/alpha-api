import logging
import os
from .config import Settings

# Load settings
settings = Settings()
log_level = settings.log_level.upper()
numeric_level = getattr(logging, log_level, logging.INFO)

# Configure logging
logging.basicConfig(
    level=numeric_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("app")