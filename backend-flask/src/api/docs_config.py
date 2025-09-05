#!/usr/bin/env python3
"""
Configurazione documentazione API con Flask-RESTX
"""

from flask_restx import Api, Resource
from flask import Blueprint

# Blueprint per la documentazione API
docs_bp = Blueprint('docs', __name__)

# Configurazione Flask-RESTX
api = Api(
    docs_bp,
    version='1.0.0',
    title='Wallet Fingerprinting API',
    description='''
    ## API per l'analisi e il fingerprinting di wallet Bitcoin
    
    Questa API fornisce strumenti avanzati per:
    - 🔍 Analisi delle transazioni Bitcoin
    - 👤 Fingerprinting di indirizzi e wallet
    - 📊 Analisi dei pattern comportamentali
    - ⚡ Aggiornamenti real-time tramite SSE
    
    ### Autenticazione
    Attualmente l'API è pubblica per scopi di demo. In produzione implementare autenticazione JWT.
    
    ### Rate Limiting
    - Limite di 100 richieste/minuto per IP
    - Analisi complesse: 10 richieste/minuto
    
    ### Fonti Dati
    - Bitcoin Core RPC (opzionale)
    - Mempool.space API
    - Blockstream API (fallback)
    ''',
    doc='/docs/',
    prefix='/api',
    contact='Supporto API',
    contact_email='support@example.com',
    license='MIT License',
    license_url='https://opensource.org/licenses/MIT',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Bearer token (formato: Bearer <token>)'
        }
    }
)

# Namespace per organizzare gli endpoint
analyze_ns = api.namespace('analyze', description='Operazioni di analisi Bitcoin')
address_ns = api.namespace('address', description='Analisi indirizzi Bitcoin')
transaction_ns = api.namespace('transaction', description='Analisi transazioni')
block_ns = api.namespace('block', description='Analisi blocchi Bitcoin')
fingerprint_ns = api.namespace('fingerprint', description='Fingerprinting wallet')

# Route documentate sono definite direttamente qui sotto

# Modelli di dati per la documentazione
from flask_restx import fields

# Modello per risposta di successo generica
success_model = api.model('SuccessResponse', {
    'status': fields.String(required=True, description='Stato della richiesta', example='success'),
    'message': fields.String(required=True, description='Messaggio descrittivo'),
    'timestamp': fields.DateTime(required=True, description='Timestamp della risposta'),
    'data': fields.Raw(description='Dati della risposta')
})

# Modello per errore
error_model = api.model('ErrorResponse', {
    'status': fields.String(required=True, description='Stato della richiesta', example='error'),
    'error': fields.String(required=True, description='Tipo di errore'),
    'message': fields.String(required=True, description='Messaggio di errore'),
    'timestamp': fields.DateTime(required=True, description='Timestamp dell\'errore'),
    'details': fields.Raw(description='Dettagli aggiuntivi dell\'errore')
})

# Modello per transazione Bitcoin
transaction_model = api.model('Transaction', {
    'txid': fields.String(required=True, description='Transaction ID', example='1a2b3c4d...'),
    'block_height': fields.Integer(description='Altezza del blocco'),
    'confirmations': fields.Integer(description='Numero di conferme'),
    'fee': fields.Integer(description='Fee in satoshi'),
    'size': fields.Integer(description='Dimensione in bytes'),
    'inputs': fields.List(fields.Raw, description='Input della transazione'),
    'outputs': fields.List(fields.Raw, description='Output della transazione'),
    'timestamp': fields.DateTime(description='Timestamp della transazione')
})

# Modello per indirizzo Bitcoin
address_model = api.model('Address', {
    'address': fields.String(required=True, description='Indirizzo Bitcoin', example='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'),
    'balance': fields.Integer(description='Saldo in satoshi'),
    'total_received': fields.Integer(description='Totale ricevuto in satoshi'),
    'total_sent': fields.Integer(description='Totale inviato in satoshi'),
    'tx_count': fields.Integer(description='Numero di transazioni'),
    'first_seen': fields.DateTime(description='Prima volta visto'),
    'last_seen': fields.DateTime(description='Ultima volta visto')
})

# Modello per analisi fingerprinting
fingerprint_model = api.model('FingerprintAnalysis', {
    'wallet_id': fields.String(description='ID identificativo del wallet'),
    'confidence': fields.Float(description='Livello di confidenza (0-1)', min=0, max=1),
    'patterns': fields.List(fields.String, description='Pattern identificati'),
    'behavioral_score': fields.Float(description='Punteggio comportamentale'),
    'risk_level': fields.String(description='Livello di rischio', enum=['low', 'medium', 'high']),
    'cluster_addresses': fields.List(fields.String, description='Indirizzi nel cluster'),
    'analysis_timestamp': fields.DateTime(description='Timestamp dell\'analisi')
})

# Modello per richiesta di analisi
analyze_request_model = api.model('AnalyzeRequest', {
    'target': fields.String(required=True, description='Target da analizzare (txid, address, block)'),
    'depth': fields.Integer(description='Profondità dell\'analisi (1-5)', min=1, max=5, default=3),
    'include_patterns': fields.Boolean(description='Includere pattern analysis', default=True),
    'include_clustering': fields.Boolean(description='Includere cluster analysis', default=False),
    'realtime_updates': fields.Boolean(description='Abilitare aggiornamenti real-time', default=False)
})

# Modello per risposta di analisi
analyze_response_model = api.model('AnalyzeResponse', {
    'analysis_id': fields.String(required=True, description='ID univoco dell\'analisi'),
    'status': fields.String(required=True, description='Stato dell\'analisi', enum=['pending', 'processing', 'completed', 'failed']),
    'progress': fields.Float(description='Progresso dell\'analisi (0-100)', min=0, max=100),
    'results': fields.Nested(fingerprint_model, description='Risultati dell\'analisi'),
    'metadata': fields.Raw(description='Metadati dell\'analisi'),
    'estimated_completion': fields.DateTime(description='Tempo stimato di completamento')
})

# Headers comuni per le risposte
response_headers = {
    'X-RateLimit-Limit': 'Limite di richieste per periodo',
    'X-RateLimit-Remaining': 'Richieste rimanenti nel periodo corrente',
    'X-RateLimit-Reset': 'Timestamp di reset del limite'
}

# Registra le route documentate
@transaction_ns.route('/analyze')
class TransactionAnalysis(Resource):
    @api.doc('analyze_transaction')
    @api.marshal_with(success_model, code=200, description='Analisi completata con successo')
    @api.marshal_with(error_model, code=400, description='Parametri non validi')
    @api.marshal_with(error_model, code=500, description='Errore interno del server')
    @api.response(200, 'Successo', success_model, headers=response_headers)
    @api.response(400, 'Errore validazione', error_model)
    @api.response(500, 'Errore server', error_model)
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
        
        **Esempio di risposta (200):**
        ```json
        {
            "status": "success",
            "message": "Transazione analizzata con successo",
            "timestamp": "2025-09-05T11:30:00.000Z",
            "data": {
                "analysis_id": "tx_7a2c087cb02a758b_1725531000",
                "target": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166",
                "analysis_type": "transaction",
                "transaction": {
                    "txid": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166",
                    "version": 2,
                    "locktime": 0,
                    "inputs_count": 1,
                    "outputs_count": 2,
                    "input_types": ["P2WPKH"],
                    "output_types": ["P2WPKH", "P2WPKH"],
                    "size": 225,
                    "fee": 1000
                },
                "fingerprint": {
                    "wallet": "Electrum",
                    "confidence": 0.85,
                    "reasoning": "Pattern di input/output tipico di Electrum, uso di P2WPKH",
                    "is_clear": true,
                    "risk_level": "medium"
                },
                "metadata": {
                    "analysis_time": 1.23,
                    "depth": 3,
                    "include_patterns": true,
                    "block_explorer": "https://mempool.space/tx/7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166",
                    "timestamp": "2025-09-05T11:30:00.000Z"
                }
            }
        }
        ```
        
        **Esempio di errore (400):**
        ```json
        {
            "status": "error",
            "error": "InvalidTxid",
            "message": "txid non valido",
            "timestamp": "2025-09-05T11:30:00.000Z",
            "details": {
                "field": "txid",
                "value": "invalid_txid",
                "expected_format": "64 caratteri hex"
            }
        }
        ```
        """
        return {'message': 'Endpoint in sviluppo'}

@address_ns.route('/analyze')
class AddressAnalysis(Resource):
    @api.doc('analyze_address')
    @api.marshal_with(success_model, code=200, description='Analisi completata con successo')
    @api.marshal_with(error_model, code=400, description='Parametri non validi')
    @api.marshal_with(error_model, code=500, description='Errore interno del server')
    @api.response(200, 'Successo', success_model, headers=response_headers)
    @api.response(400, 'Errore validazione', error_model)
    @api.response(500, 'Errore server', error_model)
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
        
        **Esempio di risposta (200):**
        ```json
        {
            "status": "success",
            "message": "Indirizzo analizzato con successo",
            "timestamp": "2025-09-05T11:30:00.000Z",
            "data": {
                "analysis_id": "addr_bc1qynqu36tgkn_1725531000",
                "target": "bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
                "analysis_type": "address",
                "address_info": {
                    "address": "bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
                    "total_transactions": 127,
                    "analyzed_transactions": 50,
                    "address_type": "P2WPKH"
                },
                "fingerprint": {
                    "wallet_distribution": {
                        "Electrum": 45,
                        "Bitcoin Core": 12,
                        "Unknown": 8
                    },
                    "wallet_percentages": {
                        "Electrum": 0.69,
                        "Bitcoin Core": 0.18,
                        "Unknown": 0.13
                    },
                    "main_wallet": "Electrum",
                    "pattern_type": "HD_Wallet",
                    "confidence": 0.69,
                    "risk_level": "low"
                },
                "timeline": [
                    {
                        "date": "2025-09-01",
                        "transactions": 15,
                        "volume_sats": 2500000
                    },
                    {
                        "date": "2025-09-02", 
                        "transactions": 8,
                        "volume_sats": 1200000
                    }
                ],
                "metadata": {
                    "analysis_time": 2.45,
                    "limit": 50,
                    "depth": 3,
                    "block_explorer": "https://mempool.space/address/bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
                    "timestamp": "2025-09-05T11:30:00.000Z"
                }
            }
        }
        ```
        
        **Esempio di errore (400):**
        ```json
        {
            "status": "error",
            "error": "InvalidAddress",
            "message": "Indirizzo Bitcoin non valido",
            "timestamp": "2025-09-05T11:30:00.000Z",
            "details": {
                "field": "address",
                "value": "invalid_address",
                "expected_format": "Indirizzo Bitcoin valido (P2PKH, P2SH, P2WPKH, P2WSH)"
            }
        }
        ```
        """
        return {'message': 'Endpoint in sviluppo'}

@block_ns.route('/analyze')
class BlockAnalysis(Resource):
    @api.doc('analyze_block')
    @api.marshal_with(success_model, code=200, description='Analisi completata con successo')
    @api.marshal_with(error_model, code=400, description='Parametri non validi')
    @api.marshal_with(error_model, code=500, description='Errore interno del server')
    @api.response(200, 'Successo', success_model, headers=response_headers)
    @api.response(400, 'Errore validazione', error_model)
    @api.response(500, 'Errore server', error_model)
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
        
        **Esempio di risposta (200):**
        ```json
        {
            "status": "success",
            "message": "Blocco analizzato con successo",
            "timestamp": "2025-09-05T11:30:00.000Z",
            "data": {
                "analysis_id": "block_0000000000000000_1725531000",
                "target": "00000000000000000004bcc50688d02a74d778201a47cc704a877d1442a58431",
                "analysis_type": "block",
                "block_info": {
                    "block_hash": "00000000000000000004bcc50688d02a74d778201a47cc704a877d1442a58431",
                    "total_transactions": 2847,
                    "analyzed_transactions": 100,
                    "is_latest": false
                },
                "fingerprint": {
                    "wallet_distribution": {
                        "Electrum": 1250,
                        "Bitcoin Core": 890,
                        "Exodus": 340,
                        "Unknown": 367
                    },
                    "wallet_percentages": {
                        "Electrum": 0.44,
                        "Bitcoin Core": 0.31,
                        "Exodus": 0.12,
                        "Unknown": 0.13
                    },
                    "dominant_wallets": ["Electrum", "Bitcoin Core"],
                    "diversity_score": 0.35
                },
                "metadata": {
                    "analysis_time": 5.67,
                    "limit": 100,
                    "block_explorer": "https://mempool.space/block/00000000000000000004bcc50688d02a74d778201a47cc704a877d1442a58431",
                    "timestamp": "2025-09-05T11:30:00.000Z"
                }
            }
        }
        ```
        
        **Esempio di errore (400):**
        ```json
        {
            "status": "error",
            "error": "InvalidBlockHash",
            "message": "Block hash non valido",
            "timestamp": "2025-09-05T11:30:00.000Z",
            "details": {
                "field": "block_hash",
                "value": "invalid_hash",
                "expected_format": "64 caratteri hex"
            }
        }
        ```
        """
        return {'message': 'Endpoint in sviluppo'}

@api.route('/health')
class HealthCheck(Resource):
    @api.doc('health_check')
    @api.marshal_with(success_model, code=200, description='Servizio operativo')
    @api.response(200, 'Servizio operativo', success_model)
    def get(self):
        """
        Controllo stato del servizio
        
        Endpoint per verificare che l'API sia operativa e funzionante.
        Fornisce informazioni sullo stato dei servizi e la versione dell'API.
        
        **Esempio di risposta (200):**
        ```json
        {
            "status": "success",
            "message": "Servizio operativo",
            "timestamp": "2025-09-05T11:30:00.000Z",
            "data": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2025-09-05T11:30:00.000Z",
                "services": {
                    "mempool_api": "active",
                    "fingerprinting_engine": "active",
                    "documentation": "active"
                },
                "uptime": "2h 15m 30s",
                "memory_usage": "45.2 MB",
                "cpu_usage": "12.5%"
            }
        }
        ```
        """
        return {
            'status': 'healthy',
            'version': '1.0.0',
            'timestamp': '2025-09-05T09:23:49.443601'
        }
