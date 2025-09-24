# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from agent_factory import create_agent_executor

# 初始化 FastAPI 应用
app = FastAPI(
    title="Multi-Agent Research API",
    description="一个可以在云端运行并随时调用的多智能体研究应用 API",
    version="1.0.0",
)

# 定义请求的数据模型，确保前端传来的数据格式正确
class ResearchRequest(BaseModel):
    topic: str
    mode: str  # "ai" or "general"
    user_profile: str = "（未提供）" # 为通用模式提供默认值

# 定义 API 的主端点，地址是 /research
@app.post("/research")
async def research(request: ResearchRequest):
    """
    接收研究请求，调用相应的智能体，并返回结果。
    """
    print(f"--- [API Received]: Mode='{request.mode}', Topic='{request.topic}' ---")
    try:
        agent_executor = create_agent_executor(mode=request.mode)
        
        if request.mode == "ai":
            input_data = {"input": request.topic}
        else: # general mode
            input_data = {
                "input": request.topic,
                "user_profile": request.user_profile
            }
        
        # 【核心】调用你的智能体
        result = agent_executor.invoke(input_data)
        
        print("--- [API Responded]: Successfully returned agent output. ---")
        return {"status": "success", "output": result['output']}
        
    except ValueError as e:
        # 如果模式错误，返回清晰的错误信息
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 如果智能体运行出错，返回服务器错误
        print(f"--- [Agent Error]: An unexpected error occurred: {e} ---")
        raise HTTPException(status_code=500, detail=f"智能体在执行时发生内部错误: {e}")

# 添加一个根路径，用于测试服务是否启动成功
@app.get("/")
def read_root():
    return {"message": "欢迎使用多智能体研究 API!"}

# 方便你在本地电脑上直接运行测试
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)