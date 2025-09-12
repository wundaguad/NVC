#!/usr/bin/env python3
"""
Lokale Web-Version des Nominalwert-Rechners
Läuft auf localhost - kein Hosting nötig!
"""

import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import os

def create_html():
    """Erstellt eine standalone HTML-Datei mit der kompletten App"""
    html_content = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💹 Nominalwert-Rechner</title>
    <style>
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: #1a1a1a; 
            color: #ffffff; 
            margin: 0; 
            padding: 20px; 
        }
        .container { 
            max-width: 600px; 
            margin: 0 auto; 
            background: #2d2d2d; 
            padding: 20px; 
            border-radius: 10px; 
        }
        .title { 
            text-align: center; 
            color: #e2ff00; 
            font-size: 24px; 
            margin-bottom: 20px; 
        }
        .input-group { 
            margin-bottom: 15px; 
        }
        label { 
            display: block; 
            margin-bottom: 5px; 
            font-weight: bold; 
        }
        input, select { 
            width: 100%; 
            padding: 10px; 
            background: #3d3d3d; 
            border: 2px solid #555; 
            border-radius: 5px; 
            color: white; 
            font-size: 16px; 
        }
        button { 
            background: #4CAF50; 
            color: white; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 16px; 
            margin: 10px 5px; 
        }
        button:hover { background: #45a049; }
        .reset-btn { background: #ff6b6b; }
        .reset-btn:hover { background: #ff5252; }
        .results { 
            background: #333; 
            padding: 15px; 
            border-radius: 5px; 
            margin-top: 20px; 
        }
        .result-row { 
            display: flex; 
            justify-content: space-between; 
            margin: 10px 0; 
            padding: 8px; 
            background: #404040; 
            border-radius: 3px; 
        }
        .success { color: #4CAF50; }
        .warning { color: #FFC107; }
        .danger { color: #F44336; }
        .profit { color: #00E676; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">💹 Nominalwert-Rechner</h1>
        <p style="text-align: center; color: #9598a1;">Created with ♥ by WUNDAGUAD for our community</p>
        
        <div class="input-group">
            <label>Richtung:</label>
            <select id="direction">
                <option value="long">📈 Long</option>
                <option value="short">📉 Short</option>
            </select>
        </div>
        
        <div class="input-group">
            <label>Order Price:</label>
            <input type="number" id="price" step="0.01" placeholder="z.B. 50000">
        </div>
        
        <div class="input-group">
            <label>Max. Loss (€):</label>
            <input type="number" id="maxLoss" step="0.01" value="10.00">
        </div>
        
        <div class="input-group">
            <label>Stop-Loss %:</label>
            <input type="number" id="stopLoss" step="0.01" value="0">
        </div>
        
        <div class="input-group">
            <label>Leverage:</label>
            <input type="range" id="leverage" min="1" max="100" value="1" oninput="updateLeverage()">
            <span id="leverageValue">1X</span>
        </div>
        
        <button onclick="calculate()">Berechnen</button>
        <button class="reset-btn" onclick="resetForm()">🔄 Reset</button>
        
        <div class="results" id="results" style="display: none;">
            <h3>📊 Ergebnisse</h3>
            <div class="result-row">
                <span>💰 Nominal Value:</span>
                <span id="nominal" class="success">0.00</span>
            </div>
            <div class="result-row">
                <span>💳 Margin:</span>
                <span id="margin" class="warning">0.00</span>
            </div>
            <div class="result-row">
                <span>🛑 Stop-Loss:</span>
                <span id="slPrice" class="danger">0.00</span>
            </div>
            <div class="result-row">
                <span>🎯 TP1:</span>
                <span id="tp1" class="profit">0.00</span>
            </div>
        </div>
    </div>

    <script>
        function updateLeverage() {
            const leverage = document.getElementById('leverage').value;
            document.getElementById('leverageValue').textContent = leverage + 'X';
        }
        
        function calculate() {
            const price = parseFloat(document.getElementById('price').value) || 0;
            const maxLoss = parseFloat(document.getElementById('maxLoss').value) || 0;
            const stopLoss = parseFloat(document.getElementById('stopLoss').value) || 0;
            const leverage = parseInt(document.getElementById('leverage').value) || 1;
            
            if (price <= 0 || stopLoss <= 0) {
                alert('Bitte gültige Werte eingeben!');
                return;
            }
            
            // Vereinfachte Berechnung (wie im Python-Script)
            const effectivePct = stopLoss / 100;
            const marginRequired = maxLoss / effectivePct;
            const nominal = marginRequired * leverage;
            const slPrice = price * (1 - effectivePct);
            const tp1 = price * (1 + effectivePct * 2);
            
            // Ergebnisse anzeigen
            document.getElementById('nominal').textContent = nominal.toFixed(2);
            document.getElementById('margin').textContent = marginRequired.toFixed(2);
            document.getElementById('slPrice').textContent = slPrice.toFixed(2);
            document.getElementById('tp1').textContent = tp1.toFixed(2);
            
            document.getElementById('results').style.display = 'block';
        }
        
        function resetForm() {
            document.getElementById('price').value = '';
            document.getElementById('maxLoss').value = '10.00';
            document.getElementById('stopLoss').value = '0';
            document.getElementById('leverage').value = '1';
            updateLeverage();
            document.getElementById('results').style.display = 'none';
        }
    </script>
</body>
</html>
"""
    
    with open('nominalwert_rechner.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML-Datei erstellt: nominalwert_rechner.html")
    print("📂 Einfach die Datei doppelklicken zum Öffnen!")

def start_local_server():
    """Startet lokalen Server für die Web-App"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    class Handler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Cache-Control', 'no-cache')
            super().end_headers()
    
    server = HTTPServer(('localhost', 8080), Handler)
    print("🌐 Server läuft auf: http://localhost:8080")
    print("🔄 Drücke Ctrl+C zum Beenden")
    
    # Browser automatisch öffnen
    webbrowser.open('http://localhost:8080/nominalwert_rechner.html')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server beendet")
        server.shutdown()

if __name__ == "__main__":
    create_html()
    
    choice = input("\n1) HTML-Datei erstellen (offline)\n2) Lokalen Server starten\nWahl (1/2): ")
    
    if choice == "2":
        start_local_server()
    else:
        print("✅ HTML-Datei erstellt! Einfach doppelklicken zum Öffnen.")
