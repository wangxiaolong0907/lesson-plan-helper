"""
教案自动生成助手 - Web应用
提供Web界面供用户输入课程信息并生成教案
"""

import os
import sys
from flask import Flask, render_template, request, jsonify

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.agent import generate_lesson_plan_with_agent

app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """生成教案接口"""
    try:
        data = request.get_json()
        
        course_topic = data.get('course_topic', '')
        class_hours = data.get('class_hours', '')
        teaching_objectives = data.get('teaching_objectives', '')
        
        # 验证输入
        if not all([course_topic, class_hours, teaching_objectives]):
            return jsonify({
                'success': False,
                'error': '请完整填写所有字段'
            }), 400
        
        # 使用Agent生成教案
        lesson_plan = generate_lesson_plan_with_agent(course_topic, class_hours, teaching_objectives)
        
        return jsonify({
            'success': True,
            'data': lesson_plan
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'生成教案时出错：{str(e)}'
        }), 500


if __name__ == '__main__':
    # 从环境变量获取端口，默认8080（用于公网访问）
    port = int(os.getenv('FLASK_PORT', 8080))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    print(f"教案自动生成助手启动中...")
    print(f"访问地址: http://{host}:{port}")
    print(f"公网访问地址: https://64ece794-6d53-4f0a-87cc-81f93298f911.dev.coze.site")
    
    app.run(host=host, port=port, debug=False)
