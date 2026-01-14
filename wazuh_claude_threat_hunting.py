import os
import requests
import anthropic
import urllib3
urllib3.disable_warnings()

# =========================
# Indexer 設定（9200）
# =========================
INDEXER_URL = "https://192.168.1.103:9200"
INDEXER_USER = "admin"
INDEXER_PASS = "6Yxun+y8UmX5lQqkjMQMAJzbYoN4MDp+"

# =========================
# Claude 設定
# =========================
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

if not CLAUDE_API_KEY:
    raise RuntimeError("請先設定 CLAUDE_API_KEY 環境變數")

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
# =========================
# 1. 從 Indexer 拿 alerts
# =========================
query = {
    "size": 5,
    "sort": [
        {"@timestamp": {"order": "desc"}}
    ]
}

res = requests.get(
    f"{INDEXER_URL}/wazuh-alerts-*/_search",
    auth=(INDEXER_USER, INDEXER_PASS),
    json=query,
    verify=False,
    timeout=30
)
res.raise_for_status()

hits = res.json()["hits"]["hits"]
print(f"✅ 取得 alerts 數量：{len(hits)}")

# =========================
# 2. 整理成 Claude 看得懂的文字
# =========================
alert_text = ""
for h in hits:
    src = h["_source"]
    alert_text += f"""
- 主機: {src.get('agent', {}).get('name')}
- 等級: {src.get('rule', {}).get('level')}
- 事件: {src.get('rule', {}).get('description')}
- 時間: {src.get('@timestamp')}
"""

# =========================
# 3. 丟給 Claude 分析
# =========================
prompt = f"""
你是一位資安分析師，以下是 Wazuh 偵測到的安全事件。

請幫我：
1. 判斷是否有高風險事件
2. 用白話中文摘要目前系統狀況
3. 提供管理者建議行動

安全事件如下：
{alert_text}
"""

response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=800,
    messages=[{"role": "user", "content": prompt}]
)

print("\n🔐 Claude 威脅分析結果：\n")
print(response.content[0].text)

