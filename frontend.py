# frontend.py
import streamlit as st
import requests

# --- API 地址配置 ---
# 【重要】现在它指向本地测试地址。部署后，我们会修改这里。
API_URL = "http://127.0.0.1:8000/research" 

# --- 页面基础设置 ---
st.set_page_config(page_title="多智能体研究助手", page_icon="🧠", layout="wide")

st.title("🧠 你的专属研究智能体")
st.caption("随时随地，在你的手机上进行深度研究。由 Gemini & LangChain 强力驱动。")

# --- 用户输入区域 ---
st.subheader("1. 选择智能体模式")
agent_mode = st.radio(
    "选择你的分析师:",
    ('AI 技术分析师', '通用证据驱动分析师'),
    captions=("专攻 AI 领域，提供深度洞察", "适用于任何话题，提供可追溯来源的报告"),
    horizontal=True
)
mode = "ai" if agent_mode == 'AI 技术分析师' else "general"

st.subheader("2. 提出你的研究问题")
topic = st.text_input("主题", placeholder="例如：大语言模型在端侧的部署挑战")

user_profile = ""
if mode == 'general':
    user_profile = st.text_input("你的背景 (可选)", placeholder="例如：华工AI大二学生", help="这能帮助智能体为你提供更个性化的报告。")

# --- 提交按钮与逻辑 ---
if st.button("🚀 开始研究", type="primary"):
    if not topic:
        st.warning("请输入一个研究主题！")
    else:
        with st.spinner('智能体正在思考和研究中，请稍候...'):
            try:
                payload = {
                    "topic": topic,
                    "mode": mode,
                    "user_profile": user_profile
                }
                
                # 通过网络请求，调用后端 API
                response = requests.post(API_URL, json=payload, timeout=300)
                
                if response.status_code == 200:
                    result = response.json()
                    st.divider()
                    st.subheader("📜 研究简报")
                    st.markdown(result['output'])
                else:
                    st.error(f"请求失败，服务器返回错误: {response.status_code}")
                    st.error(response.text)
                    
            except requests.exceptions.RequestException as e:
                st.error(f"网络连接失败，请确保后端 API 服务正在运行。")
                st.error(f"错误详情: {e}")