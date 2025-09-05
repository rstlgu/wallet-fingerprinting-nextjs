# 🔍 Wallet Fingerprinting API

**Backend Flask per analisi e rilevamento wallet Bitcoin**

Un'API REST completa per identificare il software wallet utilizzato per creare transazioni Bitcoin, basata sull'analisi delle impronte digitali delle transazioni.

## 🚀 Quick Start

### Installazione
```bash
# Clona il repository
git clone <repository-url>
cd wallet-fingerprinting-api

# Crea virtual environment
python3 -m venv venv
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Avvia API
python src/app.py
```

### Test API
```bash
# Test rapido
curl http://localhost:5000/health

# Test analisi transazione
curl -X POST http://localhost:5000/api/analyze/tx \
  -H "Content-Type: application/json" \
  -d '{"txid": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166"}'
```

## 📚 Endpoints API

### `POST /api/analyze/tx`
Analizza una singola transazione Bitcoin.

**Request:**
```json
{
  "txid": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Transazione analizzata con successo",
  "data": {
    "transaction": {
      "txid": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166",
      "version": 2,
      "locktime": 0,
      "inputs_count": 2,
      "outputs_count": 2,
      "input_types": ["v0_p2wpkh", "v0_p2wpkh"],
      "output_types": ["v0_p2wpkh", "v0_p2wpkh"]
    },
    "detection": {
      "wallet": "Blue Wallet",
      "confidence": 95.0,
      "reasoning": ["No Anti-fee-sniping", "All compressed public keys", ...],
      "is_clear": true
    },
    "analysis_time": 0.123,
    "block_explorer": "https://mempool.space/tx/..."
  },
  "timestamp": "2024-09-04T16:58:00.000Z"
}
```

### `POST /api/analyze/address`
Analizza un indirizzo Bitcoin.

**Request:**
```json
{
  "address": "bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
  "limit": 20
}
```

### `POST /api/analyze/block`
Analizza un blocco Bitcoin.

**Request:**
```json
{
  "block_hash": "00000000000000000004bcc50688d02a74d778201a47cc704a877d1442a58431",
  "num_txs": 50
}
```

### `GET /api/docs`
Documentazione completa dell'API.

### `GET /api/status`
Stato dell'API.

### `GET /health`
Health check dell'API.

## 🏗️ Architettura

```
wallet-fingerprinting-api/
├── src/
│   ├── app.py                 # Applicazione Flask principale
│   ├── fingerprinting.py      # Core del sistema di fingerprinting
│   ├── fetch_txs.py          # Gestione sorgenti dati
│   ├── bitcoin_core.py       # Interfaccia Bitcoin Core RPC
│   ├── mempool_space.py      # Interfaccia mempool.space API
│   ├── rpc_config.ini        # Configurazione RPC
│   ├── api/
│   │   ├── routes.py         # Endpoints API
│   │   ├── services.py       # Logica di business
│   │   └── middleware.py     # Middleware e validazione
│   ├── models/
│   │   └── responses.py      # Modelli per risposte
│   └── utils/
│       └── logger.py         # Sistema di logging
├── tests/                    # Test suite
├── docs/                     # Documentazione
├── scripts/                  # Script di utilità
├── requirements.txt          # Dipendenze Python
└── config.env.example       # Configurazione esempio
```

## ⚙️ Configurazione

### Variabili d'Ambiente
```bash
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key
PORT=5000

# Logging
LOG_FILE=api.log
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Bitcoin Core (Opzionale)
```bash
BITCOIN_CORE_URL=http://127.0.0.1:8332/
BITCOIN_CORE_USER=your_username
BITCOIN_CORE_PASSWORD=your_password
```

## 🔧 Sviluppo

### Struttura Modulare
- **Routes**: Gestione endpoint HTTP
- **Services**: Logica di business
- **Models**: Strutture dati
- **Middleware**: Validazione e logging

### Validazione Input
- **TXID**: 64 caratteri esadecimali
- **Address**: Indirizzi Bitcoin validi (1, 3, bc1)
- **Block Hash**: 64 caratteri esadecimali

### Gestione Errori
- Errori standardizzati
- Logging completo
- CORS configurato per frontend

## 🚀 Produzione

### Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.app:create_app()
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.app:create_app()"]
```

## 📊 Performance

- **Analisi transazione**: ~0.1-0.5s
- **Analisi indirizzo**: ~2-10s (dipende da numero transazioni)
- **Analisi blocco**: ~5-30s (dipende da numero transazioni)

## 🔗 Integrazione Frontend

L'API è progettata per integrarsi perfettamente con Next.js:

```javascript
// Esempio chiamata da Next.js
const response = await fetch('http://localhost:5000/api/analyze/tx', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    txid: '7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166'
  })
});

const result = await response.json();
```

## 🎯 Wallet Supportati

| Wallet | Tipo | Caratteristiche |
|--------|------|-----------------|
| **Bitcoin Core** | Desktop | Anti-fee-sniping, low-r signatures |
| **Electrum** | Desktop | BIP-69, RBF signaling |
| **Blue Wallet** | Mobile | Multi-output, change detection |
| **Trezor** | Hardware | BIP-69, historical ordering |
| **Ledger** | Hardware | Historical ordering, change last |
| **Exodus** | Multi-crypto | P2PKH spending, no RBF |
| **Trust Wallet** | Mobile | P2PKH spending, address reuse |
| **Coinbase** | Exchange | No RBF, no OP_RETURN |

## 🔬 Tecniche di Analisi

- **Anti-fee-sniping** (locktime analysis)
- **Ordinamento input/output** (BIP-69, cronologico, crescente/decrescente)  
- **Analisi chiavi pubbliche** (compresse vs non compresse)
- **Low-R signature grinding**
- **Replace-by-Fee (RBF) signaling**
- **Struttura output** (singolo, doppio, multiplo)
- **Rilevamento change address**
- **Address reuse patterns**
- **Script type analysis** (P2PKH, P2WPKH, P2WSH, Taproot)

## 📈 Esempi di Output

### Analisi Dettagliata
```
🎯 Wallet rilevato: Blue Wallet
📋 Analisi dettagliata:
   1. No Anti-fee-sniping
   2. All compressed public keys  
   3. nVersion = 2
   4. Low r signatures only
   5. signals RBF
   6. Change type matched inputs
   7. No address reuse between vin and vout
   8. BIP-69 followed by outputs
   9. BIP-69 followed by inputs
  10. Inputs ordered historically
```

### Distribuzione Blocco
```
📊 Distribuzione wallet:
   Electrum       :  1 transazioni ( 10.0%)
   Blue Wallet    :  2 transazioni ( 20.0%)
   Ledger         :  2 transazioni ( 20.0%)
   Other          :  4 transazioni ( 40.0%)
```

## ⚠️ Limitazioni

- **Risultati probabilistici** - non certezze assolute
- **8 wallet supportati** - altri classificati come "Other"
- **Possibili falsi positivi** con wallet che imitano fingerprint
- **Dipendenza da dati storici** per alcune euristiche

## 🧪 Testing

```bash
# Test completo
python -m pytest tests/

# Test specifico
python -c "
import requests
response = requests.post('http://localhost:5000/api/analyze/tx', 
  json={'txid': 'TXID_HERE'})
print(response.json())
"
```

## 📚 Risorse

- [Documentazione originale](https://ishaana.com/blog/wallet_fingerprinting/)
- [Bitcoin Core RPC](https://developer.bitcoin.org/reference/rpc/)
- [mempool.space API](https://mempool.space/api)

---

**Backend API pronto per integrazione con frontend Next.js!** 🎉
