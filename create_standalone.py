#!/usr/bin/env python3
"""
Erstellt eine standalone HTML-Datei - KEIN Hosting nötig!
Einfach die HTML-Datei verschicken und im Browser öffnen.
"""

def create_standalone_html():
    html_content = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💹 Nominalwert-Rechner</title>
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container { 
            max-width: 800px;
            margin: 0 auto;
            background: rgba(45, 45, 45, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .title { 
            color: #e2ff00;
            font-size: 28px;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(226, 255, 0, 0.3);
        }
        .subtitle {
            color: #9598a1;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .input-group { 
            margin-bottom: 15px;
        }
        .input-group.full-width {
            grid-column: 1 / -1;
        }
        label { 
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #e0e0e0;
        }
        input, select { 
            width: 100%;
            padding: 12px;
            background: #3d3d3d;
            border: 2px solid #555;
            border-radius: 8px;
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #e2ff00;
            box-shadow: 0 0 10px rgba(226, 255, 0, 0.2);
        }
        .leverage-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .leverage-slider {
            flex: 1;
        }
        .leverage-value {
            background: #e2ff00;
            color: #1a1a1a;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            min-width: 60px;
            text-align: center;
        }
        .button-group {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 30px 0;
        }
        button { 
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }
        .reset-btn { 
            background: linear-gradient(135deg, #ff6b6b 0%, #ff5252 100%);
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        }
        .reset-btn:hover { 
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
        }
        .results { 
            background: linear-gradient(135deg, #333 0%, #404040 100%);
            padding: 25px;
            border-radius: 12px;
            margin-top: 30px;
            border: 1px solid #555;
        }
        .results h3 {
            color: #e2ff00;
            margin-bottom: 20px;
            text-align: center;
        }
        .result-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .result-card {
            background: rgba(64, 64, 64, 0.8);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #555;
        }
        .result-label {
            font-size: 14px;
            color: #b0b0b0;
            margin-bottom: 5px;
        }
        .result-value {
            font-size: 18px;
            font-weight: bold;
        }
        .success { color: #4CAF50; }
        .warning { color: #FFC107; }
        .danger { color: #F44336; }
        .profit { color: #00E676; }
        .info { color: #2196F3; }
        
        @media (max-width: 768px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            .result-grid {
                grid-template-columns: 1fr;
            }
            .button-group {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">💹 Nominalwert-Rechner</h1>
            <p class="subtitle">Professional Trading Position Calculator</p>
        </div>
        
        <div class="form-grid">
            <div class="input-group">
                <label>📊 Richtung:</label>
                <select id="direction">
                    <option value="long">📈 Long Position</option>
                    <option value="short">📉 Short Position</option>
                </select>
            </div>
            
            <div class="input-group">
                <label>💰 Order Price:</label>
                <input type="number" id="price" step="0.01" placeholder="z.B. 50000.00">
            </div>
            
            <div class="input-group">
                <label>🛡️ Max. Loss (€):</label>
                <input type="number" id="maxLoss" step="0.01" value="10.00">
            </div>
            
            <div class="input-group">
                <label>🛑 Stop-Loss %:</label>
                <input type="number" id="stopLoss" step="0.01" value="0.5" placeholder="z.B. 0.5">
            </div>
            
            <div class="input-group full-width">
                <label>⚡ Leverage:</label>
                <div class="leverage-container">
                    <input type="range" id="leverage" class="leverage-slider" min="1" max="100" value="1" oninput="updateLeverage()">
                    <span id="leverageValue" class="leverage-value">1X</span>
                </div>
            </div>
        </div>
        
        <div class="button-group">
            <button onclick="calculate()">🧮 Berechnen</button>
            <button class="reset-btn" onclick="resetForm()">🔄 Reset</button>
        </div>
        
        <div class="results" id="results" style="display: none;">
            <h3>📊 Berechnungsergebnisse</h3>
            <div class="result-grid">
                <div class="result-card">
                    <div class="result-label">💰 Nominal Value</div>
                    <div id="nominal" class="result-value success">0.00 €</div>
                </div>
                <div class="result-card">
                    <div class="result-label">💳 Margin Required</div>
                    <div id="margin" class="result-value warning">0.00 €</div>
                </div>
                <div class="result-card">
                    <div class="result-label">🛑 Stop-Loss Price</div>
                    <div id="slPrice" class="result-value danger">0.00</div>
                </div>
                <div class="result-card">
                    <div class="result-label">🎯 Take-Profit 1</div>
                    <div id="tp1" class="result-value profit">0.00</div>
                </div>
                <div class="result-card">
                    <div class="result-label">📈 Units</div>
                    <div id="units" class="result-value info">0.00</div>
                </div>
                <div class="result-card">
                    <div class="result-label">📊 Risk/Reward</div>
                    <div id="riskReward" class="result-value info">1:2</div>
                </div>
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
            const direction = document.getElementById('direction').value;
            
            if (price <= 0 || stopLoss <= 0 || maxLoss <= 0) {
                alert('⚠️ Bitte gültige Werte eingeben!\\n\\n• Order Price > 0\\n• Stop-Loss % > 0\\n• Max Loss > 0');
                return;
            }
            
            // Berechnung basierend auf dem Python-Script
            const fees = 0.1; // 0.1% Gebühren
            const effectivePct = (stopLoss + fees) / 100;
            const marginRequired = maxLoss / effectivePct;
            const nominal = marginRequired * leverage;
            
            // Stop-Loss und Take-Profit Preise
            let slPrice, tp1;
            if (direction === 'long') {
                slPrice = price * (1 - effectivePct);
                tp1 = price * (1 + effectivePct * 2);
            } else {
                slPrice = price * (1 + effectivePct);
                tp1 = price * (1 - effectivePct * 2);
            }
            
            const units = nominal / price;
            
            // Ergebnisse anzeigen
            document.getElementById('nominal').textContent = nominal.toFixed(2) + ' €';
            document.getElementById('margin').textContent = marginRequired.toFixed(2) + ' €';
            document.getElementById('slPrice').textContent = slPrice.toFixed(2);
            document.getElementById('tp1').textContent = tp1.toFixed(2);
            document.getElementById('units').textContent = units.toFixed(6);
            document.getElementById('riskReward').textContent = '1:2';
            
            document.getElementById('results').style.display = 'block';
            
            // Smooth scroll zu den Ergebnissen
            document.getElementById('results').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'nearest' 
            });
        }
        
        function resetForm() {
            document.getElementById('price').value = '';
            document.getElementById('maxLoss').value = '10.00';
            document.getElementById('stopLoss').value = '0.5';
            document.getElementById('leverage').value = '1';
            document.getElementById('direction').value = 'long';
            updateLeverage();
            document.getElementById('results').style.display = 'none';
        }
        
        // Enter-Taste für Berechnung
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                calculate();
            }
        });
        
        // Initial setup
        updateLeverage();
    </script>
</body>
</html>"""
    
    with open('NominalwertRechner.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Standalone HTML-App erstellt!")
    print("Datei: NominalwertRechner.html")
    print("Einfach die HTML-Datei verschicken - laeuft in jedem Browser!")
    print("Kein Hosting, kein Server, keine Installation noetig!")

if __name__ == "__main__":
    create_standalone_html()
