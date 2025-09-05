import { useState, useCallback } from 'react';
import axios from 'axios';
import { TransactionAnalysis, AddressAnalysis } from '@/lib/types';

export function useWalletAnalysis() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeTransaction = useCallback(async (txid: string): Promise<TransactionAnalysis | null> => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/analyze-tx', { txid });
      return response.data.data;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Errore durante l\'analisi della transazione');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const analyzeAddress = useCallback(async (address: string, limit = 20): Promise<AddressAnalysis | null> => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/analyze-address', { 
        address, 
        limit 
      });
      return response.data.data;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Errore durante l\'analisi dell\'indirizzo');
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
}
