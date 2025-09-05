/**
 * Hook React per gestire Server-Sent Events (SSE)
 * Fornisce comunicazione real-time con il backend
 */

import { useEffect, useState, useCallback, useRef } from 'react';

export interface SSEMessage {
  type: 'connected' | 'started' | 'progress' | 'completed' | 'error' | 'heartbeat';
  timestamp: string;
  data: {
    message?: string;
    progress?: number;
    result?: any;
    error?: string;
    session_id?: string;
  };
}

export interface SSEState {
  isConnected: boolean;
  isAnalyzing: boolean;
  progress: number;
  messages: SSEMessage[];
  currentMessage: string;
  result: any;
  error: string | null;
}

const API_BASE = process.env.WALLET_API_URL || 'http://127.0.0.1:5000';

export function useSSE(sessionId: string) {
  const [state, setState] = useState<SSEState>({
    isConnected: false,
    isAnalyzing: false,
    progress: 0,
    messages: [],
    currentMessage: '',
    result: null,
    error: null
  });

  const eventSourceRef = useRef<EventSource | null>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);
  const [usePolling, setUsePolling] = useState(false);

  // Connetti a SSE stream
  const connect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const eventSource = new EventSource(`${API_BASE}/sse/stream/${sessionId}`);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      console.log('SSE connection opened successfully:', `${API_BASE}/sse/stream/${sessionId}`);
      setState(prev => ({
        ...prev,
        isConnected: true,
        error: null
      }));
    };

    eventSource.onmessage = (event) => {
      try {
        const message: SSEMessage = JSON.parse(event.data);
        
        setState(prev => {
          const newMessages = [...prev.messages, message];
          let newState = {
            ...prev,
            messages: newMessages
          };

          switch (message.type) {
            case 'connected':
              newState.currentMessage = message.data.message || 'Connesso';
              break;
              
            case 'started':
              newState.isAnalyzing = true;
              newState.progress = message.data.progress || 0;
              newState.currentMessage = message.data.message || 'Analisi avviata';
              newState.result = null;
              newState.error = null;
              break;
              
            case 'progress':
              newState.progress = message.data.progress || prev.progress;
              newState.currentMessage = message.data.message || prev.currentMessage;
              break;
              
            case 'completed':
              newState.isAnalyzing = false;
              newState.progress = 100;
              newState.currentMessage = message.data.message || 'Completato';
              newState.result = message.data.result;
              break;
              
            case 'error':
              newState.isAnalyzing = false;
              newState.error = message.data.error || message.data.message || 'Errore sconosciuto';
              newState.currentMessage = message.data.message || 'Errore durante analisi';
              break;
              
            case 'heartbeat':
              // Non cambiare lo stato per heartbeat
              break;
          }

          return newState;
        });
      } catch (e) {
        console.error('Error parsing SSE message:', e);
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE connection error:', error);
      console.error('EventSource readyState:', eventSource.readyState);
      console.error('EventSource URL:', eventSource.url);
      
      setState(prev => ({
        ...prev,
        isConnected: false,
        error: `Connessione SSE interrotta (ReadyState: ${eventSource.readyState})`
      }));

      // Fallback a polling dopo 3 tentativi SSE falliti
      if (!usePolling) {
        timeoutRef.current = setTimeout(() => {
          console.log('SSE fallito, passaggio a polling...');
          setUsePolling(true);
          startPolling();
        }, 3000);
      }
    };
  }, [sessionId, usePolling]);

  // Polling fallback
  const startPolling = useCallback(() => {
    console.log('Avvio polling per session:', sessionId);
    
    const poll = async () => {
      try {
        const response = await fetch(`${API_BASE}/sse/messages/${sessionId}`);
        if (response.ok) {
          const data = await response.json();
          if (data.success && data.messages) {
            setState(prev => {
              const newMessages = data.messages.slice(prev.messages.length);
              if (newMessages.length > 0) {
                const lastMessage = newMessages[newMessages.length - 1];
                let updates: any = {
                  messages: data.messages,
                  isConnected: true
                };

                switch (lastMessage.type) {
                  case 'started':
                    updates.isAnalyzing = true;
                    updates.progress = lastMessage.data.progress || 0;
                    updates.currentMessage = lastMessage.data.message;
                    break;
                  case 'progress':
                    updates.progress = lastMessage.data.progress || prev.progress;
                    updates.currentMessage = lastMessage.data.message;
                    break;
                  case 'completed':
                    updates.isAnalyzing = false;
                    updates.progress = 100;
                    updates.result = lastMessage.data.result;
                    updates.currentMessage = lastMessage.data.message;
                    break;
                  case 'error':
                    updates.isAnalyzing = false;
                    updates.error = lastMessage.data.error;
                    break;
                }

                return { ...prev, ...updates };
              }
              return prev;
            });
          }
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    };

    // Poll ogni 2 secondi
    const pollInterval = setInterval(poll, 2000);
    pollingRef.current = pollInterval;
    
    // Poll iniziale
    poll();
  }, [sessionId]);

  // Disconnetti da SSE
  const disconnect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
    setState(prev => ({
      ...prev,
      isConnected: false
    }));
  }, []);

  // Reset stato
  const reset = useCallback(() => {
    setState({
      isConnected: false,
      isAnalyzing: false,
      progress: 0,
      messages: [],
      currentMessage: '',
      result: null,
      error: null
    });
  }, []);

  // Analizza transazione con SSE
  const analyzeTransaction = useCallback(async (txid: string) => {
    try {
      reset();
      
      const response = await fetch(`${API_BASE}/sse/analyze/tx/${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ txid })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Errore durante richiesta');
      }

      const result = await response.json();
      if (!result.success) {
        throw new Error(result.message || 'Errore durante analisi');
      }

      return result;
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Errore sconosciuto',
        isAnalyzing: false
      }));
      throw error;
    }
  }, [sessionId, reset]);

  // Analizza indirizzo con SSE
  const analyzeAddress = useCallback(async (address: string, limit: number = 20) => {
    try {
      reset();
      
      const response = await fetch(`${API_BASE}/sse/analyze/address/${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ address, limit })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Errore durante richiesta');
      }

      const result = await response.json();
      if (!result.success) {
        throw new Error(result.message || 'Errore durante analisi');
      }

      return result;
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Errore sconosciuto',
        isAnalyzing: false
      }));
      throw error;
    }
  }, [sessionId, reset]);

  // Effect per gestire connessione
  useEffect(() => {
    if (usePolling) {
      startPolling();
    } else {
      connect();
    }
    return () => {
      disconnect();
    };
  }, [connect, disconnect, usePolling, startPolling]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
    };
  }, []);

  return {
    ...state,
    connect,
    disconnect,
    reset,
    analyzeTransaction,
    analyzeAddress
  };
}
