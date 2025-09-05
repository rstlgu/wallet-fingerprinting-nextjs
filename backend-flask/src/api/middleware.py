"""
Middleware per gestione errori e logging
"""

from flask import request, jsonify, current_app
from datetime import datetime
import traceback
import sys
import os

# Aggiungi path per importare moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.responses import create_error_response
from utils.logger import setup_logger, log_request, log_response

logger = setup_logger()

def error_handler(error):
    """Handler globale per errori"""
    
    # Log dell'errore
    logger.error(f"Unhandled error: {str(error)}", exc_info=True)
    
    # Determina il tipo di errore
    if hasattr(error, 'code'):
        status_code = error.code
    elif hasattr(error, 'status_code'):
        status_code = error.status_code
    else:
        status_code = 500
    
    # Messaggio di errore
    if status_code == 500:
        message = "Errore interno del server"
        error_type = "InternalServerError"
    elif status_code == 404:
        message = "Endpoint non trovato"
        error_type = "NotFound"
    elif status_code == 400:
        message = "Richiesta non valida"
        error_type = "BadRequest"
    else:
        message = str(error)
        error_type = "UnknownError"
    
    return jsonify(create_error_response(
        error=error_type,
        message=message,
        code=status_code
    )), status_code

def validate_txid(txid: str) -> bool:
    """Valida un transaction ID Bitcoin"""
    if not txid:
        return False
    
    # Bitcoin txid è esadecimale di 64 caratteri
    if len(txid) != 64:
        return False
    
    try:
        int(txid, 16)
        return True
    except ValueError:
        return False

def validate_address(address: str) -> bool:
    """Valida un indirizzo Bitcoin"""
    if not address:
        return False
    
    # Controlli base per indirizzi Bitcoin
    if len(address) < 26 or len(address) > 62:
        return False
    
    # Deve iniziare con 1, 3, o bc1
    if not (address.startswith('1') or address.startswith('3') or address.startswith('bc1')):
        return False
    
    return True

def validate_block_hash(block_hash: str) -> bool:
    """Valida un block hash Bitcoin"""
    if not block_hash:
        return False
    
    # Bitcoin block hash è esadecimale di 64 caratteri
    if len(block_hash) != 64:
        return False
    
    try:
        int(block_hash, 16)
        return True
    except ValueError:
        return False

def log_api_request():
    """Log di una richiesta API"""
    log_request(
        logger=logger,
        method=request.method,
        endpoint=request.endpoint or request.path,
        ip=request.remote_addr
    )

def log_api_response(status_code: int, response_time: float):
    """Log di una risposta API"""
    log_response(
        logger=logger,
        status_code=status_code,
        response_time=response_time
    )

def validate_api_key():
    """Valida l'API KEY dalla richiesta"""
    # Endpoint che non richiedono autenticazione
    public_endpoints = ['/health', '/', '/api/docs', '/api/redoc', '/api/swagger-ui', '/api/status']
    
    # Se è un endpoint pubblico, non validare l'API KEY
    if request.path in public_endpoints:
        return True
    
    # Controlla se l'API KEY è presente
    api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization')
    
    # Rimuovi "Bearer " se presente
    if api_key and api_key.startswith('Bearer '):
        api_key = api_key[7:]
    
    if not api_key:
        return False
    
    # Confronta con l'API KEY configurata
    expected_api_key = current_app.config.get('API_KEY')
    if not expected_api_key:
        logger.error("API_KEY non configurata nel server")
        return False
    
    return api_key == expected_api_key

def require_api_key():
    """Decorator per richiedere API KEY"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if not validate_api_key():
                return jsonify(create_error_response(
                    error="Unauthorized",
                    message="API KEY richiesta. Invia l'API KEY nell'header X-API-Key o Authorization",
                    code=401
                )), 401
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator
