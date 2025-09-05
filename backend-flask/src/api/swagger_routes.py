#!/usr/bin/env python3
"""
Route aggiuntive per Swagger UI personalizzata
"""

from flask import Blueprint, render_template_string, jsonify
from api.docs_config import api

swagger_bp = Blueprint('swagger', __name__)

# Template HTML personalizzato per Swagger UI
SWAGGER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Wallet Fingerprinting API - Documentazione</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
    <link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAABP0lEQVR4nO2WMU7DMBBF35vYTpxODUhQUHABTsAJuAA3gAtwA25AQ0NJQ0lLSQNNhRQFEhIhNqutxGuwYzuJHLGVAFJuYfn9mf/9M5OIiIhcK2VZXjHGbhljr5zzN8bYC2PslnP+wDl/Y4y9MsaujTFfSimPMfbCOX/nnL8xxl4ZY9eMMb/rup7W2q8ikUgkEolEIpFIJBKJRCKRSCQS+a8AGGNujLHbvu8vsixbcs59z/MmjLFrzrmvlPIZY+9KKZ8xds8Y83ut7hljvoqilFK+53nTWmufy+Wy1lprnudNFUUxzTl/Z4y9cM5fOOdvjLFXxtg1Y8yPh8PhtFLK55y/M8ZeOOevnPNXxtgbY+yVMXbNGPN7e3u7oLXOFUWx2DSNb9u253me1zRNnhTFtOu6+DdPKBKJRCKRSCQSiUQikUgkEolEIpFI5P8B38Y9wRFQ5sIAAAAASUVORK5CYII=" sizes="32x32" />
    <style>
        html {
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }
        
        *, *:before, *:after {
            box-sizing: inherit;
        }
        
        body {
            margin:0;
            background: #fafafa;
            font-family: "Open Sans", sans-serif;
        }
        
        .swagger-ui .topbar {
            background: linear-gradient(135deg, #f39800 0%, #f7941d 100%);
            border-bottom: 1px solid #e0e0e0;
        }
        
        .swagger-ui .topbar .link {
            color: white;
            font-weight: bold;
        }
        
        .custom-header {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .custom-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
        }
        
        .custom-header p {
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .features {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 1rem 0;
            flex-wrap: wrap;
        }
        
        .feature {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        
        .swagger-ui .info {
            margin: 2rem 0;
        }
        
        @media (max-width: 768px) {
            .custom-header h1 {
                font-size: 2rem;
            }
            .features {
                gap: 1rem;
            }
        }
    </style>
</head>

<body>
    <div class="custom-header">
        <h1>🔍 Wallet Fingerprinting API</h1>
        <p>API avanzata per l'analisi e il fingerprinting di wallet Bitcoin</p>
        <div class="features">
            <div class="feature">⚡ Real-time Analysis</div>
            <div class="feature">🎯 Pattern Detection</div>
            <div class="feature">📊 Clustering Analysis</div>
            <div class="feature">🔐 Privacy Insights</div>
        </div>
    </div>
    
    <div id="swagger-ui"></div>

    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: '/api/swagger.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                theme: "flattop",
                docExpansion: "list",
                defaultModelRendering: "model",
                showRequestHeaders: true,
                showCommonExtensions: true,
                tryItOutEnabled: true,
                requestInterceptor: function(request) {
                    // Aggiungi headers personalizzati se necessario
                    request.headers['Accept'] = 'application/json';
                    return request;
                },
                responseInterceptor: function(response) {
                    // Log delle risposte per debug
                    console.log('API Response:', response);
                    return response;
                }
            });
            
            // Personalizzazioni aggiuntive
            window.ui = ui;
        };
    </script>
</body>
</html>
'''

@swagger_bp.route('/swagger-ui')
def swagger_ui():
    """Interfaccia Swagger UI personalizzata"""
    return render_template_string(SWAGGER_TEMPLATE)

@swagger_bp.route('/swagger.json')
def swagger_json():
    """Spec OpenAPI in formato JSON"""
    return jsonify(api.__schema__)

@swagger_bp.route('/openapi.json')
def openapi_json():
    """Alias per swagger.json"""
    return jsonify(api.__schema__)

@swagger_bp.route('/redoc')
def redoc():
    """Documentazione con ReDoc"""
    redoc_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Wallet Fingerprinting API - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <redoc spec-url='/api/swagger.json'></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    '''
    return render_template_string(redoc_template)
