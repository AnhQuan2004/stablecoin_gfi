# from flask import Flask, jsonify, Response, request
# import requests
# import json

# app = Flask(__name__)

# # Danh sách blockchain
# CHAINS = [
#     "Ethereum", "Solana", "Near", "Bitcoin", "Sui", 
#     "Aptos", "Arbitrum", "Sei", "Base", "BSC", 
#     "Polygon", "Optimism", "Fantom", "Avalanche", "Celo"
# ]

# # API URL template
# BASE_API_URL = "https://tvl-defillama-service-1094890588015.us-central1.run.app"

# @app.route('/api/stablecoins/<chain_id>', methods=['GET'])
# def get_stablecoins_for_chain(chain_id):
#     """API endpoint to get stablecoins data for a specific chain."""
#     if chain_id not in CHAINS:
#         return jsonify({"error": f"Invalid chain ID. Supported chains: {', '.join(CHAINS)}"}), 400
        
#     api_url = f"{BASE_API_URL}/stablecoins/{chain_id}"
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": f"Error fetching data from API: {str(e)}"}), 500

# @app.route('/api/stablecoins/all', methods=['GET'])
# def get_all_stablecoins():
#     """API endpoint to get stablecoins data for all chains."""
#     all_data = {"chains": []}
    
#     for chain in CHAINS:
#         api_url = f"{BASE_API_URL}/stablecoins/{chain}"
#         try:
#             response = requests.get(api_url)
#             if response.status_code == 200:
#                 chain_data = {"chain": chain, "data": response.json()}
#                 all_data["chains"].append(chain_data)
#         except Exception as e:
#             print(f"Error fetching data for {chain}: {e}")
    
#     return jsonify(all_data)

# @app.route('/api/tvl/<chain_id>', methods=['GET'])
# def get_tvl_for_chain(chain_id):
#     """API endpoint to get TVL data for a specific chain."""
#     if chain_id not in CHAINS:
#         return jsonify({"error": f"Invalid chain ID. Supported chains: {', '.join(CHAINS)}"}), 400
        
#     api_url = f"{BASE_API_URL}/tvl/{chain_id}"
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": f"Error fetching data from API: {str(e)}"}), 500

# @app.route('/api/tvl/all', methods=['GET'])
# def get_all_tvl():
#     """API endpoint to get TVL data for all chains."""
#     all_data = {"chains": []}
    
#     for chain in CHAINS:
#         api_url = f"{BASE_API_URL}/tvl/{chain}"
#         try:
#             response = requests.get(api_url)
#             if response.status_code == 200:
#                 chain_data = {"chain": chain, "data": response.json()}
#                 all_data["chains"].append(chain_data)
#         except Exception as e:
#             print(f"Error fetching data for {chain}: {e}")
    
#     return jsonify(all_data)

# @app.route('/api/dexs/<chain_id>', methods=['GET'])
# def get_dexs_for_chain(chain_id):
#     """API endpoint to get DEX data for a specific chain."""
#     if chain_id not in CHAINS:
#         return jsonify({"error": f"Invalid chain ID. Supported chains: {', '.join(CHAINS)}"}), 400
        
#     api_url = f"{BASE_API_URL}/dexs/{chain_id}"
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": f"Error fetching data from API: {str(e)}"}), 500

# @app.route('/api/dexs/all', methods=['GET'])
# def get_all_dexs():
#     """API endpoint to get DEX data for all chains."""
#     all_data = {"chains": []}
    
#     for chain in CHAINS:
#         api_url = f"{BASE_API_URL}/dexs/{chain}"
#         try:
#             response = requests.get(api_url)
#             if response.status_code == 200:
#                 chain_data = {"chain": chain, "data": response.json()}
#                 all_data["chains"].append(chain_data)
#         except Exception as e:
#             print(f"Error fetching data for {chain}: {e}")
    
#     return jsonify(all_data)

# @app.route('/', methods=['GET'])
# def home():
#     return """
#     <html>
#         <head>
#             <title>DeFi Llama API Proxy</title>
#             <style>
#                 body { font-family: Arial, sans-serif; margin: 20px; }
#                 h1 { color: #2c3e50; }
#                 .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; }
#                 code { background: #e9ecef; padding: 2px 5px; border-radius: 3px; }
#             </style>
#         </head>
#         <body>
#             <h1>DeFi Llama API Proxy</h1>
#             <p>API proxy cho dữ liệu từ DeFi Llama</p>
            
#             <h2>Stablecoins</h2>
#             <div class="endpoint">
#                 <h3>Lấy dữ liệu stablecoin cho một blockchain:</h3>
#                 <code>GET /api/stablecoins/{chain_id}</code>
#                 <p>Ví dụ: <a href="/api/stablecoins/Ethereum">/api/stablecoins/Ethereum</a></p>
#             </div>
            
#             <div class="endpoint">
#                 <h3>Lấy dữ liệu stablecoin cho tất cả blockchain:</h3>
#                 <code>GET /api/stablecoins/all</code>
#                 <p>Ví dụ: <a href="/api/stablecoins/all">/api/stablecoins/all</a></p>
#             </div>
            
#             <h2>TVL</h2>
#             <div class="endpoint">
#                 <h3>Lấy dữ liệu TVL cho một blockchain:</h3>
#                 <code>GET /api/tvl/{chain_id}</code>
#                 <p>Ví dụ: <a href="/api/tvl/Ethereum">/api/tvl/Ethereum</a></p>
#             </div>
            
#             <div class="endpoint">
#                 <h3>Lấy dữ liệu TVL cho tất cả blockchain:</h3>
#                 <code>GET /api/tvl/all</code>
#                 <p>Ví dụ: <a href="/api/tvl/all">/api/tvl/all</a></p>
#             </div>
            
#             <h2>DEXs</h2>
#             <div class="endpoint">
#                 <h3>Lấy dữ liệu DEX cho một blockchain:</h3>
#                 <code>GET /api/dexs/{chain_id}</code>
#                 <p>Ví dụ: <a href="/api/dexs/Ethereum">/api/dexs/Ethereum</a></p>
#             </div>
            
#             <div class="endpoint">
#                 <h3>Lấy dữ liệu DEX cho tất cả blockchain:</h3>
#                 <code>GET /api/dexs/all</code>
#                 <p>Ví dụ: <a href="/api/dexs/all">/api/dexs/all</a></p>
#             </div>
            
#             <h3>Blockchain hỗ trợ:</h3>
#             <ul>
#                 """ + "".join([f"<li>{chain}</li>" for chain in CHAINS]) + """
#             </ul>
#         </body>
#     </html>
#     """

# @app.route('/<path:path>', methods=['GET'])
# def catch_all(path):
#     """
#     Catch-all route to proxy any other paths directly to the original API.
#     This allows proxying any endpoint that might exist on the original API.
#     """
#     api_url = f"{BASE_API_URL}/{path}"
    
#     # Forward query parameters
#     params = request.args.to_dict()
    
#     try:
#         response = requests.get(api_url, params=params)
#         return jsonify(response.json()), response.status_code
#     except Exception as e:
#         return jsonify({"error": f"Error proxying request: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, jsonify, Response, request
import requests
import json
import concurrent.futures

app = Flask(__name__)

# Danh sách blockchain
CHAINS = [
    "Ethereum", "Solana", "Near", "Bitcoin", "Sui", 
    "Aptos", "Arbitrum", "Sei", "Base", "BSC", 
    "Polygon", "Optimism", "Fantom", "Avalanche", "Celo"
]

# API URL template
BASE_API_URL = "https://tvl-defillama-service-1094890588015.us-central1.run.app"
LLAMA_API_URL = "https://api.llama.fi"

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
    
    # Sử dụng ThreadPoolExecutor để lấy dữ liệu song song
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_chain = {
            executor.submit(requests.get, f"{BASE_API_URL}/stablecoins/{chain}"): chain 
            for chain in CHAINS
        }
        
        for future in concurrent.futures.as_completed(future_to_chain):
            chain = future_to_chain[future]
            try:
                response = future.result()
                if response.status_code == 200:
                    chain_data = {"chain": chain, "data": response.json()}
                    all_data["chains"].append(chain_data)
                else:
                    print(f"Error fetching data for {chain}: {response.status_code}")
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
    
    # Sử dụng ThreadPoolExecutor để lấy dữ liệu song song
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_chain = {
            executor.submit(requests.get, f"{BASE_API_URL}/tvl/{chain}"): chain 
            for chain in CHAINS
        }
        
        for future in concurrent.futures.as_completed(future_to_chain):
            chain = future_to_chain[future]
            try:
                response = future.result()
                if response.status_code == 200:
                    # Format lại dữ liệu TVL theo yêu cầu
                    raw_data = response.json()
                    formatted_data = []
                    
                    for item in raw_data:
                        # Xử lý date thành format 2025-MM-DD
                        try:
                            import datetime
                            date_unix = int(item.get('date', 0))
                            date_obj = datetime.datetime.fromtimestamp(date_unix)
                            date_str = f"2025-{date_obj.month:02d}-{date_obj.day:02d}"
                            
                            formatted_data.append({
                                "date": date_str,
                                "tvl": item.get('tvl', 0)
                            })
                        except Exception as e:
                            print(f"Error formatting date for {chain}: {e}")
                    
                    chain_data = {"chain": chain, "history": formatted_data}
                    all_data["chains"].append(chain_data)
                else:
                    print(f"Error fetching data for {chain}: {response.status_code}")
            except Exception as e:
                print(f"Error fetching data for {chain}: {e}")
    
    return jsonify(all_data)

@app.route('/api/dexs/<chain_id>', methods=['GET'])
def get_dexs_for_chain(chain_id):
    """API endpoint to get DEX data for a specific chain using the llama.fi API."""
    if chain_id not in CHAINS:
        return jsonify({"error": f"Invalid chain ID. Supported chains: {', '.join(CHAINS)}"}), 400
        
    api_url = f"{LLAMA_API_URL}/overview/dexs/{chain_id}?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=false&dataType=dailyVolume"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        # Fallback to original API
        try:
            fallback_url = f"{BASE_API_URL}/dexs/{chain_id}"
            fallback_response = requests.get(fallback_url)
            fallback_response.raise_for_status()
            return jsonify(fallback_response.json())
        except Exception as fallback_e:
            return jsonify({"error": f"Error fetching data from both APIs: {str(e)}, fallback: {str(fallback_e)}"}), 500

@app.route('/api/dexs/all', methods=['GET'])
def get_all_dexs():
    """API endpoint to get DEX data for all chains using the llama.fi API."""
    result = {}
    
    # Sử dụng ThreadPoolExecutor để lấy dữ liệu song song
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_chain = {
            executor.submit(
                requests.get, 
                f"{LLAMA_API_URL}/overview/dexs/{chain}?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=false&dataType=dailyVolume"
            ): chain 
            for chain in CHAINS
        }
        
        for future in concurrent.futures.as_completed(future_to_chain):
            chain = future_to_chain[future]
            try:
                response = future.result()
                if response.status_code == 200:
                    data = response.json()
                    # Lấy các trường theo yêu cầu
                    result[chain] = {
                        "totalDataChart": data.get("totalDataChart", []),
                        "totalDataChartBreakdown": data.get("totalDataChartBreakdown", {})
                    }
                else:
                    print(f"Error fetching data for {chain}: {response.status_code}")
                    # Thử fallback API
                    try:
                        fallback_url = f"{BASE_API_URL}/dexs/{chain}"
                        fallback_response = requests.get(fallback_url)
                        if fallback_response.status_code == 200:
                            fallback_data = fallback_response.json()
                            result[chain] = {
                                "totalDataChart": fallback_data.get("totalDataChart", []),
                                "totalDataChartBreakdown": fallback_data.get("totalDataChartBreakdown", {})
                            }
                    except Exception as fallback_e:
                        print(f"Fallback error for {chain}: {fallback_e}")
            except Exception as e:
                print(f"Error fetching data for {chain}: {e}")
    
    return jsonify(result)

@app.route('/api/overview/fees', methods=['GET'])
def get_fees_overview():
    """API endpoint to get fees overview for a specific chain."""
    chain = request.args.get("chain")
    if not chain or chain not in CHAINS:
        return jsonify({"error": f"Invalid or missing chain parameter. Supported chains: {', '.join(CHAINS)}"}), 400
        
    api_url = f"{LLAMA_API_URL}/overview/fees/{chain}?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=false"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data.get("totalDataChart", []))
    except requests.exceptions.RequestException as e:
        # Fallback to original API
        try:
            fallback_url = f"{BASE_API_URL}/fees/{chain}"
            fallback_response = requests.get(fallback_url)
            fallback_response.raise_for_status()
            fallback_data = fallback_response.json()
            return jsonify(fallback_data.get("totalDataChart", []))
        except Exception as fallback_e:
            return jsonify({"error": f"Error fetching data from both APIs: {str(e)}, fallback: {str(fallback_e)}"}), 500

@app.route('/api/overview/dexs', methods=['GET'])
def get_dexs_overview():
    """API endpoint to get DEXs overview for a specific chain."""
    chain = request.args.get("chain")
    if not chain or chain not in CHAINS:
        return jsonify({"error": f"Invalid or missing chain parameter. Supported chains: {', '.join(CHAINS)}"}), 400
        
    api_url = f"{LLAMA_API_URL}/overview/dexs/{chain}?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=false&dataType=dailyVolume"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data.get("totalDataChart", []))
    except requests.exceptions.RequestException as e:
        # Fallback to original API
        try:
            fallback_url = f"{BASE_API_URL}/dexs/{chain}"
            fallback_response = requests.get(fallback_url)
            fallback_response.raise_for_status()
            fallback_data = fallback_response.json()
            return jsonify(fallback_data.get("totalDataChart", []))
        except Exception as fallback_e:
            return jsonify({"error": f"Error fetching data from both APIs: {str(e)}, fallback: {str(fallback_e)}"}), 500

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
            
            <h2>Overview</h2>
            <div class="endpoint">
                <h3>Lấy tổng quan phí cho một blockchain:</h3>
                <code>GET /api/overview/fees?chain={chain_id}</code>
                <p>Ví dụ: <a href="/api/overview/fees?chain=Ethereum">/api/overview/fees?chain=Ethereum</a></p>
            </div>
            
            <div class="endpoint">
                <h3>Lấy tổng quan DEX cho một blockchain:</h3>
                <code>GET /api/overview/dexs?chain={chain_id}</code>
                <p>Ví dụ: <a href="/api/overview/dexs?chain=Ethereum">/api/overview/dexs?chain=Ethereum</a></p>
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