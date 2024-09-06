# Elasticsearch Cluster with Prometheus and Grafana Monitoring

架設一個 based on Docker 的 Elasticsearch cluster，並使用一個 Python script 來自動生成健康資料持續寫入到 Elasticsearch 中。最後使用 Prometheus 和 Grafana 進行監控。

## 專案結構

- `docker-compose.yml`: Docker Compose 設定檔，包含 Elasticsearch cluster、Prometheus、Grafana 與自動生成資料的 Python container。
- `Dockerfile`: 用來建立資料生成器的 Python container，會執行一個生成健康資料的 script。
- `generate_health_data.py`: 一個 Python script，會定期生成隨機健康資料並寫入 Elasticsearch 中名為 health_info 的 index。
- `prometheus.yml`: Prometheus 設定檔，負責從 Elasticsearch Exporter 中抓取監控數據。

## 系統需求

- Docker
- Docker Compose

## 如何啟動

1. git clone 專案
```
git clone https://github.com/ianwang777/elasticsearch_cluster.git
cd elasticsearch_cluster
```

2. 使用 Docker Compose 啟動所有服務
```
docker-compose up --build -d
```

3. 確認服務已成功啟動
- Elasticsearch 入口為 http://localhost:9200
- Kibana 入口為 http://localhost:5601
- Grafana 入口為 http://localhost:3000 (Grafana 初始登入帳號和密碼均為 admin)

4. Grafana 設定
- 新增 Prometheus 作為 data source
- 頁面上的 Connection 區塊下的 Prometheus server URL 設為 http://prometheus:9090
- 新增圖表來監控 Elasticsearch 的各項指標。

5. 停止服務
- 一般停止服務
```
docker-compose down
```
- 若想要刪除停止前儲存到 Elasticsearch 中的資料，可加上 -v option
```
docker-compose down -v
```

## container 概述
- Elasticsearch cluster
 - 包含 elasticsearch1、elasticsearch2、elasticsearch3 三個 node。
- Elasticsearch Exporter
 - 提供 Elasticsearch cluster 的監控數據給 Prometheus。
- Prometheus
 - 用於監控系統，從 Elasticsearch Exporter 取得監控數據。
- Grafana
 - 用於視覺化呈現 Prometheus 抓取到的監控數據。
- Data Generator
 - 自動生成健康資料並每 5 秒寫入到 Elasticsearch 中名為 health_info 的 index。
- Kibana
 - 用於查詢 Elasticsearch 中 index 的資料，與其他監控指標。

## Grafana explore metrics 的使用
- 入口為 http://localhost:3000/explore/metrics
- 點擊 `+ New metric exploration` 按鈕
- 進入畫面後確保左上角 `Data source` 是選擇 `prometheus` 後即可看到各種 metric 折線圖
- 右上角可選擇欲觀看的時間區間，如 `Last 5 minutes` 與 `Last 1 hour` 等等
- `Search metrics` 欄位可輸入想觀察的 metric 名稱
- `View by` 可以選擇列出所有以 elasticsearch_ 開頭的 metrics

## Kibana dev_tools console 的使用
- 入口為 http://localhost:5601/app/dev_tools#/console
- console 左側可輸入語法，執行後結果會顯示於右側，以下為語法範例
- 取得 health_info index 內的資料
```
GET health_info/_search
```
- 取得 cluster 的健康狀態
```
GET /_cluster/health
```
