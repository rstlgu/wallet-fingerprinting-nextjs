'use client';

import { useSSE } from '@/hooks/useSSE';
import { Button } from '@/registry/new-york-v4/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/registry/new-york-v4/ui/card';
import { useState } from 'react';

export default function TestSSE() {
  const [sessionId] = useState(() => `test-${Date.now()}`);
  const sse = useSSE(sessionId);

  const testTransaction = () => {
    sse.analyzeTransaction('7a2c087cb02a758b2d04d809f46bd5d5d46dd38492f7a3cc3cc7eded7e3ce166');
  };

  const testAddress = () => {
    sse.analyzeAddress('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 5);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold">Test SSE Connection</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>Connection Status</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <p>Session ID: <code>{sessionId}</code></p>
          <p>Connected: {sse.isConnected ? '✅' : '❌'}</p>
          <p>Analyzing: {sse.isAnalyzing ? '⏳' : '🔄'}</p>
          <p>Progress: {sse.progress}%</p>
          <p>Message: {sse.currentMessage || 'None'}</p>
          {sse.error && <p className="text-red-500">Error: {sse.error}</p>}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Test Actions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <Button onClick={testTransaction} disabled={sse.isAnalyzing}>
            Test Transaction Analysis
          </Button>
          <Button onClick={testAddress} disabled={sse.isAnalyzing}>
            Test Address Analysis
          </Button>
          <Button onClick={sse.reset}>Reset</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Messages ({sse.messages.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="max-h-64 overflow-y-auto space-y-1">
            {sse.messages.map((msg, i) => (
              <div key={i} className="text-xs font-mono">
                <span className="text-gray-500">{new Date(msg.timestamp).toLocaleTimeString()}</span>{' '}
                <span className="font-bold">{msg.type}</span>: {msg.data.message || JSON.stringify(msg.data)}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {sse.result && (
        <Card>
          <CardHeader>
            <CardTitle>Result</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="text-xs overflow-auto">{JSON.stringify(sse.result, null, 2)}</pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
