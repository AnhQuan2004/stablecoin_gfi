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
def get_all_protocols_fees():
    """API endpoint để lấy dữ liệu fees cho nhiều protocol từ file."""
    # Danh sách protocol có thể được cung cấp qua query parameter
    protocols_param = request.args.get('protocols')
    protocol = ["Vader AI",
"Frax",
"Frax FPI",
"Snake Finance",
"Ethena USDe",
"Stables Labs USDX",
"SolvBTC",
"Garden",
"Allbridge Classic",
"Sky Lending",
"Liquity V1",
"crvUSD",
"Inverse Finance FiRM",
"fx Protocol",
"Orby Network",
"Abracadabra Spell",
"Angle",
"Thala CDP",
"Liquity V2",
"QiDao",
"Lybra V2",
"Threshold thUSD",
"Stout",
"Lybra V1",
"PrismaLST",
"Teddy Cash",
"Vesta Finance",
"Fraxtal",
"Gravity",
"Immutable zkEVM",
"Kroma",
"Stargate V2",
"Across",
"Stargate V1",
"Synapse",
"Hop Protocol",
"SideShift",
"Firebird",
"Paraswap",
"Jupiter Perpetual Exchange",
"Drift Trade",
"GMX V2 Perps",
"GMX V1",
"Synthetix V3",
"Derive V2",
"Vertex Perps",
"dYdX V3",
"APX Finance",
"ApeX Pro",
"Gains Network",
"Orderly Perps",
"Fulcrom Perps",
"Bluefin Perps",
"MUX Perps",
"Adrena Protocol",
"HMX",
"Perpetual Protocol",
"BMX Classic Perps",
"Flex Perpetuals",
"Level Perps",
"YFX V4",
"Amped Finance",
"LogX V2",
"Sudo Finance",
"Mummy Finance",
"Pingu Exchange",
"Javsphere",
"Vela Exchange",
"KTX Perps",
"El Dorado Exchange",
"UniDex Perp",
"Y2K V1",
"SOBAX",
"Equation V3",
"Equation V1",
"Cryptex V2",
"Xena Finance",
"Mango Markets V4 Perps",
"Equation V2",
"Nether.Fi",
"Y2K V2",
"Voodoo Trade Base",
"EDEBASE",
"Unlimited Network",
"Covo V2",
"YFX",
"Lexer Markets",
"LionDEX",
"Metavault.Trade",
"Metavault Derivatives V2",
"Uniswap V3",
"Curve DEX",
"PancakeSwap AMM",
"Raydium AMM",
"Uniswap V2",
"Aerodrome Slipstream",
"Balancer V2",
"SUNSwap V1",
"PancakeSwap AMM V3",
"Aerodrome V1",
"SUNSwap V2",
"Orca",
"VVS Standard",
"SUNSwap V3",
"Cetus AMM",
"Thorchain",
"SushiSwap",
"Quickswap Dex",
"iZiSwap",
"Balancer V3",
"Joe V2.2",
"Bluefin AMM",
"Beets DEX",
"Camelot V3",
"SwapX Algebra",
"Cellana Finance",
"Shadow Exchange CLMM",
"Beets DEX V3",
"ThalaSwap V2",
"Ekubo",
"PancakeSwap StableSwap",
"Quickswap V3",
"Gyroscope Protocol",
"Pharaoh CL",
"Joe DEX",
"Joe V2.1",
"DODO AMM",
"ThalaSwap",
"SushiSwap V3",
"Jellyverse",
"Maverick V2",
"Shadow Exchange Legacy",
"WAGMI",
"Chainflip",
"Saber",
"ShibaSwap",
"Camelot V2",
"Balancer V1",
"Balanced Exchange",
"Ferro",
"SpookySwap V2",
"ApeSwap AMM",
"BurrBear",
"Alien Base V2",
"Pharaoh Legacy",
"SmarDex",
"Wombat Exchange",
"Uniswap V1",
"SwapX V2",
"Pangolin",
"Clipper",
"BaseSwap V2",
"Equalizer Exchange",
"Verse",
"Kinetix AMM V3",
"Integral",
"Solidly V3",
"RadioShack",
"Maverick V1",
"2THICK",
"KyberSwap Classic",
"Ramses CL",
"Defi Swap",
"Honeyswap",
"KIM Exchange V3",
"SilverSwap",
"DefiPlaza",
"Elk",
"BaseX",
"ArcherSwap",
"Joe V2",
"Scale",
"WOOFi Swap",
"Holdstation Swap",
"Thick",
"SwapBased AMM",
"KIM Exchange V2",
"KyberSwap Elastic",
"DackieSwap V3",
"Apex DeFi",
"Pearl V1",
"Chronos V1",
"Retro",
"Lifinity V1",
"DackieSwap V2",
"Solidly V2",
"SquadSwap V2",
"Arbitrum Exchange V2",
"Arbitrum Exchange V3",
"Zyberswap V3",
"SolidLizard Dex",
"Horiza",
"Zyberswap AMM",
"Embr Finance",
"Auragi Finance",
"Archly V1",
"SquadSwap V3",
"ZyberSwap Stableswap",
"Viridian Exchange",
"dexSWAP",
"Hydrometer Finance",
"Kinetix AMM V2",
"Monocerus",
"Beralis V3",
"Houdini Swap",
"Zeebu",
"Illuvium",
"Reserve Protocol",
"dHEDGE",
"PinkSale",
"Juicebox V1",
"AAVE V3",
"JustLend",
"Morpho Blue",
"Venus Core Pool",
"Kamino Lend",
"Euler V2",
"Maple",
"Compound V2",
"NAVI Lending",
"AAVE V2",
"Benqi Lending",
"Save",
"Scallop Lend",
"Moonwell",
"Gearbox",
"Silo V1",
"Iron Bank",
"Strike",
"Impermax V2",
"Tarot",
"Joe Lend",
"Radiant V2",
"Yamfore",
"Sonne Finance",
"Polter Finance",
"Extra Finance Leverage Farming",
"Lido",
"Jito",
"Rocket Pool",
"Marinade Liquid Staking",
"StakeWise V2",
"Stader",
"Liquid Collective",
"Benqi Staked Avax",
"Beets LST",
"Bifrost Liquid Staking",
"Stride",
"Kamino Liquidity",
"Gamma",
"Bunni V2",
"X2Y2",
"Blur Bids",
"Sudoswap V2",
"Sudoswap V1",
"LooksRare",
"BlueMove Staking",
"ether.fi Liquid",
"Hegic",
"SOFA.org",
"Stryke CLAMM",
"Premia V3",
"Derive V1",
"Premia V2",
"Buffer Finance",
"OptionBlitz",
"Ribbon",
"Step Finance",
"BetSwirl",
"Tornado Cash",
"Railgun",
"0x0.ai",
"Ondo Finance",
"Usual",
"Paxos Gold",
"Tangible RWA",
"Zivoe",
"Goldfinch",
"Eggs Finance",
"Furucombo",
"GET Protocol",
"Meowl",
"Bank AI",
"friend.tech V1",
"FriendRoom",
"Marinade Native",
"Alchemix",
"Synthetix v1+v2",
"PAAL AI",
"UNCX Network V2",
"Pendle",
"Convex Finance",
"Aura",
"Equilibria",
"Penpie",
"StakeDAO",
"VaultCraft",
"Concentrator",
"Beradrome",
"D2 Finance",
"Radpie",
"Vaultka",
"Liquis",
"Wompie",
"Colony",
"Factor V2",
"Manga FI",
"GND Protocol",
"Sharpe Magnum",
"Caviar Tangible",
"Ducata",
"Beefy",
"Instadapp Lite",
"Yield Yak Aggregator",
"Goat Protocol",
"BounceBit CeDeFi Yield",
"WBTC",
"Allbridge Core",
"deBridge",
"Beraborrow",
"Defi Saver",
"Summer.fi Pro",
"World Chain",
"K2",
"Hemi",
"Ancient8",
"Redstone",
"Paradex",
"KiloEx",
"MYX Finance",
"Contango V2",
"SynFutures V3",
"Surf Protocol",
"Apex Omni",
"Avantis",
"FlashTrade",
"Ostium",
"Merkle Trade",
"IntentX",
"edgeX",
"Satori Perp",
"TsunamiX",
"Thetis Perps",
"Filament V1",
"DESK Perps",
"JOJO",
"FWX Derivatives",
"Crypto Valley Exchange",
"BMX Freestyle",
"AGDEX",
"Substance Exchange",
"SATOSHI PERPS",
"Predy V5",
"Predy V3.2",
"BLEX",
"SpaceWhale",
"Gambit Trade",
"EMDX",
"Filament Beta",
"Kodiak V3",
"Meteora DLMM",
"BEX",
"Meteora pools",
"Sailor",
"PumpSwap",
"Frax Swap",
"Dragon Swap V3",
"Splash Protocol",
"Hyperion",
"Magma",
"STEAMM",
"Glyph V4",
"Kodiak V2",
"Invariant",
"stabble",
"Carbon Defi",
"Metropolis DLMM",
"Metropolis AMM",
"Econia",
"Ekubo EVM",
"Ethervista",
"Haedal AMM Protocol",
"Nabla Finance",
"Wasabee",
"Dragon Swap V2",
"MooniSwap",
"Sushi Trident",
"Infusion",
"FWX DEX",
"DerpDEX",
"Sobal",
"Glyph V2",
"VaporDex V2",
"FeeFree",
"E3",
"MM Stableswap Polygon",
"Haedal Vault",
"BCraft",
"SunPump",
"flaunch",
"Emojicoin.fun",
"GraFun",
"g8keep",
"Ape.Store",
"Degen Express",
"wen markets",
"SparkLend",
"Fluid Lending",
"Dolomite",
"Suilend",
"Yei Finance",
"Echelon Market",
"Sumer.money",
"Resupply",
"Flux Finance",
"Superposition",
"Rain.fi",
"Shoebill V2",
"Size Credit",
"MachFi",
"Levvy for Tokens",
"Keom Protocol",
"Wise Lending V2",
"Zarban",
"Chedda Finance",
"0vix",
"Vicuna Leveraged Farming",
"Mellow LRT",
"Infrared Finance",
"Frax Ether",
"StakeStone STONE",
"Stability",
"Arrakis V2",
"Levvy for NFTs",
"Llamalend",
"Veda",
"Umoja Synths",
"Valorem",
"Hedgey",
"Sablier Legacy",
"Polymarket",
"DoubleUp",
"Azuro",
"Privacy Pools",
"Franklin Templeton",
"Hashnote USYC",
"Spiko",
"OpenEden",
"Superstate USTB",
"Danogo",
"The Arena",
"Tribe.run",
"PostTechSoFi",
"time.fun",
"cipher.rip",
"Chainchat",
"scoop",
"SquaDeFi",
"LSP.Finance",
"GoPlus Locker V2",
"Wildcat Protocol",
"Royco Protocol",
"Toros",
"Amphor",
"Napier",
"CLever",
"Tea-Fi",
"Liquid Bolt",
"CIAN Yield Layer",
"Rings",
"vfat.io",
"Origin Dollar",
"Zunami Protocol",
"maxAPY"
                ]
    
    if protocols_param:
        # Nếu có danh sách protocol được cung cấp qua query parameter
        protocols = [p.strip() for p in protocols_param.split(',')]
    else:
        # Nếu không có, thử đọc từ file
        try:
            protocols = protocol
        except FileNotFoundError:
            return jsonify({"error": "protocols.txt file not found and no protocols parameter provided"}), 400
    
    if not protocols:
        return jsonify({"error": "No protocols specified"}), 400
    
    total_protocols = len(protocols)
    app.logger.info(f"Testing API for {total_protocols} protocols")
    
    # Danh sách kết quả
    result_list = []
    
    # Giới hạn số lượng protocol đồng thời để tránh quá tải API
    max_workers = min(10, total_protocols)
    
    # Sử dụng ThreadPoolExecutor để thực hiện song song
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_protocol = {
            executor.submit(get_protocol_data, protocol): protocol 
            for protocol in protocols
        }
        
        count = 0
        for future in concurrent.futures.as_completed(future_to_protocol):
            protocol = future_to_protocol[future]
            count += 1
            
            # Log tiến trình sau mỗi 10 protocol
            if count % 10 == 0 or count == total_protocols:
                app.logger.info(f"Progress: {count}/{total_protocols}")
            
            try:
                result = future.result()
                result_list.append(result)
            except Exception as e:
                app.logger.error(f"Error processing protocol {protocol}: {str(e)}")
                result_list.append({
                    "protocol": protocol,
                    "data": {"error": str(e)}
                })
    
    return jsonify(result_list)

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