# 📦 Guida Installazione - Bitcoin Wallet Analyzer

## 🚀 Installazione Rapida

### 1. Avvia il Backend API
```bash
# Vai nella directory del backend
cd /home/microsot/projects/fingerprint/backend-flask

# Attiva l'ambiente virtuale
source venv/bin/activate

# Avvia il server
python run.py
```

Verifica che il server sia attivo visitando: http://localhost:5000/health

### 2. Installa l'Estensione Chrome

#### Metodo A: Caricamento Manuale (Raccomandato)
1. Apri Google Chrome
2. Vai su `chrome://extensions/`
3. Abilita "Modalità sviluppatore" (toggle in alto a destra)
4. Clicca "Carica estensione non pacchettizzata"
5. Seleziona la cartella: `/home/microsot/projects/fingerprint/chrome-extension`
6. L'estensione apparirà nella lista con icona 🔍

#### Metodo B: Drag & Drop
1. Apri `chrome://extensions/`
2. Abilita "Modalità sviluppatore"
3. Trascina la cartella `chrome-extension` nella pagina
4. L'estensione verrà caricata automaticamente

### 3. Configura l'Estensione
1. Clicca sull'icona 🔍 nella barra degli strumenti
2. Verifica che l'URL API sia: `http://localhost:5000`
3. Clicca "Testa Connessione"
4. Se tutto OK, vedrai "✅ Connesso all'API"

## 🧪 Test dell'Estensione

### Test Base
1. Vai su [Mempool.space](https://mempool.space/)
2. Cerca una transazione Bitcoin
3. Clicca su un TXID (dovrebbe essere evidenziato)
4. Dovrebbe apparire il panel di analisi

### Test su Chainalysis
1. Vai su [Chainalysis](https://www.chainalysis.com/)
2. Naviga nei grafici delle transazioni
3. Clicca su qualsiasi transazione
4. L'estensione dovrebbe analizzare automaticamente

### Test con TXID Specifico
1. Clicca sull'icona dell'estensione
2. Inserisci un TXID valido nel campo "Testa con TXID"
3. Clicca "Analizza Transazione"
4. Dovrebbe aprire una nuova tab con i risultati

## 🔧 Risoluzione Problemi

### ❌ "Disconnesso dall'API"
**Causa**: Backend non avviato o URL errato
**Soluzione**:
```bash
# Verifica che il backend sia attivo
curl http://localhost:5000/health

# Se non risponde, avvia il backend
cd backend-flask
source venv/bin/activate
python run.py
```

### ❌ "Errore durante l'analisi"
**Causa**: TXID non valido o API non disponibile
**Soluzione**:
1. Verifica che il TXID sia valido (64 caratteri hex)
2. Controlla la connessione API
3. Prova con un TXID diverso

### ❌ Estensione non appare
**Causa**: Estensione non caricata correttamente
**Soluzione**:
1. Vai su `chrome://extensions/`
2. Verifica che l'estensione sia abilitata
3. Ricarica l'estensione (icona refresh)
4. Ricarica la pagina web

### ❌ TXID non evidenziati
**Causa**: Content script non iniettato
**Soluzione**:
1. Ricarica la pagina
2. Verifica che il sito sia supportato
3. Controlla la console per errori (F12)

## 🎯 Siti Supportati

- ✅ **Chainalysis.com** - Analisi grafici transazioni
- ✅ **Mempool.space** - Block explorer Bitcoin
- ✅ **Blockstream.info** - Block explorer Bitcoin
- ✅ **Blockchain.info** - Block explorer Bitcoin

## ⚙️ Configurazione Avanzata

### Profondità Analisi
- **1**: Veloce (solo pattern base)
- **2**: Standard (pattern + clustering)
- **3**: Completa (pattern + clustering + behavioral)
- **4**: Approfondita (+ analisi temporale)
- **5**: Massima (+ analisi avanzate)

### Impostazioni Consigliate
- **API URL**: `http://localhost:5000`
- **Profondità**: 3 (bilanciata)
- **Analisi Automatica**: ✅ Abilitata
- **Pattern Analysis**: ✅ Abilitata
- **Notifiche**: ✅ Abilitate

## 🔍 Debug e Log

### Console Browser
1. Apri DevTools (F12)
2. Vai su Console
3. Cerca messaggi con prefisso "Bitcoin Wallet Analyzer"

### Console Estensione
1. Vai su `chrome://extensions/`
2. Clicca "Inspect views" per background script
3. Controlla la console per errori

### Log Backend
```bash
# Visualizza log del backend
tail -f backend-flask/api.log
```

## 📱 Utilizzo Mobile

L'estensione funziona solo su Chrome Desktop. Per mobile:
1. Usa il backend API direttamente
2. Integra l'API in app mobile
3. Usa la documentazione API: http://localhost:5000/api/docs/

## 🔄 Aggiornamenti

### Aggiornare l'Estensione
1. Sostituisci i file nella cartella `chrome-extension`
2. Vai su `chrome://extensions/`
3. Clicca "Ricarica" sull'estensione

### Aggiornare il Backend
```bash
cd backend-flask
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

## 🆘 Supporto

Se hai problemi:
1. Controlla questa guida
2. Verifica i log di debug
3. Controlla la documentazione API
4. Apri un issue su GitHub

## ✅ Checklist Installazione

- [ ] Backend API avviato su porta 5000
- [ ] Estensione caricata in Chrome
- [ ] Connessione API testata e funzionante
- [ ] Test su Mempool.space completato
- [ ] Test su Chainalysis completato
- [ ] Configurazione personalizzata salvata

🎉 **Installazione completata!** L'estensione è pronta per l'uso.
