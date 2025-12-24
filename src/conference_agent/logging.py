"""
Logging configuration for the conference agent.

This module provides a centralized logging configuration with colored output
and structured logging capabilities.
"""

import logging
import sys

import colorlog


def setup_logger(name: str = "conference_agent", level: str = "INFO") -> logging.Logger:
    """
    Set up and configure a logger with colored console output.
    
    Args:
        name: Logger name (default: "conference_agent")
        level: Logging level (default: "INFO")
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if logger already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create console handler with colored formatter
    console_handler = colorlog.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Define color scheme
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Create default logger instance
logger = setup_logger()

