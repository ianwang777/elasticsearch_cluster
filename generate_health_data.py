from datetime import datetime, timezone, timedelta
import random
import string
import time
import requests

# elasticsearch 的 URL
ES_URL = "http://elasticsearch1:9200/health_info/_doc"

# 隨機生成使用者編號
def generate_user_id():
    letters = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(string.digits, k=7))
    return letters + numbers

# 隨機生成健康數據
def generate_health_data():
    taiwan_timezone = timezone(timedelta(hours=8))  # 設定台灣時區（UTC+8）
    current_time_in_taiwan = datetime.now(taiwan_timezone).strftime('%Y-%m-%d %H:%M:%S')

    return {
        "user_id": generate_user_id(),
        "heart_rate": random.randint(60, 100),
        "blood_oxygen": random.randint(90, 100),
        "systolic_blood_pressure": random.randint(120, 140),
        "diastolic_blood_pressure": random.randint(80, 90),
        "data_generated_time": current_time_in_taiwan
    }

# 等待 elasticsearch 準備就緒
def wait_for_elasticsearch():
    while True:
        try:
            response = requests.get("http://elasticsearch1:9200/_cluster/health")
            if response.status_code == 200:
                print("ElasticSearch is ready.")
                break
        except requests.exceptions.ConnectionError:
            print("Waiting for ElasticSearch to be ready...")
        time.sleep(5)

# 等待 elasticsearch 準備就緒
wait_for_elasticsearch()

# 每 n 秒生成並寫入一筆健康數據到 elasticsearch
count = 0
while count < 10000:
    health_data = generate_health_data()
    try:
        response = requests.post(ES_URL, json=health_data)
        if response.status_code == 201:
            print("Data written to ElasticSearch:", health_data)
        else:
            print("Failed to write data:", response.status_code, response.text)
    except Exception as e:
        print("Error connecting to ElasticSearch:", e)
    time.sleep(5) # 5, 1, 0.01
    count += 1
