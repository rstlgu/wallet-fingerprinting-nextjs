# 🔍 Bitcoin Wallet Analyzer - Chrome Extension

Estensione Chrome per analizzare wallet Bitcoin direttamente da Chainalysis e altri block explorer.

## 🚀 Funzionalità

- **Analisi Real-time**: Clicca su qualsiasi TXID o indirizzo Bitcoin per analizzarlo
- **Integrazione Chainalysis**: Funziona direttamente sui grafici di Chainalysis
- **Supporto Multi-Sito**: Compatibile con Mempool.space, Blockstream, Blockchain.info
- **UI Moderna**: Interfaccia elegante con risultati dettagliati
- **Configurabile**: Impostazioni personalizzabili per profondità analisi

## 📦 Installazione

### 1. Preparazione Backend
```bash
# Avvia il backend API
cd backend-flask
source venv/bin/activate
python run.py
```

### 2. Installazione Estensione
1. Apri Chrome e vai su `chrome://extensions/`
2. Abilita "Modalità sviluppatore" in alto a destra
3. Clicca "Carica estensione non pacchettizzata"
4. Seleziona la cartella `chrome-extension`
5. L'estensione apparirà nella barra degli strumenti

## 🎯 Utilizzo

### Su Chainalysis
1. Vai su [Chainalysis](https://www.chainalysis.com/)
2. Clicca su qualsiasi transazione nel grafico
3. L'estensione mostrerà automaticamente l'analisi del wallet

### Su Altri Block Explorer
1. Vai su Mempool.space, Blockstream.info, o Blockchain.info
2. Clicca su TXID o indirizzi Bitcoin (evidenziati automaticamente)
3. Visualizza i risultati dell'analisi

### Configurazione
1. Clicca sull'icona dell'estensione
2. Configura l'URL dell'API backend
3. Imposta la profondità di analisi (1-5)
4. Abilita/disabilita funzionalità

## 🔧 Configurazione

### Impostazioni Disponibili
- **URL API Backend**: Indirizzo del server API (default: http://localhost:5000)
- **Profondità Analisi**: Livello di dettaglio (1=Veloce, 5=Massima)
- **Analisi Automatica**: Analizza automaticamente al click
- **Pattern Analysis**: Includi analisi dei pattern comportamentali
- **Notifiche**: Mostra notifiche di stato

### API Endpoints Utilizzati
- `POST /api/transaction/analyze` - Analisi transazioni
- `POST /api/address/analyze` - Analisi indirizzi
- `GET /api/health` - Test connessione

## 🎨 Interfaccia

### Popup Principale
- Status connessione API
- Configurazione rapida
- Test di connessione
- Test analisi con TXID

### Panel di Analisi
- Wallet rilevato con confidenza
- Livello di rischio
- Ragionamento dell'analisi
- Link al block explorer
- Distribuzione wallet (per indirizzi)

## 🔍 Rilevamento Wallet

L'estensione identifica automaticamente:
- **Electrum**: Wallet desktop popolare
- **Bitcoin Core**: Client ufficiale
- **Exodus**: Wallet multi-currency
- **Ledger/Trezor**: Hardware wallets
- **Exchange**: Wallet di scambio
- **Unknown**: Wallet non identificati

## 🛠️ Sviluppo

### Struttura File
```
chrome-extension/
├── manifest.json          # Configurazione estensione
├── background.js          # Service worker
├── content.js            # Script di iniezione
├── popup.html            # Interfaccia popup
├── popup.js              # Logica popup
├── styles.css            # Stili UI
├── icons/                # Icone estensione
└── README.md             # Documentazione
```

### Debug
1. Apri Chrome DevTools
2. Vai su `chrome://extensions/`
3. Clicca "Inspect views" per background o popup
4. Per content script, usa DevTools della pagina

### Test
1. Testa su siti supportati
2. Verifica connessione API
3. Controlla console per errori
4. Testa con TXID reali

## 🔒 Permessi

L'estensione richiede:
- **activeTab**: Accesso alla tab corrente
- **storage**: Salvataggio impostazioni
- **scripting**: Iniezione script
- **tabs**: Gestione tab
- **host_permissions**: Accesso a block explorer

## 🐛 Risoluzione Problemi

### Estensione Non Funziona
1. Verifica che il backend API sia avviato
2. Controlla l'URL API nelle impostazioni
3. Testa la connessione dal popup
4. Controlla la console per errori

### Analisi Non Disponibile
1. Verifica che il TXID sia valido
2. Controlla la connessione API
3. Prova con un TXID diverso
4. Verifica i log del backend

### UI Non Appare
1. Ricarica la pagina
2. Disabilita/riabilita l'estensione
3. Controlla che il sito sia supportato
4. Verifica i permessi dell'estensione

## 📝 Changelog

### v1.0.0
- Rilascio iniziale
- Supporto Chainalysis
- Analisi transazioni e indirizzi
- UI moderna e responsive
- Configurazione completa

## 🤝 Contributi

1. Fork del repository
2. Crea feature branch
3. Commit delle modifiche
4. Push al branch
5. Apri Pull Request

## 📄 Licenza

MIT License - Vedi file LICENSE per dettagli

## 🔗 Link Utili

- [Backend API Documentation](http://localhost:5000/api/docs/)
- [Chrome Extensions Developer Guide](https://developer.chrome.com/docs/extensions/)
- [Bitcoin Wallet Fingerprinting](https://github.com/your-repo/wallet-fingerprinting)
