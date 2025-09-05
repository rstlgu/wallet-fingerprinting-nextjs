'use client';

import React, { useState, useEffect } from 'react';
import { useSSE } from '@/hooks/useSSE';
import { TransactionAnalysis, AddressAnalysis } from '@/lib/types';
import { Button } from '@/registry/new-york-v4/ui/button';
import { Input } from '@/registry/new-york-v4/ui/input';
import { Label } from '@/registry/new-york-v4/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/registry/new-york-v4/ui/card';
import { Alert, AlertDescription } from '@/registry/new-york-v4/ui/alert';
import { Badge } from '@/registry/new-york-v4/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/registry/new-york-v4/ui/tabs';
import { Separator } from '@/registry/new-york-v4/ui/separator';
import { ExternalLink, Search, Wallet, Hash, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import AnalysisProgress from './AnalysisProgress';

export default function WalletAnalyzer() {
  const [input, setInput] = useState('');
  const [txResult, setTxResult] = useState<TransactionAnalysis | null>(null);
  const [addressResult, setAddressResult] = useState<AddressAnalysis | null>(null);
  const [activeTab, setActiveTab] = useState('transaction');
  
  // Genera session ID unico per SSE
  const [sessionId] = useState(() => `session-${Date.now()}-${Math.random().toString(36).slice(2)}`);
  const sse = useSSE(sessionId);

  // Aggiorna risultati quando SSE completa l'analisi
  useEffect(() => {
    if (sse.result) {
      if (sse.result.transaction) {
        setTxResult(sse.result);
      } else if (sse.result.address) {
        setAddressResult(sse.result);
      }
    }
  }, [sse.result]);

  const handleAnalyze = async () => {
    if (!input.trim()) return;
    
    setTxResult(null);
    setAddressResult(null);
    sse.reset();
    
    // Determina se è un TXID (64 caratteri hex) o un indirizzo
    const isTransaction = /^[a-fA-F0-9]{64}$/.test(input.trim());
    
    try {
      if (isTransaction) {
        setActiveTab('transaction');
        await sse.analyzeTransaction(input.trim());
      } else {
        setActiveTab('address');
        await sse.analyzeAddress(input.trim(), 20);
      }
    } catch (error) {
      console.error('Errore durante analisi:', error);
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return 'bg-green-500';
    if (confidence >= 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getConfidenceIcon = (confidence: number) => {
    if (confidence >= 90) return <CheckCircle className="h-4 w-4" />;
    return <AlertCircle className="h-4 w-4" />;
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold tracking-tight">Bitcoin Wallet Fingerprinting</h1>
        <p className="text-muted-foreground text-lg">
          Analizza transazioni e indirizzi Bitcoin per identificare il wallet utilizzato
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5" />
            Analisi
          </CardTitle>
          <CardDescription>
            Inserisci un TXID (64 caratteri) o un indirizzo Bitcoin per iniziare l'analisi
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <div className="flex-1">
              <Label htmlFor="input" className="sr-only">
                Transaction ID o Bitcoin Address
              </Label>
              <Input
                id="input"
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="es. 7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166 o bc1q..."
                className="font-mono text-sm"
              />
            </div>
            <Button
              onClick={handleAnalyze}
              disabled={sse.isAnalyzing || !input.trim()}
              className="px-6"
            >
              {sse.isAnalyzing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                  Analizzando...
                </>
              ) : (
                <>
                  <Search className="h-4 w-4 mr-2" />
                  Analizza
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {(sse.error || sse.isAnalyzing || sse.result) && (
        <AnalysisProgress 
          sseState={sse} 
          title={sse.isAnalyzing ? "Analisi in Corso" : sse.result ? "Analisi Completata" : "Errore Analisi"}
        />
      )}

      {(txResult || addressResult) && (
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="transaction" className="flex items-center gap-2">
              <Hash className="h-4 w-4" />
              Transazione
            </TabsTrigger>
            <TabsTrigger value="address" className="flex items-center gap-2">
              <Wallet className="h-4 w-4" />
              Indirizzo
            </TabsTrigger>
          </TabsList>

          <TabsContent value="transaction" className="space-y-4">
            {txResult && (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <Wallet className="h-5 w-5" />
                        Wallet Rilevato
                      </span>
                      <Badge 
                        variant="secondary" 
                        className={`${getConfidenceColor(txResult.detection.confidence)} text-white flex items-center gap-1`}
                      >
                        {getConfidenceIcon(txResult.detection.confidence)}
                        {txResult.detection.confidence}% confidenza
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <h3 className="text-2xl font-bold text-primary mb-2">
                          {txResult.detection.wallet}
                        </h3>
                        <Badge variant={txResult.detection.is_clear ? "default" : "secondary"}>
                          {txResult.detection.is_clear ? "Identificazione chiara" : "Identificazione incerta"}
                        </Badge>
                      </div>

                      <Separator />

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <h4 className="font-semibold mb-2">Informazioni Transazione</h4>
                          <div className="space-y-1 text-sm">
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Version:</span>
                              <span className="font-mono">{txResult.transaction.version}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Inputs:</span>
                              <span>{txResult.transaction.inputs_count}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Outputs:</span>
                              <span>{txResult.transaction.outputs_count}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Locktime:</span>
                              <span className="font-mono">{txResult.transaction.locktime}</span>
                            </div>
                          </div>
                        </div>

                        <div>
                          <h4 className="font-semibold mb-2">Tipi Script</h4>
                          <div className="space-y-2">
                            <div>
                              <span className="text-muted-foreground text-sm">Input Types:</span>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {txResult.transaction.input_types.map((type, idx) => (
                                  <Badge key={idx} variant="outline" className="text-xs">
                                    {type}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                            <div>
                              <span className="text-muted-foreground text-sm">Output Types:</span>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {txResult.transaction.output_types.map((type, idx) => (
                                  <Badge key={idx} variant="outline" className="text-xs">
                                    {type}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <Separator />

                      <div>
                        <h4 className="font-semibold mb-3">Analisi Dettagliata</h4>
                        <div className="space-y-2">
                          {txResult.detection.reasoning.map((reason, index) => (
                            <div key={index} className="flex items-start gap-2 text-sm">
                              <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                              <span>{reason}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      <Separator />

                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <Clock className="h-4 w-4" />
                          Tempo di analisi: {txResult.analysis_time.toFixed(3)}s
                        </div>
                        <Button variant="outline" size="sm" asChild>
                          <a
                            href={txResult.block_explorer}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-2"
                          >
                            <ExternalLink className="h-4 w-4" />
                            Block Explorer
                          </a>
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>

          <TabsContent value="address" className="space-y-4">
            {addressResult && (
              <Card>
                <CardHeader>
                  <CardTitle>Analisi Indirizzo</CardTitle>
                  <CardDescription>
                    Risultati dell'analisi per l'indirizzo: {addressResult.address}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold">{addressResult.analyzed_transactions}</div>
                        <div className="text-sm text-muted-foreground">Transazioni Analizzate</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-primary">{addressResult.main_wallet}</div>
                        <div className="text-sm text-muted-foreground">Wallet Più Probabile</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold">{addressResult.total_transactions}</div>
                        <div className="text-sm text-muted-foreground">Totale Transazioni</div>
                      </div>
                    </div>

                    <Separator />

                    <div>
                      <h4 className="font-semibold mb-3">Distribuzione Wallet</h4>
                      <div className="space-y-2">
                        {addressResult.wallet_distribution && Object.entries(addressResult.wallet_distribution).map(([wallet, count]) => (
                          <div key={wallet} className="flex items-center justify-between p-2 border rounded">
                            <span className="font-medium">{wallet}</span>
                            <div className="flex items-center gap-2">
                              <Badge variant="secondary">{count} tx</Badge>
                              {addressResult.wallet_percentages && addressResult.wallet_percentages[wallet] && (
                                <Badge variant="outline">{addressResult.wallet_percentages[wallet].toFixed(1)}%</Badge>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {addressResult.pattern_type && (
                      <>
                        <Separator />
                        <div className="flex items-center gap-2">
                          <Badge variant={addressResult.pattern_type === 'Single-wallet' ? 'default' : 'secondary'}>
                            {addressResult.pattern_type}
                          </Badge>
                          <span className="text-sm text-muted-foreground">Pattern rilevato</span>
                        </div>
                      </>
                    )}

                    {addressResult.timeline && addressResult.timeline.length > 0 && (
                      <>
                        <Separator />
                        <div>
                          <h4 className="font-semibold mb-3">Timeline Transazioni</h4>
                          <div className="max-h-32 overflow-y-auto space-y-1">
                            {addressResult.timeline.slice(0, 5).map((item, index) => (
                              <div key={index} className="flex items-center justify-between text-xs p-2 bg-muted rounded">
                                <span className="font-mono">{item.date}</span>
                                <span className="font-medium">{item.wallet}</span>
                                <span className="text-muted-foreground">{item.txid}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </>
                    )}

                    <Separator />

                    <div className="flex items-center gap-2">
                      <Button variant="outline" size="sm" asChild>
                        <a href={addressResult.block_explorer} target="_blank" rel="noopener noreferrer">
                          <ExternalLink className="h-4 w-4 mr-2" />
                          Visualizza su Block Explorer
                        </a>
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}
