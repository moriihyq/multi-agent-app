# tools.py

import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def research_topic(topic: str) -> list[dict]:
    """
    一个专业的研究工具。它会搜索并返回一个包含多个信息源的列表。
    列表中的每一项都是一个字典，包含 'url' 和 'content' 两个键。
    这个结构化的输出是为了方便后续进行引用和溯源。
    """
    print(f"--- [工具执行中]: 正在为主题 '{topic}' 进行结构化信息检索... ---")
    try:
        response = tavily_client.search(
            query=topic, 
            search_depth="advanced",
            max_results=5
        )
        
        structured_results = [{"url": res["url"], "content": res["content"]} for res in response.get("results", [])]
        return structured_results
    except Exception as e:
        print(f"--- [工具错误]: Tavily 搜索失败: {e} ---")

        return []


