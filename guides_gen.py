"""NorthLedger Tools guides generator.

Separate from gen.py on purpose: gen.py owns calculators/home/sitemap; this file owns /guides/ and /guides-fr/
and then post-processes (idempotently) the shared files so they link to the guides.
Run order:  python3 gen.py && python3 guides_gen.py   (safe to re-run)
"""
import json, os, html, re, sys
from guides_lib import *
import guides_lib
# ---------------- page shell ----------------
STYLE = """<style>.callout{background:#eef8f6;border-left:5px solid #2A9D8F;padding:.7rem 1rem;margin:1rem 0;border-radius:0 8px 8px 0}
.meta{font-size:.85rem;color:#5b6878;margin:.2rem 0 1rem}.toc{background:#fff;border:1px solid #d9e0e8;border-radius:10px;padding:.6rem 1rem;margin:1rem 0;font-size:.95rem}
.toc ol{margin:.3rem 0 .3rem 1.1rem;padding:0}.rel{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.6rem;margin:.6rem 0}
.rel a{display:block;background:#fff;border:1px solid #d9e0e8;border-radius:8px;padding:.6rem .8rem;text-decoration:none}.rel a b{display:block;color:#1F3A5F}
.ex{background:#fff;border:1px solid #d9e0e8;border-radius:10px;padding:.7rem 1rem;margin:1rem 0}.ex b.t{display:block;color:#1F3A5F;margin-bottom:.2rem}
table.num td:not(:first-child),table.num th:not(:first-child){text-align:right}</style>"""

def nav_html(lang):
    return ('<nav><a href="/tfsa-contribution-room-calculator/">TFSA</a><a href="/fhsa-contribution-room-calculator/">FHSA</a><a href="/rrsp-tax-refund-calculator/">RRSP</a>'
            '<a href="/self-employed-tax-calculator/">Self-employed tax</a><a href="/freelancer-tax-set-aside-calculator/">Set-aside</a><a href="/impot-travailleur-autonome-quebec/">Québec</a>'
            '<a href="/homebrew-calculator/">Homebrew</a><a href="/guides/">Guides</a></nav>')

def shell(path, title, desc, body, lang, ld, alt=None):
    url = BASE + path
    L = "fr-CA" if lang == "fr" else "en-CA"
    hl = "".join(f'<link rel="alternate" hreflang="{h}" href="{BASE + p}">' for h, p in (alt or []))
    if alt: hl += f'<link rel="alternate" hreflang="x-default" href="{BASE + [p for h, p in alt if h.startswith("en")][0]}">'
    ldj = f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False)}</script>'
    foot = ("Fait au Canada. Aucun suivi, aucun témoin, aucune publicité. Les calculs se font dans votre navigateur." if lang == "fr" else
            "Made in Canada. No tracking, no cookies, no ads. Calculations run in your browser; nothing you type is sent anywhere.")
    doc = f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">{hl}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="article"><meta property="og:site_name" content="{BRAND}">
<meta name="theme-color" content="#1F3A5F"><link rel="stylesheet" href="/assets/style.css">{STYLE}<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">{ldj}</head>
<body><header class="top"><div class="w"><a class="brand" href="/">North<span>Ledger</span> Tools</a>{nav_html(lang)}</div></header><main class="w">{body}</main>
<footer><div class="w">{foot} · <a href="/privacy/">{"Confidentialité" if lang == "fr" else "Privacy"}</a> · {"Mis à jour le" if lang == "fr" else "Updated"} {UPD}</div></footer></body></html>'''
    os.makedirs(path, exist_ok=True)
    open(os.path.join(path, "index.html"), "w").write(doc)

def gpath(g): return ("guides-fr/" if g["lang"] == "fr" else "guides/") + g["slug"] + "/"

def render_guide(g, by_slug):
    lang = g["lang"]; fr = lang == "fr"
    path = gpath(g)
    # table of contents from <h2 id=..>
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', g["body"])
    toc = ""
    if len(heads) >= 3:
        toc = f'<div class="toc"><b>{"Dans ce guide" if fr else "In this guide"}</b><ol>' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads) + "</ol></div>"
    faq = ""
    if g["faq"]:
        faq = f'<h2 id="faq">{"Questions fréquentes" if fr else "Frequently asked questions"}</h2>' + "".join(
            f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in g["faq"])
    srcs = f'<h2 id="sources">{"Sources officielles" if fr else "Official sources"}</h2><ul>' + "".join(
        f'<li><a href="{u}" rel="noopener">{e(t)}</a></li>' for t, u in g["sources"]) + "</ul>"
    cards = []
    for href, label, sub in g["calcs"]:
        if exists(href): cards.append(f'<a href="{href}"><b>{label}</b>{sub}</a>')
    for s in g["rel"]:
        o = by_slug.get(s)
        if o: cards.append(f'<a href="/{gpath(o)}"><b>{o["h1"]}</b>{o["short"]}</a>')
    rel = (f'<h2 id="related">{"À lire et à essayer ensuite" if fr else "Try next"}</h2><div class="rel">' + "".join(cards) + "</div>") if cards else ""
    cta = ""
    if g["cta"]:
        gum, ety, name, price, blurb = CTA[g["cta"]]
        if fr:
            cta = f'<div class="cta"><b>{name}</b><p>{blurb}</p><a class="btn" href="{gum}">Voir le tableur ({price}) →</a> <a class="alt" href="{ety}" rel="noopener">ou sur Etsy</a></div>'
        else:
            cta = f'<div class="cta"><b>{name}</b><p>{blurb}</p><a class="btn" href="{gum}">See the spreadsheet ({price}) →</a> <a class="alt" href="{ety}" rel="noopener">or on Etsy</a></div>'
    if fr:
        meta = f'<p class="meta">Publié le {g["pub"]} · Vérifié avec les sources officielles le {g["upd"]} · <a href="/guides-fr/">Tous les guides</a></p>'
        disc = ('<p class="disc">Information générale, pas un conseil fiscal ou financier. Les chiffres viennent des sources officielles citées ci-dessus à la date indiquée; '
                "votre avis de cotisation, votre dossier à l'ARC et à Revenu Québec restent la référence pour votre situation. "
                "Rédigé par NorthLedger avec l'aide d'outils d'IA; chaque chiffre est vérifié à la source avant publication. "
                'Une erreur? Écrivez-nous par notre <a href="https://northledgertools.gumroad.com/">boutique Gumroad</a>.</p>')
    else:
        meta = f'<p class="meta">Published {g["pub"]} · Checked against official sources {g["upd"]} · <a href="/guides/">All guides</a></p>'
        disc = ('<p class="disc">General information, not tax or financial advice. Figures come from the official sources listed above as of the date shown; '
                "your notice of assessment and your CRA / Revenu Québec accounts remain the record for your own situation. "
                "Written by NorthLedger with help from AI tools; every figure is traced to the source before publishing. "
                'Spotted a mistake? Tell us through our <a href="https://northledgertools.gumroad.com/">Gumroad store</a>.</p>')
    body = f'<nav class="meta" aria-label="breadcrumb"><a href="/">{"Accueil" if fr else "Home"}</a> › <a href="/{"guides-fr" if fr else "guides"}/">{"Guides" }</a></nav><h1>{g["h1"]}</h1>{meta}<p class="lede">{g["lede"]}</p>{toc}{g["body"]}{faq}{cta}{rel}{srcs}{disc}'
    url = BASE + path
    ld = [{"@type": "Article", "headline": g["h1"], "description": g["desc"], "inLanguage": "fr-CA" if fr else "en-CA", "datePublished": g["pub"], "dateModified": g["upd"],
           "mainEntityOfPage": url, "author": {"@type": "Organization", "name": BRAND, "url": BASE}, "publisher": {"@type": "Organization", "name": BRAND, "url": BASE}},
          {"@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": BRAND, "item": BASE},
              {"@type": "ListItem", "position": 2, "name": "Guides", "item": BASE + ("guides-fr/" if fr else "guides/")},
              {"@type": "ListItem", "position": 3, "name": g["h1"], "item": url}]}]
    if g["faq"]:
        ld.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in g["faq"]]})
    shell(path, g["title"], g["desc"], body, lang, ld, g.get("alt"))

def render_hub(lang, items):
    fr = lang == "fr"
    path = "guides-fr/" if fr else "guides/"
    if fr:
        title = "Guides fiscaux pour Canadiens et Québécois : CELI, REER, CELIAPP, acomptes | NorthLedger Tools"
        desc = "Guides pratiques avec exemples chiffrés, tirés de l'ARC et de Revenu Québec : surcotisation CELI, CELIAPP et RAP, cotisations du travailleur autonome, acomptes provisionnels."
        h1 = "Guides : impôt, CELI, REER et travail autonome au Québec"
        lede = "Des guides courts, avec des exemples chiffrés et les sources officielles à chaque page. Chacun complète un de nos calculateurs gratuits."
        other = '<p>Guides in English: <a href="/guides/">NorthLedger guides</a>.</p>'
    else:
        title = "Guides: TFSA, RRSP, FHSA, Self-Employed Tax and Instalments (Canada & US) | NorthLedger Tools"
        desc = "Practical guides with worked examples drawn from CRA, Revenu Québec and IRS sources: TFSA over-contribution, how the TFSA limit is set, FHSA and the Home Buyers' Plan, self-employed CPP, instalments, GST/HST."
        h1 = "Guides: Canadian tax, registered accounts and freelancing"
        lede = "Short guides with worked examples and the official source for every figure. Each one goes with a free NorthLedger calculator so you can run your own numbers."
        other = '<p>Guides en français : <a href="/guides-fr/">guides NorthLedger</a>.</p>'
    groups = {}
    for g in items: groups.setdefault(g["group"], []).append(g)
    parts = ""
    for gr, lst in groups.items():
        parts += f"<h2>{gr}</h2><div class=\"rel\">" + "".join(f'<a href="/{gpath(g)}"><b>{g["h1"]}</b>{g["short"]}</a>' for g in lst) + "</div>"
    note = ("<h2>Comment nous travaillons</h2><p>Chaque chiffre est tiré d'une page de l'ARC, de Revenu Québec, de Retraite Québec ou de la loi, et la source est citée en bas de page. Les guides sont rédigés avec l'aide d'outils d'IA, puis vérifiés à la source; nos calculateurs sont aussi comparés aux tables officielles publiées par Revenu Québec (voir le guide sur les cotisations)." "</p>" if fr else
            "<h2>How we work</h2><p>Every figure comes from a CRA, Revenu Québec, Retraite Québec, IRS or statute page, and the source is cited at the bottom of the guide. Guides are written with help from AI tools and then checked against the source. Our calculators are also tested against official tables (see <a href=\"/guides/how-we-check-our-numbers/\">how we check our numbers</a>).</p>")
    body = f'<h1>{h1}</h1><p class="lede">{lede}</p>{parts}{note}{other}'
    url = BASE + path
    ld = [{"@type": "CollectionPage", "name": h1, "url": url, "inLanguage": "fr-CA" if fr else "en-CA", "publisher": {"@type": "Organization", "name": BRAND, "url": BASE},
           "hasPart": [{"@type": "Article", "headline": g["h1"], "url": BASE + gpath(g)} for g in items]}]
    shell(path, title, desc, body, lang, ld)

US_LINKS = {}   # filled from content.guides_us
# ---------------- load content ----------------
sys.path.insert(0, ROOT)
import importlib
for mod in ("content.guides_en", "content.guides_us", "content.guides_fr"):
    importlib.import_module(mod)
from content.guides_us import US_LINK_KEYS
US_LINKS.update(US_LINK_KEYS)

def main():
    by_slug = {g["slug"]: g for g in GUIDES}
    for g in GUIDES: render_guide(g, by_slug)
    render_hub("en", [g for g in GUIDES if g["lang"] == "en"])
    render_hub("fr", [g for g in GUIDES if g["lang"] == "fr"])
    postprocess()
    print("guides:", len(GUIDES))

# ---------------- idempotent post-processing of shared files ----------------
CALC_LINKS = {   # calculator path -> guide slugs (en unless prefixed fr:)
 "tfsa-contribution-room-calculator": ["tfsa-over-contribution-penalty", "how-the-tfsa-limit-is-set"],
 "fhsa-contribution-room-calculator": ["fhsa-and-home-buyers-plan"],
 "calcul-droits-celiapp": ["fr:celiapp-et-regime-d-accession-a-la-propriete"],
 "rrsp-tax-refund-calculator": ["rrsp-deduction-limit-explained", "fhsa-and-home-buyers-plan"],
 "calcul-remboursement-reer": ["fr:date-limite-reer-et-plafond-de-cotisation"],
 "self-employed-tax-calculator": ["self-employed-cpp-explained", "which-tax-instalment-method", "gst-hst-small-supplier-freelancers", "how-we-check-our-numbers"],
 "freelancer-tax-set-aside-calculator": ["which-tax-instalment-method", "self-employed-cpp-explained", "gst-hst-small-supplier-freelancers"],
 "quebec-self-employed-tax-calculator": ["how-we-check-our-numbers", "which-tax-instalment-method"],
 "impot-travailleur-autonome-quebec": ["fr:cotisations-travailleur-autonome-quebec-2026", "fr:acomptes-provisionnels-quelle-methode"],
 "quebec-tax-instalments-calculator": ["which-tax-instalment-method", "how-we-check-our-numbers"],
 "acomptes-provisionnels-travailleur-autonome-quebec": ["fr:acomptes-provisionnels-quelle-methode", "fr:cotisations-travailleur-autonome-quebec-2026"],
}

def _guide_by(key):
    fr = key.startswith("fr:"); slug = key[3:] if fr else key
    for g in GUIDES:
        if g["slug"] == slug and (g["lang"] == "fr") == fr: return g

def postprocess():
    # 1) nav link + contextual "related guides" block on calculator pages
    for dirpath, dirs, files in os.walk("."):
        if ".git" in dirpath or dirpath.startswith("./content") or dirpath.startswith("./guides"): continue
        if "index.html" not in files: continue
        p = os.path.join(dirpath, "index.html")
        s = open(p).read(); o = s
        if '<a href="/guides/">Guides</a>' not in s and '<a href="/homebrew-calculator/">Homebrew</a></nav>' in s:
            s = s.replace('<a href="/homebrew-calculator/">Homebrew</a></nav>', '<a href="/homebrew-calculator/">Homebrew</a><a href="/guides/">Guides</a></nav>')
        key = os.path.relpath(dirpath, ".").strip("./")
        keys = list(CALC_LINKS.get(key, [])) + list(US_LINKS.get(key, []))
        if keys:
            fr = "fr-CA" in s[:200]
            cards = ""
            for k in keys:
                g = _guide_by(k)
                if g: cards += f'<a href="/{gpath(g)}"><b>{g["h1"]}</b>{g["short"]}</a>'
            block = f'<!--nl-guides--><h2>{"Guides liés" if fr else "Related guides"}</h2><div class="rel">{cards}</div><!--/nl-guides-->'
            s = re.sub(r"<!--nl-guides-->.*?<!--/nl-guides-->", "", s, flags=re.S)
            if "<style>.rel" not in s and ".rel{" not in s:
                s = s.replace("</head>", STYLE + "</head>", 1)
            if "<h2>Sources</h2>" in s: s = s.replace("<h2>Sources</h2>", block + "<h2>Sources</h2>", 1)
            elif '<p class="disc">' in s: s = s.replace('<p class="disc">', block + '<p class="disc">', 1)
            elif '<div class="disc">' in s: s = s.replace('<div class="disc">', block + '<div class="disc">', 1)
        if s != o: open(p, "w").write(s)
    # 2) home page: guides section
    s = open("index.html").read()
    en = [g for g in GUIDES if g["lang"] == "en"]
    sec = ('<!--nl-guides--><h2>Guides</h2><p>Worked examples and the official source for every figure: <a href="/guides/">all guides</a> · <a href="/guides-fr/" hreflang="fr-CA">guides en français</a>.</p><div class="rel">'
           + "".join(f'<a href="/{gpath(g)}"><b>{g["h1"]}</b>{g["short"]}</a>' for g in en[:6]) + '</div><!--/nl-guides-->')
    s = re.sub(r"<!--nl-guides-->.*?<!--/nl-guides-->", "", s, flags=re.S)
    if ".rel{" not in s: s = s.replace("</head>", STYLE + "</head>", 1)
    s = s.replace("<h2>About</h2>", sec + "<h2>About</h2>", 1)
    open("index.html", "w").write(s)
    # 3) sitemap
    sm = open("sitemap.xml").read()
    urls = [BASE + "guides/", BASE + "guides-fr/"] + [BASE + gpath(g) for g in GUIDES]
    sm = re.sub(r"<url><loc>%s(guides|guides-fr)/[^<]*</loc>.*?</url>\n?" % re.escape(BASE), "", sm)
    add = "".join(f"<url><loc>{u}</loc><lastmod>{UPD}</lastmod></url>\n" for u in urls)
    sm = sm.replace("</urlset>", add + "</urlset>")
    open("sitemap.xml", "w").write(sm)
    # 4) llms.txt
    t = open("llms.txt").read()
    t = re.sub(r"## Guides.*?(?=\n## )", "", t, flags=re.S)
    block = "## Guides (worked examples, each figure sourced)\n" + "".join(f"- [{g['h1']}]({BASE}{gpath(g)}): {g['short']}\n" for g in GUIDES) + "\n"
    t = t.replace("## Paid spreadsheets", block + "## Paid spreadsheets", 1)
    open("llms.txt", "w").write(t)

if __name__ == "__main__":
    main()
