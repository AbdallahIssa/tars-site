"""Build the static site: wraps every page in src/pages with the shared layout.

    python build.py

Edit page content in src/pages/*.html (and src/pages/blog/*.html), then run this again.
Each page starts with three comment lines: title, description, nav (which menu item is active).
GitHub Pages serves the generated .html files from the repository root.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "pages"
SITE = "https://abdallahissa.github.io/tars-site/"  # change when the real domain exists
EMAIL = "abdallahissa9800@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/abdallaissa/"

NAV = [("home", "index.html", "Home"), ("about", "about.html", "About"), ("careers", "careers.html", "Careers"),
       ("blog", "blog/index.html", "Blog"), ("contact", "contact.html", "Contact")]

MARK = """<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-opacity=".35"/>
<circle cx="16" cy="16" r="10" fill="none" stroke="var(--accent)" stroke-width="2" stroke-dasharray="44 19" transform="rotate(-60 16 16)"/>
<circle cx="16" cy="16" r="3.2" fill="var(--accent)"/></svg>"""

LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}assets/img/dash-run.webp">
<meta name="theme-color" content="#080d12">
<link rel="icon" href="{r}assets/img/mark.svg" type="image/svg+xml">
<link rel="preload" href="{r}assets/fonts/Geist-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/icons/phosphor.css">
<link rel="stylesheet" href="{r}assets/css/site.css">
<script>try{{var t=localStorage.getItem("tars-theme");if(t)document.documentElement.dataset.theme=t;}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="brand" href="{r}index.html">{mark}<span>TARS</span></a>
    <ul class="nav-links">{links}</ul>
    <div class="nav-tools">
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch theme"></button>
      <a class="btn btn-primary btn-sm nav-cta" href="{r}contact.html">Book a demo</a>
      <button class="icon-btn menu-btn" type="button" data-menu aria-expanded="false" aria-label="Menu"><i class="ph ph-list" aria-hidden="true"></i></button>
    </div>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="brand" href="{r}index.html">{mark}<span>TARS</span></a>
        <p>An AI teammate that learns your company's knowledge and works inside your network.</p>
      </div>
      <div>
        <h4>Company</h4>
        <ul><li><a href="{r}about.html">About</a></li><li><a href="{r}careers.html">Careers</a></li><li><a href="{r}blog/index.html">Blog</a></li><li><a href="{r}contact.html">Contact</a></li></ul>
      </div>
      <div>
        <h4>Reach us</h4>
        <ul><li><a href="mailto:{email}">{email}</a></li><li><a href="{linkedin}" rel="noopener" target="_blank">LinkedIn</a></li></ul>
      </div>
    </div>
    <div class="foot-bottom"><span>&copy; <span data-year>2026</span> TARS. Made by the TARS team.</span><span>Built to run on your own machines.</span></div>
  </div>
</footer>
<script src="{r}assets/js/site.js" defer></script>
</body>
</html>
"""


def build() -> None:
    for src in sorted(SRC.rglob("*.html")):
        rel = src.relative_to(SRC).as_posix()
        text = src.read_text(encoding="utf-8")
        meta = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", text.split("\n\n", 1)[0]))
        body = re.sub(r"\A(?:<!--.*?-->\s*)+", "", text, flags=re.S)
        r = "../" * rel.count("/")
        cur = ' aria-current="page"'
        links = "".join(f'<li><a href="{r}{href}"{cur if key == meta.get("nav") else ""}>{label}</a></li>' for key, href, label in NAV)
        html = LAYOUT.format(title=meta["title"], description=meta["description"], url=SITE + rel, site=SITE, r=r, mark=MARK,
                             links=links, body=body.replace("{r}", r).replace("{email}", EMAIL).replace("{linkedin}", LINKEDIN),
                             email=EMAIL, linkedin=LINKEDIN)
        if "—" in html or "–" in html:
            raise SystemExit(f"{rel}: em/en dash found, use a hyphen or restructure the sentence")
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("built", rel)


if __name__ == "__main__":
    build()
