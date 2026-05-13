#!/usr/bin/env python3
"""
技能快捷指令插件
为所有技能创建调用快捷指令
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

CONFIG_FILE = "skill-config.json"

def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    config = {
        "favorites": [],
        "autoShowOnAt": True,
        "searchFuzzy": True
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config.update(json.load(f))
        except Exception:
            pass
    return config

def save_config(config: Dict[str, Any]) -> None:
    """保存配置文件"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def find_skills() -> List[Dict[str, str]]:
    """查找所有已安装的技能"""
    skills = []
    search_paths = [
        Path("/workspace"),
        Path.cwd() / "skills",
        Path.home() / ".trae" / "skills",
        Path.home() / ".cocoloop" / "skills",
        Path.cwd() / ".agents" / "skills",
    ]
    
    for path in search_paths:
        if not path.exists() or not path.is_dir():
            continue
        
        try:
            # 检查当前路径是否是技能目录
            skill_md = path / "SKILL.md"
            if skill_md.exists():
                skill_info = extract_skill_info(skill_md, path.name)
                if skill_info:
                    skills.append(skill_info)
            
            # 检查 .skill 文件
            for skill_file in path.glob("*.skill"):
                skill_info = extract_skill_from_json(skill_file)
                if skill_info:
                    skills.append(skill_info)
            
            # 检查子目录
            for skill_dir in path.iterdir():
                if skill_dir.is_dir() and skill_dir.name not in [".git", "__pycache__"]:
                    # 检查是否有 SKILL.md
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        skill_info = extract_skill_info(skill_md, skill_dir.name)
                        if skill_info:
                            skills.append(skill_info)
                    
                    # 检查是否有同名的 .skill 文件
                    skill_json = skill_dir / f"{skill_dir.name}.skill"
                    if skill_json.exists():
                        skill_info = extract_skill_from_json(skill_json)
                        if skill_info:
                            skills.append(skill_info)
                    
                    # 检查任意 .skill 文件在这个目录中
                    for skill_file in skill_dir.glob("*.skill"):
                        skill_info = extract_skill_from_json(skill_file)
                        if skill_info:
                            skills.append(skill_info)
        except Exception:
            continue
    
    # 去重
    seen = set()
    unique_skills = []
    for skill in skills:
        if skill["name"] not in seen:
            seen.add(skill["name"])
            unique_skills.append(skill)
    
    return unique_skills

def extract_skill_info(skill_md: Path, name: str) -> Dict[str, str]:
    """从 SKILL.md 中提取技能信息"""
    try:
        content = skill_md.read_text(encoding="utf-8")
        info = {
            "name": name,
            "title": name,
            "description": "",
            "icon": "📦",
            "path": str(skill_md.parent)
        }
        
        # 尝试解析 frontmatter
        if content.startswith("---"):
            lines = content.split("---")[1].split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("name:"):
                    info["name"] = line.split(":", 1)[1].strip()
                elif line.startswith("description:"):
                    info["description"] = line.split(":", 1)[1].strip()
                elif line.startswith("icon:"):
                    info["icon"] = line.split(":", 1)[1].strip()
                elif line.startswith("title:"):
                    info["title"] = line.split(":", 1)[1].strip()
        
        return info
    except Exception:
        return None

def extract_skill_from_json(skill_json: Path) -> Dict[str, str]:
    """从 .skill JSON 文件中提取技能信息"""
    try:
        with open(skill_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "name": data.get("name", skill_json.stem),
                "title": data.get("title", data.get("name", skill_json.stem)),
                "description": data.get("description", ""),
                "icon": data.get("icon", "📦"),
                "path": str(skill_json.parent)
            }
    except Exception:
        return None

def list_skills() -> str:
    """列出所有技能"""
    config = load_config()
    skills = find_skills()
    
    if not skills:
        return "🔍 未找到任何已安装的技能。"
    
    # 排序：收藏的优先
    favorite_names = config.get("favorites", [])
    skills_sorted = sorted(skills, key=lambda s: (s["name"] not in favorite_names, s["name"]))
    
    result = "📦 已安装的技能：\n\n"
    
    # 显示收藏的技能
    if favorite_names:
        result += "⭐ 收藏：\n"
        for skill in skills_sorted:
            if skill["name"] in favorite_names:
                result += f"  {skill['icon']} @{skill['name']} - {skill['title']}\n"
        result += "\n"
    
    # 显示所有技能
    result += "📋 所有技能：\n"
    for i, skill in enumerate(skills_sorted, 1):
        fav_mark = "⭐" if skill["name"] in favorite_names else ""
        result += f"  {i}. {skill['icon']} @{skill['name']} - {skill['title']}\n"
        if skill["description"]:
            result += f"      {skill['description']}\n"
    
    result += "\n💡 使用 @<技能名> 快速调用，例如：@豆包 你好！"
    return result

def search_skills(keyword: str) -> str:
    """搜索技能"""
    config = load_config()
    skills = find_skills()
    keyword = keyword.lower()
    
    results = []
    for skill in skills:
        name = skill["name"].lower()
        title = skill["title"].lower()
        desc = skill["description"].lower()
        
        if (config.get("searchFuzzy", True) and 
            (keyword in name or keyword in title or keyword in desc)) or keyword == name:
            results.append(skill)
    
    if not results:
        return f"🔍 未找到包含 '{keyword}' 的技能。"
    
    result = f"🔍 搜索结果（关键词：{keyword}）：\n\n"
    for i, skill in enumerate(results, 1):
        result += f"  {i}. {skill['icon']} @{skill['name']} - {skill['title']}\n"
        if skill["description"]:
            result += f"      {skill['description']}\n"
    
    return result

def favorite_skill(skill_name: str) -> str:
    """收藏技能"""
    config = load_config()
    favorites = config.get("favorites", [])
    
    if skill_name in favorites:
        return f"⚠️ 技能 '{skill_name}' 已经在收藏夹中。"
    
    # 验证技能是否存在
    skills = find_skills()
    skill_exists = any(s["name"] == skill_name for s in skills)
    
    if not skill_exists:
        return f"❌ 未找到技能 '{skill_name}'。"
    
    favorites.append(skill_name)
    config["favorites"] = favorites
    save_config(config)
    
    return f"⭐ 已收藏技能：{skill_name}"

def show_favorites() -> str:
    """显示收藏的技能"""
    config = load_config()
    favorites = config.get("favorites", [])
    skills = find_skills()
    
    if not favorites:
        return "⭐ 收藏夹是空的。使用 @favorite <技能名> 收藏技能。"
    
    result = "⭐ 收藏的技能：\n\n"
    
    for name in favorites:
        skill = next((s for s in skills if s["name"] == name), None)
        if skill:
            result += f"  {skill['icon']} @{skill['name']} - {skill['title']}\n"
        else:
            result += f"  📦 @{name} (未找到)\n"
    
    return result

def show_help() -> str:
    """显示帮助信息"""
    return """⚡ 技能快捷指令使用帮助：

📝 基本命令：
  @          - 显示所有技能快捷菜单
  @?         - 显示帮助
  @list      - 列出所有技能
  @search <关键词>  - 搜索技能
  @favorite <技能名> - 收藏技能
  @favorites - 显示收藏的技能

🎯 快速调用：
  @<技能名> <命令> - 快速调用指定技能
  
  例如：
    @豆包 你好！
    @browser 打开百度
    @cocoloop search python

💡 提示：
  - 收藏的技能会优先显示
  - 支持模糊搜索
  - 输入 @ 后会自动弹出技能选择菜单
"""

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(list_skills())
        return
    
    command = sys.argv[1]
    
    if command == "list" or command == "@list":
        print(list_skills())
    elif command == "help" or command == "@?" or command == "?":
        print(show_help())
    elif command == "search" or command.startswith("@search"):
        keyword = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not keyword:
            print("❌ 请提供搜索关键词。用法：@search <关键词>")
        else:
            print(search_skills(keyword))
    elif command == "favorite" or command.startswith("@favorite"):
        skill_name = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not skill_name:
            print("❌ 请提供技能名。用法：@favorite <技能名>")
        else:
            print(favorite_skill(skill_name))
    elif command == "favorites" or command == "@favorites":
        print(show_favorites())
    elif command == "@":
        print(list_skills())
    else:
        # 默认显示列表
        print(list_skills())

if __name__ == "__main__":
    main()
