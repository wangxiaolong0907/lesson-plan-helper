"""
教案自动生成助手 - Agent
提供教案生成能力的智能体
"""

import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage
from coze_coding_utils.runtime_ctx.context import default_headers, new_context
from storage.memory.memory_saver import get_memory_saver

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40


def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]  # type: ignore


class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]


def build_agent(ctx=None):
    """构建教案生成Agent"""
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=[],  # 教案生成不需要外部工具，LLM直接完成
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )


def generate_lesson_plan_with_agent(course_topic: str, class_hours: str, teaching_objectives: str) -> str:
    """
    使用Agent生成教案
    
    Args:
        course_topic: 课程主题
        class_hours: 课时
        teaching_objectives: 教学目标
    
    Returns:
        生成的教案内容
    """
    agent = build_agent()
    
    user_prompt = f"""请根据以下信息生成一份结构化教案：

**课程主题**：{course_topic}
**课时**：{class_hours}
**教学目标**：{teaching_objectives}"""
    
    result = agent.invoke(
        {"messages": [HumanMessage(content=user_prompt)]},
        config={"configurable": {"thread_id": "lesson_plan_generation"}}
    )
    
    # 返回最后一条消息的内容
    if result["messages"]:
        last_message = result["messages"][-1]
        if isinstance(last_message.content, str):
            return last_message.content
        elif isinstance(last_message.content, list):
            if last_message.content and isinstance(last_message.content[0], str):
                return " ".join(last_message.content)
            else:
                text_parts = []
                for item in last_message.content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                return " ".join(text_parts)
        else:
            return str(last_message.content)
    
    return "生成失败"
