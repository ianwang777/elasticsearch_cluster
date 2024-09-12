import time
import requests

# Elasticsearch 的 URL
ES_URL = "http://elasticsearch1:9200/health_info/_search"

# 定義查詢函數，查詢 health_info 資料
def search_es():
    query = {
        "query": {
            "match_all": {}
        }
    }
    
    try:
        response = requests.get(ES_URL, json=query)
        if response.status_code == 200:
            data = response.json()
            print("Search Result:", data)
        else:
            print("Search failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during search:", e)

# 每秒執行一次
while True:
    search_es()
    time.sleep(5)
