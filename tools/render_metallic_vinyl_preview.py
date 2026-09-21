from PIL import Image, ImageDraw, ImageFilter
import math

W = H = 900
cx = cy = W // 2
r = 330
img = Image.new('RGBA', (W, H), (9, 10, 13, 255))
pix = img.load()

# Match the implementation's cool graphite/silver linear metallic response.
stops = [
    (0.00, (0x56, 0x60, 0x6B)),
    (0.16, (0xB9, 0xC1, 0xCA)),
    (0.31, (0x70, 0x7B, 0x87)),
    (0.48, (0xD5, 0xDA, 0xE0)),
    (0.66, (0x62, 0x6D, 0x79)),
    (0.82, (0x9E, 0xA8, 0xB3)),
    (1.00, (0x45, 0x4E, 0x59)),
]

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def metal_color(x, y):
    t = ((x + r) / (2*r)) * 0.72 + ((y + r) / (2*r)) * 0.28
    t = max(0.0, min(1.0, t))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if t <= p1:
            return lerp(c0, c1, (t-p0)/(p1-p0))
    return stops[-1][1]

for y in range(cy-r, cy+r+1):
    for x in range(cx-r, cx+r+1):
        dx, dy = x-cx, y-cy
        if dx*dx + dy*dy <= r*r:
            pix[x, y] = (*metal_color(dx, dy), 255)

draw = ImageDraw.Draw(img, 'RGBA')
# Subtle grooves and broader pressed bands.
label_r = 116
outer = r * 0.972
for i in range(58):
    t = i / 57
    eased = t * (2-t)
    rr = label_r + (outer-label_r) * eased
    box = (cx-rr, cy-rr, cx+rr, cy+rr)
    draw.ellipse(box, outline=(255,255,255, int(7 + 6*(1-t))), width=2)
    rr2 = rr + 2.0
    draw.ellipse((cx-rr2, cy-rr2, cx+rr2, cy+rr2), outline=(0,0,0,52), width=2)
for band in (0.42, 0.63, 0.82):
    rr = label_r + (outer-label_r) * band
    draw.ellipse((cx-rr, cy-rr, cx+rr, cy+rr), outline=(0,0,0,78), width=5)

# Precalculated specular sweep inside the rotating platter.
shine = Image.new('RGBA', (W, H), (0,0,0,0))
sd = ImageDraw.Draw(shine, 'RGBA')
for a0, a1, alpha in [(18, 52, 43), (160, 205, 30), (302, 328, 22)]:
    sd.arc((cx-r*.84, cy-r*.84, cx+r*.84, cy+r*.84), a0, a1, fill=(255,255,255,alpha), width=26)
shine = shine.filter(ImageFilter.GaussianBlur(5))
img.alpha_composite(shine)

draw = ImageDraw.Draw(img, 'RGBA')
# Outer rim and label edge, with no center spindle dot.
draw.ellipse((cx-r+2, cy-r+2, cx+r-2, cy+r-2), outline=(0,0,0,140), width=6)
draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(255,255,255,35), width=3)
# Cream paper label.
draw.ellipse((cx-label_r, cy-label_r, cx+label_r, cy+label_r), fill=(246,243,236,255), outline=(0,0,0,70), width=3)
# Representative circular artwork area, standing in for the runtime album thumbnail.
art_r = 96
for rr in range(art_r, 0, -1):
    t = 1 - rr / art_r
    col = lerp((29, 72, 112), (224, 116, 66), t)
    draw.ellipse((cx-rr, cy-rr, cx+rr, cy+rr), fill=(*col,255))
draw.arc((cx-art_r, cy-art_r, cx+art_r, cy+art_r), 205, 335, fill=(255,240,190,170), width=8)
draw.ellipse((cx-art_r, cy-art_r, cx+art_r, cy+art_r), outline=(0,0,0,55), width=3)

# Small caption below the preview.
draw.text((24, 850), 'FrostSoulX metallic vinyl preview — center dot removed; artwork remains circular', fill=(215,220,228,220))
img.convert('RGB').save('/home/ubuntu/frostsoulx/metallic_vinyl_preview.png', quality=95)
