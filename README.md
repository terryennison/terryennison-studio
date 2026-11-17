# Terry Ennison

Static portfolio for Terry Ennison, creative director. Plain HTML and CSS, with a small script for the photo lightbox. No build step. It is meant to be hosted for free and pointed at terryennison.studio.

## Run locally

From this folder:

```bash
python3 -m http.server 8741
```

Open http://127.0.0.1:8741/

## Pages

- Home: work index
- Cavalry, Area 51, and SainT project pages
- About, with contact

## Photos and video

Project images belong in:

- `images/cavalry/01.jpg` through `21.jpg`
- `images/area-51/01.jpg` through `09.jpg`
- `images/saint/01.jpg` through `08.jpg`
- `images/og.jpg` (Cavalry photo 1, used for link previews)
- `video/area51-promo.mp4`

`01` is the cover. If you still have the original `photos.tar.gz` and `area51-promo.mp4`, put them in `incoming/` and run:

```bash
python3 tools/prepare_assets.py
```

That script resizes each photo so the long edge is at most 2000 pixels, keeps the original aspect ratio, and writes JPEGs into `images/`.

## Domain

See `DEPLOY.md` for GitHub Pages and the DNS records for terryennison.studio.
