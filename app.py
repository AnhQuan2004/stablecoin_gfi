from flask import Flask, jsonify, Response, request
import requests
import json

app = Flask(__name__)

# Danh sách blockchain
CHAINS = [
    "Ethereum", "Solana", "Near", "Bitcoin", "Sui", 
    "Aptos", "Arbitrum", "Sei", "Base", "BSC", 
    "Polygon", "Optimism", "Fantom", "Avalanche", "Celo"
]

# API URL template
BASE_API_URL = "https://tvl-defillama-service-1094890588015.us-central1.run.app"

@app.route('/api/stablecoins/<chain_id>', methods=['GET'])
def get_stablecoins_for_chain(chain_id):
    """API endpoint to get stablecoins data for a specific chain."""
    if chain_id not in CHAINS:
        return jsonify({"error": f"Invalid chain ID. Supported chains: {', '.join(CHAINS)}"}), 400
        
    api_url = f"{BASE_API_URL}/stablecoins/{chain_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data from API: {str(e)}"}), 500

@app.route('/api/stablecoins/all', methods=['GET'])
def get_all_stablecoins():
    """API endpoint to get stablecoins data for all chains."""
    all_data = {"chains": []}
    
    for chain in CHAINS:
        api_url = f"{BASE_API_URL}/stablecoins/{chain}"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                chain_data = {"chain": chain, "data": response.json()}
                all_data["chains"].append(chain_data)
        except Exception as e:
            print(f"Error fetching data for {chain}: {e}")
    
    return jsonify(all_data)

@app.route('/api/tvl/<chain_id>', methods=['GET'])
def get_tvl_for_chain(chain_id):
    """API endpoint to get TVL data for a specific chain."""
    if chain_id not in CHAINS:
        return jsonify({"error": f"Invalid chain ID. Supported chains: {', '.join(CHAINS)}"}), 400
        
    api_url = f"{BASE_API_URL}/tvl/{chain_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data from API: {str(e)}"}), 500

@app.route('/api/tvl/all', methods=['GET'])
def get_all_tvl():
    """API endpoint to get TVL data for all chains."""
    all_data = {"chains": []}
    
    for chain in CHAINS:
        api_url = f"{BASE_API_URL}/tvl/{chain}"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                chain_data = {"chain": chain, "data": response.json()}
                all_data["chains"].append(chain_data)
        except Exception as e:
            print(f"Error fetching data for {chain}: {e}")
    
    return jsonify(all_data)

@app.route('/api/dexs/<chain_id>', methods=['GET'])
def get_dexs_for_chain(chain_id):
    """API endpoint to get DEX data for a specific chain."""
    if chain_id not in CHAINS:
        return jsonify({"error": f"Invalid chain ID. Supported chains: {', '.join(CHAINS)}"}), 400
        
    api_url = f"{BASE_API_URL}/dexs/{chain_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data from API: {str(e)}"}), 500

@app.route('/api/dexs/all', methods=['GET'])
def get_all_dexs():
    """API endpoint to get DEX data for all chains."""
    all_data = {"chains": []}
    
    for chain in CHAINS:
        api_url = f"{BASE_API_URL}/dexs/{chain}"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                chain_data = {"chain": chain, "data": response.json()}
                all_data["chains"].append(chain_data)
        except Exception as e:
            print(f"Error fetching data for {chain}: {e}")
    
    return jsonify(all_data)

@app.route('/', methods=['GET'])
def home():
    return """
    <html>
        <head>
            <title>DeFi Llama API Proxy</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; }
                .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; }
                code { background: #e9ecef; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>DeFi Llama API Proxy</h1>
            <p>API proxy cho dữ liệu từ DeFi Llama</p>
            
            <h2>Stablecoins</h2>
            <div class="endpoint">
                <h3>Lấy dữ liệu stablecoin cho một blockchain:</h3>
                <code>GET /api/stablecoins/{chain_id}</code>
                <p>Ví dụ: <a href="/api/stablecoins/Ethereum">/api/stablecoins/Ethereum</a></p>
            </div>
            
            <div class="endpoint">
                <h3>Lấy dữ liệu stablecoin cho tất cả blockchain:</h3>
                <code>GET /api/stablecoins/all</code>
                <p>Ví dụ: <a href="/api/stablecoins/all">/api/stablecoins/all</a></p>
            </div>
            
            <h2>TVL</h2>
            <div class="endpoint">
                <h3>Lấy dữ liệu TVL cho một blockchain:</h3>
                <code>GET /api/tvl/{chain_id}</code>
                <p>Ví dụ: <a href="/api/tvl/Ethereum">/api/tvl/Ethereum</a></p>
            </div>
            
            <div class="endpoint">
                <h3>Lấy dữ liệu TVL cho tất cả blockchain:</h3>
                <code>GET /api/tvl/all</code>
                <p>Ví dụ: <a href="/api/tvl/all">/api/tvl/all</a></p>
            </div>
            
            <h2>DEXs</h2>
            <div class="endpoint">
                <h3>Lấy dữ liệu DEX cho một blockchain:</h3>
                <code>GET /api/dexs/{chain_id}</code>
                <p>Ví dụ: <a href="/api/dexs/Ethereum">/api/dexs/Ethereum</a></p>
            </div>
            
            <div class="endpoint">
                <h3>Lấy dữ liệu DEX cho tất cả blockchain:</h3>
                <code>GET /api/dexs/all</code>
                <p>Ví dụ: <a href="/api/dexs/all">/api/dexs/all</a></p>
            </div>
            
            <h3>Blockchain hỗ trợ:</h3>
            <ul>
                """ + "".join([f"<li>{chain}</li>" for chain in CHAINS]) + """
            </ul>
        </body>
    </html>
    """

@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    """
    Catch-all route to proxy any other paths directly to the original API.
    This allows proxying any endpoint that might exist on the original API.
    """
    api_url = f"{BASE_API_URL}/{path}"
    
    # Forward query parameters
    params = request.args.to_dict()
    
    try:
        response = requests.get(api_url, params=params)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error proxying request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)