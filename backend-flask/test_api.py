#!/usr/bin/env python3
"""
Script per testare l'API Wallet Fingerprinting
"""

import requests
import json
import time
import sys
import os

# Aggiungi src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

API_BASE = "http://localhost:5000"

def test_api():
    """Test completo dell'API"""
    
    print("🧪 TEST API WALLET FINGERPRINTING")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Test Health Check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
    
    # Test 2: API Status
    print("\n2️⃣ Test API Status...")
    try:
        response = requests.get(f"{API_BASE}/api/status")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
    
    # Test 3: Analisi Transazione
    print("\n3️⃣ Test Analisi Transazione...")
    try:
        data = {
            "txid": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166"
        }
        response = requests.post(f"{API_BASE}/api/analyze/tx", json=data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        if result.get('success'):
            detection = result['data']['detection']
            print(f"   Wallet: {detection['wallet']}")
            print(f"   Confidence: {detection['confidence']}%")
        else:
            print(f"   ❌ Errore: {result.get('message')}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
    
    # Test 4: Analisi Indirizzo
    print("\n4️⃣ Test Analisi Indirizzo...")
    try:
        data = {
            "address": "bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
            "limit": 10
        }
        response = requests.post(f"{API_BASE}/api/analyze/address", json=data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        if result.get('success'):
            analysis = result['data']
            print(f"   Transazioni totali: {analysis['total_transactions']}")
            print(f"   Wallet principale: {analysis['main_wallet']}")
            print(f"   Pattern: {analysis['pattern_type']}")
        else:
            print(f"   ❌ Errore: {result.get('message')}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
    
    # Test 5: Analisi Blocco
    print("\n5️⃣ Test Analisi Blocco...")
    try:
        data = {
            "num_txs": 10
        }
        response = requests.post(f"{API_BASE}/api/analyze/block", json=data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        if result.get('success'):
            analysis = result['data']
            print(f"   Transazioni analizzate: {analysis['analyzed_transactions']}")
            print(f"   Tempo analisi: {analysis['analysis_time']:.2f}s")
        else:
            print(f"   ❌ Errore: {result.get('message')}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
    
    # Test 6: Documentazione
    print("\n6️⃣ Test Documentazione...")
    try:
        response = requests.get(f"{API_BASE}/api/docs")
        print(f"   Status: {response.status_code}")
        result = response.json()
        if result.get('success'):
            docs = result['data']
            print(f"   Titolo: {docs['title']}")
            print(f"   Version: {docs['version']}")
            print(f"   Endpoints: {len(docs['endpoints'])}")
        else:
            print(f"   ❌ Errore: {result.get('message')}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
    
    print("\n🎉 Test completati!")

if __name__ == "__main__":
    print("⚠️  Assicurati che l'API sia in esecuzione su http://localhost:5000")
    print("   Avvia con: python src/app.py")
    print()
    
    input("Premi INVIO per continuare...")
    test_api()
