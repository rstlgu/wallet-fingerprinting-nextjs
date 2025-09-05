"""
Route API documentate per Wallet Fingerprinting con Flask-RESTX
"""

from flask import request
from flask_restx import Resource
from datetime import datetime
import time
import sys
import os

# Aggiungi path per importare moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.docs_config import (
    api, analyze_ns, address_ns, transaction_ns, block_ns, fingerprint_ns,
    success_model, error_model, transaction_model, address_model, 
    fingerprint_model, analyze_request_model, analyze_response_model,
    response_headers
)
from api.services import wallet_service
from api.middleware import (
    validate_txid, validate_address, validate_block_hash,
    log_api_request, log_api_response
)
from models.responses import create_success_response, create_error_response
from utils.logger import setup_logger

logger = setup_logger()

# Parser per richieste di analisi
analyze_parser = api.parser()
analyze_parser.add_argument('txid', type=str, help='Transaction ID Bitcoin', location='json')
analyze_parser.add_argument('address', type=str, help='Indirizzo Bitcoin', location='json')
analyze_parser.add_argument('block_hash', type=str, help='Block hash Bitcoin', location='json')
analyze_parser.add_argument('limit', type=int, help='Limite transazioni (1-100)', default=20, location='json')
analyze_parser.add_argument('depth', type=int, help='Profondità analisi (1-5)', default=3, location='json')
analyze_parser.add_argument('include_patterns', type=bool, help='Includere pattern analysis', default=True, location='json')
analyze_parser.add_argument('realtime_updates', type=bool, help='Aggiornamenti real-time', default=False, location='json')

@transaction_ns.route('/analyze')
class TransactionAnalysis(Resource):
    @api.doc('analyze_transaction')
    @api.expect(analyze_parser)
    @api.marshal_with(success_model, code=200, description='Analisi completata con successo')
    @api.marshal_with(error_model, code=400, description='Parametri non validi')
    @api.marshal_with(error_model, code=500, description='Errore interno del server')
    @api.response(200, 'Successo', success_model, headers=response_headers)
    def post(self):
        """
        Analizza una singola transazione Bitcoin
        
        Esegue un'analisi completa di una transazione Bitcoin per identificare:
        - Tipo di wallet utilizzato
        - Pattern comportamentali
        - Indicatori di privacy
        - Clustering di indirizzi
        
        **Esempio di richiesta:**
        ```json
        {
            "txid": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166",
            "depth": 3,
            "include_patterns": true
        }
        ```
        """
        try:
            # Valida input
            data = request.get_json() or {}
            txid = data.get('txid', '').strip()
            
            if not txid:
                return create_error_response(
                    error="MissingParameter",
                    message="txid è richiesto",
                    code=400
                ), 400
            
            if not validate_txid(txid):
                return create_error_response(
                    error="InvalidTxid", 
                    message="txid non valido",
                    code=400
                ), 400
            
            # Parametri opzionali
            depth = min(max(data.get('depth', 3), 1), 5)
            include_patterns = data.get('include_patterns', True)
            
            # Analizza transazione
            start_time = time.time()
            analysis = wallet_service.analyze_transaction(txid)
            analysis_time = time.time() - start_time
            
            # Prepara risposta
            response_data = {
                'analysis_id': f'tx_{txid[:16]}_{int(time.time())}',
                'target': txid,
                'analysis_type': 'transaction',
                'transaction': {
                    'txid': analysis.transaction.txid,
                    'version': analysis.transaction.version,
                    'locktime': analysis.transaction.locktime,
                    'inputs_count': analysis.transaction.inputs_count,
                    'outputs_count': analysis.transaction.outputs_count,
                    'input_types': analysis.transaction.input_types,
                    'output_types': analysis.transaction.output_types,
                    'size': getattr(analysis.transaction, 'size', None),
                    'fee': getattr(analysis.transaction, 'fee', None)
                },
                'fingerprint': {
                    'wallet': analysis.detection.wallet,
                    'confidence': analysis.detection.confidence,
                    'reasoning': analysis.detection.reasoning,
                    'is_clear': analysis.detection.is_clear,
                    'risk_level': 'low' if analysis.detection.confidence < 0.5 else 'medium' if analysis.detection.confidence < 0.8 else 'high'
                },
                'metadata': {
                    'analysis_time': analysis_time,
                    'depth': depth,
                    'include_patterns': include_patterns,
                    'block_explorer': f'https://mempool.space/tx/{txid}',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            return create_success_response(
                data=response_data,
                message="Transazione analizzata con successo"
            ), 200
            
        except Exception as e:
            logger.error(f"Error in analyze_transaction: {str(e)}")
            return create_error_response(
                error="AnalysisError",
                message=f"Errore durante l'analisi: {str(e)}",
                code=500
            ), 500

@address_ns.route('/analyze')
class AddressAnalysis(Resource):
    @api.doc('analyze_address')
    @api.expect(analyze_parser)
    @api.marshal_with(success_model, code=200, description='Analisi completata con successo')
    @api.marshal_with(error_model, code=400, description='Parametri non validi')
    @api.marshal_with(error_model, code=500, description='Errore interno del server')
    @api.response(200, 'Successo', success_model, headers=response_headers)
    def post(self):
        """
        Analizza un indirizzo Bitcoin
        
        Esegue un'analisi completa di un indirizzo Bitcoin per identificare:
        - Pattern di utilizzo del wallet
        - Distribuzione temporale delle transazioni
        - Clustering con altri indirizzi
        - Comportamenti tipici del wallet
        
        **Esempio di richiesta:**
        ```json
        {
            "address": "bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
            "limit": 50,
            "depth": 3
        }
        ```
        """
        try:
            # Valida input
            data = request.get_json() or {}
            address = data.get('address', '').strip()
            
            if not address:
                return create_error_response(
                    error="MissingParameter",
                    message="address è richiesto",
                    code=400
                ), 400
            
            if not validate_address(address):
                return create_error_response(
                    error="InvalidAddress",
                    message="Indirizzo Bitcoin non valido",
                    code=400
                ), 400
            
            # Parametri opzionali
            limit = min(max(data.get('limit', 20), 1), 100)
            depth = min(max(data.get('depth', 3), 1), 5)
            
            # Analizza indirizzo
            start_time = time.time()
            analysis = wallet_service.analyze_address(address, limit)
            analysis_time = time.time() - start_time
            
            # Prepara risposta
            response_data = {
                'analysis_id': f'addr_{address[:16]}_{int(time.time())}',
                'target': address,
                'analysis_type': 'address',
                'address_info': {
                    'address': analysis.address,
                    'total_transactions': analysis.total_transactions,
                    'analyzed_transactions': limit,
                    'address_type': 'P2WPKH' if address.startswith('bc1q') else 'P2SH' if address.startswith('3') else 'P2PKH'
                },
                'fingerprint': {
                    'wallet_distribution': analysis.wallet_distribution,
                    'wallet_percentages': analysis.wallet_percentages,
                    'main_wallet': analysis.main_wallet,
                    'pattern_type': analysis.pattern_type,
                    'confidence': max(analysis.wallet_percentages.values()) if analysis.wallet_percentages else 0,
                    'risk_level': 'low'
                },
                'timeline': analysis.timeline,
                'metadata': {
                    'analysis_time': analysis_time,
                    'limit': limit,
                    'depth': depth,
                    'block_explorer': f'https://mempool.space/address/{address}',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            return create_success_response(
                data=response_data,
                message="Indirizzo analizzato con successo"
            ), 200
            
        except Exception as e:
            logger.error(f"Error in analyze_address: {str(e)}")
            return create_error_response(
                error="AnalysisError",
                message=f"Errore durante l'analisi: {str(e)}",
                code=500
            ), 500

@block_ns.route('/analyze')
class BlockAnalysis(Resource):
    @api.doc('analyze_block')
    @api.expect(analyze_parser)
    @api.marshal_with(success_model, code=200, description='Analisi completata con successo')
    @api.marshal_with(error_model, code=400, description='Parametri non validi')
    @api.marshal_with(error_model, code=500, description='Errore interno del server')
    @api.response(200, 'Successo', success_model, headers=response_headers)
    def post(self):
        """
        Analizza un blocco Bitcoin
        
        Esegue un'analisi aggregata delle transazioni in un blocco per identificare:
        - Distribuzione dei wallet utilizzati
        - Pattern emergenti nel blocco
        - Statistiche di utilizzo dei wallet
        - Tendenze temporali
        
        **Esempio di richiesta:**
        ```json
        {
            "block_hash": "00000000000000000004bcc50688d02a74d778201a47cc704a877d1442a58431",
            "limit": 100
        }
        ```
        """
        try:
            # Valida input
            data = request.get_json() or {}
            block_hash = data.get('block_hash')
            limit = min(max(data.get('limit', 50), 1), 200)
            
            if block_hash and not validate_block_hash(block_hash):
                return create_error_response(
                    error="InvalidBlockHash",
                    message="Block hash non valido",
                    code=400
                ), 400
            
            # Analizza blocco
            start_time = time.time()
            analysis = wallet_service.analyze_block(block_hash, limit)
            analysis_time = time.time() - start_time
            
            # Prepara risposta
            response_data = {
                'analysis_id': f'block_{analysis.block_hash[:16]}_{int(time.time())}',
                'target': analysis.block_hash,
                'analysis_type': 'block',
                'block_info': {
                    'block_hash': analysis.block_hash,
                    'total_transactions': analysis.total_transactions,
                    'analyzed_transactions': analysis.analyzed_transactions,
                    'is_latest': analysis.block_hash == 'latest'
                },
                'fingerprint': {
                    'wallet_distribution': analysis.wallet_distribution,
                    'wallet_percentages': analysis.wallet_percentages,
                    'dominant_wallets': [wallet for wallet, pct in analysis.wallet_percentages.items() if pct > 10],
                    'diversity_score': len(analysis.wallet_distribution) / max(analysis.analyzed_transactions, 1)
                },
                'metadata': {
                    'analysis_time': analysis_time,
                    'limit': limit,
                    'block_explorer': f'https://mempool.space/block/{analysis.block_hash}' if analysis.block_hash != 'latest' else None,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            return create_success_response(
                data=response_data,
                message="Blocco analizzato con successo"
            ), 200
            
        except Exception as e:
            logger.error(f"Error in analyze_block: {str(e)}")
            return create_error_response(
                error="AnalysisError",
                message=f"Errore durante l'analisi: {str(e)}",
                code=500
            ), 500

@api.route('/health')
class HealthCheck(Resource):
    @api.doc('health_check')
    @api.marshal_with(success_model, code=200, description='Servizio operativo')
    def get(self):
        """
        Controllo stato del servizio
        
        Endpoint per verificare che l'API sia operativa e funzionante.
        """
        return create_success_response(
            data={
                'status': 'healthy',
                'version': '1.0.0',
                'timestamp': datetime.utcnow().isoformat(),
                'services': {
                    'mempool_api': 'active',
                    'fingerprinting_engine': 'active',
                    'documentation': 'active'
                }
            },
            message="Servizio operativo"
        ), 200

@api.route('/status')
class APIStatus(Resource):
    @api.doc('api_status')
    @api.marshal_with(success_model, code=200, description='Stato dettagliato dell\'API')
    def get(self):
        """
        Stato dettagliato dell'API
        
        Fornisce informazioni dettagliate sullo stato dell'API e sui servizi disponibili.
        """
        return create_success_response(
            data={
                'api_version': '1.0.0',
                'status': 'running',
                'uptime': 'N/A',  # Da implementare
                'endpoints': {
                    'transaction_analysis': '/api/transaction/analyze',
                    'address_analysis': '/api/address/analyze',
                    'block_analysis': '/api/block/analyze',
                    'documentation': '/api/docs',
                    'health_check': '/api/health'
                },
                'rate_limits': {
                    'standard': '100/minute',
                    'analysis': '10/minute'
                },
                'data_sources': [
                    'mempool.space',
                    'blockstream.info'
                ]
            },
            message="API operativa"
        ), 200

# Registra tutti i namespace
api.add_namespace(analyze_ns, path='/analyze')
api.add_namespace(address_ns, path='/address')
api.add_namespace(transaction_ns, path='/transaction')
api.add_namespace(block_ns, path='/block')
api.add_namespace(fingerprint_ns, path='/fingerprint')

