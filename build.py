"""Builds the hostable installable web app into dist/ from src/app.html."""
import json, os, re, shutil
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src", "app.html")
DIST = os.path.join(ROOT, "docs")
VERSION = "1.0.0"

src = open(SRC, encoding="utf-8").read()
head, body = src.split("<!--BODY-->", 1)

pwa_head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="A free, simple tracker for making up missed prayers (qada). No ads, no account.">
<meta name="theme-color" content="#1f6b5a" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0d1816" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Qada">
<style>:root{padding-top:env(safe-area-inset-top,0px)}</style>
"""
pwa_body_open = "</head>\n<body>\n<script>window.QADA_HOSTED=true;</script>\n"
sw_reg = """<script>
if("serviceWorker" in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){});});}
</script>
</body>
</html>
"""
os.makedirs(os.path.join(DIST, "icons"), exist_ok=True)
with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
    f.write(pwa_head + head.strip() + "\n" + pwa_body_open + body.strip() + "\n" + sw_reg)

manifest = {
    "name": "Qada Tracker",
    "short_name": "Qada",
    "description": "Make up your missed prayers, one day at a time.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#eef3f1",
    "theme_color": "#1f6b5a",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
json.dump(manifest, open(os.path.join(DIST, "manifest.webmanifest"), "w"), indent=2)

sw = """// Offline support: the app shell is cached so it opens without internet.
const CACHE = "qada-%s";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/apple-touch-icon.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (req.mode === "navigate") {
    // Network first for the page so updates arrive; fall back to the cached copy offline
    e.respondWith(fetch(req).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put("index.html", c)); return r; }).catch(() => caches.match("index.html")));
    return;
  }
  if (url.origin === location.origin || url.host.endsWith("fonts.googleapis.com") || url.host.endsWith("fonts.gstatic.com")) {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put(req, c)); return r; })));
  }
});
""" % VERSION
open(os.path.join(DIST, "sw.js"), "w").write(sw)

# ---- Icons: a progress ring with a gold tick on deep green ----
def icon(size, pad_ratio=0.0, rounded=True):
    S = size * 4
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    green = (31, 107, 90, 255)
    if rounded:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=green)
    else:
        d.rectangle([0, 0, S, S], fill=green)
    inner = S * (1 - pad_ratio)
    off = (S - inner) / 2
    cx = cy = S / 2
    r = inner * 0.30
    w = int(inner * 0.075)
    box = [cx - r, cy - r, cx + r, cy + r]
    d.arc(box, 0, 360, fill=(255, 255, 255, 60), width=w)
    d.arc(box, -90, 180, fill=(255, 255, 255, 255), width=w)
    gold = (216, 170, 90, 255)
    pts = [(cx - r * 0.42, cy + r * 0.02), (cx - r * 0.08, cy + r * 0.36), (cx + r * 0.48, cy - r * 0.32)]
    d.line(pts, fill=gold, width=int(w * 1.05), joint="curve")
    for p in (pts[0], pts[2]):
        rr = w * 0.52
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=gold)
    return img.resize((size, size), Image.LANCZOS)

icon(192).save(os.path.join(DIST, "icons", "icon-192.png"))
icon(512).save(os.path.join(DIST, "icons", "icon-512.png"))
icon(512, pad_ratio=0.2, rounded=False).save(os.path.join(DIST, "icons", "maskable-512.png"))
icon(180, rounded=False).convert("RGB").save(os.path.join(DIST, "icons", "apple-touch-icon.png"))
print("built", os.listdir(DIST))

# Shrink icons so the site stays small
for f in ("icon-192.png", "icon-512.png", "maskable-512.png", "apple-touch-icon.png"):
    p = os.path.join(DIST, "icons", f)
    Image.open(p).convert("RGBA").quantize(colors=48, method=Image.FASTOCTREE).save(p, optimize=True)
