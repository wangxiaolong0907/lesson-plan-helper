"""
教案自动生成助手 - Streamlit 版本
"""

import streamlit as st
import os
import json
from typing import Dict, Any

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
    
    # API 配置 - 优先从环境变量读取
    st.markdown("### 🔧 API 配置")
    
    # 从环境变量读取默认值（如果在 Streamlit Cloud 中配置了 Secrets）
    default_api_key = os.getenv("DOUBAO_API_KEY", "")
    default_base_url = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    default_model = os.getenv("DOUBAO_MODEL", "doubao-pro-32k")
    
    # 显示配置说明
    if default_api_key:
        st.success("✅ 已使用预配置的火山方舟（豆包）模型")
        st.info("API Key 已配置，无需手动输入")
    else:
        st.info("💡 提示：在 Streamlit Cloud Secrets 中配置 API Key 可避免每次输入")
    
    st.markdown("""
    **当前使用：火山方舟（豆包）**
    
    如需修改，请在下方输入：
    """)
    
    api_key = st.text_input(
        "API Key",
        value=default_api_key,
        type="password" if not default_api_key else "default",
        help="火山方舟 API Key",
        placeholder="pat_xxxxxxxxxx"
    )
    
    base_url = st.text_input(
        "Base URL",
        value=default_base_url,
        help="火山方舟 API Base URL",
        placeholder="https://ark.cn-beijing.volces.com/api/v3"
    )
    
    model = st.text_input(
        "模型名称",
        value=default_model,
        help="豆包模型名称",
        placeholder="doubao-pro-32k"
    )
    
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
    else:
        # 显示加载状态
        with st.spinner("正在生成教案，请稍候..."):
            try:
                # 调用 API 生成教案
                lesson_plan = generate_lesson_plan(
                    course_topic=course_topic,
                    class_hours=class_hours,
                    teaching_objectives=teaching_objectives,
                    api_key=api_key,
                    base_url=base_url,
                    model=model
                )
                
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
                
            except Exception as e:
                st.error(f"❌ 生成失败：{str(e)}")
                st.info("💡 请检查 API Key 和 Base URL 是否正确")


def generate_lesson_plan(
    course_topic: str,
    class_hours: str,
    teaching_objectives: str,
    api_key: str,
    base_url: str,
    model: str
) -> str:
    """
    使用 OpenAI 兼容的 API 生成教案
    """
    import requests
    
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
    url = f"{base_url.rstrip('/')}/chat/completions"
    
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
        "max_tokens": 4000
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    return result["choices"][0]["message"]["content"]


# 使用说明
with st.expander("💡 使用说明"):
    st.markdown("""
    ### 如何使用
    
    1. **配置 API**：
       - API Key 已预配置火山方舟（豆包），直接使用即可
       - Base URL: `https://ark.cn-beijing.volces.com/api/v3`
       - Model: `doubao-pro-32k`
    
    2. **输入课程信息**：
       - 课程主题：例如"分数的加减法"
       - 课时：例如"2课时（90分钟）"
       - 教学目标：详细描述教学目标
    
    3. **生成教案**：
       - 点击"✨ 生成教案"按钮
       - 等待生成完成
       - 可以下载为 Markdown 文件
    
    ### 当前配置
    
    - **模型**：火山方舟（豆包）
    - **Base URL**：https://ark.cn-beijing.volces.com/api/v3
    - **默认模型**：doubao-pro-32k
    
    ### 可用的豆包模型
    
    - `doubao-pro-32k` - 专业版，支持32K上下文（推荐）
    - `doubao-pro-256k` - 专业版长文本，支持256K上下文
    - `doubao-lite-32k` - 轻量版，响应更快
    
    ### 如何获取火山方舟 API Key
    
    1. 访问：https://console.volcengine.com/ark
    2. 注册/登录火山引擎账号
    3. 进入"API 密钥管理"
    4. 创建 API Key
    5. 复制保存（注意：只显示一次）
    
    ### 在 Streamlit Cloud 中配置 Secrets
    
    如果你想避免每次输入 API Key，可以在 Streamlit Cloud 中配置：
    
    1. 进入你的应用
    2. 点击 **Settings** → **Secrets**
    3. 添加以下配置：
       ```
       DOUBAO_API_KEY = pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       DOUBAO_BASE_URL = https://ark.cn-beijing.volces.com/api/v3
       DOUBAO_MODEL = doubao-pro-32k
       ```
    4. 点击 **Save**
    5. 重新部署应用
    
    配置后，应用会自动使用这些预配置的值，无需手动输入。
    
    ### 注意事项
    
    - API Key 在 Secrets 中安全存储，不会暴露
    - 生成时间取决于豆包模型的响应速度
    - 豆包模型在中文理解方面表现优秀
    - 建议使用 doubao-pro-32k 以获得最佳效果
    """)
