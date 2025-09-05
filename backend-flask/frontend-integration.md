# 🔗 Integrazione Frontend Next.js

Esempi di integrazione dell'API Wallet Fingerprinting con Next.js.

## 📦 Installazione Dipendenze

```bash
npm install axios
# oppure
yarn add axios
```

## 🚀 Esempi di Utilizzo

### 1. Analisi Transazione

```typescript
// pages/api/analyze-tx.ts
import axios from 'axios';

const API_BASE = process.env.WALLET_API_URL || 'http://localhost:5000';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { txid } = req.body;
    
    const response = await axios.post(`${API_BASE}/api/analyze/tx`, {
      txid
    });

    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ 
      error: 'Errore durante l\'analisi',
      details: error.message 
    });
  }
}
```

### 2. Hook React per Analisi

```typescript
// hooks/useWalletAnalysis.ts
import { useState, useCallback } from 'react';
import axios from 'axios';

interface WalletDetection {
  wallet: string;
  confidence: number;
  reasoning: string[];
  is_clear: boolean;
}

interface TransactionAnalysis {
  transaction: {
    txid: string;
    version: number;
    locktime: number;
    inputs_count: number;
    outputs_count: number;
    input_types: string[];
    output_types: string[];
  };
  detection: WalletDetection;
  analysis_time: number;
  block_explorer: string;
}

export const useWalletAnalysis = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeTransaction = useCallback(async (txid: string): Promise<TransactionAnalysis | null> => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/analyze-tx', { txid });
      return response.data.data;
    } catch (err) {
      setError(err.response?.data?.message || 'Errore durante l\'analisi');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const analyzeAddress = useCallback(async (address: string, limit = 20) => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/analyze-address', { 
        address, 
        limit 
      });
      return response.data.data;
    } catch (err) {
      setError(err.response?.data?.message || 'Errore durante l\'analisi');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    analyzeTransaction,
    analyzeAddress,
    loading,
    error
  };
};
```

### 3. Componente React per Analisi

```tsx
// components/WalletAnalyzer.tsx
import React, { useState } from 'react';
import { useWalletAnalysis } from '../hooks/useWalletAnalysis';

const WalletAnalyzer: React.FC = () => {
  const [txid, setTxid] = useState('');
  const [result, setResult] = useState(null);
  const { analyzeTransaction, loading, error } = useWalletAnalysis();

  const handleAnalyze = async () => {
    if (!txid.trim()) return;
    
    const analysis = await analyzeTransaction(txid);
    if (analysis) {
      setResult(analysis);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Wallet Fingerprinting</h1>
      
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Transaction ID
        </label>
        <div className="flex gap-2">
          <input
            type="text"
            value={txid}
            onChange={(e) => setTxid(e.target.value)}
            placeholder="Inserisci TXID Bitcoin..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleAnalyze}
            disabled={loading || !txid.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50"
          >
            {loading ? 'Analizzando...' : 'Analizza'}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Risultati Analisi</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium text-gray-700 mb-2">Wallet Rilevato</h3>
              <div className="text-2xl font-bold text-blue-600">
                {result.detection.wallet}
              </div>
              <div className="text-sm text-gray-500">
                Confidenza: {result.detection.confidence}%
              </div>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-700 mb-2">Informazioni Transazione</h3>
              <div className="text-sm space-y-1">
                <div>Version: {result.transaction.version}</div>
                <div>Inputs: {result.transaction.inputs_count}</div>
                <div>Outputs: {result.transaction.outputs_count}</div>
                <div>Locktime: {result.transaction.locktime}</div>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <h3 className="font-medium text-gray-700 mb-2">Analisi Dettagliata</h3>
            <ul className="text-sm space-y-1">
              {result.detection.reasoning.map((reason, index) => (
                <li key={index} className="flex items-center">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                  {reason}
                </li>
              ))}
            </ul>
          </div>

          <div className="mt-4">
            <a
              href={result.block_explorer}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:text-blue-700 text-sm"
            >
              Visualizza su Block Explorer →
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default WalletAnalyzer;
```

### 4. API Routes per Next.js

```typescript
// pages/api/analyze-address.ts
import axios from 'axios';

const API_BASE = process.env.WALLET_API_URL || 'http://localhost:5000';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { address, limit } = req.body;
    
    const response = await axios.post(`${API_BASE}/api/analyze/address`, {
      address,
      limit: limit || 20
    });

    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ 
      error: 'Errore durante l\'analisi indirizzo',
      details: error.message 
    });
  }
}
```

### 5. Variabili d'Ambiente

```bash
# .env.local
WALLET_API_URL=http://localhost:5000
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### 6. Configurazione CORS

L'API è già configurata per accettare richieste da:
- `http://localhost:3000` (Next.js dev server)
- `http://127.0.0.1:3000`
- `https://yourdomain.com` (produzione)

### 7. Esempio di Utilizzo Completo

```tsx
// pages/index.tsx
import { useState } from 'react';
import WalletAnalyzer from '../components/WalletAnalyzer';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <WalletAnalyzer />
    </div>
  );
}
```

## 🚀 Deploy

### Backend (API)
```bash
# Produzione con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Docker
docker build -t wallet-fingerprinting-api .
docker run -p 5000:5000 wallet-fingerprinting-api
```

### Frontend (Next.js)
```bash
# Build
npm run build

# Start
npm start

# Docker
docker build -t wallet-fingerprinting-frontend .
docker run -p 3000:3000 wallet-fingerprinting-frontend
```

## 📊 Esempi di Risposta API

### Analisi Transazione
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
      "reasoning": [
        "No Anti-fee-sniping",
        "All compressed public keys",
        "nVersion = 2",
        "Low r signatures only",
        "signals RBF"
      ],
      "is_clear": true
    },
    "analysis_time": 0.682,
    "block_explorer": "https://mempool.space/tx/..."
  },
  "timestamp": "2024-09-04T16:58:00.000Z"
}
```

---

**Integrazione completa tra Backend Flask e Frontend Next.js!** 🎉
