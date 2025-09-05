# 🔍 Wallet Fingerprinting API

**Backend Flask per analisi e rilevamento wallet Bitcoin**

## 🚀 Quick Start

### Installazione
```bash
# Attiva virtual environment
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Avvia API
python backend/app.py
```

### Test API
```bash
# Test completo
python test_api.py

# Test manuale
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

**Response:**
```json
{
  "success": true,
  "message": "Indirizzo analizzato con successo",
  "data": {
    "address": "bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
    "total_transactions": 13,
    "analyzed_transactions": 20,
    "wallet_distribution": {
      "Coinbase Wallet": 4,
      "Exodus Wallet": 3,
      "Blue Wallet": 2,
      "Other": 4
    },
    "wallet_percentages": {
      "Coinbase Wallet": 30.8,
      "Exodus Wallet": 23.1,
      "Blue Wallet": 15.4,
      "Other": 30.8
    },
    "timeline": [...],
    "main_wallet": "Coinbase Wallet",
    "pattern_type": "Multi-wallet",
    "block_explorer": "https://mempool.space/address/..."
  },
  "timestamp": "2024-09-04T16:58:00.000Z"
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
backend/
├── app.py                 # Applicazione Flask principale
├── api/
│   ├── routes.py         # Endpoints API
│   ├── services.py       # Logica di business
│   └── middleware.py     # Middleware e validazione
├── models/
│   └── responses.py      # Modelli per risposte
└── utils/
    └── logger.py         # Sistema di logging
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
- CORS configurato per Next.js

## 🚀 Produzione

### Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:create_app()
```

### Docker (opzionale)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:create_app()"]
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

---

**Backend pronto per integrazione con frontend Next.js!** 🎉
