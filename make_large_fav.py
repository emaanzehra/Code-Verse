from PIL import Image, ImageChops

src = 'edited-image-1778364356061.png'

def load_im(path):
    im = Image.open(path).convert('RGBA')
    return im

def auto_crop_to_content(im):
    # Create alpha mask: if image has transparency use it, otherwise detect non-white pixels
    if 'A' in im.getbands():
        alpha = im.split()[-1]
        bbox = alpha.getbbox()
        if bbox:
            return im.crop(bbox)
    # fallback: compute bbox of non-white pixels
    bg = Image.new('RGBA', im.size, (255,255,255,255))
    diff = ImageChops.difference(im.convert('RGBA'), bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

def make_square_canvas(im, size, padding=0.08):
    # im should be cropped to content; paste into square canvas with some padding
    w,h = im.size
    # compute target inner size (account padding fraction)
    inner = int(size * (1 - padding*2))
    # resize im to fit inner box
    ratio = min(inner/w, inner/h)
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
    # Create sizes we want
    targets = [512, 256, 180, 128, 96, 64, 48, 32, 16]
    for t in targets:
        out = f'favicon-{t}.png'
        canvas = make_square_canvas(cropped, t, padding=0.10)
        canvas.save(out)
        print('Saved', out)
    # apple-touch
    Image.open('favicon-180.png').save('apple-touch-icon.png')
    # Create favicon.ico with common sizes
    ico_sizes = [16,32,48,64,128,256]
    frames = [Image.open(f'favicon-{s}.png') for s in ico_sizes]
    frames[0].save('favicon.ico', sizes=[(s,s) for s in ico_sizes])
    print('Saved favicon.ico')
