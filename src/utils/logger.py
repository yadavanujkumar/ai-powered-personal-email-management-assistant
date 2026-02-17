"""Logging configuration"""
import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Setup application logging"""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reduce verbosity of external libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("imaplib").setLevel(logging.WARNING)
