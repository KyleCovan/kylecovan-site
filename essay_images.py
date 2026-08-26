"""Build inlined data URIs for essay images.

    source .venv/bin/activate && python3 essay_images.py

handoff §2: a visitor's browser fetches exactly one file per page. Essay photos
ship as WebP data URIs in src/data/essay/<slug>/, the same pattern as the
portrait. Source JPEGs live in assets/essay/<slug>/ and are never linked from
HTML directly.

Run after adding or replacing any source file in assets/essay/.
"""
import base64
import io
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).parent
MAX_WIDTH = 800
WEBP_QUALITY = 80

ESSAYS = {
    'new-direction-reflections': [
        'two-paths-old-and-new-direction.jpg',
        'door-in-the-field-new-direction.jpg',
        'forest-path-at-dusk.jpg',
        'music-studio-mid-session.jpg',
        'grandmother-and-grandson-portrait.jpg',
        'sun-on-the-horizon-always-new.jpg',
    ],
}


def data_uri(im: Image.Image) -> str:
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=WEBP_QUALITY, method=6)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'data:image/webp;base64,{b64}'


def resize_to_column(path: pathlib.Path) -> Image.Image:
    im = Image.open(path).convert('RGB')
    w, h = im.size
    if w > MAX_WIDTH:
        nh = round(h * MAX_WIDTH / w)
        im = im.resize((MAX_WIDTH, nh), Image.LANCZOS)
        print(f'  {path.name}: {w}x{h} -> {im.size[0]}x{im.size[1]}')
    else:
        print(f'  {path.name}: {w}x{h} (no resize)')
    return im


def main() -> None:
    for slug, files in ESSAYS.items():
        src_dir = ROOT / 'assets' / 'essay' / slug
        out_dir = ROOT / 'src' / 'data' / 'essay' / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f'{slug}:')
        for name in files:
            src = src_dir / name
            if not src.exists():
                raise SystemExit(f'missing source: {src}')
            im = resize_to_column(src)
            uri = data_uri(im)
            stem = src.stem
            out = out_dir / f'{stem}.txt'
            out.write_text(uri)
            print(f'    -> {out.relative_to(ROOT)}  {len(uri):,} chars')


if __name__ == '__main__':
    main()
