"""Regenerate every image asset for kylecovan.com from headshot.jpg.

RESCUED INTO THE REPO on July 29, 2026. This script previously lived only as a
Claude project doc and was the single copy in existence; the pre-Astro project
docs were deleted that day, so it lives here now.

IT CANNOT RUN AS-IS: `headshot.jpg` is NOT in this repo. Find the original
studio headshot before using this. Everything below describes the pipeline that
produced the current assets, and the two crop constants are the ones that were
tuned with Kyle over several rounds -- they are the valuable part.

WHAT CHANGED ON JULY 29, AFTER THIS SCRIPT LAST RAN:
  * The favicon is no longer a circle. `circle()` below flattens onto cream,
    which on iOS read as a round photo inside a white-cornered box. It is now
    a plain `square()` crop, matching the squared page portrait.
  * The page portrait was re-cut from the existing 360px output rather than
    re-exported from source -- 20px trimmed off the top at Kyle's request, so
    src/data/portrait.txt is 340px, not 360px. If this script is ever run
    again with the real headshot, prefer raising HEAD_CENTRE slightly over
    lowering D_MAIN, and re-export at 360px.

The source headshot frames Kyle's head almost to the top edge, so a plain crop
hugs his hair and chin. This script first synthesises 300px of extra studio
backdrop above the original frame (continuing the vignette, then blurring the
seam away), which buys the room needed to crop with real padding.

Outputs:
  headshot_ext.png  the extended source, for reference
  og_portrait.png   for the share card
  assets.json       data URIs for the page portrait and the favicon
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, base64, io, json

src = Image.open('headshot.jpg').convert('RGB')
W, H = src.size
PAD_TOP = 300
CREAM = (0xFB, 0xF8, 0xF2)

a = np.asarray(src).astype(np.float32)
ext = np.repeat(a[0:1, :, :], PAD_TOP, axis=0) * np.linspace(0.86, 1.0, PAD_TOP)[:, None, None]
img = Image.fromarray(np.clip(np.vstack([ext, a]), 0, 255).astype('uint8'))

band = img.crop((0, 0, W, PAD_TOP + 60)).filter(ImageFilter.GaussianBlur(26))
m = np.full((PAD_TOP + 60, W), 255, dtype='uint8')
m[PAD_TOP - 10:PAD_TOP + 60, :] = np.linspace(255, 0, 70).astype('uint8')[:, None]
img.paste(band, (0, 0), Image.fromarray(m))
img.save('headshot_ext.png')

HEAD_CENTRE = (48 + 610) / 2 + PAD_TOP     # head midpoint in extended coords

def square(size, D):
    """Square crop of side D (extended-source px), rendered at `size`.
    No mask: the page's rounded corners live in CSS, not in the asset."""
    cy, cx = HEAD_CENTRE + 0.04 * D, 500
    box = (int(cx - D/2), int(cy - D/2), int(cx + D/2), int(cy + D/2))
    return img.crop(box).resize((size, size), Image.LANCZOS)

def circle(size, D, ss=8):
    """Circular crop, flattened onto cream.

    RETIRED July 29, 2026 -- kept for reference only. The favicon is a square
    crop now. Do not reintroduce this without rendering it at 16/32/64px
    beside the square first; the cream corners are exactly what looked wrong."""
    c = square(size, D)
    mk = Image.new('L', (size*ss, size*ss), 0)
    ImageDraw.Draw(mk).ellipse([0, 0, size*ss-1, size*ss-1], fill=255)
    cv = Image.new('RGB', (size, size), CREAM)
    cv.paste(c, (0, 0), mk.resize((size, size), Image.LANCZOS))
    return cv

D_MAIN = 720    # page portrait + share card.
                #   Head fills ~78% of the box. 906 left too much dead backdrop;
                #   660 puts the hair back against the top edge. Don't go below
                #   ~700. Chosen from rendered options -- "R2 balanced".
D_FAV  = 680    # favicon -- tighter again, since 16px needs every pixel.

buf = io.BytesIO(); square(360, D_MAIN).save(buf, 'WEBP', quality=82, method=6)
portrait = 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()

# Square, not circle() -- see the July 29 note at the top of this file.
buf = io.BytesIO(); square(64, D_FAV).save(buf, 'PNG', optimize=True)
favicon = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

square(960, D_MAIN).save('og_portrait.png')
json.dump({'portrait': portrait, 'favicon': favicon}, open('assets.json', 'w'))
print('portrait %d chars, favicon %d chars, %.1f KB total'
      % (len(portrait), len(favicon), (len(portrait)+len(favicon))/1024))
