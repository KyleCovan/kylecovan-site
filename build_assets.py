"""Rebuild every image on the site from one source file.

    source .venv/bin/activate && python3 build_assets.py

handoff §7 item 7 recorded that this script and `headshot.jpg` were both missing
from the repo, and that they had to be recovered before any image work. That is
what this is. Both now live here, so the next portrait change is one command
rather than an archaeology exercise.

WHY THE IMAGES ARE TEXT FILES. handoff §2: a visitor's browser fetches exactly
one file per page. The portrait and favicon are therefore base64 data URIs
inlined into the HTML, not files a browser goes and gets. `og.png` is the
documented exception, since only crawlers fetch it.

THREE OUTPUTS, ONE SOURCE:

  src/data/portrait.txt   340px WebP, quality 80, as a data URI
  src/data/favicon.txt     64px PNG, as a data URI
  public/og.png           1200x630 share card, photo replaced in place

The portrait is NOT pre-masked. handoff §3: the square and its 3px radius live
entirely in CSS, so the source stays a plain square and the shape stays
editable without a re-export.

THE FAVICON HAS ITS OWN SOURCE, as of August 3, and this is a deliberate
exception to handoff §3. That rule said to cut the favicon from the same crop as
the portrait, because two separately tuned crops of one face drift apart, and
the July 29 rebuild existed because that had already happened.

What changed: the new portrait has an outdoor background, and at 16px the fence
and foliage swallowed the face entirely. Rendered at 16, 32 and 64 before
deciding. So `headshot-favicon.jpg` is a tighter crop of THE SAME PHOTOGRAPH,
supplied by Kyle for this purpose. That is the distinction that keeps §3's
intent intact: one photograph, framed twice on purpose, rather than two photos
drifting apart unattended. If the portrait is ever replaced, replace both.

ABOUT og.png. This script does NOT redraw the card. It paints over the photo
box and composites the new portrait into it, leaving every text pixel of the
existing card untouched. That is on purpose: the typography was set once in a
design tool that is not in this repo, and regenerating it here would mean
guessing at fonts the site does not otherwise use. Painting the box with the
background colour first makes the operation idempotent, so running this twice
gives the same file as running it once.

If the card's WORDS ever need to change, this script cannot do it. That needs
the original design source, and this comment is the warning that it is missing.
"""
import base64
import pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).parent
SOURCE = ROOT / 'headshot.jpg'
# Same photograph, cropped tighter. See the note above before merging the two.
FAVICON_SOURCE = ROOT / 'headshot-favicon.jpg'

# The cream the whole site is built on. verify.py asserts contrast against this
# exact triple, so it is not a value to nudge by eye.
BG = (251, 248, 242)

# Where the portrait sits inside the 1200x630 card, measured off the shipped
# og.png rather than assumed. Radius 6 is the site's 3px portrait radius scaled
# to this size, and matches what was measured on the original.
OG_BOX = (783, 154, 1104, 475)
OG_RADIUS = 6

PORTRAIT_PX = 340   # handoff §3: ships at 340, do not scale the CSS box past ~170
FAVICON_PX = 64     # legible at 32, mush at 16. Known and accepted.
WEBP_QUALITY = 80


def load_square(path=SOURCE):
    """The source must be square. The shape is CSS's job, the framing is not."""
    im = Image.open(path).convert('RGB')
    w, h = im.size
    if w != h:
        side = min(w, h)
        im = im.crop(((w - side) // 2, (h - side) // 2,
                      (w + side) // 2, (h + side) // 2))
        print(f'  source was {w}x{h}, centre-cropped to {side}x{side}')
    return im


def data_uri(im, fmt, **save_args):
    import io
    buf = io.BytesIO()
    im.save(buf, fmt, **save_args)
    mime = 'image/webp' if fmt == 'WEBP' else 'image/png'
    return f'data:{mime};base64,' + base64.b64encode(buf.getvalue()).decode()


def rounded_mask(size, radius):
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (size[0] - 1, size[1] - 1)],
                                           radius=radius, fill=255)
    return mask


def main():
    src = load_square()
    print(f'source: {SOURCE.name} {src.size[0]}x{src.size[1]}')

    portrait = src.resize((PORTRAIT_PX, PORTRAIT_PX), Image.LANCZOS)
    uri = data_uri(portrait, 'WEBP', quality=WEBP_QUALITY, method=6)
    (ROOT / 'src/data/portrait.txt').write_text(uri)
    print(f'  portrait.txt  {PORTRAIT_PX}px webp q{WEBP_QUALITY}  {len(uri):,} chars')

    fav_src = load_square(FAVICON_SOURCE) if FAVICON_SOURCE.exists() else src
    if not FAVICON_SOURCE.exists():
        print('  ! no headshot-favicon.jpg, falling back to the portrait crop')
    favicon = fav_src.resize((FAVICON_PX, FAVICON_PX), Image.LANCZOS)
    uri = data_uri(favicon, 'PNG', optimize=True)
    (ROOT / 'src/data/favicon.txt').write_text(uri)
    print(f'  favicon.txt   {FAVICON_PX}px png            {len(uri):,} chars')

    card = Image.open(ROOT / 'public/og.png').convert('RGB')
    l, t, r, b = OG_BOX
    side = r - l + 1
    # Paint the box out first so this never depends on what is already there.
    ImageDraw.Draw(card).rectangle([(l, t), (r, b)], fill=BG)
    photo = src.resize((side, side), Image.LANCZOS)
    card.paste(photo, (l, t), rounded_mask((side, side), OG_RADIUS))
    card.save(ROOT / 'public/og.png', 'PNG', optimize=True)
    print(f'  og.png        photo replaced at {side}x{side}, text untouched')


if __name__ == '__main__':
    main()
