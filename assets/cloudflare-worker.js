/**
 * Cloudflare Worker 配置文件
 * 用于将教案生成助手的临时链接转换为永久链接
 *
 * 使用方法：
 * 1. 访问 https://dash.cloudflare.com
 * 2. 创建 Worker
 * 3. 复制此代码到 Worker 编辑器
 * 4. 保存并部署
 * 5. 获得永久链接
 */

// 配置：您的原始链接
const TARGET_URL = "https://64ece794-6d53-4f0a-87cc-81f93298f911.dev.coze.site";

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const proxyUrl = url.pathname + url.search;

    // 处理 CORS 预检请求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    // 构建目标 URL
    const newUrl = new URL(proxyUrl, TARGET_URL);

    // 创建新的请求
    const newRequest = new Request(newUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: 'follow',
    });

    // 移除可能导致问题的头
    newRequest.headers.delete('Host');
    newRequest.headers.delete('Origin');

    try {
      const response = await fetch(newRequest, {
        cf: {
          cacheTtl: 60,
          cacheEverything: false,
        },
      });

      // 创建新的响应
      const newResponse = new Response(response.body, response);

      // 复制响应头
      response.headers.forEach((value, key) => {
        newResponse.headers.set(key, value);
      });

      // 添加 CORS 头
      newResponse.headers.set('Access-Control-Allow-Origin', '*');
      newResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
      newResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

      return newResponse;
    } catch (error) {
      // 错误处理
      console.error('Proxy error:', error);

      return new Response(
        JSON.stringify({
          error: 'Proxy Error',
          message: error.message,
          target: TARGET_URL,
        }),
        {
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        }
      );
    }
  },
};
