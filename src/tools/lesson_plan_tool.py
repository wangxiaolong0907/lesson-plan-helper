"""
教案生成工具
根据课程主题、课时、教学目标生成结构化教案
"""

import os
import json
from typing import Optional
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import HumanMessage, SystemMessage
from coze_coding_utils.runtime_ctx.context import new_context

LLM_CONFIG = "config/agent_llm_config.json"


def get_llm_config() -> dict:
    """读取LLM配置"""
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    return cfg


def generate_lesson_plan(course_topic: str, class_hours: str, teaching_objectives: str) -> str:
    """
    生成教案
    
    Args:
        course_topic: 课程主题
        class_hours: 课时（例如：2课时，90分钟）
        teaching_objectives: 教学目标
    
    Returns:
        生成的教案内容（Markdown格式）
    """
    cfg = get_llm_config()
    
    # 构建用户消息
    user_prompt = f"""请根据以下信息生成一份结构化教案：

**课程主题**：{course_topic}
**课时**：{class_hours}
**教学目标**：{teaching_objectives}

请按照配置文件中要求的输出格式生成教案。"""
    
    messages = [
        SystemMessage(content=cfg.get("sp", "")),
        HumanMessage(content=user_prompt)
    ]
    
    # 创建LLM客户端
    ctx = new_context(method="generate_lesson_plan")
    client = LLMClient(ctx=ctx)
    
    # 调用LLM生成教案
    response = client.invoke(
        messages=messages,
        model=cfg['config'].get("model"),
        temperature=cfg['config'].get('temperature', 0.7),
        top_p=cfg['config'].get('top_p', 0.9),
        max_completion_tokens=cfg['config'].get('max_completion_tokens', 10000),
        timeout=cfg['config'].get('timeout', 600)
    )
    
    # 处理响应内容
    if isinstance(response.content, str):
        return response.content
    elif isinstance(response.content, list):
        if response.content and isinstance(response.content[0], str):
            return " ".join(response.content)
        else:
            text_parts = []
            for item in response.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            return " ".join(text_parts)
    else:
        return str(response.content)
