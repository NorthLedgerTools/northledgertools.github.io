"""Bill 96 / Québec French checklist pages for NorthLedger Tools (EN + FR). Self-contained generator.
Run from the site root AFTER guides_gen.py and BEFORE crosslinks.py (build.sh does this once publish_bill96.py has run):
    python3 bill96_gen.py
Reads  bill96_rules.json (copy of products/07-bill96-localisation/gapcheck/rules.json) and bill96.js.
Writes quebec-french-gap-check/index.html, verification-francais-boutique-quebec/index.html, assets/bill96.js,
then idempotently adds the sitemap + llms.txt entries and one marker-delimited link block on the home page. Safe to re-run."""
import html, json, os, re, sys
# Modes (publish_bill96.py writes them into the build.sh line, so every ./build.sh repeats the same output):
#   --en-only   build and link only the English page; the French page is not generated, linked, or listed anywhere
#   --pricing   include the pricing section (OFF by default: it publishes only after the Auditor has read it)
EN_ONLY = "--en-only" in sys.argv
PRICING = "--pricing" in sys.argv
BUILDING = __name__ == "__main__"
sys.path.insert(0, os.getcwd())
try:
    from brand_head import head_extra, more_tools  # lives in the site root (northledger-tools/); the generator runs from there
except ImportError:
    if BUILDING:
        sys.exit("bill96_gen: brand_head.py not found in the current folder. Run from the site root (build.sh does).")
    def head_extra(path):  # imported by tests / the French review pack, which never build a page
        raise RuntimeError("head_extra is only available when running from a site root")
    more_tools = head_extra
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.getcwd()
BASE = "https://northledgertools.com/"
BRAND = "NorthLedger Tools"
CHECKED = "2026-10-26"          # date the official sources were read (matches rules.json checked_on)
LASTMOD = "2026-10-28"          # page "Updated" date, JSON-LD dateModified, sitemap lastmod (publish day; Auditor L1)
P_EN = "quebec-french-gap-check/"
P_FR = "verification-francais-boutique-quebec/"
e = lambda s: html.escape(s, quote=True)

def find(name):
    for d in (HERE, os.path.join(HERE, "..", "gapcheck")):
        p = os.path.join(d, name)
        if os.path.isfile(p): return p
    sys.exit("bill96_gen: missing " + name)
RULES = json.load(open(find("bill96_rules.json" if os.path.isfile(os.path.join(HERE, "bill96_rules.json")) else "rules.json"), encoding="utf-8"))
assert RULES["checked_on"] == CHECKED, "rules.json checked_on differs from CHECKED"
SRC = RULES["sources"]
SHORT = {  # short source names shown on the page
    "en": {"C11-EN": "Charter of the French language, English text (Légis Québec)", "C11-FR": "Charte de la langue française, French text (Légis Québec)",
           "OQLF-FICHE": "OQLF fiche, social media, websites and advertising documents (2022)", "QC-OBLIG": "Gouvernement du Québec, business obligations page",
           "OQLF-FAQ": "OQLF, frequently asked questions", "OTTIAQ": "OTTIAQ, position on AI in translation (2024)", "NA-BILL96": "National Assembly of Québec, Bill 96 page"},
    "fr": {"C11-EN": "Charte de la langue française, texte anglais (Légis Québec)", "C11-FR": "Charte de la langue française, texte français (Légis Québec)",
           "OQLF-FICHE": "fiche de l'OQLF « Médias sociaux, sites Web et documents publicitaires » (2022)", "QC-OBLIG": "Gouvernement du Québec, page sur les obligations des commerces",
           "OQLF-FAQ": "OQLF, foire aux questions", "OTTIAQ": "OTTIAQ, position sur l'IA en traduction (2024)", "NA-BILL96": "Assemblée nationale du Québec, page du projet de loi 96"},
}
ASK = {  # my own checklist questions: "yes" always means "available in French"
 "R-SITE": ("Is your website, including product pages, available in French?", "Votre site Web, y compris les fiches de produits, est-il offert en français?"),
 "R-LISTINGS": ("Are your product listings, catalogues and brochures available in French?", "Vos fiches de produits, catalogues et brochures sont-ils offerts en français?"),
 "R-ORDER": ("Are your cart, checkout and order form available in French?", "Votre panier, votre page de paiement et votre bon de commande sont-ils offerts en français?"),
 "R-TERMS": ("Are your terms of sale or terms of service available in French?", "Vos conditions de vente ou d'utilisation sont-elles offertes en français?"),
 "R-POLICIES": ("Are your shipping, returns and privacy pages available in French?", "Vos pages sur la livraison, les retours et la confidentialité sont-elles offertes en français?"),
 "R-INVOICE": ("Are the invoices and receipts you send available in French?", "Les factures et reçus que vous envoyez sont-ils offerts en français?"),
 "R-PRODUCT": ("Are product labels, packaging, directions for use and warranty documents in French?", "Les étiquettes, l'emballage, le mode d'emploi et les documents de garantie qui accompagnent vos produits sont-ils en français?"),
 "R-ADS": ("Is your commercial advertising, including commercial social-media posts, in French?", "Votre publicité commerciale, y compris vos publications commerciales sur les médias sociaux, est-elle en français?"),
 "R-SERVICE": ("Are your customers informed and served in French, including customers who write to you in French?", "Vos clients sont-ils informés et servis en français, y compris ceux qui vous écrivent en français?"),
 "R-SOFTWARE": ("Only if you sell software or games: is there a French version?", "Seulement si vous vendez des logiciels ou des jeux : existe-t-il une version française?"),
}
STRIP = {"en": "Not detectable from a public page. ", "fr": "Non détectable à partir d'une page publique. "}
UI = {
 "en": {"your_answer": "your answer:", "ans": {"no": "No", "unsure": "Not sure", "yes": "Yes", "na": "Does not apply"},
        "list_title": "Your list of items to review", "list_date": "Made in your browser on", "sources": "Official sources:", "quotes": "Show the official wording",
        "g_review": "Items to review", "g_review_intro": "From your answers “No” or “Not sure”. This is a list of things to look at, not a finding.",
        "g_none": "Not answered yet", "g_none_intro": "You left these blank, so they are included for review.",
        "g_yes": "You answered “Yes”", "g_yes_intro": "These are your own answers. They are not a check of your site.", "g_na": "Marked as not applicable",
        "disclaimer": RULES["disclaimer_en"], "copied": "Copied.", "copy_failed": "Could not copy. Select the list and copy it by hand.",
        "kinds": {"few": "too few counted words to tell (at least 25 are needed)", "fr": "mostly French", "en": "mostly English", "mix": "a mix of French and English"},
        "est_counts": "Counted French function words: {fr}. Counted English function words: {en}.", "est_share": "French share:", "est_reading": "Rough reading:", "dec": "."},
 "fr": {"your_answer": "votre réponse :", "ans": {"no": "Non", "unsure": "Incertain", "yes": "Oui", "na": "Sans objet"},
        "list_title": "Votre liste d'éléments à revoir", "list_date": "Produite dans votre navigateur le", "sources": "Sources officielles :", "quotes": "Voir le texte officiel",
        "g_review": "Éléments à revoir", "g_review_intro": "D'après vos réponses « Non » ou « Incertain ». C'est une liste de points à examiner, non une conclusion.",
        "g_none": "Pas encore de réponse", "g_none_intro": "Vous avez laissé ces points vides; ils figurent donc dans la liste à revoir.",
        "g_yes": "Vous avez répondu « Oui »", "g_yes_intro": "Ce sont vos propres réponses. Elles ne constituent pas une vérification de votre site.", "g_na": "Marqués sans objet",
        "disclaimer": RULES["disclaimer_fr"], "copied": "Copié.", "copy_failed": "Copie impossible. Sélectionnez la liste et copiez-la à la main.",
        "kinds": {"few": "trop peu de mots comptés pour conclure (il en faut au moins 25)", "fr": "surtout en français", "en": "surtout en anglais", "mix": "un mélange de français et d'anglais"},
        "est_counts": "Mots-outils français comptés : {fr}. Mots-outils anglais comptés : {en}.", "est_share": "Part du français :", "est_reading": "Lecture approximative :", "dec": ","},
}
T = {  # page copy
 "en": {"h1": "Québec French checklist for online stores", "title": "Québec French Checklist for Online Stores (Bill 96)",
  "desc": "Free checklist of items to review for a French version of your online store, each with its official Québec source. Runs in your browser.",
  "lede": "Answer ten questions about your online store. You get a list of items to review, each with the official source for the rule, that you can copy or print. Nothing you type is sent anywhere.",
  "box": "<b>General information, not legal advice.</b> This page lists possible gaps and items to review. It does not decide whether any business meets any law, and no result here means a business is or is not in order. Whether the Charter of the French language applies to your business, and what to do about it, is a question for the OQLF or a lawyer.",
  "ai": "<b>Built with AI assistance.</b> NorthLedger Tools drafted this page with AI tools and checked the wording against the official sources listed below, which were read on %s. A lawyer has not reviewed it. The French version of this page is AI-drafted too.",
  "alt_label": "Version française", "alt_note": "Le texte français de cette page a été rédigé avec l'aide de l'IA et n'a pas encore été révisé par une personne de langue maternelle française.",
  "h_check": "1. Answer the checklist", "check_hint": "For each line, “Yes” means that part is available in French. Unsure or blank lines go on the list to review.",
  "yes": "Yes", "no": "No", "unsure": "Not sure", "na": "Does not apply", "make": "Make my list", "reset": "Clear answers", "copy": "Copy as text", "print": "Print",
  "h_est": "2. Optional: estimate the language of some text", "est_hint": "Paste the text of one of your pages. The tool counts common French and English function words (such as “the”, “and”, “le”, “et”) in your browser. It is a rough word count, not a legal test, and it says nothing about the quality of the French.",
  "est_label": "Your text", "est_btn": "Estimate", "est_ph": "Paste at least a few sentences here",
  "h_know": "Good to know from official sources", "h_src": "Official sources used", "h_ai": "About French text produced with AI",
  "ai_txt": "We recommend a human quality-control step by a qualified translator or a native French speaker before machine-translated store pages, policies or terms are used with customers. The OTTIAQ goes further: it says a language professional should be involved whenever there are real-world consequences (see the source below). That is a professional order's position, not a legal requirement.",
  "noscript": "This checklist needs JavaScript to build the list. The sources are listed below.",
  "limits": "<b>What this page cannot do.</b> It cannot see your site, invoices, packaging or advertising; it only turns your own answers into a list. Rules and guidance change, so read the official pages linked above before you act.",
 "h_contact": "Questions or a quote request",
  "contact_txt": "To ask a question or request a quote for a French version of your store text, write to {mail}. Replies are drafted by an AI assistant and approved by a person before they are sent. We cannot give legal advice. Any French text we produce is an AI-assisted draft that needs a human quality-control step by a qualified translator or native French speaker. Please do not send passwords or payment details.",
  "breadcrumb": "Québec French checklist"},
 "fr": {"h1": "Liste de vérification en français pour boutiques en ligne (Québec)", "title": "Boutique en ligne en français : liste à revoir (Québec)",
  "desc": "Liste gratuite d'éléments à revoir pour offrir votre boutique en ligne en français, chacun avec sa source officielle québécoise. Dans votre navigateur.",
  "lede": "Répondez à dix questions sur votre boutique en ligne. Vous obtenez une liste d'éléments à revoir, chacun avec la source officielle de la règle, que vous pouvez copier ou imprimer. Rien de ce que vous écrivez n'est envoyé.",
  "box": "<b>Information générale, pas un avis juridique.</b> Cette page énumère des écarts possibles et des éléments à revoir. Elle ne détermine pas si une entreprise respecte une loi, et aucun résultat ici ne signifie qu'une entreprise est ou n'est pas en règle. Savoir si la Charte de la langue française s'applique à votre entreprise, et quoi faire, est une question pour l'OQLF ou un juriste.",
  "ai": "<b>Conçu avec l'aide de l'IA.</b> NorthLedger Tools a rédigé cette page avec des outils d'IA et en a vérifié le libellé d'après les sources officielles citées plus bas, lues le %s. Un juriste ne l'a pas révisée. <b>Le texte français de cette page a été rédigé avec l'aide de l'IA et n'a pas encore été révisé par une personne de langue maternelle française.</b>",
  "alt_label": "English version", "alt_note": "",
  "h_check": "1. Répondez à la liste", "check_hint": "Pour chaque ligne, « Oui » signifie que cet élément est offert en français. Les lignes incertaines ou laissées vides vont dans la liste à revoir.",
  "yes": "Oui", "no": "Non", "unsure": "Incertain", "na": "Sans objet", "make": "Produire ma liste", "reset": "Effacer les réponses", "copy": "Copier en texte", "print": "Imprimer",
  "h_est": "2. Facultatif : estimer la langue d'un texte", "est_hint": "Collez le texte d'une de vos pages. L'outil compte, dans votre navigateur, des mots-outils courants français et anglais (comme « le », « et », « the », « and »). C'est un comptage approximatif, pas un test juridique, et il ne dit rien de la qualité du français.",
  "est_label": "Votre texte", "est_btn": "Estimer", "est_ph": "Collez ici au moins quelques phrases",
  "h_know": "Bon à savoir, d'après les sources officielles", "h_src": "Sources officielles utilisées", "h_ai": "À propos du texte français produit avec l'IA",
  "ai_txt": "Nous recommandons une étape de contrôle de la qualité par une personne traductrice qualifiée ou de langue maternelle française avant d'utiliser avec la clientèle des pages, politiques ou conditions traduites automatiquement. L'OTTIAQ va plus loin : selon lui, un professionnel de la langue devrait intervenir chaque fois que la traduction a des conséquences concrètes (voir la source ci-dessous). C'est la position d'un ordre professionnel, non une exigence légale.",
  "noscript": "Cette liste nécessite JavaScript pour produire le résultat. Les sources sont indiquées plus bas.",
  "limits": "<b>Ce que cette page ne peut pas faire.</b> Elle ne voit ni votre site, ni vos factures, ni vos emballages, ni votre publicité; elle transforme seulement vos propres réponses en liste. Les règles et les orientations changent; lisez les pages officielles liées ci-dessus avant d'agir.",
 "h_contact": "Questions ou demande de soumission",
  "contact_txt": "Pour poser une question ou demander une soumission pour une version française des textes de votre boutique, écrivez à {mail}. Les réponses sont rédigées par un assistant d'IA et approuvées par une personne avant d'être envoyées. Nous ne pouvons pas donner d'avis juridique. Tout texte français que nous produisons est une ébauche rédigée avec l'aide de l'IA, qui doit passer par une étape de contrôle de la qualité par une personne traductrice qualifiée ou de langue maternelle française. N'envoyez ni mot de passe ni données de paiement.",
  "breadcrumb": "Liste de vérification en français"},
}
SEC_RE = re.compile(r"^(C11-EN|C11-FR) s\.(.+)$")
def src_label(lang, ref):
    m = SEC_RE.match(ref)
    if m:
        sid, sec = m.groups()
        base = SHORT[lang][sid]
        return (base + (", s. " if lang == "en" else ", art. ") + sec, SRC[sid]["url"])
    return (SHORT[lang][ref], SRC[ref]["url"])

def rule_data(lang):
    out = []
    for r in RULES["rules"]:
        todo = r["review_" + lang]
        if r["id"] == "R-SITE": todo = {"en": "Review whether your site, including product pages, is available in French.", "fr": "Vérifier si votre site, y compris les fiches de produits, est offert en français."}[lang]
        todo = todo.replace(STRIP[lang], "")
        assert "détect" not in todo and "detect" not in todo, r["id"]
        qs = [q for q in r["quotes"] if q["lang"] == lang] or r["quotes"]
        quotes = []
        for q in qs:
            if q["lang"] == lang: note = ""
            elif q["lang"] == "en": note = "official English text only" if lang == "en" else "texte officiel en anglais seulement"
            else: note = "official French text" if lang == "en" else "texte officiel en français"
            nm = SHORT[lang][q["src"]] + ((", s. " if lang == "en" else ", art. ") + q["section"] if q.get("section") else "")
            quotes.append({"text": q["text"], "src": nm, "note": note})
        out.append({"id": r["id"], "label": r["label_" + lang], "ask": ASK[r["id"]][0 if lang == "en" else 1], "todo": todo,
                    "sources": [dict(zip(("label", "url"), src_label(lang, s))) for s in r["sources"]], "quotes": quotes})
    return out

CONTACT = "northledgertools@gmail.com"
MAILLINK = f'<a href="mailto:{CONTACT}">{CONTACT}</a>'
STYLE = """<style>.callout{background:#eef8f6;border-left:5px solid #2A9D8F;padding:.7rem 1rem;margin:1rem 0;border-radius:0 8px 8px 0}.warnbox{background:#fff7e6;border-left:5px solid #c77d0a;padding:.7rem 1rem;margin:1rem 0;border-radius:0 8px 8px 0}
.q{border-top:1px solid #d9e0e8;padding:.7rem 0}.q:first-of-type{border-top:0}.q p{margin:0 0 .3rem;font-weight:600}.opts{display:flex;gap:1rem;flex-wrap:wrap}.opts label{display:inline-flex;gap:.3rem;align-items:center;font-weight:400;margin:0}.opts input{width:auto}
.btns button{margin-right:.5rem}button.sec{background:#fff;color:#1F3A5F;border:1px solid #1F3A5F}textarea{width:100%;min-height:8rem;padding:.55rem;border:1px solid #b9c4d0;border-radius:6px;font:inherit}
blockquote{margin:.4rem 0;padding:.4rem .8rem;border-left:3px solid #b9c4d0;background:#f6f8fb}#b96-out li{margin:.6rem 0}.meta{font-size:.85rem;color:#5b6878;margin:.2rem 0 1rem}
@media print{header.top,footer,#b96-form,.noprint,#b96-est-card,.btns{display:none!important}}</style>"""

def nav_html(lang='en'):
    if lang == 'fr':
        return ('<nav><a href="/calcul-droits-celi/">CELI</a><a href="/calcul-droits-celiapp/">CELIAPP</a><a href="/calcul-remboursement-reer/">REER</a>'
                '<a href="/impot-travailleur-autonome-quebec/">Travailleur autonome</a><a href="/acomptes-provisionnels-travailleur-autonome-quebec/">Acomptes</a><a href="/guides-fr/">Guides</a></nav>')
    return ('<nav><a href="/tfsa-contribution-room-calculator/">TFSA</a><a href="/fhsa-contribution-room-calculator/">FHSA</a><a href="/rrsp-tax-refund-calculator/">RRSP</a>'
            '<a href="/self-employed-tax-calculator/">Self-employed tax</a><a href="/freelancer-tax-set-aside-calculator/">Set-aside</a><a href="/impot-travailleur-autonome-quebec/">Québec</a>'
            '<a href="/1099-self-employment-tax-calculator/">US tax</a><a href="/guides/">Guides</a></nav>')

# ---------- Pricing section (OFF unless --pricing; Auditor must read it first) ----------
TAX_EN = "Prices are in Canadian dollars. No GST, HST or QST is added to these prices at this time. If that changes, we'll tell you before you confirm an order."
TAX_FR = "Les prix sont en dollars canadiens. Ni la TPS, ni la TVH, ni la TVQ ne sont ajoutées à ces prix pour le moment. Si cela change, nous vous le dirons avant que vous confirmiez une commande."
PRICE = {
 "en": {"h": "Prices",
  "intro": "Besides this free checklist, NorthLedger Tools offers AI-assisted Québec-French drafts of store text, each with a checklist of items to review. Launch prices, which may change:",
  "items": [
   ("Free gap-check.", "We run this checklist on the public pages of your store and email you a short list of possible gaps and items to review. It is general information, not legal advice."),
   ("Policy set: C$129.", "French (Québec) versions of up to 4 store policy pages, about 2,500 words in total."),
   ("Product descriptions: C$4 each (first 25).", "The price applies to the first 25 descriptions in one order, up to about 150 words each. Pricing for more is quoted on request."),
   ("Small-store pack: C$399.", "The policy set, up to 25 product descriptions, store interface strings (menus, buttons, checkout and email templates, up to about 800 words) and one round of revisions. Launch price."),
  ],
  "terms": "Delivery target: 5 business days after the scope and payment are confirmed. Every text is an AI-assisted Québec-French draft with a checklist. A review of the French by a native speaker is not included; it can be added as an optional extra, quoted at cost.",
  "tax": TAX_EN,
  "order": "To order or ask for a quote, write to the address in the section below. We confirm the scope and the payment details by email before you pay anything."},
 "fr": {"h": "Prix",
  "intro": "En plus de cette liste gratuite, NorthLedger Tools offre des ébauches en français du Québec, rédigées avec l'aide de l'IA, pour les textes de votre boutique, chacune accompagnée d'une liste d'éléments à revoir. Prix de lancement, susceptibles de changer :",
  "items": [
   ("Vérification gratuite.", "Nous appliquons cette liste aux pages publiques de votre boutique et vous envoyons par courriel une courte liste d'écarts possibles et d'éléments à revoir. Information générale, pas un avis juridique."),
   ("Ensemble de politiques : 129 $ CA.", "Versions en français (Québec) d'au plus 4 pages de politiques de la boutique, environ 2 500 mots au total."),
   ("Descriptions de produits : 4 $ CA chacune (les 25 premières).", "Le prix s'applique aux 25 premières descriptions d'une même commande, d'au plus environ 150 mots chacune. Le prix pour un plus grand nombre est donné sur demande."),
   ("Forfait petite boutique : 399 $ CA.", "L'ensemble de politiques, jusqu'à 25 descriptions de produits, les textes d'interface de la boutique (menus, boutons, modèles de paiement et de courriel, jusqu'à environ 800 mots) et une série de modifications. Prix de lancement."),
  ],
  "terms": "Délai visé : 5 jours ouvrables après la confirmation de la portée du travail et du paiement. Chaque texte est une ébauche en français du Québec rédigée avec l'aide de l'IA, accompagnée d'une liste de contrôle. Une révision du français par une personne de langue maternelle française n'est pas comprise; elle peut être ajoutée en option, sur soumission, au prix coûtant.",
  "tax": TAX_FR,
  "order": "Pour commander ou demander une soumission, écrivez à l'adresse indiquée dans la section ci-dessous. Nous confirmons la portée du travail et les modalités de paiement par courriel avant tout paiement."},
}
def pricing_html(lang):
    if not PRICING: return ""
    q = PRICE[lang]
    lis = "".join(f"<li><b>{e(a)}</b> {e(b)}</li>" for a, b in q["items"])
    return (f'<h2 id="prices">{e(q["h"])}</h2><p>{e(q["intro"])}</p><ul>{lis}</ul><p>{e(q["terms"])}</p>'
            f'<p><b>{e(q["tax"])}</b></p><p>{e(q["order"])}</p>\n')

def page(lang):
    t = T[lang]; fr = lang == "fr"; path = P_FR if fr else P_EN; other = P_EN if fr else P_FR
    rules = rule_data(lang)
    ids = [r["id"] for r in rules]
    # sources + facts shown on the page
    fact_ids = ["F-BILL96", "F-OUTSIDE", "F-FINES", "F-FICHE-NOLEGAL", "F-OTTIAQ"]
    facts = {f["id"]: f for f in RULES["facts"]}
    know = "".join(f'<li>{e(facts[i]["text_" + lang])} <span class="hint">[<a href="{e(SRC[facts[i]["source"]]["url"])}" rel="noopener">{e(SHORT[lang][facts[i]["source"]])}</a>]</span></li>' for i in fact_ids)
    used = ["C11-EN", "C11-FR", "OQLF-FICHE", "QC-OBLIG", "OQLF-FAQ", "OTTIAQ", "NA-BILL96"]
    srcs = "".join(f'<li><a href="{e(SRC[s]["url"])}" rel="noopener">{e(SHORT[lang][s])}</a></li>' for s in used)
    qs = "".join(f'<div class="q"><p id="q-{r["id"]}">{e(r["ask"])}</p><div class="opts" role="radiogroup" aria-labelledby="q-{r["id"]}">'
                 + "".join(f'<label><input type="radio" name="q_{r["id"]}" value="{v}"> {e(t[v])}</label>' for v in ("yes", "no", "unsure", "na")) + "</div></div>" for r in rules)
    data = {"lang": lang, "ui": UI[lang], "rules": rules, "words": RULES["lang_words"]}
    ai_html = t["ai"] % CHECKED
    alt_note = t["alt_note"]
    alt_link = f' · <a href="/{other}" hreflang="{"en-CA" if fr else "fr-CA"}" lang="{"en" if fr else "fr"}">{e(t["alt_label"])}</a>'
    if EN_ONLY and not fr:   # the French page is not published: no link to it and no sentence about it
        alt_link = ""; alt_note = ""
        assert ai_html.endswith(" The French version of this page is AI-drafted too."), ai_html[-80:]
        ai_html = ai_html[:-len(" The French version of this page is AI-drafted too.")]
    body = f'''<h1>{e(t["h1"])}</h1><p class="lede">{e(t["lede"])}</p>
<p class="meta">{"Sources officielles lues le" if fr else "Official sources read on"} {CHECKED}{alt_link}</p>
<div class="warnbox">{t["box"]}</div>
<div class="callout">{ai_html}{(" " + e(alt_note)) if alt_note else ""}</div>
<noscript><p class="bad">{e(t["noscript"])}</p></noscript>
<h2 id="check">{e(t["h_check"])}</h2><p class="hint">{e(t["check_hint"])}</p>
<form id="b96-form" class="card" onsubmit="return false">{qs}<div class="btns"><button type="button" id="b96-make">{e(t["make"])}</button><button type="button" class="sec" id="b96-reset">{e(t["reset"])}</button></div></form>
<div id="b96-out-card" class="card result" hidden><div id="b96-out"></div><div class="btns noprint"><button type="button" id="b96-copy">{e(t["copy"])}</button><button type="button" class="sec" id="b96-print">{e(t["print"])}</button> <span id="b96-status" class="hint" role="status"></span></div></div>
<h2 id="estimate">{e(t["h_est"])}</h2><div class="card" id="b96-est-card"><p class="hint">{e(t["est_hint"])}</p><label for="b96-text">{e(t["est_label"])}</label><textarea id="b96-text" placeholder="{e(t["est_ph"])}"></textarea><button type="button" id="b96-est">{e(t["est_btn"])}</button><p id="b96-est-out" role="status"></p></div>
<h2 id="know">{e(t["h_know"])}</h2><ul>{know}</ul>
<h2 id="ai">{e(t["h_ai"])}</h2><p>{e(t["ai_txt"])}</p>
{pricing_html(lang)}<h2 id="contact">{e(t["h_contact"])}</h2><p>{e(t["contact_txt"]).replace("{mail}", MAILLINK)}</p>
<h2 id="sources">{e(t["h_src"])}</h2><ul>{srcs}</ul>
<p class="disc">{t["limits"]} {e(RULES["disclaimer_" + lang])}</p>
<script type="application/json" id="b96-data">{json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script><script src="/assets/bill96.js"></script>'''
    return body

def shell(path, title, desc, body, lang, alt):
    assert len(title) <= 60, (len(title), title)
    assert len(desc) <= 160, (len(desc), desc)
    url = BASE + path; L = "fr-CA" if lang == "fr" else "en-CA"
    hl = "".join(f'<link rel="alternate" hreflang="{h}" href="{BASE + p}">' for h, p in alt) + f'<link rel="alternate" hreflang="x-default" href="{BASE + P_EN}">'
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "name": title, "url": url, "inLanguage": L, "description": desc,
          "isPartOf": {"@type": "WebSite", "name": BRAND, "url": BASE}, "dateModified": LASTMOD}]}
    foot = ("Fait au Canada. Aucun suivi, aucun témoin, aucune publicité. Les calculs se font dans votre navigateur." if lang == "fr" else
            "Made in Canada. No tracking, no cookies, no ads. Calculations run in your browser; nothing you type is sent anywhere.")
    doc = f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">{hl}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}">
<meta name="theme-color" content="#1F3A5F"><link rel="stylesheet" href="/assets/style.css">{STYLE}{head_extra(path)}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>
<body><header class="top"><div class="w"><a class="brand" href="/">North<span>Ledger</span> Tools</a>{nav_html(lang)}</div></header><main class="w">{body}</main>
<footer><div class="w">{foot} · <a href="/privacy/">{"Confidentialité" if lang == "fr" else "Privacy"}</a>{more_tools(lang, path)} · {"Mis à jour le" if lang == "fr" else "Updated"} {LASTMOD}</div></footer></body></html>'''
    os.makedirs(path, exist_ok=True)
    open(os.path.join(path, "index.html"), "w", encoding="utf-8").write(doc)

HOME_DESC = "Free tax and TFSA calculators for Canadians (plus US and UK tools), a free Québec French checklist and AI-assisted French drafts for online stores."
assert len(HOME_DESC) <= 160, len(HOME_DESC)

def main():
    os.makedirs("assets", exist_ok=True)
    open("assets/bill96.js", "w", encoding="utf-8").write(open(find("bill96.js"), encoding="utf-8").read())
    langs = (("en", P_EN),) if EN_ONLY else (("en", P_EN), ("fr", P_FR))
    paths = [p for _, p in langs]
    alt = [("en-CA", P_EN)] if EN_ONLY else [("en-CA", P_EN), ("fr-CA", P_FR)]
    if EN_ONLY and os.path.isdir(P_FR):   # a generated French page from an earlier full build must not stay behind
        import shutil; shutil.rmtree(P_FR)
    for lang, path in langs:
        body = page(lang)
        shell(path, T[lang]["title"], T[lang]["desc"], body, lang, alt)
    # sitemap (idempotent)
    sm = open("sitemap.xml", encoding="utf-8").read()
    for p in (P_EN, P_FR): sm = re.sub(r"<url><loc>%s</loc>.*?</url>\n?" % re.escape(BASE + p), "", sm)
    sm = sm.replace("</urlset>", "".join(f"<url><loc>{BASE + p}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for p in paths) + "</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    # llms.txt (idempotent, marker block before the guides section)
    t = open("llms.txt", encoding="utf-8").read()
    t = re.sub(r"## Québec French checklist.*?(?=\n## )\n?", "", t, flags=re.S)
    fr_link = "" if EN_ONLY else f" ([français]({BASE}{P_FR}))"
    block = ("## Québec French checklist for online stores (free, runs in the browser)\n"
             f"- [{T['en']['h1']}]({BASE}{P_EN}){fr_link}: ten questions give a copyable list of items to review for a French version of an online store, each with its official Québec source (Charter of the French language, OQLF, quebec.ca). General information, not legal advice.\n\n")
    assert "## Guides" in t
    t = t.replace("## Guides", block + "## Guides", 1)
    open("llms.txt", "w", encoding="utf-8").write(t)
    # home page: link block + meta description (idempotent)
    s = open("index.html", encoding="utf-8").read()
    s = re.sub(r"<!--nl-b96-->.*?<!--/nl-b96-->", "", s, flags=re.S)
    fr_home = "" if EN_ONLY else f' · <a href="/{P_FR}" hreflang="fr-CA">version française</a>'
    blk = (f'<!--nl-b96--><h2>Québec French checklist</h2><p>Selling online to customers in Québec? A free checklist that turns your answers into a list of items to review, each with its official source: '
           f'<a href="/{P_EN}">Québec French checklist for online stores</a>{fr_home}. AI-assisted French drafts of store text are available on request.</p><!--/nl-b96-->')
    assert "<h2>About</h2>" in s
    s = s.replace("<h2>About</h2>", blk + "<h2>About</h2>", 1)
    s, n1 = re.subn(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(HOME_DESC)}">', s, count=1)
    s, n2 = re.subn(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(HOME_DESC)}">', s, count=1)
    assert n1 == 1 and n2 == 1
    open("index.html", "w", encoding="utf-8").write(s)
    # guides hub link block(s) (idempotent)
    hubs = [("guides/index.html", "Québec French checklist for online stores", P_EN, "A free checklist that turns your answers into a list of items to review for a French version of an online store, each with its official source.", "For online stores")]
    if not EN_ONLY:
        hubs.append(("guides-fr/index.html", "Liste de vérification en français pour boutiques en ligne (Québec)", P_FR, "Une liste gratuite qui transforme vos réponses en éléments à revoir pour offrir une boutique en ligne en français, chacun avec sa source officielle.", "Pour les boutiques en ligne"))
    for f, name, pth, blurb, h in hubs:
        g = open(f, encoding="utf-8").read()
        g = re.sub(r"<!--nl-b96-->.*?<!--/nl-b96-->", "", g, flags=re.S)
        blk = f'<!--nl-b96--><h2>{e(h)}</h2><div class="rel"><a href="/{pth}"><b>{e(name)}</b>{e(blurb)}</a></div><!--/nl-b96-->'
        assert g.count("</main>") == 1, f
        g = g.replace("</main>", blk + "</main>", 1)
        open(f, "w", encoding="utf-8").write(g)
    print("bill96: generated", ", ".join(paths), "(en-only)" if EN_ONLY else "", "(pricing on)" if PRICING else "(pricing off)")
if __name__ == "__main__": main()
