# frontend.py
import streamlit as st
import requests
import re

# --- API 地址配置 ---
API_URL = "https://multi-agent-app-qj2u.onrender.com/research" 

# --- 页面基础设置 ---
st.set_page_config(page_title="多智能体研究助手", page_icon="🧠", layout="wide")

st.title("🧠 你的专属研究智能体")
st.caption("随时随地，在你的手机上进行深度研究。由 Gemini & LangChain 强力驱动。")

# --- 用户输入区域 ---
# ... (这部分代码保持不变) ...
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
        with st.spinner('智能体正在思考和研究中，这可能需要1-2分钟...'):
            try:
                payload = { "topic": topic, "mode": mode, "user_profile": user_profile }
                response = requests.post(API_URL, json=payload, timeout=300)
                
                if response.status_code == 200:
                    result = response.json()
                    output_text = result['output']
                    
                    st.divider()
                    st.subheader("📜 研究简报")
                    
                    # --- ✨ 全新的美化渲染逻辑 ✨ ---
                    # 从报告中提取标题信息并展示
                    title_match = re.search(r"# (.*?)\n\n\*\*面向 \(To\):(.*?)\n\*\*来自 \(From\):(.*?)\n\*\*主题 \(Topic\):(.*?)\n", output_text)
                    if title_match:
                        st.markdown(f"## {title_match.group(1).strip()}")
                        st.caption(f"面向: {title_match.group(2).strip()} | 来自: {title_match.group(3).strip()} | 主题: {title_match.group(4).strip()}")
                    
                    # 使用我们定义的标记来分割报告
                    parts = re.split(r'###-(?:SUMMARY|TREND|ADVICE)-###', output_text)
                    
                    if len(parts) >= 4:
                        summary_content = parts[1]
                        trend_content_1 = parts[2]
                        trend_content_2 = parts[3] # 假设总有两个趋势
                        advice_content = parts[4] if len(parts) > 4 else ""

                        # 1. 渲染摘要
                        with st.container(border=True):
                            st.markdown(summary_content.strip())

                        # 2. 用可折叠容器渲染每个趋势
                        st.markdown("---")
                        with st.expander("深度剖析：趋势一", expanded=True):
                            st.markdown(trend_content_1.strip())
                        
                        with st.expander("深度剖析：趋势二"):
                            st.markdown(trend_content_2.strip())
                        
                        # 3. 渲染学习建议
                        st.markdown("---")
                        st.markdown("### 🎓 给你的学习建议")
                        st.success(advice_content.strip())

                    else:
                        # 如果解析失败，就按老方法直接显示
                        st.markdown(output_text)
                
                else:
                    st.error(f"请求失败，服务器返回错误: {response.status_code}")
                    st.error(response.text)
                    
            except requests.exceptions.RequestException as e:
                st.error(f"网络连接失败，请确保后端 API 服务正在运行。")
                st.error(f"错误详情: {e}")

