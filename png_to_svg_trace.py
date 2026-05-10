from PIL import Image
import numpy as np
import potrace

src = 'favicon.png'
out_svg = 'icon.svg'

im = Image.open(src).convert('L')
# resize to moderate size for tracing if extremely large
max_dim = 1024
if max(im.size) > max_dim:
    ratio = max_dim / max(im.size)
    im = im.resize((int(im.size[0]*ratio), int(im.size[1]*ratio)), Image.LANCZOS)

arr = np.array(im)
# threshold to binary (invert if background is transparent/white)
# assume foreground is colored on transparent; use alpha if available
orig = Image.open(src).convert('RGBA')
alpha = orig.split()[-1]
if alpha.getextrema()[0] < 255:
    # has transparency, use alpha as mask
    mask = np.array(alpha) > 10
else:
    # no transparency, threshold luminance
    mask = arr < 200

bmp = potrace.Bitmap(mask.astype(np.uint8))
path = bmp.trace()

w,h = im.size
svg_parts = []
svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">')
svg_parts.append('<g fill="#00FF00">')
for curve in path:
    d = []
    start = curve.start_point
    d.append(f'M {start.x} {start.y}')
    for segment in curve:
        if segment.is_corner:
            c = segment.c
            d.append(f'L {c.x} {c.y}')
        else:
            c1 = segment.c1
            c2 = segment.c2
            end = segment.end_point
            d.append(f'C {c1.x} {c1.y} {c2.x} {c2.y} {end.x} {end.y}')
    d.append('Z')
    svg_parts.append(f'<path d="{' '.join(d)}" />')
svg_parts.append('</g>')
svg_parts.append('</svg>')

svg_content = '\n'.join(svg_parts)
with open(out_svg, 'w', encoding='utf-8') as f:
    f.write(svg_content)
print('Saved', out_svg)
