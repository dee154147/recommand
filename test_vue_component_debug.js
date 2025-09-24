// 测试Vue组件中的showMetricInfo函数
const metricInfoData = {
  popularity: {
    title: '受欢迎程度评分',
    description: '基于用户交互行为计算的商品受欢迎程度评分',
    formula: '受欢迎程度 = (点击次数 × 0.3 + 查看次数 × 0.4 + 收藏次数 × 0.5 + 购买次数 × 1.0) / 总用户数 × 10',
    steps: [
      '获取相似商品的用户交互数据',
      '收集各类交互行为数据（点击、查看、收藏、购买）',
      '计算各类交互行为的权重分数',
      '统计交互用户总数',
      '计算加权平均分数',
      '转换为10分制评分'
    ],
    details: '该指标综合考虑了相似商品的用户交互行为，通过加权计算得出商品的受欢迎程度。'
  }
};

const showMetricInfo = (metricType) => {
  console.log('showMetricInfo called with:', metricType);
  const info = metricInfoData[metricType];
  if (!info) {
    console.log('No info found for metricType:', metricType);
    return;
  }
  
  console.log('Info found:', info);
  console.log('Title:', info.title);
  console.log('Description:', info.description);
  
  return {
    title: info.title,
    body: `
      <div class="metric-info-section">
        <h4>📊 指标说明</h4>
        <p>${info.description}</p>
      </div>
      
      <div class="metric-info-section">
        <h4>🧮 计算公式</h4>
        <div class="metric-info-formula">${info.formula}</div>
      </div>
      
      <div class="metric-info-section">
        <h4>📋 计算步骤</h4>
        <ol class="metric-info-steps">
          ${info.steps.map(step => `<li>${step}</li>`).join('')}
        </ol>
      </div>
      
      <div class="metric-info-section">
        <h4>💡 详细说明</h4>
        <p>${info.details}</p>
      </div>
    `
  };
};

// 测试函数
console.log('Testing showMetricInfo function...');
const result = showMetricInfo('popularity');
console.log('Result:', result);

// 测试不存在的指标
const result2 = showMetricInfo('nonexistent');
console.log('Result for nonexistent:', result2);
