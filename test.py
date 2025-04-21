import requests
import json

# URL API cần lấy dữ liệu
url = "https://tvl-defillama-service-1094890588015.us-central1.run.app/stablecoins/Solana"

try:
    # Gửi request GET
    response = requests.get(url)
    
    # Kiểm tra xem request có thành công không
    response.raise_for_status()
    
    # Lấy dữ liệu JSON
    data = response.json()
    
    # Hiển thị dữ liệu gốc đã format đẹp
    print(json.dumps(data, indent=2))
    
except requests.exceptions.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")
except json.JSONDecodeError:
    print("Lỗi khi giải mã JSON từ response")