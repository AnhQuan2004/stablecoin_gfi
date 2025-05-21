from flask import Flask, jsonify, Response, request
import requests
import json
import concurrent.futures
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Danh sách blockchain
CHAINS = [
    "Ethereum", "Solana", "Near", "Bitcoin", "Sui", 
    "Aptos", "Arbitrum", "Sei", "Base", "BSC", 
    "Polygon", "Optimism", "Fantom", "Avalanche", "Celo"
]

# API URL template
BASE_API_URL = "https://tvl-defillama-service-1094890588015.us-central1.run.app"
LLAMA_API_URL = "https://api.llama.fi"
DUNE_API_URL = "https://api.dune.com/api/v1"
DUNE_API_KEY = os.environ.get('DUNE_API_KEY', 'mtrULhgGW3gS6LldSlQ28qsnESTAamIq')

@app.route('/api/trending/contracts', methods=['GET'])
def get_trending_contracts():
    """API endpoint để lấy dữ liệu trending contracts từ Dune Analytics."""
    app.logger.info("Getting trending contracts data from Dune Analytics")
    
    # Query ID cho trending contracts 2.0
    query_id = "4995232"
    
    url = f"{DUNE_API_URL}/query/{query_id}/results"
    params = {
        "api_key": DUNE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Trả về dữ liệu nguyên bản từ Dune không xử lý gì thêm
        # Sử dụng Response để trả về chính xác nội dung từ API
        return Response(response.content, mimetype='application/json')
            
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching data from Dune API: {str(e)}")
        return jsonify({
            "error": f"Error fetching data from Dune API: {str(e)}"
        }), 500

@app.route('/api/binance-net-inflow', methods=['GET'])
def get_binance_net_inflow():
    """API endpoint để lấy dữ liệu Binance Net Inflow 24h từ Dune Analytics."""
    app.logger.info("Getting Binance net inflow data from Dune Analytics")
    
    url = f"{DUNE_API_URL}/endpoints/gfi_research/binance-net-inflow-24h/results"
    params = {
        "api_key": DUNE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Trả về dữ liệu nguyên bản từ Dune không xử lý gì thêm
        return Response(response.content, mimetype='application/json')
            
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching Binance net inflow data from Dune API: {str(e)}")
        return jsonify({
            "error": f"Error fetching Binance net inflow data from Dune API: {str(e)}"
        }), 500

@app.route('/api/nft-marketplaces-overview', methods=['GET'])
def get_nft_marketplaces_overview():
    """API endpoint để lấy dữ liệu NFT Marketplaces Overview từ Dune Analytics."""
    app.logger.info("Getting NFT Marketplaces Overview data from Dune Analytics")
    
    url = f"{DUNE_API_URL}/endpoints/gfi_research/nft-marketplaces-overview/results"
    params = {
        "api_key": DUNE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    
        return Response(response.content, mimetype='application/json')

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching NFT Marketplaces Overview data from Dune API: {str(e)}")
        return jsonify({
            "error": f"Error fetching NFT Marketplaces Overview data from Dune API: {str(e)}"
        }), 500



@app.route('/api/fees/protocol/<protocol>', methods=['GET'])
def get_protocol_fees(protocol):
    """API endpoint để lấy dữ liệu fees của một protocol cụ thể."""
    app.logger.info(f"Getting fees data for protocol: {protocol}")
    
    url = f"{LLAMA_API_URL}/summary/fees/{protocol}?dataType=dailyFees"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        # Lấy dữ liệu đầy đủ
        full_data = response.json()
        
        # Lọc chỉ các trường cần thiết
        filtered_data = {
            "id": full_data.get("id"),
            "name": full_data.get("name"),
            "logo": full_data.get("logo"),
            "gecko_id": full_data.get("gecko_id"),
            "governanceID": full_data.get("governanceID"),
            "totalDataChart": full_data.get("totalDataChart"),
            "totalDataChartBreakdown": full_data.get("totalDataChartBreakdown")
        }
        
        return jsonify({
            "protocol": protocol,
            "data": filtered_data
        })
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching API data: {str(e)}")
        return jsonify({
            "protocol": protocol,
            "data": {"error": str(e)}
        }), 500



@app.route('/api/fees/protocols/all', methods=['GET'])
def get_all_protocols_fees_paginated():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    protocols_param = request.args.get('protocols')

    if protocols_param:
        protocols = [p.strip() for p in protocols_param.split(',')]
    else:
        try:
            with open('./working_protocols.txt', 'r') as f:
                protocols = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return jsonify({"error": "working_protocols.txt not found and no protocols param"}), 400

    if not protocols:
        return jsonify({"error": "No protocols specified"}), 400

    total_protocols = len(protocols)
    start = (page - 1) * limit
    end = start + limit
    selected_protocols = protocols[start:end]

    app.logger.info(f"Processing {len(selected_protocols)} protocols (page {page})")
    result_list = []

    max_workers = min(10, len(selected_protocols))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_protocol = {
            executor.submit(get_protocol_data, protocol): protocol 
            for protocol in selected_protocols
        }

        for future in concurrent.futures.as_completed(future_to_protocol):
            protocol = future_to_protocol[future]
            try:
                result = future.result()
                result_list.append(result)
            except Exception as e:
                result_list.append({"protocol": protocol, "data": {"error": str(e)}})

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total_protocols,
        "data": result_list
    })


def get_protocol_data(protocol):
    """Hàm để lấy dữ liệu của một protocol."""
    try:
        url = f"{LLAMA_API_URL}/summary/fees/{protocol}?dataType=dailyFees"
        response = requests.get(url)
        
        if response.status_code == 200:
            full_data = response.json()
            
            # Lọc chỉ các trường cần thiết
            filtered_data = {
                "id": full_data.get("id"),
                "name": full_data.get("name"),
                "logo": full_data.get("logo"),
                "gecko_id": full_data.get("gecko_id"),
                "governanceID": full_data.get("governanceID"),
                "totalDataChart": full_data.get("totalDataChart"),
                "totalDataChartBreakdown": full_data.get("totalDataChartBreakdown")
            }
            return {"protocol": protocol, "data": filtered_data}
        else:
            return {"protocol": protocol, "data": {"error": f"API trả về status code: {response.status_code}"}}
    except Exception as e:
        return {"protocol": protocol, "data": {"error": str(e)}}

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
def get_all_stablecoins_paginated():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))
    total_chains = len(CHAINS)
    start = (page - 1) * limit
    end = start + limit
    selected_chains = CHAINS[start:end]

    all_data = {"chains": []}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_chain = {
            executor.submit(requests.get, f"{BASE_API_URL}/stablecoins/{chain}"): chain 
            for chain in selected_chains
        }

        for future in concurrent.futures.as_completed(future_to_chain):
            chain = future_to_chain[future]
            try:
                response = future.result()
                if response.status_code == 200:
                    chain_data = {"chain": chain, "data": response.json()}
                    all_data["chains"].append(chain_data)
                else:
                    all_data["chains"].append({"chain": chain, "error": f"Status {response.status_code}"})
            except Exception as e:
                all_data["chains"].append({"chain": chain, "error": str(e)})

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total_chains,
        "data": all_data
    })


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
def get_all_tvl_paginated():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))
    total_chains = len(CHAINS)
    start = (page - 1) * limit
    end = start + limit
    selected_chains = CHAINS[start:end]

    all_data = {"chains": []}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_chain = {
            executor.submit(requests.get, f"{BASE_API_URL}/tvl/{chain}"): chain
            for chain in selected_chains
        }

        for future in concurrent.futures.as_completed(future_to_chain):
            chain = future_to_chain[future]
            try:
                response = future.result()
                if response.status_code == 200:
                    raw_data = response.json()
                    formatted_data = []
                    for item in raw_data:
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
                            formatted_data.append({"error": str(e)})
                    all_data["chains"].append({"chain": chain, "history": formatted_data})
                else:
                    all_data["chains"].append({"chain": chain, "error": f"Status {response.status_code}"})
            except Exception as e:
                all_data["chains"].append({"chain": chain, "error": str(e)})

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total_chains,
        "data": all_data
    })


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
def get_all_dexs_paginated():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))
    total_chains = len(CHAINS)
    start = (page - 1) * limit
    end = start + limit
    selected_chains = CHAINS[start:end]

    result = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_chain = {
            executor.submit(
                requests.get, 
                f"{LLAMA_API_URL}/overview/dexs/{chain}?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=false&dataType=dailyVolume"
            ): chain for chain in selected_chains
        }

        for future in concurrent.futures.as_completed(future_to_chain):
            chain = future_to_chain[future]
            try:
                response = future.result()
                if response.status_code == 200:
                    data = response.json()
                    result[chain] = {
                        "totalDataChart": data.get("totalDataChart", []),
                        "totalDataChartBreakdown": data.get("totalDataChartBreakdown", {})
                    }
                else:
                    result[chain] = {"error": f"Status {response.status_code}"}
            except Exception as e:
                result[chain] = {"error": str(e)}

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total_chains,
        "data": result
    })


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
            
            <h2>Trending Contracts</h2>
            <div class="endpoint">
                <h3>Lấy dữ liệu trending contracts từ Dune Analytics:</h3>
                <code>GET /api/trending/contracts</code>
                <p>Ví dụ: <a href="/api/trending/contracts">/api/trending/contracts</a></p>
                <p>Lấy dữ liệu thô: <a href="/api/trending/contracts?raw=true">/api/trending/contracts?raw=true</a></p>
            </div>
            
            <h2>Binance Net Inflow</h2>
            <div class="endpoint">
                <h3>Lấy dữ liệu Binance Net Inflow 24h từ Dune Analytics:</h3>
                <code>GET /api/binance-net-inflow</code>
                <p>Ví dụ: <a href="/api/binance-net-inflow">/api/binance-net-inflow</a></p>
            </div>

            <h2>NFT Marketplaces Overview</h2>
            <div class="endpoint">
                <h3>Lấy dữ liệu NFT Marketplaces Overview từ Dune Analytics:</h3>
                <code>GET /api/nft-marketplaces-overview</code>
                <p>Ví dụ: <a href="/api/nft-marketplaces-overview">/api/nft-marketplaces-overview</a></p>
            </div>
            
            <h2>Protocol Fees</h2>
            <div class="endpoint">
                <h3>Lấy dữ liệu fees cho một protocol cụ thể:</h3>
                <code>GET /api/fees/protocol/{protocol}</code>
                <p>Ví dụ: <a href="/api/fees/protocol/uniswap">/api/fees/protocol/uniswap</a></p>
            </div>
            
            <div class="endpoint">
                <h3>Lấy dữ liệu fees cho nhiều protocol:</h3>
                <code>GET /api/fees/protocols/all?protocols=uniswap,aave,compound</code>
                <p>Hoặc lấy danh sách mặc định: <a href="/api/fees/protocols/all">/api/fees/protocols/all</a></p>
            </div>
            
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
