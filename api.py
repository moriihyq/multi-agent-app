# api.py (异步任务架构版)
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn
from agent_factory import create_agent_executor
import uuid
import time

# --- 应用和内存数据库初始化 ---
app = FastAPI(title="Multi-Agent Research API")

# 【重要】这是一个简单的内存“数据库”，用于存储任务状态。
# 在免费服务上，如果服务器休眠或重启，任务会丢失，但这对于个人使用已足够。
tasks = {}

# --- 数据模型定义 ---
class ResearchRequest(BaseModel):
    topic: str
    mode: str
    user_profile: str = "（未提供）"

# --- 后台任务执行函数 ---
def run_agent_in_background(task_id: str, request: ResearchRequest):
    """这个函数将在后台运行，不会阻塞API响应。"""
    try:
        # 标记任务开始执行
        tasks[task_id]["status"] = "running"
        tasks[task_id]["start_time"] = time.time()
        
        agent_executor = create_agent_executor(mode=request.mode)
        
        if request.mode == "ai":
            input_data = {"input": request.topic}
        else:
            input_data = {"input": request.topic, "user_profile": request.user_profile}
        
        result = agent_executor.invoke(input_data)
        
        # 任务成功完成
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = result['output']
        tasks[task_id]["end_time"] = time.time()
        
    except Exception as e:
        # 任务失败
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["result"] = f"An error occurred: {str(e)}"
        tasks[task_id]["end_time"] = time.time()

# --- API 端点定义 ---

@app.post("/start-research")
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """接收任务，立即返回一个任务ID，并在后台开始执行。"""
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "pending", "result": None}
    
    # 【核心】将耗时的 agent 调用添加到后台任务队列
    background_tasks.add_task(run_agent_in_background, task_id, request)
    
    return {"task_id": task_id}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """根据任务ID查询任务的当前状态。"""
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": task["status"]}

@app.get("/task-result/{task_id}")
async def get_task_result(task_id: str):
    """根据任务ID获取最终的执行结果。"""
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": task["status"], "result": task["result"]}
