// 测试前端逻辑
const axios = require('axios');

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5004/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
  }
});

// 响应拦截器
api.interceptors.response.use(
  response => {
    const { data } = response;
    console.log('响应数据:', data);
    
    if (data.success === true) {
      return data;
    } else {
      console.error('请求失败:', data.message || '请求失败');
      return Promise.reject(new Error(data.message || '请求失败'));
    }
  },
  error => {
    console.error('网络错误:', error);
    const message = error.response?.data?.message || error.message || '网络错误';
    return Promise.reject(error);
  }
);

// 模拟前端逻辑
async function testUserLogin() {
  const userId = '张七';
  console.log(`开始测试用户登录: ${userId}`);
  
  try {
    // 尝试从后端获取用户信息
    console.log('1. 尝试获取用户信息...');
    const response = await api.get(`/v1/users/${userId}`);
    console.log('✅ 用户信息获取成功:', response.data);
    
    const currentUser = {
      id: response.data.id,
      name: response.data.username || `用户${userId}`,
      email: response.data.email || `${userId}@example.com`
    };
    
    console.log('✅ 用户登录成功:', currentUser);
    return currentUser;
    
  } catch (error) {
    console.error('❌ 获取用户信息失败:', error.message);
    
    // 检查错误类型
    if (error.response?.status === 404) {
      console.log('用户不存在，尝试创建新用户...');
      try {
        await registerTestUser(userId);
      } catch (registerError) {
        console.error('创建测试用户失败:', registerError.message);
        throw new Error('用户不存在且无法创建新用户');
      }
    } else {
      console.log('其他错误，使用模拟数据...');
      const currentUser = {
        id: userId,
        name: `用户${userId}`,
        email: `${userId}@example.com`
      };
      console.log('✅ 使用模拟用户数据:', currentUser);
      return currentUser;
    }
  }
}

async function registerTestUser(userId) {
  try {
    console.log('2. 尝试注册用户...');
    const response = await api.post('/v1/users/register', {
      user_id: userId,
      username: userId,
      email: `${userId}@example.com`
    });
    
    console.log('✅ 用户注册成功:', response.data);
    return response.data;
    
  } catch (error) {
    console.error('❌ 用户注册失败:', error.message);
    
    // 检查是否是用户已存在的错误
    if (error.response?.status === 409 || error.response?.data?.error?.includes('已存在')) {
      console.log('用户已存在，尝试重新获取用户信息...');
      try {
        const response = await api.get(`/v1/users/${userId}`);
        console.log('✅ 重新获取用户信息成功:', response.data);
        return response.data;
      } catch (getUserError) {
        console.error('重新获取用户信息失败:', getUserError.message);
        throw getUserError;
      }
    } else {
      console.error('其他注册错误');
      throw error;
    }
  }
}

// 运行测试
testUserLogin()
  .then(user => {
    console.log('🎉 测试完成，用户登录成功:', user);
  })
  .catch(error => {
    console.error('💥 测试失败:', error.message);
  });

