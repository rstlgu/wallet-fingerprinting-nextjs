#!/usr/bin/env python3
"""
Script di avvio per Wallet Fingerprinting API
"""

import os
import sys
from pathlib import Path

# Aggiungi src al path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

if __name__ == '__main__':
    from app import create_app
    
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Avviando Wallet Fingerprinting API su porta {port}")
    print(f"🔗 URL: http://localhost:{port}")
    print(f"📚 Docs: http://localhost:{port}/api/docs")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
