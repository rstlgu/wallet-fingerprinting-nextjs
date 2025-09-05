// Content script per Bitcoin Wallet Analyzer Extension
// Si integra con Chainalysis e altri block explorer

console.log('Bitcoin Wallet Analyzer: Content script loaded');

// Configurazione
let isAnalyzing = false;
let currentAnalysis = null;
let settings = {};

// Inizializza l'estensione
async function init() {
  try {
    // Carica impostazioni
    settings = await getSettings();
    
    // Rileva il tipo di sito
    const siteType = detectSiteType();
    console.log('Detected site type:', siteType);
    
    // Inietta UI e listener
    injectUI();
    setupEventListeners();
    
    // Se è Chainalysis, cerca transazioni nel grafico
    if (siteType === 'chainalysis') {
      setupChainalysisIntegration();
    }
    
    console.log('Bitcoin Wallet Analyzer initialized successfully');
  } catch (error) {
    console.error('Error initializing extension:', error);
  }
}

// Rileva il tipo di sito
function detectSiteType() {
  const hostname = window.location.hostname;
  
  if (hostname.includes('chainalysis.com')) {
    return 'chainalysis';
  } else if (hostname.includes('mempool.space')) {
    return 'mempool';
  } else if (hostname.includes('blockstream.info')) {
    return 'blockstream';
  } else if (hostname.includes('blockchain.info')) {
    return 'blockchain';
  }
  
  return 'unknown';
}

// Inietta l'UI dell'analizzatore
function injectUI() {
  // Crea il container principale
  const analyzerContainer = document.createElement('div');
  analyzerContainer.id = 'btc-wallet-analyzer';
  analyzerContainer.innerHTML = `
    <div class="btc-analyzer-panel">
      <div class="btc-analyzer-header">
        <h3>🔍 Bitcoin Wallet Analyzer</h3>
        <button id="btc-analyzer-close" class="btc-close-btn">×</button>
      </div>
      <div class="btc-analyzer-content">
        <div id="btc-analyzer-loading" class="btc-loading" style="display: none;">
          <div class="btc-spinner"></div>
          <p>Analizzando transazione...</p>
        </div>
        <div id="btc-analyzer-results" class="btc-results" style="display: none;">
          <!-- Risultati dell'analisi -->
        </div>
        <div id="btc-analyzer-error" class="btc-error" style="display: none;">
          <!-- Messaggi di errore -->
        </div>
      </div>
    </div>
  `;
  
  // Aggiungi al body
  document.body.appendChild(analyzerContainer);
  
  // Setup eventi UI
  setupUIEvents();
}

// Setup eventi per l'UI
function setupUIEvents() {
  const closeBtn = document.getElementById('btc-analyzer-close');
  const panel = document.querySelector('.btc-analyzer-panel');
  
  closeBtn?.addEventListener('click', () => {
    panel.style.display = 'none';
  });
  
  // Click fuori per chiudere
  document.addEventListener('click', (e) => {
    if (!panel.contains(e.target) && !e.target.closest('[data-btc-txid]')) {
      panel.style.display = 'none';
    }
  });
}

// Setup listener per eventi
function setupEventListeners() {
  // Listener per click su elementi con txid
  document.addEventListener('click', async (e) => {
    const txid = e.target.closest('[data-btc-txid]')?.dataset.btcTxid;
    const address = e.target.closest('[data-btc-address]')?.dataset.btcAddress;
    
    if (txid && !isAnalyzing) {
      e.preventDefault();
      e.stopPropagation();
      await analyzeTransaction(txid);
    } else if (address && !isAnalyzing) {
      e.preventDefault();
      e.stopPropagation();
      await analyzeAddress(address);
    }
  });
  
  // Listener per hover per preview
  document.addEventListener('mouseover', (e) => {
    const txid = e.target.closest('[data-btc-txid]')?.dataset.btcTxid;
    if (txid) {
      showPreview(e.target, txid);
    }
  });
  
  document.addEventListener('mouseout', (e) => {
    const txid = e.target.closest('[data-btc-txid]')?.dataset.btcTxid;
    if (txid) {
      hidePreview();
    }
  });
}

// Setup integrazione specifica per Chainalysis
function setupChainalysisIntegration() {
  // Observer per cambiamenti nel DOM
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList') {
        // Cerca nuovi elementi di transazione
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            enhanceTransactionElements(node);
          }
        });
      }
    });
  });
  
  // Inizia osservazione
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  // Migliora elementi esistenti
  enhanceTransactionElements(document.body);
}

// Migliora elementi di transazione esistenti
function enhanceTransactionElements(container) {
  // Cerca pattern comuni di txid Bitcoin
  const txidPattern = /\b[a-fA-F0-9]{64}\b/g;
  const addressPattern = /\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|\bbc1[a-z0-9]{39,59}\b/g;
  
  // Funzione per processare un elemento di testo
  function processTextNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent;
      let hasMatches = false;
      let newHTML = text;
      
      // Sostituisci txid
      newHTML = newHTML.replace(txidPattern, (match) => {
        hasMatches = true;
        return `<span class="btc-txid" data-btc-txid="${match}" title="Clicca per analizzare">${match}</span>`;
      });
      
      // Sostituisci indirizzi
      newHTML = newHTML.replace(addressPattern, (match) => {
        hasMatches = true;
        return `<span class="btc-address" data-btc-address="${match}" title="Clicca per analizzare">${match}</span>`;
      });
      
      if (hasMatches) {
        const wrapper = document.createElement('span');
        wrapper.innerHTML = newHTML;
        node.parentNode.replaceChild(wrapper, node);
      }
    }
  }
  
  // Processa tutti i nodi di testo
  const walker = document.createTreeWalker(
    container,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );
  
  const textNodes = [];
  let node;
  while (node = walker.nextNode()) {
    textNodes.push(node);
  }
  
  textNodes.forEach(processTextNode);
}

// Analizza una transazione
async function analyzeTransaction(txid) {
  if (isAnalyzing) return;
  
  isAnalyzing = true;
  showLoading();
  
  try {
    const result = await sendMessage({
      action: 'analyzeTransaction',
      txid: txid,
      options: {
        depth: settings.analysisDepth || 3,
        includePatterns: settings.includePatterns !== false,
        realtimeUpdates: false
      }
    });
    
    if (result.success) {
      showResults(result.data, 'transaction');
    } else {
      showError(result.error);
    }
  } catch (error) {
    console.error('Error analyzing transaction:', error);
    showError('Errore durante l\'analisi: ' + error.message);
  } finally {
    isAnalyzing = false;
  }
}

// Analizza un indirizzo
async function analyzeAddress(address) {
  if (isAnalyzing) return;
  
  isAnalyzing = true;
  showLoading();
  
  try {
    const result = await sendMessage({
      action: 'analyzeAddress',
      address: address,
      options: {
        limit: 20,
        depth: settings.analysisDepth || 3
      }
    });
    
    if (result.success) {
      showResults(result.data, 'address');
    } else {
      showError(result.error);
    }
  } catch (error) {
    console.error('Error analyzing address:', error);
    showError('Errore durante l\'analisi: ' + error.message);
  } finally {
    isAnalyzing = false;
  }
}

// Mostra loading
function showLoading() {
  const loading = document.getElementById('btc-analyzer-loading');
  const results = document.getElementById('btc-analyzer-results');
  const error = document.getElementById('btc-analyzer-error');
  const panel = document.querySelector('.btc-analyzer-panel');
  
  loading.style.display = 'block';
  results.style.display = 'none';
  error.style.display = 'none';
  panel.style.display = 'block';
}

// Mostra risultati
function showResults(data, type) {
  const loading = document.getElementById('btc-analyzer-loading');
  const results = document.getElementById('btc-analyzer-results');
  const error = document.getElementById('btc-analyzer-error');
  const panel = document.querySelector('.btc-analyzer-panel');
  
  loading.style.display = 'none';
  error.style.display = 'none';
  results.style.display = 'block';
  panel.style.display = 'block';
  
  // Genera HTML per i risultati
  results.innerHTML = generateResultsHTML(data, type);
}

// Mostra errore
function showError(message) {
  const loading = document.getElementById('btc-analyzer-loading');
  const results = document.getElementById('btc-analyzer-results');
  const error = document.getElementById('btc-analyzer-error');
  const panel = document.querySelector('.btc-analyzer-panel');
  
  loading.style.display = 'none';
  results.style.display = 'none';
  error.style.display = 'block';
  panel.style.display = 'block';
  
  error.innerHTML = `
    <div class="btc-error-content">
      <h4>❌ Errore</h4>
      <p>${message}</p>
    </div>
  `;
}

// Genera HTML per i risultati
function generateResultsHTML(data, type) {
  if (type === 'transaction') {
    return `
      <div class="btc-result-content">
        <h4>📊 Analisi Transazione</h4>
        <div class="btc-info-grid">
          <div class="btc-info-item">
            <label>Wallet Rilevato:</label>
            <span class="btc-wallet ${getWalletClass(data.fingerprint?.wallet)}">
              ${data.fingerprint?.wallet || 'Sconosciuto'}
            </span>
          </div>
          <div class="btc-info-item">
            <label>Confidenza:</label>
            <span class="btc-confidence">
              ${Math.round((data.fingerprint?.confidence || 0) * 100)}%
            </span>
          </div>
          <div class="btc-info-item">
            <label>Livello Rischio:</label>
            <span class="btc-risk ${data.fingerprint?.risk_level || 'unknown'}">
              ${getRiskLabel(data.fingerprint?.risk_level)}
            </span>
          </div>
        </div>
        ${data.fingerprint?.reasoning ? `
          <div class="btc-reasoning">
            <h5>🔍 Ragionamento:</h5>
            <ul>
              ${data.fingerprint.reasoning.map(r => `<li>${r}</li>`).join('')}
            </ul>
          </div>
        ` : ''}
        <div class="btc-actions">
          <button onclick="window.open('${data.metadata?.block_explorer}', '_blank')" class="btc-btn">
            🔗 Visualizza su Block Explorer
          </button>
        </div>
      </div>
    `;
  } else if (type === 'address') {
    return `
      <div class="btc-result-content">
        <h4>👤 Analisi Indirizzo</h4>
        <div class="btc-info-grid">
          <div class="btc-info-item">
            <label>Wallet Principale:</label>
            <span class="btc-wallet ${getWalletClass(data.fingerprint?.main_wallet)}">
              ${data.fingerprint?.main_wallet || 'Sconosciuto'}
            </span>
          </div>
          <div class="btc-info-item">
            <label>Transazioni Analizzate:</label>
            <span>${data.address_info?.analyzed_transactions || 0}</span>
          </div>
          <div class="btc-info-item">
            <label>Pattern:</label>
            <span>${data.fingerprint?.pattern_type || 'Sconosciuto'}</span>
          </div>
        </div>
        ${data.fingerprint?.wallet_percentages ? `
          <div class="btc-wallet-distribution">
            <h5>📈 Distribuzione Wallet:</h5>
            <div class="btc-distribution-chart">
              ${Object.entries(data.fingerprint.wallet_percentages).map(([wallet, pct]) => `
                <div class="btc-distribution-item">
                  <span class="btc-wallet-name">${wallet}</span>
                  <div class="btc-progress-bar">
                    <div class="btc-progress-fill" style="width: ${pct}%"></div>
                  </div>
                  <span class="btc-percentage">${pct.toFixed(1)}%</span>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
        <div class="btc-actions">
          <button onclick="window.open('${data.metadata?.block_explorer}', '_blank')" class="btc-btn">
            🔗 Visualizza su Block Explorer
          </button>
        </div>
      </div>
    `;
  }
  
  return '<p>Risultati non disponibili</p>';
}

// Utility functions
function getWalletClass(wallet) {
  if (!wallet) return 'unknown';
  return wallet.toLowerCase().replace(/\s+/g, '-');
}

function getRiskLabel(risk) {
  const labels = {
    'low': '🟢 Basso',
    'medium': '🟡 Medio', 
    'high': '🔴 Alto'
  };
  return labels[risk] || '❓ Sconosciuto';
}

function showPreview(element, txid) {
  // Implementa preview al hover
}

function hidePreview() {
  // Nasconde preview
}

// Invia messaggio al background script
function sendMessage(message) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(message, (response) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve(response);
      }
    });
  });
}

// Ottieni impostazioni
function getSettings() {
  return new Promise((resolve) => {
    chrome.storage.sync.get({
      apiUrl: 'http://localhost:5000',
      autoAnalyze: true,
      showNotifications: true,
      analysisDepth: 3,
      includePatterns: true,
      theme: 'dark'
    }, resolve);
  });
}

// Inizializza quando il DOM è pronto
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
