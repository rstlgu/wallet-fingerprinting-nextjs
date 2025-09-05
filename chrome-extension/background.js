// Background script per Bitcoin Wallet Analyzer Extension

// Configurazione API
const API_BASE_URL = 'http://localhost:5000/api';
const API_KEY = 'dev-api-key-12345'; // Sostituisci con la tua API KEY

// Listener per messaggi dal content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Background received message:', request);
  
  switch (request.action) {
    case 'analyzeTransaction':
      analyzeTransaction(request.txid, request.options)
        .then(result => sendResponse({ success: true, data: result }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true; // Mantieni il canale aperto per risposta asincrona
      
    case 'analyzeAddress':
      analyzeAddress(request.address, request.options)
        .then(result => sendResponse({ success: true, data: result }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;
      
    case 'getSettings':
      getSettings()
        .then(settings => sendResponse({ success: true, data: settings }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;
      
    case 'saveSettings':
      saveSettings(request.settings)
        .then(() => sendResponse({ success: true }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;
      
    default:
      sendResponse({ success: false, error: 'Unknown action' });
  }
});

// Funzione per analizzare una transazione
async function analyzeTransaction(txid, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze/tx`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
      mode: 'cors',
      body: JSON.stringify({
        txid: txid,
        depth: options.depth || 3,
        include_patterns: options.includePatterns !== false,
        realtime_updates: options.realtimeUpdates || false
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.message || 'Unknown error');
    }
    
    return data.data;
  } catch (error) {
    console.error('Error analyzing transaction:', error);
    throw error;
  }
}

// Funzione per analizzare un indirizzo
async function analyzeAddress(address, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze/address`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
      mode: 'cors',
      body: JSON.stringify({
        address: address,
        limit: options.limit || 20,
        depth: options.depth || 3
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.message || 'Unknown error');
    }
    
    return data.data;
  } catch (error) {
    console.error('Error analyzing address:', error);
    throw error;
  }
}

// Funzione per ottenere le impostazioni
async function getSettings() {
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

// Funzione per salvare le impostazioni
async function saveSettings(settings) {
  return new Promise((resolve, reject) => {
    chrome.storage.sync.set(settings, () => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve();
      }
    });
  });
}

// Funzione per testare la connessione API
async function testAPIConnection() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors'
    });
    
    if (!response.ok) {
      console.error(`HTTP error! status: ${response.status}`);
      return false;
    }
    
    const data = await response.json();
    return data.status === 'healthy';
  } catch (error) {
    console.error('API connection test failed:', error);
    return false;
  }
}

// Listener per installazione/aggiornamento
chrome.runtime.onInstalled.addListener((details) => {
  console.log('Bitcoin Wallet Analyzer installed/updated:', details);
  
  // Imposta valori di default
  chrome.storage.sync.set({
    apiUrl: 'http://localhost:5000',
    autoAnalyze: true,
    showNotifications: true,
    analysisDepth: 3,
    includePatterns: true,
    theme: 'dark'
  });
  
  // Testa la connessione API
  testAPIConnection().then(isConnected => {
    if (!isConnected) {
      console.warn('API not available. Please start the backend server.');
    }
  });
});

// Listener per aggiornamenti tab
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    // Verifica se la tab è su un sito supportato
    const supportedSites = [
      'chainalysis.com',
      'mempool.space',
      'blockstream.info',
      'blockchain.info'
    ];
    
    const isSupported = supportedSites.some(site => tab.url.includes(site));
    
    if (isSupported) {
      // Aggiorna l'icona dell'estensione
      chrome.action.setIcon({
        tabId: tabId,
        path: {
          16: "icons/icon16-active.png",
          32: "icons/icon32-active.png",
          48: "icons/icon48-active.png",
          128: "icons/icon128-active.png"
        }
      });
    } else {
      // Ripristina icona normale
      chrome.action.setIcon({
        tabId: tabId,
        path: {
          16: "icons/icon16.png",
          32: "icons/icon32.png",
          48: "icons/icon48.png",
          128: "icons/icon128.png"
        }
      });
    }
  }
});
