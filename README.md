# TARS website

Static site for TARS: Home, About, Careers, Contact and Blog. No framework and no build server needed.

## Edit content
Page content lives in `src/pages/` (blog posts in `src/pages/blog/`). After editing, run:

```
python build.py
```

This wraps each page in the shared header and footer and writes the `.html` files at the repository root.
The build fails if a page contains an em dash or en dash (house style).

## Preview locally
```
python -m http.server 8000
```
Then open http://localhost:8000.

## Publish on GitHub Pages
Settings > Pages > Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
When a custom domain exists, update `SITE` in `build.py` and add it under Settings > Pages.

## Assets
- Fonts: Geist and Geist Mono (SIL Open Font License, see `assets/fonts/LICENSE.TXT`)
- Icons: Phosphor (MIT, see `assets/icons/LICENSE`)
- Diagrams are plain HTML and CSS, so they follow the site's fonts, colors and light/dark theme.
