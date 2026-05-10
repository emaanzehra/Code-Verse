import cv2
import numpy as np
from PIL import Image

src = 'favicon.png'
out_svg = 'icon.svg'

# Load with alpha preserved via PIL then convert to OpenCV
orig = Image.open(src).convert('RGBA')
arr = np.array(orig)
alpha = arr[:,:,3]
if alpha.max() > 10:
    mask = (alpha > 10).astype(np.uint8)*255
else:
    # fallback threshold on luminance
    gray = cv2.cvtColor(arr[:,:,:3], cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)

# find contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# get average color of non-transparent pixels
rgb = arr[:,:,:3]
mask_bool = mask.astype(bool)
if mask_bool.any():
    avg_color = rgb[mask_bool].mean(axis=0).astype(int)
    fill = f'rgb({avg_color[0]},{avg_color[1]},{avg_color[2]})'
else:
    fill = 'black'

h, w = mask.shape
svg_parts = []
svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">')
svg_parts.append(f'<g fill="{fill}">')

for cnt in contours:
    # simplify contour
    eps = 0.01 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, eps, True)
    if approx.shape[0] < 3:
        continue
    path = []
    for i,pt in enumerate(approx):
        x,y = pt[0]
        cmd = 'M' if i==0 else 'L'
        path.append(f'{cmd} {x} {y}')
    path.append('Z')
    svg_parts.append(f'<path d="{' '.join(path)}" />')

svg_parts.append('</g>')
svg_parts.append('</svg>')

with open(out_svg, 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg_parts))
print('Saved', out_svg)
