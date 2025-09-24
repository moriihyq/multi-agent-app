# agent_factory.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from tools import research_topic
from prompts import AI_ANALYST_PROMPT, GENERAL_ANALYST_PROMPT

def create_agent_executor(mode: str) -> AgentExecutor:
    """
    一个工厂函数，根据所选模式创建并返回一个 AgentExecutor。
    
    Args:
        mode (str): 期望的智能体模式，可选值为 "ai" 或 "general"。
        
    Returns:
        AgentExecutor: 一个配置完毕、随时可以被调用的智能体。
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.6)
    tools = [research_topic]

    if mode == "ai":
        prompt_template = AI_ANALYST_PROMPT
    elif mode == "general":
        prompt_template = GENERAL_ANALYST_PROMPT
    else:
        raise ValueError(f"未知的模式: {mode}。请选择 'ai' 或 'general'。")

    prompt = PromptTemplate.from_template(prompt_template)
    agent = create_react_agent(llm, tools, prompt)
    

    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
