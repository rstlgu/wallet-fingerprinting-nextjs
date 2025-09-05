# Wallet Fingerprinting Project

Un progetto completo per l'analisi e il fingerprinting di wallet Bitcoin, composto da:

## 🏗️ Struttura del Progetto

### Frontend (Next.js 15)
- **Path**: `nextjs-15-starter-shadcn/`
- **Tech Stack**: Next.js 15, React, TypeScript, Tailwind CSS, Shadcn UI
- **Features**:
  - Interfaccia moderna e responsive per l'analisi dei wallet
  - Componenti UI personalizzati con Shadcn/UI
  - Integrazione con API backend tramite Server-Sent Events (SSE)
  - Analisi in tempo reale delle transazioni Bitcoin

### Backend API (Python)
- **Path**: `wallet-fingerprinting-api/`
- **Tech Stack**: Python, Flask, Bitcoin Core RPC
- **Features**:
  - API RESTful per l'analisi di indirizzi e transazioni Bitcoin
  - Integrazione con Bitcoin Core e Mempool.space
  - Server-Sent Events per aggiornamenti in tempo reale
  - Algoritmi avanzati di fingerprinting

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- Bitcoin Core (opzionale, per RPC diretto)

### Frontend Setup
```bash
cd nextjs-15-starter-shadcn
npm install
npm run dev
```

### Backend Setup
```bash
cd wallet-fingerprinting-api
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python run.py
```

## 📚 Documentation

- [Frontend Integration Guide](wallet-fingerprinting-api/frontend-integration.md)
- [API Documentation](wallet-fingerprinting-api/README.md)
- [Wallet Analysis README](nextjs-15-starter-shadcn/README-WALLET-ANALYSIS.md)

## 🛠️ Development

Il progetto utilizza:
- **Frontend**: Next.js App Router, TypeScript, Tailwind CSS
- **Backend**: Flask, Bitcoin Core RPC, Mempool.space API
- **Real-time**: Server-Sent Events (SSE)
- **UI**: Shadcn UI components

## 📄 License

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE.md` per maggiori dettagli.
