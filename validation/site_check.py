"""Site checks: internal links resolve, JSON-LD parses, unique titles/descriptions, canonical matches path, guide word counts.
Usage: python3 validation/site_check.py [--external]   (--external also HTTP-checks every outbound URL; needs network)"""
import os, re, sys, json, glob, urllib.request, concurrent.futures as cf
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
pages = [p for p in glob.glob("**/index.html", recursive=True) if not p.startswith(("content/", "validation/"))] + ["index.html"]
pages = sorted(set(pages)); bad = 0; titles = {}; descs = {}; ext = set()
def err(*a):
    global bad; bad += 1; print("ERR", *a)
for p in pages:
    s = open(p).read(); d = os.path.dirname(p)
    url = "https://northledgertools.com/" + (d + "/" if d else "")
    m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if "noindex" not in s and (not m or m.group(1) != url): err(p, "canonical", m and m.group(1))
    t = re.search(r"<title>(.*?)</title>", s, re.S); de = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not t or not de:
        if "noindex" not in s: err(p, "title/description missing")
        continue
    titles.setdefault(t.group(1), []).append(p); descs.setdefault(de.group(1), []).append(p)
    if len(de.group(1)) > 175: print("WARN", p, "description", len(de.group(1)), "chars")
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j)
        except Exception as e: err(p, "json-ld", e)
    for h in re.findall(r'href="([^"#]+)(?:#[^"]*)?"', s):
        if h.startswith("/"):
            tgt = h.strip("/")
            if not (os.path.isfile(tgt) or os.path.isfile(os.path.join(tgt, "index.html")) or tgt == ""): err(p, "broken internal link", h)
        elif h.startswith("http"): ext.add(h)
    for hl in re.findall(r'hreflang="[^"]+" href="https://northledgertools.com/([^"]*)"', s):
        if not os.path.isfile(os.path.join(hl, "index.html")) and hl: err(p, "hreflang target missing", hl)
    ids = set(re.findall(r'id="([^"]+)"', s))
    for a in re.findall(r'href="#([^"]+)"', s):
        if a not in ids: err(p, "dead anchor", a)
for k, v in titles.items():
    if len(v) > 1: err("duplicate title", v)
for k, v in descs.items():
    if len(v) > 1: err("duplicate description", v)
for p in sorted(glob.glob("guides*/*/index.html")):
    txt = re.sub(r"<[^>]+>", " ", re.search(r"<main.*?</main>", open(p).read(), re.S).group(0))
    print(f"{len(txt.split()):5d} words  {p}")
sm = open("sitemap.xml").read()
for p in pages:
    d = os.path.dirname(p)
    if d in ("etsy-callback", "etsy-connect", "privacy") or p == "404.html": continue
    if ("https://northledgertools.com/" + (d + "/" if d else "")) not in sm: err("not in sitemap", p)
if "--external" in sys.argv:
    def chk(u):
        try:
            r = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (link check)"}); x = urllib.request.urlopen(r, timeout=25); return u, x.status
        except Exception as e: return u, str(e)[:60]
    skip = ("northledgertools.com", "gumroad.com", "etsy.com")
    with cf.ThreadPoolExecutor(8) as ex:
        for u, st in ex.map(chk, sorted(x for x in ext if not any(k in x for k in skip))):
            if st != 200: print("EXT", st, u)
print("errors:", bad); sys.exit(1 if bad else 0)
