#!/usr/bin/env python3
"""
Wallet Fingerprinting Flask API - Entry Point per Vercel
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carica variabili d'ambiente
config_path = Path(__file__).parent / 'config.env'
if config_path.exists():
    load_dotenv(config_path)

# Aggiungi src al path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Importa l'app da src
from app import create_app

# Crea l'app per Vercel
app = create_app()

# Per Vercel, l'app deve essere esposta come 'app'
if __name__ == '__main__':
    # Solo per sviluppo locale
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Avviando Wallet Fingerprinting API su porta {port}")
    print(f"🔗 URL: http://localhost:{port}")
    print(f"📚 Docs: http://localhost:{port}/api/docs")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
