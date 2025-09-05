// Popup script per Bitcoin Wallet Analyzer Extension

document.addEventListener('DOMContentLoaded', async () => {
  // Elementi DOM
  const status = document.getElementById('status');
  const statusIcon = document.getElementById('status-icon');
  const statusText = document.getElementById('status-text');
  const apiUrlInput = document.getElementById('apiUrl');
  const analysisDepthSelect = document.getElementById('analysisDepth');
  const autoAnalyzeCheckbox = document.getElementById('autoAnalyze');
  const includePatternsCheckbox = document.getElementById('includePatterns');
  const showNotificationsCheckbox = document.getElementById('showNotifications');
  const testConnectionBtn = document.getElementById('testConnection');
  const testText = document.getElementById('testText');
  const testSpinner = document.getElementById('testSpinner');
  const saveSettingsBtn = document.getElementById('saveSettings');
  const testTxidInput = document.getElementById('testTxid');
  const testAnalysisBtn = document.getElementById('testAnalysis');
  const openDocsLink = document.getElementById('openDocs');
  const openSettingsLink = document.getElementById('openSettings');
  
  // Carica impostazioni
  await loadSettings();
  
  // Testa connessione iniziale
  await testConnection();
  
  // Event listeners
  testConnectionBtn.addEventListener('click', testConnection);
  saveSettingsBtn.addEventListener('click', saveSettings);
  testAnalysisBtn.addEventListener('click', testAnalysis);
  openDocsLink.addEventListener('click', openDocumentation);
  openSettingsLink.addEventListener('click', openAdvancedSettings);
  
  // Auto-save su cambio impostazioni
  [apiUrlInput, analysisDepthSelect, autoAnalyzeCheckbox, includePatternsCheckbox, showNotificationsCheckbox]
    .forEach(element => {
      element.addEventListener('change', saveSettings);
    });
  
  // Carica impostazioni salvate
  async function loadSettings() {
    try {
      const settings = await chrome.storage.sync.get({
        apiUrl: 'http://localhost:5000',
        autoAnalyze: true,
        showNotifications: true,
        analysisDepth: 3,
        includePatterns: true,
        theme: 'dark'
      });
      
      apiUrlInput.value = settings.apiUrl;
      analysisDepthSelect.value = settings.analysisDepth;
      autoAnalyzeCheckbox.checked = settings.autoAnalyze;
      includePatternsCheckbox.checked = settings.includePatterns;
      showNotificationsCheckbox.checked = settings.showNotifications;
      
      console.log('Settings loaded:', settings);
    } catch (error) {
      console.error('Error loading settings:', error);
      showNotification('Errore nel caricamento delle impostazioni', 'error');
    }
  }
  
  // Salva impostazioni
  async function saveSettings() {
    try {
      const settings = {
        apiUrl: apiUrlInput.value.trim(),
        analysisDepth: parseInt(analysisDepthSelect.value),
        autoAnalyze: autoAnalyzeCheckbox.checked,
        includePatterns: includePatternsCheckbox.checked,
        showNotifications: showNotificationsCheckbox.checked
      };
      
      await chrome.storage.sync.set(settings);
      console.log('Settings saved:', settings);
      
      showNotification('Impostazioni salvate', 'success');
      
      // Testa connessione se URL è cambiato
      if (settings.apiUrl !== 'http://localhost:5000') {
        await testConnection();
      }
    } catch (error) {
      console.error('Error saving settings:', error);
      showNotification('Errore nel salvataggio delle impostazioni', 'error');
    }
  }
  
  // Testa connessione API
  async function testConnection() {
    setLoading(true);
    
    try {
      const apiUrl = apiUrlInput.value.trim() || 'http://localhost:5000';
      const response = await fetch(`${apiUrl}/api/health`, {
        method: 'GET',
        timeout: 5000
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setStatus('connected', '✅', 'Connesso all\'API');
          showNotification('Connessione API riuscita', 'success');
        } else {
          setStatus('disconnected', '❌', 'API non disponibile');
          showNotification('API non risponde correttamente', 'error');
        }
      } else {
        setStatus('disconnected', '❌', `Errore HTTP: ${response.status}`);
        showNotification(`Errore HTTP: ${response.status}`, 'error');
      }
    } catch (error) {
      console.error('Connection test failed:', error);
      setStatus('disconnected', '❌', 'Connessione fallita');
      showNotification('Impossibile connettersi all\'API', 'error');
    } finally {
      setLoading(false);
    }
  }
  
  // Testa analisi con TXID
  async function testAnalysis() {
    const txid = testTxidInput.value.trim();
    
    if (!txid) {
      showNotification('Inserisci un TXID valido', 'error');
      return;
    }
    
    if (!isValidTxid(txid)) {
      showNotification('TXID non valido', 'error');
      return;
    }
    
    setLoading(true);
    
    try {
      const result = await chrome.runtime.sendMessage({
        action: 'analyzeTransaction',
        txid: txid,
        options: {
          depth: parseInt(analysisDepthSelect.value),
          includePatterns: includePatternsCheckbox.checked
        }
      });
      
      if (result.success) {
        showNotification('Analisi completata con successo!', 'success');
        console.log('Analysis result:', result.data);
        
        // Mostra risultato in una nuova tab
        const resultWindow = window.open('', '_blank');
        resultWindow.document.write(`
          <html>
            <head>
              <title>Risultato Analisi - ${txid}</title>
              <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .header { background: #f39800; color: white; padding: 15px; margin: -20px -20px 20px -20px; border-radius: 8px 8px 0 0; }
                .result { margin: 20px 0; }
                .info { background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 10px 0; }
                .label { font-weight: bold; color: #333; }
                .value { color: #666; }
              </style>
            </head>
            <body>
              <div class="container">
                <div class="header">
                  <h1>🔍 Risultato Analisi Bitcoin</h1>
                  <p>TXID: ${txid}</p>
                </div>
                <div class="result">
                  <div class="info">
                    <span class="label">Wallet Rilevato:</span>
                    <span class="value">${result.data.fingerprint?.wallet || 'Sconosciuto'}</span>
                  </div>
                  <div class="info">
                    <span class="label">Confidenza:</span>
                    <span class="value">${Math.round((result.data.fingerprint?.confidence || 0) * 100)}%</span>
                  </div>
                  <div class="info">
                    <span class="label">Livello Rischio:</span>
                    <span class="value">${result.data.fingerprint?.risk_level || 'Sconosciuto'}</span>
                  </div>
                  ${result.data.fingerprint?.reasoning ? `
                    <div class="info">
                      <span class="label">Ragionamento:</span>
                      <ul>
                        ${result.data.fingerprint.reasoning.map(r => `<li>${r}</li>`).join('')}
                      </ul>
                    </div>
                  ` : ''}
                </div>
              </div>
            </body>
          </html>
        `);
      } else {
        showNotification(`Errore nell'analisi: ${result.error}`, 'error');
      }
    } catch (error) {
      console.error('Test analysis failed:', error);
      showNotification('Errore durante il test di analisi', 'error');
    } finally {
      setLoading(false);
    }
  }
  
  // Apre documentazione
  function openDocumentation() {
    chrome.tabs.create({
      url: 'http://localhost:5000/api/docs/'
    });
  }
  
  // Apre impostazioni avanzate
  function openAdvancedSettings() {
    chrome.tabs.create({
      url: chrome.runtime.getURL('settings.html')
    });
  }
  
  // Utility functions
  function setStatus(type, icon, text) {
    status.className = `status ${type}`;
    statusIcon.textContent = icon;
    statusText.textContent = text;
  }
  
  function setLoading(loading) {
    testConnectionBtn.disabled = loading;
    testText.classList.toggle('hidden', loading);
    testSpinner.classList.toggle('hidden', !loading);
  }
  
  function showNotification(message, type = 'info') {
    // Crea notifica temporanea
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#F44336' : '#2196F3'};
      color: white;
      padding: 10px 15px;
      border-radius: 4px;
      font-size: 12px;
      z-index: 1000;
      animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.remove();
    }, 3000);
  }
  
  function isValidTxid(txid) {
    return /^[a-fA-F0-9]{64}$/.test(txid);
  }
  
  // Aggiungi stili per animazioni
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `;
  document.head.appendChild(style);
});
