# Wallet Fingerprinting API - Esempi

## 🚀 Esempi di utilizzo dell'API

### 1. Analisi Transazione

**Richiesta:**
```bash
curl -X POST "http://localhost:5000/api/transaction/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "txid": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166",
    "depth": 3,
    "include_patterns": true
  }'
```

**Risposta:**
```json
{
  "success": true,
  "message": "Transazione analizzata con successo",
  "data": {
    "analysis_id": "tx_7a2c087cb02a758b_1704067200",
    "target": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166",
    "analysis_type": "transaction",
    "transaction": {
      "txid": "7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166",
      "version": 2,
      "locktime": 0,
      "inputs_count": 1,
      "outputs_count": 2,
      "input_types": ["P2WPKH"],
      "output_types": ["P2WPKH", "P2SH"]
    },
    "fingerprint": {
      "wallet": "Electrum",
      "confidence": 0.85,
      "reasoning": ["BIP125 RBF enabled", "Round number output"],
      "is_clear": true,
      "risk_level": "high"
    },
    "metadata": {
      "analysis_time": 0.45,
      "depth": 3,
      "include_patterns": true,
      "block_explorer": "https://mempool.space/tx/7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166",
      "timestamp": "2024-01-01T12:00:00.000Z"
    }
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### 2. Analisi Indirizzo

**Richiesta:**
```bash
curl -X POST "http://localhost:5000/api/address/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
    "limit": 50,
    "depth": 3
  }'
```

**Risposta:**
```json
{
  "success": true,
  "message": "Indirizzo analizzato con successo",
  "data": {
    "analysis_id": "addr_bc1qynqu36tgknqv_1704067200",
    "target": "bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
    "analysis_type": "address",
    "address_info": {
      "address": "bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
      "total_transactions": 125,
      "analyzed_transactions": 50,
      "address_type": "P2WPKH"
    },
    "fingerprint": {
      "wallet_distribution": {
        "Electrum": 35,
        "Core": 10,
        "Unknown": 5
      },
      "wallet_percentages": {
        "Electrum": 70.0,
        "Core": 20.0,
        "Unknown": 10.0
      },
      "main_wallet": "Electrum",
      "pattern_type": "consistent_wallet",
      "confidence": 0.70,
      "risk_level": "low"
    },
    "timeline": [
      {"date": "2024-01-01", "transactions": 5, "main_wallet": "Electrum"},
      {"date": "2024-01-02", "transactions": 3, "main_wallet": "Electrum"}
    ],
    "metadata": {
      "analysis_time": 1.23,
      "limit": 50,
      "depth": 3,
      "block_explorer": "https://mempool.space/address/bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl",
      "timestamp": "2024-01-01T12:00:00.000Z"
    }
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### 3. Analisi Blocco

**Richiesta:**
```bash
curl -X POST "http://localhost:5000/api/block/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "block_hash": "00000000000000000004bcc50688d02a74d778201a47cc704a877d1442a58431",
    "limit": 100
  }'
```

**Risposta:**
```json
{
  "success": true,
  "message": "Blocco analizzato con successo",
  "data": {
    "analysis_id": "block_00000000000000000004_1704067200",
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
        "Core": 45,
        "Electrum": 25,
        "Exodus": 15,
        "Unknown": 15
      },
      "wallet_percentages": {
        "Core": 45.0,
        "Electrum": 25.0,
        "Exodus": 15.0,
        "Unknown": 15.0
      },
      "dominant_wallets": ["Core", "Electrum", "Exodus"],
      "diversity_score": 0.04
    },
    "metadata": {
      "analysis_time": 2.15,
      "limit": 100,
      "block_explorer": "https://mempool.space/block/00000000000000000004bcc50688d02a74d778201a47cc704a877d1442a58431",
      "timestamp": "2024-01-01T12:00:00.000Z"
    }
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### 4. Health Check

**Richiesta:**
```bash
curl -X GET "http://localhost:5000/api/health"
```

**Risposta:**
```json
{
  "success": true,
  "message": "Servizio operativo",
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "timestamp": "2024-01-01T12:00:00.000Z",
    "services": {
      "mempool_api": "active",
      "fingerprinting_engine": "active",
      "documentation": "active"
    }
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## 📚 Codici di Errore

### 400 - Bad Request
```json
{
  "success": false,
  "error": "InvalidTxid",
  "message": "txid non valido",
  "code": 400,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### 500 - Internal Server Error
```json
{
  "success": false,
  "error": "AnalysisError",
  "message": "Errore durante l'analisi: Connection timeout",
  "code": 500,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## 🔧 Rate Limits

- **Standard endpoints**: 100 richieste/minuto
- **Analysis endpoints**: 10 richieste/minuto

### Headers di risposta:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704067260
```

## 🌐 URLs Documentazione

- **Swagger UI**: `http://localhost:5000/api/docs/`
- **Swagger UI Personalizzata**: `http://localhost:5000/api/swagger-ui`
- **ReDoc**: `http://localhost:5000/api/redoc`
- **OpenAPI JSON**: `http://localhost:5000/api/swagger.json`

## 🧪 Test con JavaScript

```javascript
// Esempio con fetch API
async function analyzeTransaction(txid) {
  try {
    const response = await fetch('http://localhost:5000/api/transaction/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        txid: txid,
        depth: 3,
        include_patterns: true
      })
    });
    
    const data = await response.json();
    
    if (data.success) {
      console.log('Analisi completata:', data.data);
      return data.data;
    } else {
      console.error('Errore:', data.message);
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Errore di rete:', error);
    throw error;
  }
}

// Utilizzo
analyzeTransaction('7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166')
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

## 🐍 Test con Python

```python
import requests
import json

def analyze_address(address, limit=20):
    url = "http://localhost:5000/api/address/analyze"
    payload = {
        "address": address,
        "limit": limit,
        "depth": 3
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        if data['success']:
            print(f"Analisi completata per {address}")
            return data['data']
        else:
            print(f"Errore: {data['message']}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete: {e}")
        return None

# Utilizzo
result = analyze_address("bc1qynqu36tgknqvm3m5cs4e5mulj42xcju5vn8mvl")
if result:
    print(json.dumps(result, indent=2))
```
