# Wazuh × Claude 智慧威脅獵捕系統

## 一、專題簡介
本專題結合 **Wazuh SIEM 資安監控系統** 與 **Claude 大型語言模型（LLM）**，
建置一套「AI 輔助的威脅獵捕（Threat Hunting）系統」。

系統可自動蒐集 Wazuh 偵測到的安全事件，並透過大型語言模型進行分析，
協助管理者快速理解事件風險、目前系統狀況，以及後續可採取的處理行動。

---

## 二、系統架構說明
系統整體流程如下：

Wazuh Agent
↓
Wazuh Manager
↓
Elasticsearch（wazuh-alerts-*）
↓
Python 威脅獵捕程式
↓
Claude LLM 事件分析與建議

---

## 三、系統功能
本系統具備以下功能：

- 自動從 Wazuh 取得近期安全事件（Alerts）
- 彙整事件內容（來源主機、等級、規則描述等）
- 透過 Claude LLM 分析事件風險
- 以白話中文產出：
  - 是否存在高風險事件
  - 目前系統整體安全狀況摘要
  - 管理者可採取的建議行動

---

## 四、執行環境與需求
- Python 3.9 以上
- Wazuh 4.x
- Elasticsearch（Wazuh 預設）
- Claude API Key

---

## 五、執行方式

1. 安裝套件
```bash
pip install -r requirements.txt

3. 設定 Claude API Key
export CLAUDE_API_KEY="你的_API_KEY"


2. 執行程式
python3 wazuh_claude_threat_hunting.py

六、系統輸出範例

系統會輸出類似以下的分析結果：

🔐 Claude 威脅分析結果：
1. 判斷是否存在高風險事件
2. 目前系統狀況摘要
3. 建議管理者可採取的處理行動
