"""Chuẩn bị tài nguyên (cần Pillow).

Ảnh nguồn được giữ cục bộ, chỉ các bản tối ưu trong assets được deploy.
"""
from pathlib import Path
import sys
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)

def prepare_gallery():
    for source in sorted((OUT / 'gallery').glob('anh-*.webp')):
        if not source.stem.removeprefix('anh-').isdigit():
            continue
        thumbnail = source.with_name(f'{source.stem}-640.webp')
        if thumbnail.exists() and thumbnail.stat().st_mtime >= source.stat().st_mtime:
            continue
        with Image.open(source) as image:
            resized = image.convert('RGB')
            if resized.width > 640:
                height = max(1, round(640 * resized.height / resized.width))
                resized = resized.resize((640, height), Image.Resampling.LANCZOS)
            resized.save(thumbnail, quality=82, method=6)
            print(f'{source.name}: {image.width}x{image.height} -> {thumbnail.name}')

prepare_gallery()
if '--gallery' in sys.argv:
    sys.exit(0)

def webp(source, name, width, limit):
    image = Image.open(ROOT / source).convert('RGB')
    image.thumbnail((width, width * 3), Image.Resampling.LANCZOS)
    for quality in range(82, 39, -3):
        image.save(OUT / name, quality=quality, method=6)
        if (OUT / name).stat().st_size <= limit:
            break
    assert (OUT / name).stat().st_size <= limit, name

webp('hero-desktop.png', 'hero-desktop.webp', 1920, 350000)
webp('hero-mobile.png', 'hero-mobile.webp', 820, 120000)
webp('background-ban-dem.png', 'bg-night.webp', 1440, 140000)
logo = Image.open(ROOT / 'logo-khong-vien.png').convert('RGBA')
for width, filename in [(900, 'logo-mark.webp'), (720, 'logo-mark-720.webp'), (520, 'logo-mark-520.webp'), (96, 'logo-mark-96.webp')]:
    resized = logo.copy()
    resized.thumbnail((width, width), Image.Resampling.LANCZOS)
    resized.save(OUT / filename, quality=84, method=6)
fallback = logo.copy()
fallback.thumbnail((900, 900), Image.Resampling.LANCZOS)
fallback.quantize(colors=192, method=Image.Quantize.FASTOCTREE).save(OUT / 'logo-mark.png', optimize=True)
assert (OUT / 'logo-mark.png').stat().st_size < 300000
og = ImageOps.fit(Image.open(ROOT / 'og-v2.png').convert('RGB'), (1200, 630), Image.Resampling.LANCZOS)
og.save(OUT / 'og-v2.jpg', quality=85, optimize=True)

# Chín ô lấy từ tấm icon gốc, giữ cả nền ánh sáng của bộ hình.
sheet = Image.open(ROOT / '9icon.png').convert('RGB')
boxes = [(180, 0, 540, 365), (585, 0, 965, 365), (990, 0, 1390, 365),
         (170, 365, 555, 690), (600, 355, 965, 690), (990, 350, 1390, 685),
         (165, 685, 550, 1024), (610, 685, 970, 1024), (985, 680, 1395, 1024)]
icons = OUT / 'icons'
icons.mkdir(exist_ok=True)
names = ['sinh-ton', 'van-may', 'trang-bi', 'nong-cu', 'boss', 'bang-hoi', 'giai-tri', 'dien-thoai', 'chong-hack']
for name, box in zip(names, boxes):
    icon = ImageOps.pad(sheet.crop(box), (128, 128), color='#22262b', method=Image.Resampling.LANCZOS)
    icon.quantize(colors=96).save(icons / f'{name}.png', optimize=True)
print('V2 assets ready:', sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()), 'bytes')
