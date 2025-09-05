"""
Logger per l'API Flask
"""

import logging
import os
from datetime import datetime

def setup_logger(name: str = 'wallet_fingerprinting_api') -> logging.Logger:
    """Setup del logger per l'API"""
    
    # Crea logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evita duplicazione di handler
    if logger.handlers:
        return logger
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (opzionale)
    log_file = os.environ.get('LOG_FILE', 'api.log')
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_request(logger: logging.Logger, method: str, endpoint: str, ip: str):
    """Log di una richiesta API"""
    logger.info(f"Request: {method} {endpoint} from {ip}")

def log_response(logger: logging.Logger, status_code: int, response_time: float):
    """Log di una risposta API"""
    logger.info(f"Response: {status_code} in {response_time:.3f}s")

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """Log di un errore"""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)
