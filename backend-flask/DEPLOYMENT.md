# 🚀 Guida al Deployment - Wallet Fingerprinting API

## 📁 Struttura del Progetto

```
backend-flask/
├── app.py                 # Entry point per Vercel
├── run.py                 # Script di avvio per sviluppo locale
├── src/
│   └── app.py            # Applicazione Flask principale
├── vercel.json           # Configurazione Vercel
├── requirements.txt      # Dipendenze Python
├── config.env           # Variabili d'ambiente (locale)
└── env.example          # Template variabili d'ambiente
```

## 🏠 Sviluppo Locale

### Opzione 1: Usando run.py (raccomandato)
```bash
cd backend-flask
source venv/bin/activate
python run.py
```

### Opzione 2: Usando app.py direttamente
```bash
cd backend-flask
source venv/bin/activate
python app.py
```

## ☁️ Deployment su Vercel

### 1. Preparazione
```bash
# Copia le variabili d'ambiente
cp env.example .env

# Modifica .env con i tuoi valori
nano .env
```

### 2. Configurazione Vercel

**Opzione A: Via CLI (Raccomandato)**
```bash
# Installa Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Segui le istruzioni:
# - Framework: Other
# - Root Directory: ./
# - Build Command: (lascia vuoto)
# - Output Directory: (lascia vuoto)
```

**Opzione B: Via Dashboard Vercel**
1. Vai su [vercel.com](https://vercel.com)
2. Clicca "New Project"
3. Connetti il tuo repository GitHub
4. Framework: **Other**
5. Root Directory: `./`
6. Build Command: (lascia vuoto)
7. Output Directory: (lascia vuoto)

### 3. Variabili d'Ambiente su Vercel
Nel dashboard Vercel, vai in Settings > Environment Variables e aggiungi:
- `API_KEY`: La tua API key
- `SECRET_KEY`: Chiave segreta per Flask
- `FLASK_ENV`: `production`
- `CORS_ORIGINS`: URL del tuo frontend

### 4. Test del Deployment
```bash
# Test locale
curl http://localhost:5000/api/status

# Test Vercel
curl https://your-app.vercel.app/api/status
```

## 🔧 Configurazione

### Variabili d'Ambiente Richieste
- `API_KEY`: Chiave API per autenticazione
- `SECRET_KEY`: Chiave segreta Flask
- `FLASK_ENV`: `development` o `production`
- `CORS_ORIGINS`: Origini CORS consentite

### Endpoint Disponibili
- `GET /api/status` - Stato API (pubblico)
- `GET /api/docs` - Documentazione (pubblico)
- `POST /api/analyze/tx` - Analizza transazione (protetto)
- `POST /api/analyze/address` - Analizza indirizzo (protetto)
- `POST /api/analyze/block` - Analizza blocco (protetto)

## 🔐 Autenticazione

Tutti gli endpoint protetti richiedono API key:

```bash
# Header X-API-Key
curl -H "X-API-Key: your-api-key" https://your-app.vercel.app/api/analyze/tx

# Header Authorization
curl -H "Authorization: Bearer your-api-key" https://your-app.vercel.app/api/analyze/tx
```

## 📝 Note

- Vercel usa `app.py` come entry point
- Le variabili d'ambiente vanno configurate nel dashboard Vercel
- Per sviluppo locale, usa `run.py` che carica `config.env`
- Il progetto è ottimizzato per serverless (Vercel)
