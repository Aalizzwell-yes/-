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
            "path": str(skill_md.parent),
            "aliases": []
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
        
        # 为常见技能添加中文别名
        info["aliases"] = get_chinese_aliases(info["name"], info["title"])
        
        return info
    except Exception:
        return None

def get_chinese_aliases(name: str, title: str) -> List[str]:
    """获取技能的中文别名"""
    aliases = []
    name_lower = name.lower()
    
    # 常见技能的中文别名映射
    alias_map = {
        "doubao": ["豆包", "db"],
        "browser": ["浏览器", "浏览"],
        "cocoloop": ["coco", "循环"],
        "playwright": ["剧作家", "pw"],
        "skill": ["技能", "快捷"],
    }
    
    for key, alias_list in alias_map.items():
        if key in name_lower:
            aliases.extend(alias_list)
    
    # 如果标题已经是中文，添加到别名
    if any('\u4e00' <= char <= '\u9fff' for char in title):
        aliases.append(title)
    
    return aliases

def extract_skill_from_json(skill_json: Path) -> Dict[str, str]:
    """从 .skill JSON 文件中提取技能信息"""
    try:
        with open(skill_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            name = data.get("name", skill_json.stem)
            title = data.get("title", data.get("name", skill_json.stem))
            
            return {
                "name": name,
                "title": title,
                "description": data.get("description", ""),
                "icon": data.get("icon", "📦"),
                "path": str(skill_json.parent),
                "aliases": get_chinese_aliases(name, title)
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
                aliases = skill.get("aliases", [])
                alias_str = f" (别名：{', '.join(aliases)})" if aliases else ""
                result += f"  {skill['icon']} @{skill['name']}{alias_str} - {skill['title']}\n"
        result += "\n"
    
    # 显示所有技能
    result += "📋 所有技能：\n"
    for i, skill in enumerate(skills_sorted, 1):
        fav_mark = "⭐" if skill["name"] in favorite_names else ""
        aliases = skill.get("aliases", [])
        alias_str = f" (别名：{', '.join(aliases)})" if aliases else ""
        result += f"  {i}. {skill['icon']} @{skill['name']}{alias_str} - {skill['title']}\n"
        if skill["description"]:
            result += f"      {skill['description']}\n"
    
    result += "\n💡 使用 @<技能名> 或 @<中文别名> 快速调用，例如：@豆包 你好！"
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
        aliases = [a.lower() for a in skill.get("aliases", [])]
        
        # 检查名称、标题、描述和别名
        found = (keyword == name or 
                 keyword in title or 
                 keyword in desc or
                 any(keyword in alias for alias in aliases) or
                 keyword in name)
        
        if config.get("searchFuzzy", True):
            if (keyword in name or keyword in title or keyword in desc or 
                any(keyword in alias for alias in aliases)):
                results.append(skill)
        elif found:
            results.append(skill)
    
    if not results:
        return f"🔍 未找到包含 '{keyword}' 的技能。"
    
    result = f"🔍 搜索结果（关键词：{keyword}）：\n\n"
    for i, skill in enumerate(results, 1):
        aliases = skill.get("aliases", [])
        alias_str = f" (别名：{', '.join(aliases)})" if aliases else ""
        result += f"  {i}. {skill['icon']} @{skill['name']}{alias_str} - {skill['title']}\n"
        if skill["description"]:
            result += f"      {skill['description']}\n"
    
    return result

def find_skill_by_name_or_alias(query: str) -> Dict[str, str]:
    """根据名称或别名查找技能"""
    skills = find_skills()
    query_lower = query.lower()
    
    for skill in skills:
        # 检查名称
        if skill["name"].lower() == query_lower:
            return skill
        # 检查标题
        if skill["title"].lower() == query_lower:
            return skill
        # 检查别名
        aliases = skill.get("aliases", [])
        if query_lower in [a.lower() for a in aliases]:
            return skill
    
    return None

def favorite_skill(skill_name: str) -> str:
    """收藏技能"""
    config = load_config()
    favorites = config.get("favorites", [])
    
    # 查找技能（支持别名）
    skill = find_skill_by_name_or_alias(skill_name)
    
    if not skill:
        return f"❌ 未找到技能 '{skill_name}'。"
    
    actual_name = skill["name"]
    if actual_name in favorites:
        return f"⚠️ 技能 '{actual_name}' 已经在收藏夹中。"
    
    favorites.append(actual_name)
    config["favorites"] = favorites
    save_config(config)
    
    return f"⭐ 已收藏技能：{actual_name}（别名：{', '.join(skill.get('aliases', []))}）"

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
    return """⚡ 技能快捷指令使用帮助（全中文支持）：

📝 基本命令：
  @          - 显示所有技能快捷菜单
  @?         - 显示此帮助
  @列表       - 列出所有技能（也可输入 @list）
  @搜索 <关键词>  - 搜索技能（也可输入 @search）
  @收藏 <技能名> - 收藏技能（也可输入 @favorite）
  @我的收藏    - 显示收藏的技能（也可输入 @favorites）

🎯 快速调用：
  @<技能名> <命令> - 快速调用指定技能
  @<中文别名> <命令> - 也可以用中文别名调用
  
  例如：
    @豆包 你好！
    @浏览器 打开百度
    @coco 搜索 python
    @技能快捷 显示帮助

💡 提示：
  - 收藏的技能会优先显示
  - 支持模糊搜索和中文别名
  - 输入 @ 后会自动弹出技能选择菜单
  - 所有命令都支持中文和英文两种写法
"""

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(list_skills())
        return
    
    command = sys.argv[1]
    
    # 中文命令映射
    command_map = {
        "列表": "list",
        "帮助": "help",
        "搜索": "search",
        "收藏": "favorite",
        "我的收藏": "favorites",
    }
    
    # 处理带 @ 前缀的命令
    if command.startswith("@"):
        base_command = command[1:]
        if base_command in command_map:
            command = command_map[base_command]
        elif base_command == "?":
            command = "help"
        elif base_command == "":
            command = "list"
        else:
            # 可能是 @<技能名> 的形式
            pass
    elif command in command_map:
        command = command_map[command]
    
    if command == "list" or command == "@list" or command == "列表":
        print(list_skills())
    elif command == "help" or command == "@?" or command == "?" or command == "帮助":
        print(show_help())
    elif command == "search" or command.startswith("@search") or command == "搜索":
        keyword = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not keyword:
            print("❌ 请提供搜索关键词。用法：@搜索 <关键词>")
        else:
            print(search_skills(keyword))
    elif command == "favorite" or command.startswith("@favorite") or command == "收藏":
        skill_name = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not skill_name:
            print("❌ 请提供技能名。用法：@收藏 <技能名>")
        else:
            print(favorite_skill(skill_name))
    elif command == "favorites" or command == "@favorites" or command == "我的收藏":
        print(show_favorites())
    elif command == "@":
        print(list_skills())
    else:
        # 默认显示列表
        print(list_skills())

if __name__ == "__main__":
    main()
