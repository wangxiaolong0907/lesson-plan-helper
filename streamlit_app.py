"""
教案自动生成助手 - Streamlit 版本（支持 Coze API）
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
    base_url: str,
    model: str
) -> str:
    """
    使用 OpenAI 兼容的 API 生成教案
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
    
    # API 配置 - 支持多种平台
    st.markdown("### 🔧 API 配置")
    
    # 平台选择
    platform = st.selectbox(
        "选择平台",
        ["Coze（扣子）", "OpenAI", "火山方舟", "自定义"],
        help="选择使用的 AI 平台"
    )
    
    # 根据平台设置默认值
    if platform == "Coze（扣子）":
        default_api_key = os.getenv("COZE_API_KEY", "")
        default_base_url = os.getenv("COZE_BASE_URL", "https://api.coze.cn/v1")
        default_model = os.getenv("COZE_MODEL", "coze-pro")
        st.success("✅ 已切换到 Coze（扣子）平台")
    elif platform == "OpenAI":
        default_api_key = os.getenv("OPENAI_API_KEY", "")
        default_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        default_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        st.info("💡 已切换到 OpenAI 平台")
    elif platform == "火山方舟":
        default_api_key = os.getenv("DOUBAO_API_KEY", "")
        default_base_url = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/v3")
        default_model = os.getenv("DOUBAO_MODEL", "doubao-pro-32k")
        st.warning("⚠️ 已切换到火山方舟平台")
    else:
        default_api_key = ""
        default_base_url = ""
        default_model = ""
    
    # 显示配置说明
    if default_api_key:
        st.info("✅ API Key 已配置，无需手动输入")
    else:
        st.info("💡 请在下方的 API Key 输入框中输入您的 API Key")
    
    st.markdown("---")
    
    # API 输入
    api_key = st.text_input(
        "API Key",
        value=default_api_key,
        type="password" if not default_api_key else "default",
        help="输入您的 API Key",
        placeholder="pat_xxxxxxxxxx 或 sk-xxxxxxxxx"
    )
    
    base_url = st.text_input(
        "Base URL",
        value=default_base_url,
        help="API Base URL",
        placeholder="https://api.coze.cn/v1"
    )
    
    model = st.text_input(
        "模型名称 / Bot ID",
        value=default_model,
        help="模型名称或 Bot ID",
        placeholder="coze-pro 或 bot_id"
    )
    
    # 平台说明
    st.markdown("---")
    st.markdown("### 📋 平台说明")
    
    if platform == "Coze（扣子）":
        st.markdown("""
        **Coze（扣子）配置：**
        
        1. 访问：https://www.coze.cn/open/api
        2. 获取 API Key
        3. Base URL: `https://api.coze.cn/v1`
        4. 模型名称：`coze-pro` 或 Bot ID
        
        **优势：**
        - ✅ 免费额度
        - ✅ 中文优化
        - ✅ 配置简单
        """)
    elif platform == "OpenAI":
        st.markdown("""
        **OpenAI 配置：**
        
        1. 访问：https://platform.openai.com/api-keys
        2. 获取 API Key
        3. Base URL: `https://api.openai.com/v1`
        4. 模型名称：`gpt-4o-mini`
        
        **优势：**
        - ✅ 最稳定
        - ✅ 效果最好
        - ✅ 文档完善
        """)
    elif platform == "火山方舟":
        st.markdown("""
        **火山方舟配置：**
        
        1. 访问：https://console.volcengine.com/ark
        2. 获取 API Key
        3. Base URL: `https://ark.cn-beijing.volces.com/v3`
        4. 模型名称：`doubao-pro-32k`
        
        **注意：**
        ⚠️ 配置较复杂，建议使用 Coze 或 OpenAI
        """)
    
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
                st.info(f"💡 当前使用平台：{platform}")
                st.info("💡 请检查 API Key、Base URL 和模型名称是否正确")
                if platform == "火山方舟":
                    st.warning("⚠️ 火山方舟配置较复杂，建议切换到 Coze 或 OpenAI")


# 使用说明
with st.expander("💡 使用说明"):
    st.markdown("""
    ### 如何使用
    
    1. **选择平台**：
       - 在左侧边栏选择使用的 AI 平台
       - 推荐：Coze（扣子）或 OpenAI
    
    2. **配置 API**：
       - 输入 API Key
       - 输入 Base URL（会自动填充默认值）
       - 输入模型名称（会自动填充默认值）
    
    3. **输入课程信息**：
       - 课程主题：例如"分数的加减法"
       - 课时：例如"2课时（90分钟）"
       - 教学目标：详细描述教学目标
    
    4. **生成教案**：
       - 点击"✨ 生成教案"按钮
       - 等待生成完成
       - 可以下载为 Markdown 文件
    
    ### 平台对比
    
    | 平台 | 免费额度 | 中文支持 | 稳定性 | 推荐度 |
    |------|---------|---------|--------|--------|
    | **Coze（扣子）** | ✅ 有 | ✅ 优秀 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
    | **OpenAI** | ⚠️ 付费 | ✅ 优秀 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
    | **火山方舟** | ✅ 有 | ✅ 优秀 | ⭐⭐⭐ | ⭐⭐ |
    
    ### 如何获取 Coze API Key
    
    1. 访问：https://www.coze.cn/open/api
    2. 登录/注册 Coze 账号
    3. 点击"个人访问令牌"
    4. 创建令牌
    5. 复制保存
    
    ### Coze 配置示例
    
    ```
    平台: Coze（扣子）
    API Key: pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    Base URL: https://api.coze.cn/v1
    模型: coze-pro
    ```
    
    ### 如何获取 OpenAI API Key
    
    1. 访问：https://platform.openai.com/api-keys
    2. 注册/登录 OpenAI 账号
    3. 点击 "Create new secret key"
    4. 复制保存
    
    ### OpenAI 配置示例
    
    ```
    平台: OpenAI
    API Key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    Base URL: https://api.openai.com/v1
    模型: gpt-4o-mini
    ```
    
    ### 注意事项
    
    - Coze 有免费额度，适合测试和日常使用
    - OpenAI 需要付费，但效果最稳定
    - 火山方舟配置复杂，不推荐新手使用
    - API Key 请妥善保管，不要泄露
    """)
