# 🪙 Bitcoin Wallet Fingerprinting Frontend

Frontend Next.js moderno per l'analisi delle transazioni Bitcoin e identificazione dei wallet.

## 🚀 Funzionalità

- **Analisi Transazioni**: Inserisci un TXID per identificare il wallet utilizzato
- **Analisi Indirizzi**: Analizza un indirizzo Bitcoin per determinare il wallet più probabile
- **UI Moderna**: Interfaccia responsiva costruita con Shadcn UI e Tailwind CSS
- **Risultati Dettagliati**: Visualizzazione completa dell'analisi con livelli di confidenza

## 📦 Installazione

```bash
# Installa le dipendenze
npm install

# Configura le variabili d'ambiente
cp .env.local.example .env.local
# Modifica WALLET_API_URL se necessario (default: http://localhost:5000)

# Avvia il server di sviluppo
npm run dev
```

## 🔧 Configurazione

Il frontend si collega automaticamente all'API wallet fingerprinting. Assicurati che:

1. L'API backend sia in esecuzione su `http://localhost:5000`
2. Le variabili d'ambiente siano configurate correttamente in `.env.local`

## 📱 Utilizzo

1. **Analisi Transazione**:
   - Inserisci un TXID Bitcoin (64 caratteri esadecimali)
   - Clicca "Analizza"
   - Visualizza i risultati con wallet identificato, confidenza e dettagli tecnici

2. **Analisi Indirizzo**:
   - Inserisci un indirizzo Bitcoin (qualsiasi formato valido)
   - Il sistema analizzerà automaticamente le transazioni dell'indirizzo
   - Visualizza statistiche aggregate e wallet più probabile

## 🎨 Componenti

- **WalletAnalyzer**: Componente principale per l'inserimento e visualizzazione
- **useWalletAnalysis**: Hook React per le chiamate API
- **API Routes**: Endpoint Next.js per proxy alle API backend

## 🔗 Integrazione API

Il frontend comunica con l'API backend tramite:

- `POST /api/analyze-tx` - Analisi transazioni
- `POST /api/analyze-address` - Analisi indirizzi

## 🛠 Tecnologie

- **Next.js 15** con App Router
- **TypeScript** per type safety
- **Shadcn UI** per i componenti
- **Tailwind CSS** per lo styling
- **Lucide React** per le icone
- **Axios** per le chiamate HTTP

## 📊 Esempio di Utilizzo

```typescript
// Hook per analisi
const { analyzeTransaction, loading, error } = useWalletAnalysis();

// Analizza una transazione
const result = await analyzeTransaction('7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166');

// Risultato contiene:
// - detection.wallet: "Blue Wallet"
// - detection.confidence: 95.0
// - detection.reasoning: ["No Anti-fee-sniping", ...]
// - transaction: { txid, version, inputs_count, ... }
```

## 🚀 Deploy

```bash
# Build per produzione
npm run build

# Start produzione
npm start

# Docker (opzionale)
docker build -t wallet-frontend .
docker run -p 3000:3000 wallet-frontend
```

---

**Frontend completo per Bitcoin Wallet Fingerprinting! 🎉**
