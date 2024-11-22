import os
import logging
from logging.handlers import RotatingFileHandler

# Создаём папку для логов, если она не существует
os.makedirs("logs", exist_ok=True)

# Настройка основного логгера для обычных логов
main_logger = logging.getLogger("main_logger")
main_logger.setLevel(logging.INFO)

# Настройка обработчика для обычных логов
main_handler = RotatingFileHandler(
    "logs/main.log", maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
main_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
main_logger.addHandler(main_handler)
