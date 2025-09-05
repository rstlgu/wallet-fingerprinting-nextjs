"""
Route API per Wallet Fingerprinting
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import time
import sys
import os

# Aggiungi path per importare moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services import wallet_service
from api.middleware import (
    validate_txid, validate_address, validate_block_hash,
    log_api_request, log_api_response, validate_api_key
)
from models.responses import create_success_response, create_error_response
from utils.logger import setup_logger

logger = setup_logger()

# Crea blueprint
api_bp = Blueprint('api', __name__)

@api_bp.before_request
def before_request():
    """Middleware per logging richieste e validazione API KEY"""
    log_api_request()
    
    # Valida API KEY per endpoint protetti
    if not validate_api_key():
        return jsonify(create_error_response(
            error="Unauthorized",
            message="API KEY richiesta. Invia l'API KEY nell'header X-API-Key o Authorization",
            code=401
        )), 401

@api_bp.after_request
def after_request(response):
    """Middleware per logging risposte"""
    # Calcola tempo di risposta
    if hasattr(request, 'start_time'):
        response_time = time.time() - request.start_time
        log_api_response(response.status_code, response_time)
    return response

@api_bp.route('/analyze/tx', methods=['POST'])
def analyze_transaction():
    """Analizza una singola transazione"""
    try:
        # Valida input
        data = request.get_json()
        if not data or 'txid' not in data:
            return jsonify(create_error_response(
                error="MissingParameter",
                message="txid è richiesto",
                code=400
            )), 400
        
        txid = data['txid'].strip()
        if not validate_txid(txid):
            return jsonify(create_error_response(
                error="InvalidTxid",
                message="txid non valido",
                code=400
            )), 400
        
        # Analizza transazione
        request.start_time = time.time()
        analysis = wallet_service.analyze_transaction(txid)
        
        # Prepara risposta
        response_data = {
            'transaction': {
                'txid': analysis.transaction.txid,
                'version': analysis.transaction.version,
                'locktime': analysis.transaction.locktime,
                'inputs_count': analysis.transaction.inputs_count,
                'outputs_count': analysis.transaction.outputs_count,
                'input_types': analysis.transaction.input_types,
                'output_types': analysis.transaction.output_types
            },
            'detection': {
                'wallet': analysis.detection.wallet,
                'confidence': analysis.detection.confidence,
                'reasoning': analysis.detection.reasoning,
                'is_clear': analysis.detection.is_clear
            },
            'analysis_time': analysis.analysis_time,
            'block_explorer': f'https://mempool.space/tx/{txid}'
        }
        
        return jsonify(create_success_response(
            data=response_data,
            message="Transazione analizzata con successo"
        ))
        
    except Exception as e:
        logger.error(f"Error in analyze_transaction: {str(e)}")
        return jsonify(create_error_response(
            error="AnalysisError",
            message=f"Errore durante l'analisi: {str(e)}",
            code=500
        )), 500

@api_bp.route('/analyze/address', methods=['POST'])
def analyze_address():
    """Analizza un indirizzo Bitcoin"""
    try:
        # Valida input
        data = request.get_json()
        if not data or 'address' not in data:
            return jsonify(create_error_response(
                error="MissingParameter",
                message="address è richiesto",
                code=400
            )), 400
        
        address = data['address'].strip()
        if not validate_address(address):
            return jsonify(create_error_response(
                error="InvalidAddress",
                message="Indirizzo Bitcoin non valido",
                code=400
            )), 400
        
        # Limite transazioni (opzionale)
        limit = data.get('limit', 20)
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            limit = 20
        
        # Analizza indirizzo
        request.start_time = time.time()
        analysis = wallet_service.analyze_address(address, limit)
        
        # Prepara risposta
        response_data = {
            'address': analysis.address,
            'total_transactions': analysis.total_transactions,
            'analyzed_transactions': limit,
            'wallet_distribution': analysis.wallet_distribution,
            'wallet_percentages': analysis.wallet_percentages,
            'timeline': analysis.timeline,
            'main_wallet': analysis.main_wallet,
            'pattern_type': analysis.pattern_type,
            'block_explorer': f'https://mempool.space/address/{address}'
        }
        
        return jsonify(create_success_response(
            data=response_data,
            message="Indirizzo analizzato con successo"
        ))
        
    except Exception as e:
        logger.error(f"Error in analyze_address: {str(e)}")
        return jsonify(create_error_response(
            error="AnalysisError",
            message=f"Errore durante l'analisi: {str(e)}",
            code=500
        )), 500

@api_bp.route('/analyze/block', methods=['POST'])
def analyze_block():
    """Analizza un blocco Bitcoin"""
    try:
        # Valida input
        data = request.get_json() or {}
        block_hash = data.get('block_hash')
        num_txs = data.get('num_txs', 50)
        
        if block_hash and not validate_block_hash(block_hash):
            return jsonify(create_error_response(
                error="InvalidBlockHash",
                message="Block hash non valido",
                code=400
            )), 400
        
        if not isinstance(num_txs, int) or num_txs < 1 or num_txs > 200:
            num_txs = 50
        
        # Analizza blocco
        request.start_time = time.time()
        analysis = wallet_service.analyze_block(block_hash, num_txs)
        
        # Prepara risposta
        response_data = {
            'block_hash': analysis.block_hash,
            'total_transactions': analysis.total_transactions,
            'analyzed_transactions': analysis.analyzed_transactions,
            'wallet_distribution': analysis.wallet_distribution,
            'wallet_percentages': analysis.wallet_percentages,
            'analysis_time': analysis.analysis_time,
            'block_explorer': f'https://mempool.space/block/{analysis.block_hash}' if analysis.block_hash != 'latest' else None
        }
        
        return jsonify(create_success_response(
            data=response_data,
            message="Blocco analizzato con successo"
        ))
        
    except Exception as e:
        logger.error(f"Error in analyze_block: {str(e)}")
        return jsonify(create_error_response(
            error="AnalysisError",
            message=f"Errore durante l'analisi: {str(e)}",
            code=500
        )), 500

@api_bp.route('/docs', methods=['GET'])
def api_docs():
    """Documentazione API"""
    docs = {
        'title': 'Wallet Fingerprinting API',
        'version': '1.0.0',
        'description': 'API per analisi e rilevamento wallet Bitcoin',
        'authentication': {
            'type': 'API Key',
            'header': 'X-API-Key',
            'description': 'Invia la tua API KEY nell\'header X-API-Key o Authorization'
        },
        'endpoints': {
            'POST /api/analyze/tx': {
                'description': 'Analizza una singola transazione',
                'authentication': 'Required',
                'parameters': {
                    'txid': 'string (required) - Transaction ID Bitcoin'
                },
                'headers': {
                    'X-API-Key': 'string (required) - La tua API KEY'
                },
                'example': {
                    'txid': '7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166'
                }
            },
            'POST /api/analyze/address': {
                'description': 'Analizza un indirizzo Bitcoin',
                'authentication': 'Required',
                'parameters': {
                    'address': 'string (required) - Indirizzo Bitcoin',
                    'limit': 'integer (optional) - Numero max transazioni da analizzare (default: 20)'
                },
                'headers': {
                    'X-API-Key': 'string (required) - La tua API KEY'
                },
                'example': {
                    'address': 'bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl',
                    'limit': 20
                }
            },
            'POST /api/analyze/block': {
                'description': 'Analizza un blocco Bitcoin',
                'authentication': 'Required',
                'parameters': {
                    'block_hash': 'string (optional) - Block hash (default: ultimo blocco)',
                    'num_txs': 'integer (optional) - Numero transazioni da analizzare (default: 50)'
                },
                'headers': {
                    'X-API-Key': 'string (required) - La tua API KEY'
                },
                'example': {
                    'block_hash': '00000000000000000004bcc50688d02a74d778201a47cc704a877d1442a58431',
                    'num_txs': 50
                }
            }
        },
        'response_format': {
            'success': 'boolean',
            'message': 'string',
            'data': 'object',
            'timestamp': 'string (ISO 8601)'
        },
        'error_format': {
            'success': 'boolean (false)',
            'error': 'string',
            'message': 'string',
            'code': 'integer',
            'timestamp': 'string (ISO 8601)'
        }
    }
    
    return jsonify(create_success_response(
        data=docs,
        message="Documentazione API"
    ))

@api_bp.route('/status', methods=['GET'])
def api_status():
    """Stato dell'API"""
    return jsonify(create_success_response(
        data={
            'status': 'running',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'endpoints_available': [
                '/api/analyze/tx',
                '/api/analyze/address', 
                '/api/analyze/block',
                '/api/docs',
                '/api/status'
            ]
        },
        message="API in esecuzione"
    ))
