export interface WalletDetection {
  wallet: string;
  confidence: number;
  reasoning: string[];
  is_clear: boolean;
}

export interface TransactionInfo {
  txid: string;
  version: number;
  locktime: number;
  inputs_count: number;
  outputs_count: number;
  input_types: string[];
  output_types: string[];
}

export interface TransactionAnalysis {
  transaction: TransactionInfo;
  detection: WalletDetection;
  analysis_time: number;
  block_explorer: string;
}

export interface AnalysisResponse {
  success: boolean;
  message: string;
  data: TransactionAnalysis;
  timestamp: string;
}

export interface AddressAnalysis {
  address: string;
  total_transactions: number;
  analyzed_transactions: number;
  wallet_distribution: Record<string, number>;
  wallet_percentages: Record<string, number>;
  timeline: Array<{
    date: string;
    wallet: string;
    txid: string;
  }>;
  main_wallet: string;
  pattern_type: string;
  block_explorer: string;
}
