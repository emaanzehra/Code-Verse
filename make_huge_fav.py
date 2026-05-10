from PIL import Image, ImageChops

src = 'edited-image-1778364356061.png'

def load_im(path):
    im = Image.open(path).convert('RGBA')
    return im

def auto_crop_to_content(im):
    if 'A' in im.getbands():
        alpha = im.split()[-1]
        bbox = alpha.getbbox()
        if bbox:
            return im.crop(bbox)
    bg = Image.new('RGBA', im.size, (255,255,255,255))
    diff = ImageChops.difference(im.convert('RGBA'), bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

def make_square_canvas(im, size, padding=0.06):
    w,h = im.size
    inner = int(size * (1 - padding*2))
    ratio = min(max(1e-6, inner/w), max(1e-6, inner/h))
    new_w = max(1, int(w*ratio))
    new_h = max(1, int(h*ratio))
    im_resized = im.resize((new_w,new_h), Image.LANCZOS)
    canvas = Image.new('RGBA', (size,size), (0,0,0,0))
    x = (size - new_w)//2
    y = (size - new_h)//2
    canvas.paste(im_resized, (x,y), im_resized)
    return canvas

if __name__ == '__main__':
    im = load_im(src)
    cropped = auto_crop_to_content(im)
    # Large sizes requested
    targets = [1024, 2048, 4096]
    for t in targets:
        out = f'favicon-{t}.png'
        canvas = make_square_canvas(cropped, t, padding=0.08)
        canvas.save(out)
        print('Saved', out)
    # Also regenerate 512 and 256 just in case
    for t in [512,256]:
        out = f'favicon-{t}.png'
        canvas = make_square_canvas(cropped, t, padding=0.08)
        canvas.save(out)
        print('Saved', out)
    print('Done generating huge PNG favicons')
