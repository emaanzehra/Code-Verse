from PIL import Image

src = 'edited-image-1778364356061.png'
sizes = [16, 32, 48, 64, 96, 128, 180, 256]

def ensure_rgba(im):
    if im.mode != 'RGBA':
        return im.convert('RGBA')
    return im

im = Image.open(src)
im = ensure_rgba(im)

# Save PNGs
for s in sizes:
    out = f'favicon-{s}.png'
    resized = im.resize((s, s), Image.LANCZOS)
    resized.save(out)
    print('Saved', out)

# Save apple-touch-icon (180)
im.resize((180,180), Image.LANCZOS).save('apple-touch-icon.png')
print('Saved apple-touch-icon.png')

# Create .ico containing multiple sizes (16,32,48,64)
ico_sizes = [(16,16),(32,32),(48,48),(64,64)]
# Resize into frames and save as .ico
frames = [im.resize((s,s), Image.LANCZOS) for s in [16,32,48,64]]
frames[0].save('favicon.ico', sizes=ico_sizes)
print('Saved favicon.ico')
