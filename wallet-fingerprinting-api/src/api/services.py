"""
Servizi per l'analisi wallet
Contiene la logica di business per l'API
"""

import time
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import sys
import os

# Aggiungi path per importare moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fingerprinting import detect_wallet, analyze_txs, analyze_block, get_spending_types, get_sending_types
from fetch_txs import module
from models.responses import (
    WalletDetection, TransactionInfo, TransactionAnalysis, 
    AddressAnalysis, BlockAnalysis
)
from utils.logger import setup_logger

logger = setup_logger()

class WalletAnalysisService:
    """Servizio per analisi wallet"""
    
    @staticmethod
    def analyze_transaction(txid: str) -> TransactionAnalysis:
        """Analizza una singola transazione"""
        start_time = time.time()
        
        try:
            # Recupera dati transazione
            tx = module.get_tx(txid)
            
            # Informazioni base
            transaction_info = TransactionInfo(
                txid=txid,
                version=tx['version'],
                locktime=tx['locktime'],
                inputs_count=len(tx['vin']),
                outputs_count=len(tx['vout']),
                input_types=get_spending_types(tx),
                output_types=get_sending_types(tx)
            )
            
            # Rilevamento wallet
            wallet, reasoning = detect_wallet(tx)
            wallet_name = list(wallet)[0].value if wallet else 'Unknown'
            confidence = 95.0 if wallet and len(wallet) == 1 else 50.0
            
            detection = WalletDetection(
                wallet=wallet_name,
                confidence=confidence,
                reasoning=reasoning,
                is_clear=len(wallet) == 1
            )
            
            analysis_time = time.time() - start_time
            
            return TransactionAnalysis(
                transaction=transaction_info,
                detection=detection,
                analysis_time=analysis_time
            )
            
        except Exception as e:
            logger.error(f"Error analyzing transaction {txid}: {str(e)}")
            raise
    
    @staticmethod
    def analyze_address(address: str, limit: int = 20) -> AddressAnalysis:
        """Analizza un indirizzo Bitcoin"""
        start_time = time.time()
        
        try:
            # Recupera transazioni dell'indirizzo
            url = f'https://mempool.space/api/address/{address}/txs'
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")
            
            txs = response.json()
            total_txs = len(txs)
            
            # Limita il numero di transazioni da analizzare
            txs_to_analyze = txs[:min(limit, total_txs)]
            txids = [tx['txid'] for tx in txs_to_analyze]
            
            # Analisi batch
            results = analyze_txs(txids)
            
            # Calcola distribuzione
            wallet_distribution = {wallet: data['total'] for wallet, data in results.items()}
            total_analyzed = sum(wallet_distribution.values())
            
            wallet_percentages = {
                wallet: (count / total_analyzed * 100) if total_analyzed > 0 else 0
                for wallet, count in wallet_distribution.items()
            }
            
            # Wallet principale
            main_wallet = max(wallet_distribution.items(), key=lambda x: x[1])[0]
            
            # Timeline
            timeline = []
            for tx in txs_to_analyze:
                txid = tx['txid']
                timestamp = tx['status']['block_time']
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
                
                try:
                    tx_data = module.get_tx(txid)
                    wallet, _ = detect_wallet(tx_data)
                    detected = list(wallet)[0].value if wallet else 'Unknown'
                    timeline.append({
                        'date': date,
                        'wallet': detected,
                        'txid': txid[:16]
                    })
                except:
                    timeline.append({
                        'date': date,
                        'wallet': 'Error',
                        'txid': txid[:16]
                    })
            
            # Pattern type
            unique_wallets = set([item['wallet'] for item in timeline])
            pattern_type = 'Multi-wallet' if len(unique_wallets) > 1 else 'Single-wallet'
            
            return AddressAnalysis(
                address=address,
                total_transactions=total_txs,
                wallet_distribution=wallet_distribution,
                wallet_percentages=wallet_percentages,
                timeline=timeline,
                main_wallet=main_wallet,
                pattern_type=pattern_type
            )
            
        except Exception as e:
            logger.error(f"Error analyzing address {address}: {str(e)}")
            raise
    
    @staticmethod
    def analyze_block(block_hash: Optional[str] = None, num_txs: int = 50) -> BlockAnalysis:
        """Analizza un blocco Bitcoin"""
        start_time = time.time()
        
        try:
            # Analizza il blocco
            results = analyze_block(block_hash, num_txs)
            
            # Calcola distribuzione
            wallet_distribution = {wallet: count for wallet, count in results.items()}
            total_analyzed = sum(wallet_distribution.values())
            
            wallet_percentages = {
                wallet: (count / total_analyzed * 100) if total_analyzed > 0 else 0
                for wallet, count in wallet_distribution.items()
            }
            
            analysis_time = time.time() - start_time
            
            return BlockAnalysis(
                block_hash=block_hash or 'latest',
                total_transactions=total_analyzed,
                analyzed_transactions=num_txs,
                wallet_distribution=wallet_distribution,
                wallet_percentages=wallet_percentages,
                analysis_time=analysis_time
            )
            
        except Exception as e:
            logger.error(f"Error analyzing block {block_hash}: {str(e)}")
            raise

# Istanza globale del servizio
wallet_service = WalletAnalysisService()
