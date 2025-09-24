# 🧠 Multi-Agent Research Assistant

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Frameworks](https://img.shields.io/badge/Frameworks-LangChain%20%7C%20FastAPI%20%7C%20Streamlit-green.svg)](https://python.langchain.com/)
[![LLM](https://img.shields.io/badge/LLM-Gemini%201.5%20Flash-purple.svg)](https://deepmind.google/technologies/gemini/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Render-brightgreen)](https://render.com)

将一个本地的 Python 智能体，转变为一个可以随时随地通过手机访问的云端 AI 研究助手。

---

## ✨ 现场体验

**👉 [点击这里，立即体验你的专属研究智能体！](https://multi-agent-ui.onrender.com)**

![应用截图](https://i.imgur.com/k2E8TjA.png)

## 核心功能

*   **双智能体模式**:
    *   **🤖 AI 技术分析师**: 专为 AI 领域的研究设计，提供富有洞察力的深度分析，并结合你的学习课程给出建议。
    *   **🕵️‍♂️ 通用证据驱动分析师**: 适用于任何主题，生成的每一份报告都严格基于可追溯的在线来源，并提供完整的引用列表。
*   **云原生架构**: 后端 API 和前端 UI 分离部署，确保了应用的可扩展性和稳定性。
*   **移动优先**: UI 界面专为手机浏览器优化，让你随时随地都能进行深度研究。
*   **由大模型驱动**: 核心智能体利用 LangChain 框架和 Google Gemini 模型，具备强大的思考和工具使用能力。

## 🏛️ 技术架构

本项目采用经典的客户端-服务器架构：

```
+----------------+      +------------------------+      +---------------------+
|                |      |                        |      |                     |
|  用户 (手机浏览器) |----->|  Streamlit Frontend    |----->|  FastAPI Backend    |
|                |      |  (UI / 遥控器)         |      |  (Agent / 大脑)     |
|                |      |  (on Render)           |      |  (on Render)        |
+----------------+      +------------------------+      +----------+----------+
                                                                   |
                                                                   |
                                          +------------------------+-------------------+
                                          |                                            |
                                 +--------v--------+                           +-------v--------+
                                 |                 |                           |                |
                                 |  Google Gemini  |                           |  Tavily Search |
                                 |  (LLM Engine)   |                           |  (Research Tool)|
                                 |                 |                           |                |
                                 +-----------------+                           +----------------+
```

## 🚀 部署指南

想要将这个项目部署到你自己的云端吗？请遵循以下步骤：

### 1. 准备工作

*   确保你已经安装了 [Python 3.9+](https://www.python.org/downloads/) 和 [Git](https://git-scm.com/)。
*   拥有一个 [GitHub](https://github.com/) 账户。
*   获取 API 密钥:
    *   **Google AI Studio** (`GOOGLE_API_KEY`)
    *   **Tavily AI** (`TAVILY_API_KEY`)

### 2. 本地设置

```bash
# 1. 克隆仓库到你的本地
git clone https://github.com/YOUR_USERNAME/multi-agent-app.git
cd multi-agent-app

# 2. 安装所有依赖
pip install -r requirements.txt

# 3. 创建 .env 文件
# 在项目根目录创建一个名为 .env 的文件，并填入你的 API 密钥
# 重要：.gitignore 文件已包含 .env，确保你的密钥不会被上传到 GitHub！
```

`.env` 文件内容示例:
```
GOOGLE_API_KEY="你的Google_API密钥"
TAVILY_API_KEY="你的Tavily_API密钥"
```

### 3. 云端部署 (使用 Render)

我们在 Render 上进行免费部署，这需要两个独立的 "Web Service"。

#### a. 部署后端 API

1.  在 Render 上，点击 **New+** -> **Web Service**，选择你的 GitHub 仓库。
2.  配置如下:
    *   **Name**: `my-agent-api` (或你喜欢的名字)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
3.  在 "Advanced" 标签页下，添加你在 `.env` 文件中设置的环境变量 (`GOOGLE_API_KEY` 和 `TAVILY_API_KEY`)。
4.  点击 **Create Web Service**。部署完成后，**复制**你的 API URL (例如 `https://my-agent-api.onrender.com`)。

#### b. 部署前端 UI

1.  **修改代码**: 打开 `frontend.py` 文件，将 `API_URL` 变量的值更新为你刚刚复制的后端 API URL，并在末尾加上 `/research`。
    ```python
    API_URL = "https://my-agent-api.onrender.com/research"
    ```
2.  **推送更改**: 将这个修改 `commit` 并 `push` 到你的 GitHub 仓库。
3.  **创建新服务**: 回到 Render，再次点击 **New+** -> **Web Service**，选择同一个仓库。
4.  配置如下:
    *   **Name**: `my-agent-ui`
    *   **Start Command**: `streamlit run frontend.py --server.port $PORT --server.address=0.0.0.0`
    *   (Build Command 和 Runtime 与后端相同)
5.  点击 **Create Web Service**。

部署完成后，访问你的前端 URL (`https://my-agent-ui.onrender.com`) 即可开始使用！

---
*这个项目是我从一个本地 Python 脚本逐步构建和部署到云端的学习成果。*
