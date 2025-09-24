# frontend.py (异步轮询架构版)
import streamlit as st
import requests
import time
import re

# --- API 地址配置 ---
# 【重要】API URL 现在指向新的端点
API_BASE_URL = "https://multi-agent-app-qj2u.onrender.com" 

# --- 页面基础设置 ---
# ... (这部分代码保持不变，为简洁省略) ...
st.set_page_config(page_title="多智能体研究助手", page_icon="🧠", layout="wide")
st.title("🧠 你的专属研究智能体")
st.caption("随时随地，在你的手机上进行深度研究。由 Gemini & LangChain 强力驱动。")
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

# --- 提交按钮与新版异步逻辑 ---
if st.button("🚀 开始研究", type="primary"):
    if not topic:
        st.warning("请输入一个研究主题！")
    else:
        try:
            # 1. 发送“开始任务”的短信
            payload = {"topic": topic, "mode": mode, "user_profile": user_profile}
            start_response = requests.post(f"{API_BASE_URL}/start-research", json=payload)
            start_response.raise_for_status() # 确保请求成功
            task_id = start_response.json()['task_id']

            st.info(f"任务已提交！任务ID: {task_id[:8]}... 正在为您处理，请保持页面开启。")
            
            # 2. 开始轮询检查状态
            status_placeholder = st.empty()
            with st.spinner("智能体正在云端进行深度研究，这可能需要1-3分钟..."):
                while True:
                    status_response = requests.get(f"{API_BASE_URL}/task-status/{task_id}")
                    status = status_response.json()['status']
                    
                    status_placeholder.text(f"当前任务状态: {status}...")
                    
                    if status == "completed" or status == "failed":
                        break
                    
                    time.sleep(5) # 每5秒检查一次

            # 3. 获取并展示最终结果
            status_placeholder.text("研究完成！正在获取报告...")
            result_response = requests.get(f"{API_BASE_URL}/task-result/{task_id}")
            final_result = result_response.json()

            if final_result['status'] == "completed":
                st.success("报告生成完毕！")
                output_text = final_result['result']
                # --- (这里是我们之前写的健壮的渲染逻辑，直接复用) ---
                # ... (为了简洁，此处省略了完整的渲染代码，请确保你保留了上一版的try/except解析逻辑)
                try:
                    header_match = re.search(r"(.+?)(?=###-SUMMARY-###)", output_text, re.DOTALL)
                    if header_match: st.markdown(header_match.group(1).strip())
                    summary_match = re.search(r"###-SUMMARY-###(.*?)(?=###-TREND-###|###-ADVICE-###)", output_text, re.DOTALL)
                    if summary_match:
                        with st.container(border=True): st.markdown(summary_match.group(1).strip())
                    st.markdown("---")
                    trend_matches = re.finditer(r"###-TREND-###(.*?)(?=###-TREND-###|###-ADVICE-###)", output_text, re.DOTALL)
                    for i, match in enumerate(trend_matches):
                        with st.expander(f"深度剖析：趋势 {i+1}", expanded=(i==0)): st.markdown(match.group(1).strip())
                    advice_match = re.search(r"###-ADVICE-###(.*)", output_text, re.DOTALL)
                    if advice_match:
                        st.markdown("---")
                        advice_content = advice_match.group(1).replace("## 3. 给你的学习建议 (Actionable Advice for Your Study)", "").strip()
                        st.markdown("### 🎓 给你的学习建议")
                        st.success(advice_content)
                except Exception:
                    st.markdown(output_text)
            else:
                st.error("任务执行失败！")
                st.error(f"错误详情: {final_result['result']}")

        except requests.exceptions.RequestException as e:
            st.error(f"无法连接到后端服务: {e}")


