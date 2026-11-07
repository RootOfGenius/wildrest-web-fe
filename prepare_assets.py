"""Chạy lại khi thay logo: python prepare_assets.py (cần Pillow và fontTools)."""
from pathlib import Path
from io import BytesIO
from urllib.request import urlopen
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
logo = Image.open(ROOT / 'brand/wildrest-logo.png').convert('RGBA')
for width, name in [(900, 'logo'), (520, 'logo-520')]:
    resized = logo.resize((width, width), Image.Resampling.LANCZOS)
    resized.save(OUT / f'{name}.webp', quality=83, method=6)
    if width == 900:
        resized.save(OUT / 'logo.png', optimize=True)
icon = Image.open(ROOT / 'brand/discord-icon-512.png').convert('RGBA')
icon.resize((180, 180), Image.Resampling.LANCZOS).save(OUT / 'apple-touch-icon.png', optimize=True)
icon.save(OUT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])

# Tải đầy đủ ký tự tiếng Việt, phục vụ font tại chỗ để không gọi dịch vụ ngoài.
from fontTools.ttLib import TTFont
base = 'https://raw.githubusercontent.com/google/fonts/main/ofl/'
for path, filename in [('bevietnampro/BeVietnamPro-Regular.ttf', 'be-vietnam-pro'), ('bevietnampro/BeVietnamPro-Bold.ttf', 'be-vietnam-pro-bold'), ('vt323/VT323-Regular.ttf', 'vt323')]:
    font = TTFont(BytesIO(urlopen(base + path).read()))
    font.flavor = 'woff2'
    font.save(OUT / f'{filename}.woff2')
    assert all(ord(char) in font.getBestCmap() for char in 'Sắp ra mắt Bang hội ĐĂƠƯ'), filename
for folder in ['bevietnampro', 'vt323']:
    (OUT / f'{folder}-OFL.txt').write_bytes(urlopen(base + folder + '/OFL.txt').read())

og = Image.new('RGB', (1200, 630))
pixels = ImageDraw.Draw(og)
for y in range(630):
    t = y / 629
    pixels.line((0, y, 1200, y), fill=tuple(round(a + (b - a) * t) for a, b in zip((142, 197, 255), (255, 210, 166))))
art = logo.resize((590, 590), Image.Resampling.LANCZOS)
og.paste(art, (5, 8), art)
draw = ImageDraw.Draw(og)
font_path = 'C:/Windows/Fonts/arialbd.ttf'
draw.text((620, 170), 'WILDREST.VN', font=ImageFont.truetype(font_path, 25), fill='#72421f')
draw.text((615, 225), 'Sắp ra mắt', font=ImageFont.truetype(font_path, 66), fill='#fff2cc', stroke_width=2, stroke_fill='#7a421f')
draw.text((620, 330), 'Sinh tồn chill · sống chậm,', font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 25), fill='#492f20')
draw.text((620, 370), 'xây nhà, lái xe dạo', font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 25), fill='#492f20')
draw.rectangle((0, 606, 1200, 616), fill='#5fbf3a')
draw.rectangle((0, 617, 1200, 630), fill='#7a5232')
og.save(OUT / 'og.jpg', quality=87, optimize=True)
print('Assets ready:', OUT)
