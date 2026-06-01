import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(settings.logging.file_name)
console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[file_handler, console_handler]
)
