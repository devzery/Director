import logging


def setup_logger():
    """Setup and configure the root logger."""
    log_level = logging.INFO # Or get from environment variable, config file, etc.
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers (optional, but good practice to avoid duplicates during reloads)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # --- Console Handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)