import logging
import sys
from pathlib import Path
from datetime import datetime
from from_root import from_root
import os

def setup_logging(log_dir: Path) -> None:
    """
    Set up a global logging configuration for the entire pipeline stage.

    Args:
        log_dir (Path): Directory path to save the log files (e.g., Path("logs")).
    """
    # Resolve absolute path from project root
    log_path = Path(from_root()) / log_dir
    log_path.mkdir(parents=True, exist_ok=True)  # Correct mkdir usage

    # Create a unique log filename with timestamp
    log_file = log_path / f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

    # Clear existing handlers to prevent duplicate logs
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Set up logging configuration
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        handlers=[
            logging.FileHandler(log_file) # log to a file
            # logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info(f"Logging initialized. Log file: {log_file}")
