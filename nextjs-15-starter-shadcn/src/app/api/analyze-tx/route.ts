import axios from 'axios';
import { NextRequest, NextResponse } from 'next/server';

const API_BASE = process.env.WALLET_API_URL || 'http://127.0.0.1:5000';

// Configura axios per forzare IPv4
const axiosConfig = {
  family: 4, // Forza IPv4
  timeout: 60000 // 60 secondi per analisi complesse
};

export async function POST(request: NextRequest) {
  try {
    const { txid } = await request.json();
    
    if (!txid) {
      return NextResponse.json(
        { error: 'Transaction ID is required' },
        { status: 400 }
      );
    }

    const response = await axios.post(`${API_BASE}/api/analyze/tx`, {
      txid
    }, axiosConfig);

    return NextResponse.json(response.data);
  } catch (error: any) {
    console.error('Error analyzing transaction:', error);
    
    return NextResponse.json(
      { 
        error: 'Errore durante l\'analisi della transazione',
        details: error.response?.data?.message || error.message 
      },
      { status: 500 }
    );
  }
}
