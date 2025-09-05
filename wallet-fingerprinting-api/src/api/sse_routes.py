"""
Server-Sent Events (SSE) routes per streaming real-time
"""

import json
import time
import threading
import queue
from datetime import datetime
from flask import Blueprint, Response, request, jsonify
from typing import Dict, Any, Generator
import sys
import os

# Aggiungi path per importare moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services import wallet_service
from api.middleware import validate_txid, validate_address
from models.responses import create_error_response
from utils.logger import setup_logger

logger = setup_logger()

# Blueprint per SSE
sse_bp = Blueprint('sse', __name__)

# Store globale per i client SSE
sse_clients: Dict[str, Any] = {}

class SSEManager:
    """Manager per gestire connessioni SSE"""
    
    def __init__(self):
        self.clients = {}
    
    def add_client(self, session_id: str, generator):
        """Aggiungi un client SSE"""
        self.clients[session_id] = generator
    
    def remove_client(self, session_id: str):
        """Rimuovi un client SSE"""
        if session_id in self.clients:
            del self.clients[session_id]
    
    def send_message(self, session_id: str, message: Dict[str, Any]):
        """Invia messaggio a un client specifico"""
        if session_id in self.clients:
            formatted_msg = f"data: {json.dumps(message)}\n\n"
            try:
                self.clients[session_id].send(formatted_msg)
            except:
                self.remove_client(session_id)

sse_manager = SSEManager()

def format_sse_message(event_type: str, data: Dict[str, Any]) -> str:
    """Formatta messaggio SSE"""
    message = {
        'type': event_type,
        'timestamp': datetime.utcnow().isoformat(),
        'data': data
    }
    return f"data: {json.dumps(message)}\n\n"

@sse_bp.route('/stream/<session_id>')
def stream_analysis(session_id: str):
    """Endpoint SSE per streaming analisi"""
    
    def event_stream():
        try:
            # Crea coda per questa sessione
            message_queue = queue.Queue()
            active_generators[session_id] = message_queue
            
            # Messaggio di connessione
            yield format_sse_message('connected', {
                'session_id': session_id,
                'message': 'Connessione SSE stabilita'
            })
            
            # Invia messaggi storici se esistenti
            if session_id in sse_clients:
                for message in sse_clients[session_id]:
                    yield f"data: {json.dumps(message)}\n\n"
            
            # Loop principale per messaggi in tempo reale
            last_heartbeat = time.time()
            while True:
                try:
                    # Controlla messaggi nella coda
                    message = message_queue.get(timeout=5)
                    yield message
                except queue.Empty:
                    # Invia heartbeat ogni 30 secondi
                    current_time = time.time()
                    if current_time - last_heartbeat > 30:
                        yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': datetime.utcnow().isoformat()})}\n\n"
                        last_heartbeat = current_time
                
        except GeneratorExit:
            logger.info(f"SSE client disconnected: {session_id}")
            if session_id in active_generators:
                del active_generators[session_id]
    
    response = Response(event_stream(), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Cache-Control'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['X-Accel-Buffering'] = 'no'
    
    return response

@sse_bp.route('/analyze/tx/<session_id>', methods=['POST'])
def analyze_transaction_sse(session_id: str):
    """Analizza transazione con streaming SSE"""
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
        
        # Avvia analisi in thread separato
        def analyze_with_progress():
            try:
                # Inizio analisi
                send_progress(session_id, 'started', {
                    'message': f'Iniziando analisi transazione {txid[:16]}...',
                    'progress': 0
                })
                
                # Recupero dati
                send_progress(session_id, 'progress', {
                    'message': 'Recupero dati transazione da blockchain...',
                    'progress': 25
                })
                
                analysis = wallet_service.analyze_transaction(txid)
                
                # Analisi completata
                send_progress(session_id, 'progress', {
                    'message': 'Analisi wallet in corso...',
                    'progress': 75
                })
                
                # Risultato finale
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
                
                send_progress(session_id, 'completed', {
                    'message': 'Analisi completata con successo!',
                    'progress': 100,
                    'result': response_data
                })
                
            except Exception as e:
                send_progress(session_id, 'error', {
                    'message': f'Errore durante analisi: {str(e)}',
                    'error': str(e)
                })
        
        # Avvia in background
        thread = threading.Thread(target=analyze_with_progress)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Analisi avviata',
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_transaction_sse: {str(e)}")
        return jsonify(create_error_response(
            error="AnalysisError",
            message=f"Errore durante l'analisi: {str(e)}",
            code=500
        )), 500

@sse_bp.route('/analyze/address/<session_id>', methods=['POST'])
def analyze_address_sse(session_id: str):
    """Analizza indirizzo con streaming SSE"""
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
        
        limit = data.get('limit', 20)
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            limit = 20
        
        # Avvia analisi in thread separato
        def analyze_with_progress():
            try:
                # Inizio analisi
                send_progress(session_id, 'started', {
                    'message': f'Iniziando analisi indirizzo {address[:16]}...',
                    'progress': 0
                })
                
                # Recupero transazioni
                send_progress(session_id, 'progress', {
                    'message': 'Recupero lista transazioni...',
                    'progress': 20
                })
                
                analysis = wallet_service.analyze_address(address, limit)
                
                # Analisi in corso
                send_progress(session_id, 'progress', {
                    'message': f'Analizzando {limit} transazioni...',
                    'progress': 80
                })
                
                # Risultato finale
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
                
                send_progress(session_id, 'completed', {
                    'message': 'Analisi indirizzo completata!',
                    'progress': 100,
                    'result': response_data
                })
                
            except Exception as e:
                send_progress(session_id, 'error', {
                    'message': f'Errore durante analisi: {str(e)}',
                    'error': str(e)
                })
        
        # Avvia in background
        thread = threading.Thread(target=analyze_with_progress)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Analisi avviata',
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_address_sse: {str(e)}")
        return jsonify(create_error_response(
            error="AnalysisError",
            message=f"Errore durante l'analisi: {str(e)}",
            code=500
        )), 500

# Store globale per generators SSE attivi
active_generators = {}

def send_progress(session_id: str, event_type: str, data: Dict[str, Any]):
    """Invia aggiornamento di progresso via SSE"""
    try:
        message = {
            'type': event_type,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Store del messaggio per invio
        if session_id not in sse_clients:
            sse_clients[session_id] = []
        
        sse_clients[session_id].append(message)
        
        # Invia direttamente al generator se attivo
        if session_id in active_generators:
            try:
                formatted_msg = f"data: {json.dumps(message)}\n\n"
                active_generators[session_id].put(formatted_msg)
            except:
                # Generator non più attivo, rimuovilo
                if session_id in active_generators:
                    del active_generators[session_id]
        
        logger.info(f"Progress sent to {session_id}: {event_type} - {data.get('message', '')}")
        
    except Exception as e:
        logger.error(f"Error sending progress: {str(e)}")

@sse_bp.route('/messages/<session_id>')
def get_messages(session_id: str):
    """Recupera messaggi per una sessione (fallback per quando SSE non funziona)"""
    messages = sse_clients.get(session_id, [])
    return jsonify({
        'success': True,
        'messages': messages,
        'session_id': session_id
    })
