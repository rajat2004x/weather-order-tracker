import logging
import os


def setup_logger():
    """
    Configure application logging.
    """

    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("weather_tracker")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(
            "logs/weather_tracker.log",
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger