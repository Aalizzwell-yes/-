
#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

def create_trade_banner():
    # Banner size (适合公众号头图)
    width, height = 800, 500
    
    # Create canvas with gradient background (使用RGBA模式支持透明度)
    img = Image.new('RGBA', (width, height), color=(15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # 绘制渐变背景
    for y in range(height):
        r1, g1, b1 = 26, 26, 46
        r2, g2, b2 = 15, 52, 96
        ratio = y / height
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    
    # 装饰性发光圆圈
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    overlay_draw.ellipse([(300, -100), (900, 500)], fill=(0, 255, 136, 30))
    overlay_draw.ellipse([(-200, 200), (500, 900)], fill=(0, 212, 255, 20))
    
    img = Image.alpha_composite(img, overlay)
    
    try:
        # 尝试加载中文字体
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 48)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 28)
            skill_font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 20)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 16)
        except:
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 48)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 28)
                skill_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 20)
                small_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 16)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                skill_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        skill_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 绘制 TRAE Logo 区域
    # 使用半透明填充的方式
    logo_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    logo_draw = ImageDraw.Draw(logo_overlay)
    logo_draw.rectangle([(60, 40), (180, 100)], fill=(0, 255, 136, 38), outline=(0, 255, 136, 102), width=2)
    img = Image.alpha_composite(img, logo_overlay)
    
    draw.text((90, 50), "TRAE", font=title_font, fill=(0, 255, 136, 255))
    
    # 绘制标题
    main_title = "开发者必备：10大顶级技能"
    draw.text((70, 120), main_title, font=title_font, fill=(255, 255, 255, 255))
    
    # 副标题
    sub_title = "让你的开发效率翻倍！"
    draw.text((70, 180), sub_title, font=subtitle_font, fill=(184, 197, 214, 255))
    
    # 技能网格
    skills = [
        ("🎨", "前端设计"),
        ("📦", "缓存优化"),
        ("🌐", "全栈开发"),
        ("👀", "代码审查"),
        ("🔍", "通用审查"),
        ("🧪", "Web测试"),
        ("🚀", "CI/CD"),
        ("🔧", "代码修复")
    ]
    
    card_width = 150
    card_height = 90
    start_x = 70
    start_y = 240
    spacing_x = 30
    spacing_y = 20
    
    # 先绘制所有卡片背景
    cards_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    cards_draw = ImageDraw.Draw(cards_overlay)
    
    for i, (emoji, name) in enumerate(skills):
        x = start_x + (i % 4) * (card_width + spacing_x)
        y = start_y + (i // 4) * (card_height + spacing_y)
        
        # 技能卡片背景
        cards_draw.rectangle([x, y, x + card_width, y + card_height], 
                            fill=(255, 255, 255, 20), 
                            outline=(255, 255, 255, 38), width=1)
    
    img = Image.alpha_composite(img, cards_overlay)
    
    # 绘制文字和emoji
    for i, (emoji, name) in enumerate(skills):
        x = start_x + (i % 4) * (card_width + spacing_x)
        y = start_y + (i // 4) * (card_height + spacing_y)
        
        # Emoji
        draw.text((x + 55, y + 15), emoji, font=skill_font, fill=(255, 255, 255, 255))
        
        # 技能名称
        draw.text((x + 30, y + 55), name, font=small_font, fill=(255, 255, 255, 255))
    
    # 底部品牌区域
    bottom_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    bottom_draw = ImageDraw.Draw(bottom_overlay)
    bottom_draw.rectangle([(0, height - 60), (width, height)], fill=(0, 0, 0, 77))
    img = Image.alpha_composite(img, bottom_overlay)
    
    draw.text((70, height - 45), "TRAE", font=subtitle_font, fill=(0, 255, 136, 255))
    draw.text((170, height - 40), "The Real AI Engineer", font=small_font, fill=(136, 149, 168, 255))
    
    return img.convert('RGB')

if __name__ == "__main__":
    banner = create_trade_banner()
    banner.save("/workspace/TRAE_公众号推文_头图.png")
    print("✅ 头图已生成：TRAE_公众号推文_头图.png")
    print(f"保存位置：/workspace/TRAE_公众号推文_头图.png")
