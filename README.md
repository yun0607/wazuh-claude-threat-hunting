# Wazuh × Claude Threat Hunting Assistant

本專案整合 **Wazuh SIEM** 與 **Claude Large Language Model (LLM)**，  
實作一個可以將資安事件（alerts）轉換為「**中文可讀的威脅分析與管理建議**」的 Threat Hunting Assistant。

透過此專案，驗證以下完整流程：

> Wazuh 偵測 → Indexer 儲存 → Python Agent 擷取 → Claude 分析 → 中文風險摘要

---

## 專案目標

- 建立一套基於 **Wazuh SIEM** 的威脅監控環境
- 從 Wazuh Indexer 取得近期安全事件（alerts）
- 將結構化的安全事件轉為自然語言描述
- 使用 **Claude LLM** 進行風險判斷與管理者行動建議
- 實作 AI 輔助的 Threat Hunting 流程，而非僅止於 log 檢視

---

## 系統架構與工具

### 使用工具與技術
- **Wazuh All-in-One**（Manager / Indexer / Dashboard / API）
- **OpenSearch（Wazuh Indexer）**
- **Python 3 + requests**
- **Claude API（Anthropic）**
- **Docker（MCP Server for Wazuh）**
- **Claude Desktop（MCP Client）**

### 系統架構概念
Wazuh Agent
↓
Wazuh Manager
↓
Wazuh Indexer (OpenSearch)
↓
Python Threat Hunting Agent
↓
Claude LLM
↓
中文威脅分析與建議

---

## Wazuh All-in-One 安裝

本專案使用 Wazuh 官方提供的 **All-in-One 安裝腳本**，一次完成所有核心服務部署。

```bash
curl -sO https://packages.wazuh.com/4.12/wazuh-install.sh
sudo bash wazuh-install.sh -a
```
此指令會自動安裝並設定以下服務：
- Wazuh Manager
- Wazuh Indexer（OpenSearch）
- Wazuh Dashboard
- Wazuh API（預設 port 55000）

---

## Wazuh 服務與連線驗證
防火牆與 Port 設定，為確保外部程式可正常連線至 Wazuh API 與 Indexer，需開放以下連接埠：
```
55000/tcp：Wazuh API

9200/tcp：Wazuh Indexer（OpenSearch）

sudo ufw status
sudo ufw allow 55000/tcp
sudo ufw allow 9200/tcp
sudo ufw reload
```
 此步驟用於避免因防火牆設定導致 API 或 Indexer 無法連線。
![開放 Wazuh API（55000）與 Indexer（9200）連接埠](ufw設定) 

---

## Indexer（OpenSearch）連線測試

使用 curl 驗證 Indexer 是否正常運作：
```
curl -k -u admin:<password> https://<WAZUH_IP>:9200
```
成功回傳 OpenSearch 版本資訊，代表 Indexer 服務正常。
![成功連線至 Wazuh Indexer（OpenSearch），確認服務正常運作](圖片路徑) 

---

## MCP Server 與 Claude Desktop 串接

本專案使用 mcp-server-wazuh 作為 Claude 與 Wazuh 間的橋樑，MCP Server 啟動方式（Docker）：
```
docker run --rm -it \
  -e WAZUH_API_HOST=localhost \
  -e WAZUH_API_PORT=55000 \
  -e WAZUH_API_USERNAME=admin \
  -e WAZUH_API_PASSWORD=<WAZUH_PASSWORD> \
  -e WAZUH_INDEXER_HOST=localhost \
  -e WAZUH_INDEXER_PORT=9200 \
  -e WAZUH_INDEXER_USERNAME=admin \
  -e WAZUH_INDEXER_PASSWORD=<WAZUH_PASSWORD> \
  -e WAZUH_VERIFY_SSL=false \
  ghcr.io/gbrigandi/mcp-server-wazuh:latest
```
當 log 中出現以下訊息時，表示 MCP Server 成功以 stdio 模式 啟動：
```
INFO mcp_server_wazuh: Using stdio transport
```
(此模式與 Claude Desktop MCP 完全相容，無需額外修改程式碼。)
![MCP Server 成功以 stdio 模式啟動，可供 Claude Desktop 直接串接](圖片路徑) 

## Python 虛擬環境設定
```
sudo apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate
pip install requests anthropic
```
---

## Threat Hunting 流程說明

- 從 Wazuh Indexer（OpenSearch）查詢最新 alerts
  ![Threat Hunting Agent 成功從 Wazuh Indexer 擷取近期安全事件](圖片路徑) 
- 擷取事件關鍵欄位（主機、等級、描述、時間）
- 組合為自然語言格式的事件摘要
- 將事件摘要送至 Claude LLM
- 取得中文威脅分析與建議
- Threat Hunting Agent 執行結果（Alerts）
- 成功從 Indexer 擷取近期安全事件（如 AppArmor DENIED、PAM Login 等）：Claude 威脅分析輸出（LLM 分析）

## Claude 會根據安全事件內容，自動產生以下分析：
- 是否屬於高風險事件
- 目前系統狀況摘要（白話中文）
- 管理者可採取的建議行動
  ![Claude LLM 將 Wazuh alerts 轉換為中文可讀的威脅分析與管理建議](圖片路徑) 


