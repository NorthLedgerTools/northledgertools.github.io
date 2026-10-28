"""Post-build step (run after gen.py and guides_gen.py): adds descriptive internal-link blocks so every page has >= 6 inbound links
(Growth request 2026-10-25). Idempotent: each block sits between <!--nl-x-->...<!--/nl-x--> markers and is replaced on every run."""
import re
BASE_MARK=("<!--nl-x-->","<!--/nl-x-->")
EN={ # path: (anchor text, one-line description)
"1099-self-employment-tax-calculator/":("1099 self-employment tax calculator (US)","self-employment tax, income tax with the QBI deduction and quarterly estimated payments"),
"texas-paycheck-calculator/":("Texas paycheck calculator","take-home pay, overtime and bonus; Texas has no state income tax"),
"california-paycheck-calculator/":("California paycheck calculator","take-home pay with EDD withholding, 1.3% SDI and daily overtime"),
"uk-vat-calculator/":("UK VAT calculator","add or remove 20%, 5% or 0% VAT and check the registration deadline"),
"vat-flat-rate-scheme-calculator/":("VAT Flat Rate Scheme calculator (UK)","sector rates, the 16.5% limited cost test and the first-year discount"),
"guides/us-self-employment-tax-explained/":("Self-employment tax explained (US guide)","why it is 15.3% of 92.35% of profit, with a worked table"),
"guides/us-estimated-tax-safe-harbors/":("Estimated tax safe harbors (US guide)","how little you can pay each quarter and still avoid a penalty"),
}
USUK=["1099-self-employment-tax-calculator/","texas-paycheck-calculator/","california-paycheck-calculator/","uk-vat-calculator/","vat-flat-rate-scheme-calculator/"]
USG=["guides/us-self-employment-tax-explained/","guides/us-estimated-tax-safe-harbors/"]
CA_EN={
"tfsa-contribution-room-calculator/":("TFSA contribution room calculator","room left year by year from 2009"),
"fhsa-contribution-room-calculator/":("FHSA contribution room calculator","participation room, carry-forward and lifetime limit"),
"rrsp-tax-refund-calculator/":("RRSP tax refund calculator","tax saved by an RRSP contribution in ON, QC, BC and AB"),
"self-employed-tax-calculator/":("Self-employed tax calculator for Ontario, BC and Alberta","income tax and CPP/CPP2 on self-employment income"),
"quebec-self-employed-tax-calculator/":("Quebec self-employed tax calculator","Quebec and federal tax, QPP, QPIP and Health Services Fund"),
"quebec-tax-instalments-calculator/":("Quebec tax instalment calculator","quarterly instalments to Revenu Québec and the CRA"),
"freelancer-tax-set-aside-calculator/":("Freelancer tax set-aside calculator","what percentage of each payment to save for tax and CPP"),
}
FR_CALC={
"calcul-droits-celi/":("Calcul des droits CELI","droits de cotisation année par année depuis 2009"),
"calcul-droits-celiapp/":("Calcul des droits CELIAPP","droits de participation, report et plafond à vie"),
"calcul-remboursement-reer/":("Calcul du remboursement d'impôt REER","impôt économisé par une cotisation REER"),
"impot-travailleur-autonome-quebec/":("Impôt de travailleur autonome au Québec","impôt, RRQ, RQAP et FSS"),
"impot-travailleur-autonome-ontario-cb-alberta/":("Impôt de travailleur autonome en Ontario, C.-B. et Alberta","impôt fédéral et provincial et RPC/RPC2"),
"acomptes-provisionnels-travailleur-autonome-quebec/":("Calcul des acomptes provisionnels (Québec)","acomptes à Revenu Québec et à l'ARC"),
}
FR_GUIDES={
"guides-fr/surcotisation-celi/":("Surcotisation au CELI","l'impôt de 1 % par mois, expliqué"),
"guides-fr/celiapp-et-regime-d-accession-a-la-propriete/":("CELIAPP et RAP","utiliser les deux pour une première propriété"),
"guides-fr/date-limite-reer-et-plafond-de-cotisation/":("REER : plafond et date limite","plafonds 2026 et 2027, marge de 2 000 $"),
"guides-fr/cotisations-travailleur-autonome-quebec-2026/":("Cotisations du travailleur autonome au Québec","RRQ, RQAP et FSS"),
"guides-fr/acomptes-provisionnels-quelle-methode/":("Acomptes provisionnels : quelle méthode choisir","les trois méthodes et un exemple chiffré"),
}
CA_GUIDES={ # English Canadian guides (Growth request 2026-10-26: at least 6 inbound links each)
"guides/gst-hst-small-supplier-freelancers/":("GST/HST small supplier rule for freelancers","when a freelancer must register, with the single-quarter and four-quarter tests"),
"guides/how-the-tfsa-limit-is-set/":("How the TFSA annual limit is set","the indexation rule and a year-by-year table since 2009"),
"guides/rrsp-deduction-limit-explained/":("RRSP deduction limit explained","how the limit is built, the 2026 and 2027 limits and the March 1 deadline"),
"guides/tfsa-over-contribution-penalty/":("TFSA over-contribution penalty","how the 1% monthly tax on excess amounts works, with examples"),
}
CA_GUIDE_HOSTS=["tfsa-contribution-room-calculator/","fhsa-contribution-room-calculator/","rrsp-tax-refund-calculator/","self-employed-tax-calculator/","quebec-self-employed-tax-calculator/",
"quebec-tax-instalments-calculator/","freelancer-tax-set-aside-calculator/","guides/fhsa-and-home-buyers-plan/","guides/self-employed-cpp-explained/","guides/which-tax-instalment-method/"]
def lst(paths,table,self_path):
    return "<ul>"+"".join(f'<li><a href="/{p}">{table[p][0]}</a>: {table[p][1]}.</li>' for p in paths if p!=self_path)+"</ul>"
def block(path):
    if path in USUK:
        return ("<h2>More calculators</h2><p>Other United States and United Kingdom calculators on this site, and the matching guides:</p>"
                +lst(USUK,EN,path)+(lst(USG,EN,path) if path in USUK[:3] else "")
                +'<p>See also the <a href="/guides/">guides</a> and the <a href="/">Canadian calculators</a>.</p>')
    if path in USG:
        return "<h2>Related calculators</h2>"+lst(USUK[:3]+USG,EN,path)
    if path=="guides/":
        return "<h2>Calculators for the United States and United Kingdom</h2>"+lst(USUK,EN,"")
    if path in FR_CALC:
        return ('<h2>Voir aussi</h2><p>Autres calculateurs en français :</p>'+lst(list(FR_CALC),FR_CALC,path)
                +'<p>Guides connexes :</p>'+lst(list(FR_GUIDES),FR_GUIDES,"")+'<p><a href="/guides-fr/">Tous les guides en français</a>.</p>')
    if path in FR_GUIDES:
        return ('<h2>Voir aussi</h2><p>Autres guides :</p>'+lst(list(FR_GUIDES),FR_GUIDES,path)
                +'<p>Calculateurs en français :</p>'+lst(list(FR_CALC),FR_CALC,"")+'<p><a href="/guides-fr/">Tous les guides en français</a>.</p>')
    if path in CA_EN and path in ("quebec-self-employed-tax-calculator/","quebec-tax-instalments-calculator/","self-employed-tax-calculator/","freelancer-tax-set-aside-calculator/"):
        return ("<h2>Related calculators</h2>"+lst(["self-employed-tax-calculator/","quebec-self-employed-tax-calculator/","quebec-tax-instalments-calculator/","freelancer-tax-set-aside-calculator/","rrsp-tax-refund-calculator/"],CA_EN,path))
    return None
def guides_block(path):
    if path in CA_GUIDES or path in CA_GUIDE_HOSTS:
        return "<h2>Related Canadian tax guides</h2><p>More guides on limits, deadlines and registration:</p>"+lst(list(CA_GUIDES),CA_GUIDES,path)
    return None
def inject(path,html):
    html=re.sub(r"<!--nl-x-->.*?<!--/nl-x-->","",html,flags=re.S)
    b=block(path)
    g=guides_block(path)
    if g: b=(b or "")+g
    if not b: return html
    return html.replace("</main>",BASE_MARK[0]+b+BASE_MARK[1]+"</main>",1)
def home(html):
    html=re.sub(r"<!--nl-x-->.*?<!--/nl-x-->","",html,flags=re.S)
    sec=("<!--nl-x--><h2>United States and United Kingdom calculators</h2><p>The same approach for US and UK users, each built on the official rules:</p>"
         +lst(USUK,EN,"")+"<p>Matching US guides:</p>"+lst(USG,EN,"")+"<!--/nl-x-->")
    assert "<h2>About</h2>" in html
    return html.replace("<h2>About</h2>",sec+"<h2>About</h2>",1)
def tools_json():
    import json,html,glob
    def info(p):
        s=open(p+"index.html",encoding="utf-8").read()
        t=html.unescape(re.search(r"<title>(.*?)</title>",s).group(1)); d=html.unescape(re.search(r'<meta name="description" content="(.*?)">',s).group(1))
        l=re.search(r'<html lang="([^"]+)"',s).group(1)
        return {"name":t,"url":"https://northledgertools.com/"+p,"description":d,"language":l}
    sm=open("sitemap.xml").read(); paths=[u.replace("https://northledgertools.com/","") for u in re.findall(r"<loc>(.*?)</loc>",sm)]
    skip={"","privacy/","guides/","guides-fr/","homebrew-calculator/"}  # homebrew demoted 2026-10-28: live, not listed in the catalog
    tools=[info(p) for p in sorted(paths) if p not in skip and not p.startswith(("guides/","guides-fr/"))]
    guides=[info(p) for p in sorted(paths) if p.startswith(("guides/","guides-fr/")) and p not in skip]
    out={"site":"https://northledgertools.com","publisher":"NorthLedger Tools","pricing":"free, no sign-in, no ads","privacy":"calculations run in the browser (see /privacy/)",
         "not_advice":"Planning tools, not tax advice.","llms_txt":"https://northledgertools.com/llms.txt","sitemap":"https://northledgertools.com/sitemap.xml","tools":tools,"guides":guides}
    open("tools.json","w",encoding="utf-8").write(json.dumps(out,ensure_ascii=False,indent=1)+"\n")
def main():
    tools_json()
    for table in (EN,CA_EN,FR_CALC,FR_GUIDES,CA_GUIDES,dict.fromkeys(CA_GUIDE_HOSTS)):
        for p in table:
            f=p+"index.html"; s=open(f,encoding="utf-8").read(); open(f,"w",encoding="utf-8").write(inject(p,s))
    f="guides/index.html"; s=open(f,encoding="utf-8").read(); open(f,"w",encoding="utf-8").write(inject("guides/",s))
    s=open("index.html",encoding="utf-8").read(); open("index.html","w",encoding="utf-8").write(home(s))
if __name__=="__main__": main()
