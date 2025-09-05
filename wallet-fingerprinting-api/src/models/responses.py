"""
Modelli per le risposte API
Definisce la struttura delle risposte JSON
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class WalletDetection:
    """Risultato del rilevamento wallet"""
    wallet: str
    confidence: float
    reasoning: List[str]
    is_clear: bool

@dataclass
class TransactionInfo:
    """Informazioni base della transazione"""
    txid: str
    version: int
    locktime: int
    inputs_count: int
    outputs_count: int
    input_types: List[str]
    output_types: List[str]
    block_height: Optional[int] = None
    timestamp: Optional[datetime] = None

@dataclass
class AnalysisResult:
    """Risultato dell'analisi"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

@dataclass
class TransactionAnalysis:
    """Analisi completa di una transazione"""
    transaction: TransactionInfo
    detection: WalletDetection
    analysis_time: float

@dataclass
class AddressAnalysis:
    """Analisi di un indirizzo"""
    address: str
    total_transactions: int
    wallet_distribution: Dict[str, int]
    wallet_percentages: Dict[str, float]
    timeline: List[Dict[str, Any]]
    main_wallet: str
    pattern_type: str

@dataclass
class BlockAnalysis:
    """Analisi di un blocco"""
    block_hash: str
    total_transactions: int
    analyzed_transactions: int
    wallet_distribution: Dict[str, int]
    wallet_percentages: Dict[str, float]
    analysis_time: float

@dataclass
class ErrorResponse:
    """Risposta di errore standardizzata"""
    error: str
    message: str
    code: int
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

def create_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Crea una risposta di successo standardizzata"""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }

def create_error_response(error: str, message: str, code: int = 400) -> Dict[str, Any]:
    """Crea una risposta di errore standardizzata"""
    return {
        "success": False,
        "error": error,
        "message": message,
        "code": code,
        "timestamp": datetime.utcnow().isoformat()
    }

def serialize_dataclass(obj) -> Dict[str, Any]:
    """Serializza un dataclass in dizionario JSON-safe"""
    if hasattr(obj, '__dataclass_fields__'):
        return asdict(obj)
    return obj
