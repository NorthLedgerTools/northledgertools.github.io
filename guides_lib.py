"""Shared helpers + registry for guides (see guides_gen.py).

Separate from gen.py on purpose: gen.py owns calculators/home/sitemap; this file owns /guides/ and /guides-fr/
and then post-processes (idempotently) the shared files so they link to the guides.

Run order:  python3 gen.py && python3 guides_gen.py        (guides_gen.py is safe to run repeatedly)
"""
import json, os, html, re, sys
from datetime import date

BASE = "https://northledgertools.com/"
G = "https://northledgertools.gumroad.com/l/"
ETSY = "https://www.etsy.com/listing/"
BRAND = "NorthLedger Tools"
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

# Figures that change every January live in one place: content/limits.json (see content/updates-2027/).
LIM = json.load(open("content/limits.json"))
PUB = "2026-10-25"
UPD = LIM.get("guides_updated", PUB)

CTA = {
 "tracker": (f"{G}pdxqug", f"{ETSY}4594000039", "Canadian Contribution Room Tracker 2026 (TFSA, RRSP, FHSA)", "CA$14",
   "One Excel / Google Sheets file that logs every deposit and withdrawal, keeps TFSA, RRSP and FHSA room side by side and flags over-contributions in red. Blank file plus a filled example."),
 "se": (f"{G}bblrt", f"{ETSY}4594017328", "Self-Employed Tax Estimator 2026 (ON, BC, AB)", "CA$17",
   "The same formulas as our free calculators plus a monthly income and expense log, a set-aside percentage and instalment dates, with every rate on an editable tab beside its official source."),
 "qc": (f"{G}oymrg", f"{ETSY}4593999701", "Quebec Self-Employed Tax Estimator 2026 (bilingual)", "CA$17",
   "Quebec and federal tax, QPP in both shares, QPIP, Health Services Fund and an instalment schedule for Revenu Québec and the CRA. QPP, QPIP and FSS match Revenu Québec's own 2026 table."),
}
# Etsy listing ids as on the calculator pages in gen.py: tracker 4594000039, ON/BC/AB estimator 4594017328, Quebec estimator 4593999701.

def e(s): return html.escape(s, quote=True)

def exists(path):
    return os.path.isfile(os.path.join(path.strip("/"), "index.html"))

def table(head, rows, cls=""):
    h = "".join(f"<th>{e(x)}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

def callout(t): return f'<div class="callout">{t}</div>'
def money(x, lang="en", dec=0):
    s = f"{x:,.{dec}f}"
    if lang == "fr": return s.replace(",", "\u00a0").replace(".", ",") + "\u00a0$"
    return "$" + s

GUIDES = []
def guide(**kw):
    kw.setdefault("faq", []); kw.setdefault("calcs", []); kw.setdefault("rel", []); kw.setdefault("cta", None)
    kw.setdefault("pub", PUB); kw.setdefault("upd", UPD)
    GUIDES.append(kw); return kw

