# 🚀 更新配置后的部署步骤

## ✅ 已完成的修改

1. **修改了 `streamlit_app.py`**
   - 默认使用火山方舟（豆包）模型
   - 支持从环境变量读取 API Key
   - 添加了预配置提示

2. **创建了配置说明文档**
   - `CONFIG_DOUBAO_API.md` - 详细的配置步骤

---

## 📋 需要更新的文件

**需要更新到 GitHub：**
- `streamlit_app.py` - 已修改
- `CONFIG_DOUBAO_API.md` - 新创建

---

## 🔄 更新部署步骤

### 第一步：更新 GitHub 仓库

**方法 A：通过网页更新（最简单）**

1. 打开你的 GitHub 仓库
2. 点击 `streamlit_app.py` 文件
3. 点击右上角的 **"✏️ 编辑"**
4. 复制本地的 `streamlit_app.py` 内容
5. 粘贴替换
6. Commit message: `Update app to use Doubao model with env var support`
7. 点击 "Commit changes"

8. 创建新文件 `CONFIG_DOUBAO_API.md`
9. 复制本地的 `CONFIG_DOUBAO_API.md` 内容
10. 粘贴
11. Commit message: `Add Doubao API configuration guide`
12. 点击 "Commit changes"

**方法 B：通过 Git 命令**

```bash
cd /workspace/projects
git add streamlit_app.py CONFIG_DOUBAO_API.md
git commit -m "Update app to use Doubao model with env var support"
git push origin main
```

### 第二步：Streamlit Cloud 自动部署

Streamlit Cloud 会自动检测到 GitHub 的更新，自动重新部署。

等待 1-2 分钟，部署完成后会看到新的版本。

---

## 🔧 配置 Secrets（重要！）

部署完成后，需要配置 Secrets：

### 详细步骤：

1. 打开 Streamlit Cloud
   - 访问：https://share.streamlit.io/
   - 进入你的应用

2. 点击 **Settings** 标签

3. 找到 **Secrets** 部分

4. 点击 **"Add new secret"**

5. 添加配置：

#### 配置 1
```
Name: DOUBAO_API_KEY
Value: pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
**将 `pat_xxxxxxxxx...` 替换为你的实际 API Key**

#### 配置 2
```
Name: DOUBAO_BASE_URL
Value: https://ark.cn-beijing.volces.com/api/v3
```

#### 配置 3
```
Name: DOUBAO_MODEL
Value: doubao-pro-32k
```

6. 每添加一个配置，点击 **Save**

### 完整配置示例：

```
DOUBAO_API_KEY = pat_1234567890abcdefghijklmnopqrstuvwxyz
DOUBAO_BASE_URL = https://ark.cn-beijing.volces.com/api/v3
DOUBAO_MODEL = doubao-pro-32k
```

### 第三步：重新部署

1. 配置完 Secrets 后
2. 点击 **Deployments** 标签
3. 点击最新部署的 **"..."**
4. 点击 **Restart** 或 **Redeploy**
5. 等待 1-2 分钟

---

## ✅ 验证配置

部署完成后：

1. 打开应用链接：
   ```
   https://leappn-plan-apper-opz64hckn4rzerqoeakqz2.streamlit.app/
   ```

2. 查看左侧边栏

3. 应该显示：
   ```
   ✅ 已使用预配置的火山方舟（豆包）模型
   API Key 已配置，无需手动输入
   ```

4. **API Key 输入框应该显示默认值（遮罩显示）**

5. Base URL 和 Model 也应该有默认值

---

## 🎯 测试使用

1. 输入课程主题：`分数的加减法`
2. 输入课时：`2课时（90分钟）`
3. 输入教学目标：`学生能够理解分数的基本概念，掌握分数加减法的计算方法`
4. 点击 **"✨ 生成教案"**
5. 等待生成完成
6. 查看结果

**全程无需输入 API Key！** 🎉

---

## 📝 完整流程总结

### 步骤 1：获取 API Key（2分钟）
- 访问：https://console.volcengine.com/ark
- 创建 API Key
- 复制保存

### 步骤 2：更新 GitHub（3分钟）
- 上传修改后的 `streamlit_app.py`
- 上传 `CONFIG_DOUBAO_API.md`

### 步骤 3：配置 Secrets（3分钟）
- DOUBAO_API_KEY
- DOUBAO_BASE_URL
- DOUBAO_MODEL

### 步骤 4：重新部署（2分钟）
- 在 Streamlit Cloud 重启应用

### 步骤 5：验证使用（1分钟）
- 打开应用
- 测试生成教案

**总计：11 分钟！** ⏰

---

## 💡 快速操作（复制粘贴）

### 获取 API Key
访问：https://console.volcengine.com/ark

### Secrets 配置
```
DOUBAO_API_KEY = pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DOUBAO_BASE_URL = https://ark.cn-beijing.volces.com/api/v3
DOUBAO_MODEL = doubao-pro-32k
```

---

## 🔍 故障排查

### 问题 1：部署后还是需要输入 API Key

**解决方法：**
1. 检查 Secrets 是否配置（3个都有）
2. 确认名称拼写正确（大写）
3. 确认已重新部署
4. 清除浏览器缓存

### 问题 2：生成教案时报错

**可能原因：**
- API Key 不正确
- API Key 已过期
- 账户余额不足

**解决方法：**
1. 重新获取 API Key
2. 检查火山方舟账户余额
3. 更新 Secrets 配置
4. 重新部署

### 问题 3：更新代码后应用没有变化

**解决方法：**
1. 检查 GitHub 是否更新成功
2. 查看部署日志
3. 手动触发重新部署
4. 等待部署完成

---

## 🎉 完成后

配置完成后：

✅ 默认使用豆包模型  
✅ 无需每次输入 API Key  
✅ 随时随地快速使用  
✅ 永久有效  

---

## 📞 需要帮助？

详细配置步骤请查看：
**`CONFIG_DOUBAO_API.md`**

---

**祝你配置顺利！** 🚀
