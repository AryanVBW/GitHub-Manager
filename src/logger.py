"""
Logging configuration for GitHub Manager application.
Provides colored console logging with proper formatting.
"""
import logging
import sys
from typing import Optional
import colorlog
from src.config import Config


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure a logger with colored output.
    
    Args:
        name: Logger name (defaults to root logger)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or __name__)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Set log level from config
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler with colored output
    handler = colorlog.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # Create formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


# Create default logger
logger = setup_logger("github_manager")

