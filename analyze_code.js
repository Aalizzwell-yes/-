
// 简单的代码分析脚本
const fs = require('fs');

// 读取HTML文件
const html = fs.readFileSync('/workspace/snake_game.html', 'utf8');

console.log('📊 代码分析报告');
console.log('='.repeat(50));

// 查找潜在问题
const issues = [];

// 1. 检查硬编码的魔法数字
if (html.includes('480,480')) {
  issues.push({
    severity: 'medium',
    issue: '硬编码画布尺寸 (480,480)',
    suggestion: '建议使用常量定义：const CANVAS_WIDTH = 480, CANVAS_HEIGHT = 480'
  });
}

// 2. 检查是否有重复代码
if ((html.match(/drawAll/g) || []).length > 2) {
  issues.push({
    severity: 'low',
    issue: 'drawAll 被多次调用',
    suggestion: '可以考虑优化渲染逻辑'
  });
}

// 3. 检查是否有内存泄漏风险
if (html.includes('addEventListener')) {
  issues.push({
    severity: 'low',
    issue: '事件监听器可能未清理',
    suggestion: '考虑在页面卸载时清理事件监听器'
  });
}

// 4. 检查性能问题
if (html.includes('forEach') && html.includes('requestAnimationFrame')) {
  issues.push({
    severity: 'medium',
    issue: '可能的性能瓶颈',
    suggestion: '考虑优化粒子系统和游戏对象的更新逻辑'
  });
}

// 5. 检查代码结构
const lines = html.split('\n');
const jsLines = lines.slice(html.indexOf('&lt;script&gt;') + 1, html.indexOf('&lt;/script&gt;'));

if (jsLines.length &gt; 400) {
  issues.push({
    severity: 'low',
    issue: '单文件代码过长',
    suggestion: '建议将代码拆分为多个模块'
  });
}

console.log(`\n✅ 发现 ${issues.length} 个潜在问题：`);

issues.forEach((item, idx) =&gt; {
  const icon = item.severity === 'high' ? '🔴' : item.severity === 'medium' ? '🟡' : '🟢';
  console.log(`\n${icon} ${idx + 1}. ${item.issue}`);
  console.log(`   💡 建议：${item.suggestion}`);
});

console.log('\n\n🎨 代码优点：');
console.log('• 使用了模块化的 IIFE 封装');
console.log('• 实现了音频反馈系统');
console.log('• 支持触摸和鼠标控制');
console.log('• 有粒子特效系统');
