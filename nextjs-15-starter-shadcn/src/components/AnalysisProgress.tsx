/**
 * Componente per mostrare il progresso dell'analisi in tempo reale
 */

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/registry/new-york-v4/ui/card';
import { Progress } from '@/registry/new-york-v4/ui/progress';
import { Badge } from '@/registry/new-york-v4/ui/badge';
import { ScrollArea } from '@/registry/new-york-v4/ui/scroll-area';
import { CheckCircle, XCircle, Loader2, Wifi, WifiOff } from 'lucide-react';
import { SSEMessage, SSEState } from '@/hooks/useSSE';

interface AnalysisProgressProps {
  sseState: SSEState;
  title?: string;
}

export default function AnalysisProgress({ sseState, title = "Analisi in Corso" }: AnalysisProgressProps) {
  const [visibleMessages, setVisibleMessages] = useState<SSEMessage[]>([]);

  // Filtra messaggi utili (escludi heartbeat)
  useEffect(() => {
    const filtered = sseState.messages.filter(msg => msg.type !== 'heartbeat');
    setVisibleMessages(filtered);
  }, [sseState.messages]);

  const getStatusIcon = () => {
    if (sseState.error) return <XCircle className="h-4 w-4 text-red-500" />;
    if (sseState.result) return <CheckCircle className="h-4 w-4 text-green-500" />;
    if (sseState.isAnalyzing) return <Loader2 className="h-4 w-4 animate-spin text-blue-500" />;
    return null;
  };

  const getStatusColor = () => {
    if (sseState.error) return 'destructive';
    if (sseState.result) return 'default';
    if (sseState.isAnalyzing) return 'secondary';
    return 'outline';
  };

  const getStatusText = () => {
    if (sseState.error) return 'Errore';
    if (sseState.result) return 'Completato';
    if (sseState.isAnalyzing) return 'In corso';
    return 'In attesa';
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('it-IT', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getMessageIcon = (type: SSEMessage['type']) => {
    switch (type) {
      case 'connected':
        return <Wifi className="h-3 w-3 text-green-500" />;
      case 'started':
        return <Loader2 className="h-3 w-3 animate-spin text-blue-500" />;
      case 'progress':
        return <Loader2 className="h-3 w-3 animate-spin text-blue-500" />;
      case 'completed':
        return <CheckCircle className="h-3 w-3 text-green-500" />;
      case 'error':
        return <XCircle className="h-3 w-3 text-red-500" />;
      default:
        return null;
    }
  };

  if (!sseState.isAnalyzing && !sseState.result && !sseState.error) {
    return null;
  }

  return (
    <Card className="w-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{title}</CardTitle>
          <div className="flex items-center gap-2">
            <Badge variant={sseState.isConnected ? 'default' : 'destructive'} className="text-xs">
              {sseState.isConnected ? <Wifi className="h-3 w-3 mr-1" /> : <WifiOff className="h-3 w-3 mr-1" />}
              {sseState.isConnected ? 'Connesso' : 'Disconnesso'}
            </Badge>
            <Badge variant={getStatusColor()} className="text-xs">
              {getStatusIcon()}
              <span className="ml-1">{getStatusText()}</span>
            </Badge>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Barra di progresso */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Progresso</span>
            <span className="font-medium">{sseState.progress}%</span>
          </div>
          <Progress value={sseState.progress} className="h-2" />
        </div>

        {/* Messaggio corrente */}
        {sseState.currentMessage && (
          <div className="p-3 bg-muted rounded-md">
            <div className="flex items-center gap-2">
              {getStatusIcon()}
              <span className="text-sm font-medium">{sseState.currentMessage}</span>
            </div>
          </div>
        )}

        {/* Log messaggi */}
        {visibleMessages.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium text-muted-foreground">Log Analisi</h4>
            <ScrollArea className="h-32 rounded-md border p-2">
              <div className="space-y-1">
                {visibleMessages.map((message, index) => (
                  <div key={index} className="flex items-start gap-2 text-xs">
                    <span className="text-muted-foreground font-mono w-16 flex-shrink-0">
                      {formatTime(message.timestamp)}
                    </span>
                    <div className="flex items-center gap-1 flex-shrink-0">
                      {getMessageIcon(message.type)}
                    </div>
                    <span className="text-muted-foreground flex-1">
                      {message.data.message || `Evento: ${message.type}`}
                    </span>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </div>
        )}

        {/* Errore */}
        {sseState.error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center gap-2">
              <XCircle className="h-4 w-4 text-red-500" />
              <span className="text-sm text-red-700 font-medium">Errore</span>
            </div>
            <p className="text-sm text-red-600 mt-1">{sseState.error}</p>
          </div>
        )}

        {/* Risultato completato */}
        {sseState.result && (
          <div className="p-3 bg-green-50 border border-green-200 rounded-md">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-sm text-green-700 font-medium">Analisi Completata</span>
            </div>
            <p className="text-sm text-green-600 mt-1">
              L'analisi è stata completata con successo. I risultati sono visibili sopra.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
