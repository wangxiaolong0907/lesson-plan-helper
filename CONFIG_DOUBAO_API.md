# 🔧 配置火山方舟（豆包）API Key - 免去每次输入

## 📋 说明

已经将应用默认配置为使用火山方舟（豆包）模型。只需在 Streamlit Cloud 中配置一次 API Key，以后就不需要每次输入了。

---

## 🚀 配置步骤（2分钟）

### 第一步：获取火山方舟 API Key

1. 访问：https://console.volcengine.com/ark
2. 登录/注册火山引擎账号（免费）
3. 进入左侧菜单：**API 密钥管理**
4. 点击 **"创建 API Key"**
5. 复制生成的 API Key（**注意：只显示一次，务必保存！**）
6. 格式类似：`pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 第二步：在 Streamlit Cloud 中配置 Secrets

1. 打开你的 Streamlit 应用
   ```
   https://leappn-plan-apper-opz64hckn4rzerqoeakqz2.streamlit.app/
   ```

2. 点击右上角的 **"Manage app"** 或者访问：
   - https://share.streamlit.io/
   - 进入你的应用

3. 点击 **Settings** 标签

4. 找到 **Secrets** 部分，点击 **"Add new secret"**

5. 添加以下 3 个配置：

#### 配置 1：API Key
```
名称: DOUBAO_API_KEY
值: pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
（将 pat_xxxxxxxxx... 替换为你的实际 API Key）
```

点击 **Save**

#### 配置 2：Base URL
```
名称: DOUBAO_BASE_URL
值: https://ark.cn-beijing.volces.com/api/v3
```

点击 **Save**

#### 配置 3：Model
```
名称: DOUBAO_MODEL
值: doubao-pro-32k
```

点击 **Save**

**Secrets 应该是这样的：**
```
DOUBAO_API_KEY = pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DOUBAO_BASE_URL = https://ark.cn-beijing.volces.com/api/v3
DOUBAO_MODEL = doubao-pro-32k
```

### 第三步：重新部署应用

1. 在应用页面，点击 **"Deployments"** 标签
2. 找到最新部署记录
3. 点击右上角的 **"..."** 菜单
4. 点击 **"Restart"** 或 **"Redeploy"**
5. 等待 1-2 分钟

---

## ✅ 验证配置

重新部署后：

1. 打开应用
2. 查看左侧边栏
3. 应该显示：**✅ 已使用预配置的火山方舟（豆包）模型**
4. **不再需要手动输入 API Key**

---

## 🎯 使用方法

配置完成后，直接使用：

1. 打开应用链接
2. 输入课程信息：
   - 课程主题
   - 课时
   - 教学目标
3. 点击 **"✨ 生成教案"**
4. 等待生成完成
5. 查看结果，下载教案

**全程无需输入 API Key！** 🎉

---

## 📝 可用的豆包模型

可以在 Secrets 中修改 `DOUBAO_MODEL` 的值：

| 模型名称 | 说明 | 上下文长度 | 推荐场景 |
|---------|------|----------|---------|
| `doubao-pro-32k` | 专业版 | 32K | 推荐使用 |
| `doubao-pro-256k` | 专业版长文本 | 256K | 超长教案 |
| `doubao-lite-32k` | 轻量版 | 32K | 快速响应 |
| `doubao-seed-1-8` | 种子模型 | 32K | 测试使用 |

**推荐使用 `doubao-pro-32k`，性能和价格平衡最好。**

---

## 🔒 安全说明

- ✅ Secrets 安全存储在 Streamlit 服务器
- ✅ 不会暴露给用户
- ✅ 只在你的应用中可用
- ✅ 其他用户无法查看
- ⚠️ API Key 只显示一次，务必保存

---

## 💡 常见问题

### Q: 配置后还是需要输入 API Key？

**A:** 
1. 检查 Secrets 是否正确配置（3个都有）
2. 确认已重新部署应用
3. 清除浏览器缓存重新打开

### Q: API Key 忘记保存了怎么办？

**A:** 
1. 重新访问火山方舟控制台
2. 创建新的 API Key
3. 更新 Secrets 配置
4. 重新部署

### Q: 想换回 OpenAI 怎么办？

**A:** 
1. 删除这 3 个 Secrets
2. 重新部署
3. 在应用中手动输入 OpenAI API Key

### Q: 豆包 API 有免费额度吗？

**A:** 
- 火山方舟有免费额度
- 具体额度请查看：https://console.volcengine.com/ark
- 超出后按量计费，价格很便宜

### Q: 配置错了怎么办？

**A:** 
1. 进入 Settings → Secrets
2. 点击对应的 Secret 右侧的 **"X"** 删除
3. 重新添加正确的配置
4. 重新部署

---

## 🎉 完成后

配置完成后，你的应用将：

✅ 自动使用火山方舟（豆包）模型  
✅ 无需每次输入 API Key  
✅ 随时随地快速生成教案  
✅ 永久有效，无需维护  

---

## 📞 需要帮助？

如果遇到问题：

1. **检查 Secrets 配置**
   - 3 个配置都添加了吗？
   - 名称和值都正确吗？
   - 是否保存了？

2. **检查 API Key**
   - 是否是火山方舟的 API Key？
   - 格式是否正确（pat_ 开头）？

3. **重新部署**
   - 配置 Secrets 后必须重新部署
   - 等待部署完成

4. **查看日志**
   - Streamlit Cloud 有详细的部署日志
   - 可以看到具体的错误信息

---

**祝配置顺利！配置后就不用再输入 API Key了！** 🎉
