---
name: skill-shortcuts
version: 1.0.0
description: 为所有 skills 创建调用快捷指令，当打出 @ 时自动弹出所有 skills 供选择调用
icon: ⚡
category: 工具
author: 汤圆
keywords: ["快捷指令", "skill", "自动补全", "快捷键", "效率"]
---

# 技能快捷指令插件

为所有技能创建调用快捷指令，提升使用效率。

## 功能特性

- 🎯 自动扫描并列出所有已安装的技能
- ⚡ 当输入 @ 时自动弹出技能选择菜单
- 📝 智能记忆常用技能，优先展示
- 🔍 支持技能搜索和过滤
- 💾 自定义快捷指令

## 安装说明

### TRAE 桌面端

1. 将此技能放入项目的 `skills/` 目录或 `~/.trae/skills/` 目录
2. 重启 TRAE IDE 即可生效

### 其他平台

参考对应平台的技能安装方法。

## 使用方法

### 基本用法

在对话中输入 `@` 后，会自动弹出所有可用技能的快捷菜单。

### 快捷指令

| 指令 | 功能 |
|------|------|
| `@` | 显示所有技能 |
| `@<skill-name>` | 直接调用指定技能 |
| `@?` | 显示技能帮助 |
| `@list` | 列出所有技能 |
| `@search <keyword>` | 搜索技能 |
| `@favorite <skill-name>` | 收藏技能 |
| `@favorites` | 显示收藏的技能 |

## 配置

在项目根目录创建 `skill-config.json` 文件：

```json
{
  "favorites": ["cocoloop", "browser-automation", "doubao-model"],
  "autoShowOnAt": true,
  "searchFuzzy": true
}
```

## 示例

### 基础调用
```
@豆包 你好！
@browser 打开百度
```

### 搜索技能
```
@search 浏览器
```

### 查看帮助
```
@?
```

## 开发者

如需扩展功能，查看 [DEVELOPERS.md](DEVELOPERS.md)（如果存在）。

## 更新日志

### v1.0.0
- 初始版本
- 支持 @ 触发技能菜单
- 支持技能搜索和收藏
