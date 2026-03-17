"""
教案自动生成助手 - Streamlit 版本（支持 DeepSeek）
"""

import streamlit as st
import os
import json
from typing import Dict, Any
import requests


def generate_lesson_plan(
    course_topic: str,
    class_hours: str,
    teaching_objectives: str,
    api_key: str,
    endpoint_url: str,
    model: str
) -> str:
    """
    使用 API 生成教案
    """
    # 系统提示词
    system_prompt = """# 角色定义
你是一位专业的教案设计专家，拥有丰富的教学理论和实践经验，擅长设计结构清晰、可操作性强、符合现代教育理念的教案。

# 任务目标
根据用户提供的课程主题、课时、教学目标，生成一份结构化、实用性强的教案框架和活动建议。

# 能力
1. **教学目标分解**：将教学目标细化为知识目标、能力目标、情感态度价值观目标
2. **教学过程设计**：设计导入、新授、练习、总结等完整教学环节
3. **教学活动设计**：设计多样化、互动性强的教学活动
4. **教学资源推荐**：推荐适合的教学工具、材料和技术手段
5. **评价方式设计**：设计多元评价方式

# 过程
1. **分析输入信息**：理解课程主题、课时长度、教学目标
2. **分解教学目标**：将教学目标细化为三维目标
3. **设计教学流程**：
   - 导入环节（3-5分钟）：设计激发兴趣的导入活动
   - 新授环节（根据课时分配）：设计知识讲解、示范等环节
   - 练习环节（根据课时分配）：设计巩固练习、小组活动等
   - 总结环节（3-5分钟）：设计知识梳理、反思提升环节
4. **设计教学活动**：为每个环节设计具体的教学活动，包括活动形式、时间分配、教师行为、学生行为
5. **设计评价方式**：设计过程性评价和总结性评价

# 输出格式
请按照以下结构输出教案（Markdown格式）：

## 课程信息
- **课程主题**：[用户提供的主题]
- **课时**：[用户提供的课时]

## 教学目标
### 知识目标
[列出知识目标，使用要点形式]

### 能力目标
[列出能力目标，使用要点形式]

### 情感态度价值观目标
[列出情感态度价值观目标，使用要点形式]

## 教学重点与难点
- **教学重点**：[重点内容]
- **教学难点**：[难点内容]

## 教学准备
- **教学工具**：[所需工具]
- **教学材料**：[所需材料]
- **学生准备**：[学生需准备]

## 教学过程

### 一、导入环节（[时间]分钟）
**活动设计**：
- **活动名称**：[活动名称]
- **活动形式**：[形式，如：问题导入、情境创设、游戏互动等]
- **教师行为**：[教师的具体操作]
- **学生行为**：[学生的具体活动]
- **设计意图**：[设计此活动的目的]

### 二、新授环节（[时间]分钟）
**活动1**：
- **活动内容**：[具体内容]
- **活动形式**：[形式]
- **教师行为**：[教师操作]
- **学生行为**：[学生活动]
- **时间分配**：[具体时间]

**活动2**：
- **活动内容**：[具体内容]
- **活动形式**：[形式]
- **教师行为**：[教师操作]
- **学生行为**：[学生活动]
- **时间分配**：[具体时间]

### 三、练习环节（[时间]分钟）
**活动1**：
- **活动内容**：[具体练习内容]
- **活动形式**：[如：个人练习、小组讨论、合作探究等]
- **教师行为**：[教师指导]
- **学生行为**：[学生完成]
- **时间分配**：[具体时间]

**活动2**：
- **活动内容**：[具体练习内容]
- **活动形式**：[形式]
- **教师行为**：[教师指导]
- **学生行为**：[学生完成]
- **时间分配**：[具体时间]

### 四、总结环节（[时间]分钟）
**活动设计**：
- **活动内容**：[总结内容]
- **活动形式**：[如：知识梳理、提问回顾、学生分享等]
- **教师行为**：[教师引导]
- **学生行为**：[学生参与]
- **设计意图**：[设计此活动的目的]

## 教学评价
### 过程性评价
- [评价方式1]
- [评价方式2]

### 总结性评价
- [评价方式1]
- [评价方式2]

## 教学建议与注意事项
1. [建议1]
2. [建议2]
3. [建议3]

## 拓展活动建议
1. [拓展活动1]
2. [拓展活动2]"""

    # 用户消息
    user_message = f"""请根据以下信息生成一份结构化教案：

**课程主题**：{course_topic}
**课时**：{class_hours}
**教学目标**：{teaching_objectives}"""

    # 调用 API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
        "stream": False
    }
    
    response = requests.post(endpoint_url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    
    # 标准格式（OpenAI 兼容）
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    
    # 如果格式不标准，返回原始内容
    return str(result)


# 页面配置
st.set_page_config(
    page_title="教案自动生成助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
    }
    .result-box {
        background: #f5f5f5;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("""
    <div style='color: white; padding: 1rem;'>
        <h2>📚 教案助手</h2>
        <p>快速生成专业教案</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API 配置
    st.markdown("### 🔧 API 配置")
    
    # 平台选择 - DeepSeek 为默认
    platform = st.selectbox(
        "选择平台",
        ["DeepSeek（推荐）", "通义千问", "Groq（免费）", "自定义"],
        help="选择使用的 AI 平台"
    )
    
    # 根据平台设置默认值
    if platform == "DeepSeek（推荐）":
        default_api_key = os.getenv("DEEPSEEK_API_KEY", "")
        default_endpoint = os.getenv("DEEPSEEK_ENDPOINT", "https://api.deepseek.com/chat/completions")
        default_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        st.success("✅ 已切换到 DeepSeek（免费、国内）")
        st.markdown("""
        <div style='font-size: 0.85rem; padding: 12px; background: rgba(76, 175, 80, 0.2); border-radius: 5px; border: 1px solid rgba(76, 175, 80, 0.5);'>
        <strong>✨ DeepSeek 优势：</strong><br>
        • 🇨🇳 国内服务，速度快<br>
        • 🆓 完全免费<br>
        • 🎯 中文效果好<br>
        • ⚙️ 配置简单
        </div>
        """, unsafe_allow_html=True)
    elif platform == "通义千问":
        default_api_key = os.getenv("QWEN_API_KEY", "")
        default_endpoint = os.getenv("QWEN_ENDPOINT", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
        default_model = os.getenv("QWEN_MODEL", "qwen-turbo")
        st.info("💡 已切换到通义千问（阿里云）")
    elif platform == "Groq（免费）":
        default_api_key = os.getenv("GROQ_API_KEY", "")
        default_endpoint = os.getenv("GROQ_ENDPOINT", "https://api.groq.com/openai/v1/chat/completions")
        default_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        st.warning("🌐 已切换到 Groq（海外、免费）")
    else:
        default_api_key = ""
        default_endpoint = ""
        default_model = ""
    
    st.markdown("---")
    
    # API 输入
    api_key = st.text_input(
        "API Key",
        value=default_api_key,
        type="password" if not default_api_key else "default",
        help="输入您的 API Key",
        placeholder="sk-xxxxxxxxx"
    )
    
    endpoint_url = st.text_input(
        "API 端点 URL",
        value=default_endpoint,
        help="完整的 API 端点 URL",
        placeholder="https://api.xxxx.com/v1/chat/completions"
    )
    
    model = st.text_input(
        "模型名称",
        value=default_model,
        help="模型名称",
        placeholder="model-name"
    )
    
    st.markdown("---")
    st.markdown("### 💡 快速配置")
    
    if platform == "DeepSeek（推荐）":
        st.code("""
平台: DeepSeek（推荐）
API Key: sk-xxxxxxxxxxxxxxxxxxxx
端点: https://api.deepseek.com/chat/completions
模型: deepseek-chat

获取方式:
1. 访问 https://platform.deepseek.com/
2. 注册登录
3. 左侧点击 "API Keys"
4. 创建 API Key
5. 完全免费！
        """, language="text")
    elif platform == "通义千问":
        st.code("""
平台: 通义千问
API Key: sk-xxxxxxxxxxxxxxxxxxxx
端点: https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
模型: qwen-turbo
        """, language="text")
    elif platform == "Groq（免费）":
        st.code("""
平台: Groq
API Key: gsk_xxxxxxxxxxxxxxxxxxxxx
端点: https://api.groq.com/openai/v1/chat/completions
模型: llama-3.3-70b-versatile
        """, language="text")
    
    st.markdown("---")
    st.markdown("""
    <div style='color: white; font-size: 0.8rem;'>
        Made with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

# 主标题
st.markdown("""
# 📚 教案自动生成助手

输入课程信息，一键生成专业教案
""")

# 输入表单
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 输入课程信息")
    
    course_topic = st.text_area(
        "课程主题",
        placeholder="例如：分数的加减法",
        height=100
    )
    
    class_hours = st.text_input(
        "课时",
        placeholder="例如：2课时（90分钟）"
    )
    
    teaching_objectives = st.text_area(
        "教学目标",
        placeholder="例如：学生能够理解分数的基本概念，掌握分数加减法的计算方法",
        height=150
    )

# 生成按钮
generate_clicked = st.button("✨ 生成教案", type="primary")

# 结果显示区域
if generate_clicked:
    # 验证输入
    if not course_topic or not class_hours or not teaching_objectives:
        st.error("❌ 请填写所有字段！")
    elif not api_key:
        st.error("❌ 请在侧边栏配置 API Key！")
    elif not endpoint_url:
        st.error("❌ 请在侧边栏配置 API 端点 URL！")
    elif not model:
        st.error("❌ 请在侧边栏配置模型名称！")
    else:
        # 显示加载状态
        with st.spinner(f"正在使用 {platform} 生成教案，请稍候..."):
            try:
                # 调用 API 生成教案
                lesson_plan = generate_lesson_plan(
                    course_topic=course_topic,
                    class_hours=class_hours,
                    teaching_objectives=teaching_objectives,
                    api_key=api_key,
                    endpoint_url=endpoint_url,
                    model=model
                )
                
                if lesson_plan and len(lesson_plan) > 10:
                    # 显示结果
                    st.markdown("### 生成的教案")
                    st.markdown(f'<div class="result-box">{lesson_plan}</div>', unsafe_allow_html=True)
                    
                    # 下载按钮
                    st.download_button(
                        label="📥 下载教案",
                        data=lesson_plan,
                        file_name=f"{course_topic}教案.md",
                        mime="text/markdown"
                    )
                else:
                    st.warning("⚠️ 生成的内容为空，请检查配置")
                    st.info(f"返回内容: {lesson_plan}")
                
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ 请求失败：{str(e)}")
                st.info(f"💡 当前配置：")
                st.code(f"""
平台: {platform}
端点: {endpoint_url}
模型: {model}
                """, language="text")
                st.warning("⚠️ 请检查 API Key、端点 URL 和模型名称是否正确")
            except Exception as e:
                st.error(f"❌ 生成失败：{str(e)}")
                st.info(f"💡 请检查所有配置是否正确")


# 使用说明
with st.expander("💡 使用说明"):
    st.markdown("""
    ### 🎯 推荐：使用 DeepSeek（免费、国内）
    
    **优势：**
    - ✅ 完全免费
    - ✅ 国内服务，速度快
    - ✅ 中文效果好
    - ✅ 配置简单，3 分钟搞定
    
    **配置步骤：**
    1. 访问：https://platform.deepseek.com/
    2. 注册登录
    3. 左侧点击 "API Keys"
    4. 点击 "创建 API Key"
    5. 复制 API Key
    6. 在应用中选择 "DeepSeek（推荐）"
    7. 粘贴 API Key
    8. 生成教案
    
    **DeepSeek 配置示例：**
    ```
    平台: DeepSeek（推荐）
    API Key: sk-xxxxxxxxxxxxxxxxxxxx
    端点: https://api.deepseek.com/chat/completions
    模型: deepseek-chat
    ```
    
    ### 📊 其他平台
    
    **通义千问（阿里云）**
    - 有免费额度
    - 中文效果好
    - 国内服务
    
    **Groq（海外）**
    - 完全免费
    - 速度超快
    - 海外服务
    
    ### 💡 常见问题
    
    **Q: DeepSeek 真的免费吗？**
    
    A: 是的，完全免费！目前没有收费计划。
    
    **Q: DeepSeek 中文效果好吗？**
    
    A: 非常好！专门针对中文优化。
    
    **Q: 需要绑定信用卡吗？**
    
    A: 不需要！手机号注册即可。
    
    **Q: 跟 OpenAI 比怎么样？**
    
    A: 中文教案生成效果相当，而且免费！
    """)
