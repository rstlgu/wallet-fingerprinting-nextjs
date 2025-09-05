#!/usr/bin/env python3
"""
Wallet Fingerprinting Flask API
Backend per analisi wallet Bitcoin con frontend Next.js
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from datetime import datetime

# Aggiungi il path per importare i moduli
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.routes import api_bp
from api.sse_routes import sse_bp
from api.docs_config import docs_bp
from api.swagger_routes import swagger_bp
from api.middleware import error_handler
from utils.logger import setup_logger

def create_app():
    """Crea e configura l'applicazione Flask"""
    app = Flask(__name__)
    
    # Configurazione
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_SORT_KEYS'] = False
    
    # CORS per frontend Next.js
    CORS(app, origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
        "https://yourdomain.com"  # Produzione
    ])
    
    # Setup logging
    logger = setup_logger()
    
    # Registra blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(sse_bp, url_prefix='/sse')
    app.register_blueprint(docs_bp)  # docs_bp ha già prefix='/api'
    app.register_blueprint(swagger_bp, url_prefix='/api')
    
    # Middleware per gestione errori
    app.register_error_handler(Exception, error_handler)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Wallet Fingerprinting API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'analyze_tx': '/api/transaction/analyze',
                'analyze_address': '/api/address/analyze',
                'analyze_block': '/api/block/analyze',
                'docs': '/api/docs',
                'swagger_ui': '/api/docs/',
                'swagger_custom': '/api/swagger-ui',
                'redoc': '/api/redoc'
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Avviando Wallet Fingerprinting API su porta {port}")
    print(f"🔗 URL: http://localhost:{port}")
    print(f"📚 Docs: http://localhost:{port}/api/docs")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
