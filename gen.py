import json,os,html,datetime
BASE="https://northledgertools.github.io/"; G="https://northledgertools.gumroad.com/l/"
UPD="2026-10-13"; BRAND="NorthLedger Tools"
def faq_ld(faq): return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
def app_ld(name,url,desc,cat="FinanceApplication",lang="en-CA"):
    return {"@type":"WebApplication","name":name,"url":url,"description":desc,"applicationCategory":cat,"operatingSystem":"Any (web browser)","inLanguage":lang,
            "isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"CAD"},"publisher":{"@type":"Organization","name":BRAND,"url":BASE}}
def page(path,title,desc,body,lang="en",ld=None,alt=None,script="",extra=""):
    url=BASE+path; L="fr-CA" if lang=="fr" else "en-CA"
    hl="".join(f'<link rel="alternate" hreflang="{h}" href="{BASE+p}">' for h,p in (alt or []))
    if alt: hl+=f'<link rel="alternate" hreflang="x-default" href="{BASE+[p for h,p in alt if h.startswith("en")][0]}">'
    ldj=f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":ld},ensure_ascii=False)}</script>' if ld else ""
    nav=('<nav><a href="/tfsa-contribution-room-calculator/">TFSA</a><a href="/fhsa-contribution-room-calculator/">FHSA</a><a href="/self-employed-tax-calculator/">Self-employed tax</a><a href="/impot-travailleur-autonome-quebec/">Québec</a><a href="/homebrew-calculator/">Homebrew</a></nav>')
    foot=("Fait au Canada. Aucun suivi, aucun témoin, aucune publicité. Les calculs se font dans votre navigateur." if lang=="fr" else
          "Made in Canada. No tracking, no cookies, no ads. Calculations run in your browser; nothing you type is sent anywhere.")
    doc=f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}">{hl}
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}">
<meta name="theme-color" content="#1F3A5F">{extra}<link rel="stylesheet" href="/assets/style.css"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">{ldj}</head>
<body><header class="top"><div class="w"><a class="brand" href="/">North<span>Ledger</span> Tools</a>{nav}</div></header><main class="w">{body}</main>
<footer><div class="w">{foot} · <a href="/privacy/">{"Confidentialité" if lang=="fr" else "Privacy"}</a> · {"Mis à jour le" if lang=="fr" else "Updated"} {UPD}</div></footer>
<script src="/assets/engine.js"></script>{script}</body></html>'''
    os.makedirs(path or ".",exist_ok=True); open(os.path.join(path,"index.html") if path else "index.html","w").write(doc)
def faqhtml(faq,h="Frequently asked questions"): return f"<h2>{h}</h2>"+"".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in faq)
def src(items,h="Sources"): return f"<h2>{h}</h2><ul>"+"".join(f'<li><a href="{u}" rel="noopener">{html.escape(t)}</a></li>' for t,u in items)+"</ul>"
FMT='const $=id=>document.getElementById(id),v=id=>{const x=parseFloat(($(id).value||"").replace(/[ ,$]/g,""));return isFinite(x)?x:0};'
money_en='const f=x=>(x<0?"-":"")+"$"+Math.abs(x).toLocaleString("en-CA",{minimumFractionDigits:2,maximumFractionDigits:2});'
money_fr='const f=x=>(x<0?"-":"")+Math.abs(x).toLocaleString("fr-CA",{minimumFractionDigits:2,maximumFractionDigits:2})+" $";'

# ---------- TFSA ----------
faq=[("How is TFSA contribution room calculated?","You accumulate the annual TFSA dollar limit for every year from 2009 (or the year you turned 18, if later) in which you were a resident of Canada. Unused room carries forward indefinitely. Contributions use up room, and withdrawals are added back to your room on January 1 of the following year."),
("What is the TFSA limit for 2026?","The 2026 TFSA annual limit is $7,000. Someone who was 18 or older and resident in Canada in 2009 and has never contributed has $109,000 of total room in 2026."),
("What are the TFSA limits by year since 2009?","$5,000 for 2009–2012, $5,500 for 2013–2014, $10,000 for 2015, $5,500 for 2016–2018, $6,000 for 2019–2022, $6,500 for 2023, and $7,000 for 2024, 2025 and 2026."),
("If I withdraw from my TFSA, can I put the money back the same year?","Only if you still have unused room. The amount you withdraw is added back to your room on January 1 of the next year, not immediately. Re-contributing the same year without room is an over-contribution."),
("What is the penalty for over-contributing to a TFSA?","The CRA charges a tax of 1% per month on the highest excess amount in your TFSA for each month the excess remains."),
("Is my CRA My Account TFSA room always correct?","CRA My Account is the official record, but it is based on information your financial institutions report, usually once a year, so it may not include contributions or withdrawals from the current year. That is why tracking your own transactions matters."),
("Do transfers between my own TFSAs count as withdrawals?","A direct transfer between your TFSAs done by the institutions is not a withdrawal and does not affect your room. Withdrawing cash and depositing it into another TFSA yourself does count as a withdrawal and a new contribution."),
("What will the 2027 TFSA limit be?","As of October 2026 the CRA has not announced the 2027 limit. The limit is indexed to inflation and rounded to the nearest $500; this calculator will be updated when the CRA publishes it.")]
yrs="".join(f'<tr><td>{y}</td><td><input inputmode="decimal" id="c{y}" aria-label="Contributions {y}"></td><td><input inputmode="decimal" id="w{y}" aria-label="Withdrawals {y}"></td></tr>' for y in range(2009,2027))
body=f'''<h1>TFSA Contribution Room Calculator 2026</h1>
<p class="lede">Find out how much you can still put in your Tax-Free Savings Account this year: room is rebuilt year by year from 2009 using the CRA's annual limits, with withdrawals added back the following January, exactly the way the CRA counts it.</p>
<div class="card"><div class="grid"><div><label for="by">Birth year</label><input id="by" inputmode="numeric" placeholder="e.g. 1994"></div>
<div><label for="ry">First year you were a resident of Canada <span class="hint">(2009 or earlier: enter 2009)</span></label><input id="ry" inputmode="numeric" value="2009"></div></div>
<label>Your TFSA contributions and withdrawals by year <span class="hint">(optional; leave blank if none, totals across all your TFSAs)</span></label>
<div class="scroll"><table><thead><tr><th>Year</th><th>Contributions</th><th>Withdrawals</th></tr></thead><tbody>{yrs}</tbody></table></div>
<button id="go">Calculate my TFSA room</button></div>
<div id="out" class="card result" hidden></div>
<div class="cta"><b>Track TFSA, RRSP and FHSA in one sheet: Canadian Contribution Room Tracker 2026</b>
<p>This free calculator covers the TFSA from yearly totals. The spreadsheet version (Excel / Google Sheets) tracks all three registered accounts together and lets you:</p><ul><li>see red over-contribution warnings for TFSA, RRSP and FHSA on one summary page</li><li>log every deposit and withdrawal by date and institution, in one place</li><li>track RRSP deduction room (Mar 3, 2026 – Mar 1, 2027 window, $2,000 buffer) and FHSA room with carry-forward too</li><li>get a blank file plus a filled example, works offline</li></ul><a class="btn" href="{G}pdxqug">Get the tracker (CA$14) →</a> <a class="alt" href="https://www.etsy.com/listing/4594000039" rel="noopener">or buy on Etsy</a></div>
<h2>How the CRA counts TFSA room</h2><p>Your room for a year = unused room carried forward + withdrawals made in the previous year + the new annual limit. You earn the annual limit only for years in which you were at least 18 and resident in Canada at some point. Investment growth or losses inside the TFSA do not change your room.</p>
<div class="scroll"><table><thead><tr><th>Years</th><th>Annual limit</th></tr></thead><tbody><tr><td>2009–2012</td><td>$5,000</td></tr><tr><td>2013–2014</td><td>$5,500</td></tr><tr><td>2015</td><td>$10,000</td></tr><tr><td>2016–2018</td><td>$5,500</td></tr><tr><td>2019–2022</td><td>$6,000</td></tr><tr><td>2023</td><td>$6,500</td></tr><tr><td>2024–2026</td><td>$7,000</td></tr><tr><td><b>Total 2009–2026</b></td><td><b>$109,000</b></td></tr></tbody></table></div>
{faqhtml(faq)}
{src([("CRA: Calculate your TFSA contribution room","https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/tax-free-savings-account/contributions.html"),("CRA: MP, DB, RRSP, DPSP, ALDA, TFSA limits, YMPE and YAMPE","https://www.canada.ca/en/revenue-agency/services/tax/registered-plans-administrators/pspa/mp-rrsp-dpsp-tfsa-limits-ympe.html")])}
<p class="disc">Not tax or financial advice. Estimates use CRA limits as of October 12, 2026 and assume you were resident for every year from the year you enter. It does not handle periods of non-residency after becoming a resident, qualifying transfers, or amounts the CRA has adjusted. Your CRA My Account is the official record; check it before contributing near your limit.</p>'''
js='<script>'+FMT+money_en+'''$("go").onclick=()=>{const by=parseInt($("by").value),ry=parseInt($("ry").value)||2009,c={},w={};
for(let y=2009;y<=2026;y++){c[y]=v("c"+y);w[y]=v("w"+y);}const o=$("out");o.hidden=false;
if(!(by>1900&&by<2027)){o.innerHTML="<p class=bad>Enter your birth year (e.g. 1994).</p>";return;}
const R=NL.tfsa(by,Math.max(2009,ry),c,w),last=R[R.length-1];
if(!R.some(r=>r.eligible)){o.innerHTML="<p>You have no TFSA room yet: room starts in the year you turn 18 (and are resident in Canada).</p>";return;}
let t="<div class=scroll><table><thead><tr><th>Year</th><th>Limit</th><th>Room Jan 1</th><th>Contrib.</th><th>Withdr.</th><th>Room Dec 31</th></tr></thead><tbody>";
for(const r of R){if(!r.eligible&&!r.contrib)continue;t+=`<tr${r.left<0?" class=over":""}><td>${r.year}</td><td>${f(r.limit)}</td><td>${f(r.start)}</td><td>${f(r.contrib)}</td><td>${f(r.wd)}</td><td>${f(r.left)}</td></tr>`;}
t+="</tbody></table></div>";const over=R.find(r=>r.left<0);
o.innerHTML=`<p>TFSA room left for 2026</p><p class=big>${f(last.left)}</p>`+(last.left<0?`<p class=bad>You appear to be over-contributed by ${f(-last.left)}. The CRA charges 1% per month on the excess. Check CRA My Account and consider withdrawing the excess.</p>`:"")+
(over&&last.left>=0?`<p class=bad>Note: you appear to have been over your limit in ${over.year}.</p>`:"")+`<p class=hint>On January 1, 2027 you will also get back the ${f(last.wd)} withdrawn in 2026, plus the 2027 limit (not yet announced).</p>`+t;o.scrollIntoView({behavior:"smooth"});};</script>'''
page("tfsa-contribution-room-calculator/","TFSA Contribution Room Calculator 2026 (Free, Year by Year) | NorthLedger Tools",
 "Free TFSA room calculator for 2026: enter your birth year and contributions to see your room left, year by year from 2009 using CRA limits ($7,000 for 2026).",
 body,ld=[app_ld("TFSA Contribution Room Calculator 2026",BASE+"tfsa-contribution-room-calculator/","Calculates Canadian TFSA contribution room year by year from 2009 using CRA annual limits."),faq_ld(faq)],script=js)

# ---------- ROC self-employed ----------
faq=[("How much CPP does a self-employed person pay in 2026?","Self-employed people pay both the employee and employer shares: 11.9% of net self-employment earnings between $3,500 and $74,600 (maximum $8,460.90), plus the second additional contribution (CPP2) of 8% on earnings between $74,600 and $85,000 (maximum $832). If you also have employment income, contributions already paid through your job reduce what you owe."),
("Is the CPP I pay as self-employed deductible?","Partly. The employer half of the base contributions and the enhanced portion are deducted from income (lines 22200 and 22215), and the remaining employee base portion gives a non-refundable tax credit. This estimator applies both."),
("When is tax due for self-employed income for 2026?","For the 2026 tax year, self-employed individuals have until June 15, 2027 to file, but any balance owing must be paid by April 30, 2027 to avoid interest."),
("Do I need to pay tax instalments?","You may need to pay quarterly instalments (March 15, June 15, September 15, December 15) if your net tax owing is more than $3,000 in 2026 and in either 2025 or 2024. The CRA sends instalment reminders when they are required."),
("What is not included in this estimate?","GST/HST, EI special benefits premiums (optional for self-employed people), capital gains, dividends and their credits, pension income, tuition, medical, donations, spousal and other credits, the Canada Workers Benefit and refundable credits. Enter only business profit after expenses."),
("Which 2026 rates are used?","Federal brackets 14% / 20.5% / 26% / 29% / 33% (the lowest rate is 14% for 2026), federal basic personal amount up to $16,452, and the 2026 provincial brackets and basic personal amounts for Ontario, British Columbia (5.60% lowest rate) and Alberta (new 8% first bracket), as published by the CRA and the provinces.")]
body=f'''<h1>Self-Employed Tax Calculator 2026 (Ontario, BC, Alberta)</h1>
<p class="lede">Estimate your 2026 federal and provincial income tax plus CPP and CPP2 on freelance or business income, including Ontario surtax and Health Premium, the BC tax reduction and the Alberta 8% bracket.</p>
<div class="card"><div class="grid">
<div><label for="prov">Province of residence on Dec 31, 2026</label><select id="prov"><option value="ON">Ontario</option><option value="BC">British Columbia</option><option value="AB">Alberta</option></select></div>
<div><label for="rev">Self-employment revenue (gross)</label><input id="rev" inputmode="decimal" placeholder="60000"></div>
<div><label for="exp">Business expenses</label><input id="exp" inputmode="decimal" placeholder="8000"></div>
<div><label for="emp">Employment income (T4), if any</label><input id="emp" inputmode="decimal"></div>
<div><label for="oth">Other taxable income <span class="hint">(interest, etc.)</span></label><input id="oth" inputmode="decimal"></div>
<div><label for="rrsp">RRSP deduction</label><input id="rrsp" inputmode="decimal"></div>
<div><label for="fhsa">FHSA deduction</label><input id="fhsa" inputmode="decimal"></div>
<div><label for="wh">Tax withheld at source <span class="hint">(T4 box 22)</span></label><input id="wh" inputmode="decimal"></div>
<div><label for="paid">Instalments already paid for 2026</label><input id="paid" inputmode="decimal"></div></div>
<button id="go">Estimate my 2026 tax</button></div><div id="out" class="card result" hidden></div>
<div class="cta"><b>Track it all year: Self-Employed Tax Estimator 2026 (ON · BC · AB) spreadsheet</b><p>Same formulas as this page, plus:</p><ul><li>a monthly income and expense log so your estimate updates as the year goes</li><li>a suggested amount to set aside from each payment, and instalment due dates</li><li>every rate on an editable Rates tab with its official source</li><li>blank file + filled example; works in Excel, Google Sheets and LibreOffice</li></ul><a class="btn" href="{G}bblrt">Get the estimator (CA$17) →</a> <a class="alt" href="https://www.etsy.com/listing/4594017328" rel="noopener">or buy on Etsy</a></div>
<h2>How the estimate works</h2><p>Net self-employment income (revenue minus expenses) is added to your other income. CPP and CPP2 on self-employment earnings are calculated at the self-employed rates, minus anything already paid through employment. Deductible CPP, RRSP and FHSA amounts reduce taxable income. Federal tax uses the 2026 brackets and credits (basic personal amount, Canada employment amount, CPP and EI credits). Provincial tax adds the rules for your province: Ontario surtax, Ontario tax reduction, LIFT credit and Ontario Health Premium; the BC tax reduction; and Alberta's 2026 brackets.</p>
<p>Quebec resident? Use the <a href="/impot-travailleur-autonome-quebec/">Quebec self-employed calculator (QPP, QPIP, FSS)</a>.</p>
{faqhtml(faq)}
{src([("CRA: Canadian income tax rates for individuals","https://www.canada.ca/en/revenue-agency/services/tax/individuals/frequently-asked-questions-individuals/canadian-income-tax-rates-individuals-current-previous-years.html"),("CRA: CPP contribution rates, maximums and exemptions","https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/payroll/payroll-deductions-contributions/canada-pension-plan-cpp/cpp-contribution-rates-maximums-exemptions.html"),("CRA: T4127 Payroll Deductions Formulas (July 2026)","https://www.canada.ca/en/revenue-agency/services/forms-publications/payroll/t4127-payroll-deductions-formulas/t4127-jul.html"),("CRA: Income tax instalments","https://www.canada.ca/en/revenue-agency/services/payments/payments-cra/individual-payments/income-tax-instalments.html"),("Ontario: Low-income Individuals and Families Tax (LIFT) Credit","https://www.ontario.ca/page/low-income-individuals-and-families-tax-credit"),("BC: Personal income tax rates","https://www2.gov.bc.ca/gov/content/taxes/income-taxes/personal/tax-rates"),("CRA: T4032AB payroll tables, general information","https://www.canada.ca/en/revenue-agency/services/forms-publications/payroll/t4032-payroll-deductions-tables/t4032ab-jan/t4032ab-january-general-information.html")])}
<p class="disc">Not tax advice. A simplified estimate for 2026 using rates published as of October 12, 2026, for a single individual with no other credits. Your actual tax depends on your full return. For filing, use certified tax software or a qualified professional.</p>'''
js='<script>'+FMT+money_en+'''$("go").onclick=()=>{const p=$("prov").value,r=NL.calc(p,{rev:v("rev"),exp:v("exp"),emp:v("emp"),other:v("oth"),rrsp:v("rrsp"),fhsa:v("fhsa"),withheld:v("wh"),paid:v("paid")});
const se=Math.max(0,r.se),pct=se>0?(r.bill-0)/Math.max(1,se+v("emp")+v("oth")):0,o=$("out");o.hidden=false;
const rows=[["Net self-employment income",r.se],["Taxable income",r.ti],["Federal income tax",r.fed],["Provincial income tax"+(p==="ON"?" (incl. Health Premium "+f(r.ohp)+")":""),r.prov],["CPP (self-employed)",r.scpp],["CPP2",r.scpp2],["Total income tax + CPP",r.bill],["Less withheld and instalments paid",-(v("wh")+v("paid"))]];
o.innerHTML=`<p>${r.balance>=0?"Estimated balance owing for 2026":"Estimated refund for 2026"}</p><p class=big>${f(Math.abs(r.balance))}</p>`+
`<p class=hint>That is about ${(100*r.bill/Math.max(1,se+v("emp")+v("oth"))).toFixed(1)}% of your total income in income tax and CPP. Balance due April 30, 2027.</p>`+
(r.tax-v("wh")>3000?"<p class=hint>Your net tax owing is over $3,000: if that was also true in 2024 or 2025, the CRA expects quarterly instalments.</p>":"")+
"<table><tbody>"+rows.map(([a,b])=>`<tr><td>${a}</td><td>${f(b)}</td></tr>`).join("")+"</tbody></table>";o.scrollIntoView({behavior:"smooth"});};</script>'''
page("self-employed-tax-calculator/","Self-Employed Tax Calculator 2026: Ontario, BC, Alberta (CPP included) | NorthLedger Tools",
 "Free 2026 self-employed income tax and CPP calculator for Ontario, British Columbia and Alberta. Estimate federal + provincial tax, CPP/CPP2 and balance owing.",
 body,ld=[app_ld("Self-Employed Tax Calculator 2026 (ON, BC, AB)",BASE+"self-employed-tax-calculator/","Estimates 2026 federal and provincial income tax plus CPP for self-employed Canadians in Ontario, BC and Alberta."),faq_ld(faq)],script=js)

# ---------- Quebec FR + EN ----------
QSRC=[("Revenu Québec – Taux d'imposition / Tax rates","https://www.revenuquebec.ca/fr/citoyens/declaration-de-revenus/produire-votre-declaration-de-revenus/taux-dimposition/"),
("Revenu Québec – Travailleurs autonomes : tables d'impôt et de cotisations","https://www.revenuquebec.ca/fr/citoyens/declaration-de-revenus/produire-votre-declaration-de-revenus/travailleurs-autonomes-preparez-votre-declaration/travailleurs-autonomes-tables-dimpot-et-de-cotisations/"),
("Retraite Québec – Données du RRQ / QPP figures","https://www.retraitequebec.gouv.qc.ca/en/programs/quebec-pension-plan/quebec-pension-plan-figures"),
("Revenu Québec – RQAP : maximum des revenus assurables et taux / QPIP rates","https://www.revenuquebec.ca/en/businesses/source-deductions-and-employer-contributions/calculating-source-deductions-and-contributions/qpip-premiums/maximum-insurable-earnings-and-premium-rate/"),
("Finances Québec – Le régime d'imposition 2026","https://www.finances.gouv.qc.ca/Budget_et_mise_a_jour/maj/documents/AUTFR_RegimeImpot2026.pdf"),
("ARC/CRA – T4032-QC, renseignements généraux 2026","https://www.canada.ca/en/revenue-agency/services/forms-publications/payroll/t4032-payroll-deductions-tables/t4032qc-jan/t4032qc-january-general-information.html"),
("ARC/CRA – Acomptes provisionnels / Income tax instalments","https://www.canada.ca/en/revenue-agency/services/payments/payments-cra/individual-payments/income-tax-instalments.html")]
T={"fr":dict(path="impot-travailleur-autonome-quebec/",title="Calcul impôt travailleur autonome Québec 2026 (RRQ, RQAP, FSS) | NorthLedger Tools",
 desc="Calculateur gratuit 2026 pour travailleurs autonomes au Québec : impôt du Québec et fédéral (abattement 16,5 %), RRQ, RQAP et FSS. Solde à payer estimé.",
 h1="Calcul de l'impôt d'un travailleur autonome au Québec 2026",lede="Estimez votre impôt du Québec et fédéral, vos cotisations au RRQ et au RQAP et la cotisation au Fonds des services de santé (FSS) sur vos revenus d'entreprise ou de pigiste en 2026.",
 L=["Revenus bruts de travail autonome","Dépenses d'entreprise","Revenu d'emploi (T4/RL-1), s'il y a lieu","Autres revenus imposables","Déduction REER","Déduction CELIAPP","Impôt fédéral retenu à la source","Impôt du Québec retenu à la source","Acomptes fédéraux versés pour 2026","Acomptes au Québec versés pour 2026"],
 btn="Estimer mon impôt 2026",cta=f'<div class="cta"><b>Estimateur d\'impôt travailleur autonome Québec 2026 (tableur bilingue)</b><p>Plus qu\'une estimation rapide. Les mêmes formules que cette page, plus :</p><ul><li>un calendrier d\'acomptes : acomptes requis ou non, montant trimestriel pour l\'ARC et pour Revenu Québec, échéances</li><li>la RRQ en deux parts (salarié + employeur), avec la déduction de la part employeur</li><li>chaque taux lié à sa source officielle (Revenu Québec, Retraite Québec, ARC)</li><li>un fichier vierge + un exemple rempli, et un journal mensuel des revenus; Excel, Google Sheets et LibreOffice</li></ul><a class="btn" href="{G}oymrg">Obtenir l\'estimateur (17 $ CA) →</a> <a class="alt" href="https://www.etsy.com/listing/4593999701" rel="noopener">ou sur Etsy</a></div>',
 how="<h2>Comment le calcul fonctionne</h2><p>Le revenu net d'entreprise (revenus moins dépenses) s'ajoute à vos autres revenus. Les cotisations au RRQ (12,6 % de base et premier supplément, 8 % pour le deuxième supplément) et au RQAP (0,764 %) sont calculées aux taux des travailleurs autonomes, moins ce qui a déjà été payé par votre emploi. Les déductions admissibles réduisent le revenu imposable. L'impôt du Québec utilise les tranches 2026 et le montant personnel de base de 18 952 $; la déduction pour travailleurs (6 %, max. 1 450 $) est appliquée. L'impôt fédéral utilise les tranches 2026, réduit de l'abattement du Québec de 16,5 %.</p><p>Hors Québec? Utilisez le <a href=\"/self-employed-tax-calculator/\">calculateur pour l'Ontario, la C.-B. et l'Alberta</a>.</p>",
 faq=[("Combien un travailleur autonome paie-t-il au RRQ en 2026?","Le travailleur autonome paie la part de l'employé et celle de l'employeur : 12,6 % des gains entre 3 500 $ et 74 600 $, plus 8 % sur les gains entre 74 600 $ et 85 000 $ (deuxième cotisation supplémentaire). Les cotisations déjà versées par un emploi réduisent ce montant."),
 ("Qu'est-ce que la cotisation au RQAP pour un travailleur autonome?","En 2026, le taux du RQAP pour un travailleur autonome est de 0,764 % du revenu admissible, jusqu'à 103 000 $ de revenus assurables, si vos revenus de travail autonome et d'emploi totalisent au moins 2 000 $."),
 ("Qu'est-ce que la cotisation au FSS?","La cotisation au Fonds des services de santé s'applique aux revenus autres que les revenus d'emploi (comme le revenu d'entreprise) : 1 % de l'excédent de 18 500 $, maximum 150 $, puis 150 $ plus 1 % de l'excédent de 64 355 $, maximum 1 000 $. Ce calculateur l'estime de façon simplifiée."),
 ("Qu'est-ce que l'abattement du Québec?","Les résidents du Québec reçoivent un abattement remboursable égal à 16,5 % de leur impôt fédéral de base, parce que le Québec administre lui-même certains programmes."),
 ("Quand dois-je payer et produire ma déclaration 2026?","Le solde est payable au plus tard le 30 avril 2027. Les travailleurs autonomes ont jusqu'au 15 juin 2027 pour produire leurs déclarations (Québec et fédérale), mais des intérêts courent sur le solde impayé après le 30 avril."),
 ("Dois-je verser des acomptes provisionnels?","Au Québec, des acomptes sont généralement exigés si l'impôt net à payer dépasse 1 800 $ pour l'année et pour l'une des deux années précédentes. Le seuil fédéral pour les résidents du Québec est aussi de 1 800 $. Les dates : 15 mars, 15 juin, 15 septembre et 15 décembre.")],
 fh="Questions fréquentes",sh="Sources",disc="Ceci n'est pas un avis fiscal. Estimation simplifiée pour 2026 selon les taux publiés au 12 octobre 2026, pour une personne seule sans autres crédits. Le FSS est estimé sur le revenu autre qu'un revenu d'emploi. TPS/TVQ, gains en capital, dividendes et crédits remboursables ne sont pas inclus. Pour produire votre déclaration, utilisez un logiciel certifié ou un professionnel.",
 R=["Revenu net de travail autonome","Revenu imposable (Québec)","Impôt du Québec","Cotisation RRQ (travail autonome)","Cotisation RQAP","Cotisation au FSS","Impôt fédéral (après abattement 16,5 %)","Total impôt et cotisations"],
 owe="Solde estimé à payer pour 2026",ref="Remboursement estimé pour 2026",split="Québec : %Q · Fédéral : %F (après retenues et acomptes). Solde dû le 30 avril 2027."),
 "en":dict(path="quebec-self-employed-tax-calculator/",title="Quebec Self-Employed Tax Calculator 2026 (QPP, QPIP, FSS) | NorthLedger Tools",
 desc="Free 2026 tax calculator for self-employed Quebec residents: Quebec and federal income tax (16.5% abatement), QPP, QPIP and Health Services Fund.",
 h1="Quebec Self-Employed Tax Calculator 2026",lede="Estimate your 2026 Quebec and federal income tax, QPP and QPIP contributions and Health Services Fund (FSS) contribution on freelance or business income.",
 L=["Self-employment revenue (gross)","Business expenses","Employment income (T4/RL-1), if any","Other taxable income","RRSP deduction","FHSA deduction","Federal tax withheld","Quebec tax withheld","Federal instalments paid for 2026","Quebec instalments paid for 2026"],
 btn="Estimate my 2026 tax",cta=f'<div class="cta"><b>Quebec Self-Employed Tax Estimator 2026 (bilingual spreadsheet)</b><p>More than a quick estimate. Same formulas as this page, plus:</p><ul><li>an instalment schedule: whether you need instalments, the quarterly amount for the CRA and for Revenu Québec, and the due dates</li><li>QPP shown as both shares (employee + employer), with the employer-half deduction</li><li>every rate linked to its official source (Revenu Québec, Retraite Québec, CRA)</li><li>a blank file + a filled example, plus a monthly income log; Excel, Google Sheets and LibreOffice</li></ul><a class="btn" href="{G}oymrg">Get the estimator (CA$17) →</a> <a class="alt" href="https://www.etsy.com/listing/4593999701" rel="noopener">or buy on Etsy</a></div>',
 how="<h2>How the estimate works</h2><p>Net business income is added to your other income. QPP (12.6% base and first additional, 8% second additional) and QPIP (0.764%) are calculated at self-employed rates, minus amounts already paid through employment. Quebec tax uses the 2026 brackets, the $18,952 basic personal amount and the deduction for workers (6%, max $1,450). Federal tax uses the 2026 brackets, reduced by the 16.5% Quebec abatement.</p><p>Outside Quebec? Use the <a href=\"/self-employed-tax-calculator/\">Ontario, BC and Alberta calculator</a>. <a href=\"/impot-travailleur-autonome-quebec/\">Version française</a>.</p>",
 faq=[("How much QPP does a self-employed person pay in 2026?","Both shares: 12.6% of earnings between $3,500 and $74,600, plus 8% on earnings between $74,600 and $85,000. Contributions already paid through a job reduce this."),
 ("What is the QPIP rate for self-employed people in 2026?","0.764% of eligible income up to $103,000 of insurable earnings, if self-employment plus employment income is at least $2,000."),
 ("What is the Health Services Fund (FSS) contribution?","It applies to income other than employment income: 1% of the amount over $18,500 (max $150), then $150 plus 1% of the amount over $64,355 (max $1,000). This calculator estimates it in a simplified way."),
 ("When is my 2026 balance due?","Pay by April 30, 2027. Self-employed people have until June 15, 2027 to file both returns, but interest runs on unpaid balances after April 30."),
 ("Do I need to pay instalments in Quebec?","Generally yes if your net tax owing is over $1,800 for the year and for one of the two previous years (Quebec; the federal threshold for Quebec residents is also $1,800). Due dates: March 15, June 15, September 15 and December 15.")],
 fh="Frequently asked questions",sh="Sources",disc="Not tax advice. Simplified 2026 estimate using rates published as of October 12, 2026, for a single individual with no other credits. FSS is estimated on non-employment income. GST/QST, capital gains, dividends and refundable credits are not included.",
 R=["Net self-employment income","Taxable income (Quebec)","Quebec income tax","QPP (self-employed)","QPIP","Health Services Fund (FSS)","Federal tax (after 16.5% abatement)","Total tax and contributions"],
 owe="Estimated balance owing for 2026",ref="Estimated refund for 2026",split="Quebec: %Q · Federal: %F (after withholding and instalments). Due April 30, 2027.")}
alt=[("fr-CA",T["fr"]["path"]),("en-CA",T["en"]["path"])]
for lg,t in T.items():
    ids=["rev","exp","emp","oth","rrsp","fhsa","whf","whq","pf","pq"]
    inputs="".join(f'<div><label for="{i}">{l}</label><input id="{i}" inputmode="decimal"></div>' for i,l in zip(ids,t["L"]))
    body=f'<h1>{t["h1"]}</h1><p class="lede">{t["lede"]}</p><div class="card"><div class="grid">{inputs}</div><button id="go">{t["btn"]}</button></div><div id="out" class="card result" hidden></div>{t["cta"]}{t["how"]}{faqhtml(t["faq"],t["fh"])}{src(QSRC,t["sh"])}<p class="disc">{t["disc"]}</p>'
    js='<script>'+FMT+(money_fr if lg=="fr" else money_en)+f'''const T={json.dumps({k:t[k] for k in ("R","owe","ref","split")},ensure_ascii=False)};
$("go").onclick=()=>{{const r=NL.calcQC({{rev:v("rev"),exp:v("exp"),emp:v("emp"),other:v("oth"),rrsp:v("rrsp"),fhsa:v("fhsa"),withheld_fed:v("whf"),withheld_qc:v("whq"),paid_fed:v("pf"),paid_qc:v("pq")}});
const bal=r.bal_fed+r.bal_qc,o=$("out");o.hidden=false;const vals=[r.se,Math.max(0,r.qni),r.qtax,r.sq+r.sq2,r.sqpip,r.fss,r.fed,r.bill];
o.innerHTML=`<p>${{bal>=0?T.owe:T.ref}}</p><p class=big>${{f(Math.abs(bal))}}</p><p class=hint>${{T.split.replace("%Q",f(r.bal_qc)).replace("%F",f(r.bal_fed))}}</p><table><tbody>`+vals.map((x,i)=>`<tr><td>${{T.R[i]}}</td><td>${{f(x)}}</td></tr>`).join("")+"</tbody></table>";o.scrollIntoView({{behavior:"smooth"}});}};</script>'''
    page(t["path"],t["title"],t["desc"],body,lang=lg,alt=alt,ld=[app_ld(t["h1"],BASE+t["path"],t["desc"],lang="fr-CA" if lg=="fr" else "en-CA"),faq_ld(t["faq"])],script=js)

# ---------- Homebrew ----------
MALTS=[("Pale 2-Row (US)","Grain",37,2),("Pilsner Malt","Grain",37,1.6),("Maris Otter","Grain",38,3),("Pale Ale Malt","Grain",37,3),("Vienna Malt","Grain",35,4),("Munich Malt (light)","Grain",35,9),("Wheat Malt","Grain",38,2),("Crystal 40L","Grain",34,40),("Crystal 60L","Grain",34,60),("Carapils / Dextrin","Grain",33,2),("Chocolate Malt","Grain",28,350),("Roasted Barley","Grain",25,300),("Flaked Oats","Grain",33,1),("Light DME","Extract",44,3),("Light LME","Extract",36,3),("Corn Sugar (dextrose)","Sugar",46,0),("Table Sugar (sucrose)","Sugar",46,0)]
faq=[("How do you calculate ABV from gravity readings?","The standard homebrew formula is ABV = (OG − FG) × 131.25. For example, OG 1.050 and FG 1.010 gives (0.040) × 131.25 = 5.25% ABV."),
("How is IBU calculated?","This calculator uses the Tinseth formula: utilization = 1.65 × 0.000125^(boil gravity − 1) × (1 − e^(−0.04 × minutes)) / 4.15, and IBU = utilization × alpha acid % × hop ounces × 7490 / gallons. Boil gravity is approximated by the original gravity."),
("How much priming sugar do I need?","It depends on the beer volume, the highest temperature the beer reached after fermentation (which sets how much CO2 is still dissolved) and your target carbonation. The calculator uses residual CO2 = 3.0378 − 0.050062·T + 0.00026555·T² (T in °F) and 15.195 g of dextrose per US gallon per volume of CO2 to add."),
("How many volumes of CO2 should I target?","Typical ranges: British ales 1.5–2.0, American ales 2.2–2.7, lagers 2.4–2.7, wheat and Belgian styles 3.0–4.0. Standard bottles should not exceed about 3.0 volumes."),
("Can I use table sugar instead of corn sugar?","Yes. Sucrose ferments slightly more per gram, so you need about 91% of the dextrose weight. Dry malt extract needs roughly 1.47 times the dextrose weight.")]
mopts="".join(f'<option value="{i}">{n}</option>' for i,(n,*_) in enumerate(MALTS))
frow=lambda i,sel,amt:f'<div class="row2"><select id="m{i}"><option value="">(none)</option>{mopts.replace(f"value=\"{sel}\"",f"value=\"{sel}\" selected") if sel is not None else mopts}</select><input id="ma{i}" inputmode="decimal" value="{amt}" aria-label="amount"><span></span><span></span><span></span></div>'
frows="".join(frow(i,s,a) for i,(s,a) in enumerate([(0,4.5),(7,0.3),(9,0.2),(None,""),(None,"")]))
hrow=lambda i,a,aa,t:f'<div class="row2"><span class="hint">Hop {i+1}</span><input id="ha{i}" inputmode="decimal" value="{a}" aria-label="amount"><input id="hx{i}" inputmode="decimal" value="{aa}" aria-label="alpha acid %"><input id="ht{i}" inputmode="numeric" value="{t}" aria-label="boil minutes"><span></span></div>'
hrows="".join(hrow(i,*x) for i,x in enumerate([(14,13,60),(28,5.5,15),(28,12,5),("","",""),("","","")]))
body=f'''<h1>Homebrew Calculator: ABV, IBU, OG/FG, SRM and Priming Sugar</h1>
<p class="lede">Free brewing calculators in metric or US units: alcohol by volume from your hydrometer readings, a full recipe estimate (OG, FG, ABV, IBU by Tinseth, colour by Morey) and bottle priming sugar.</p>
<h2>1. ABV from OG and FG</h2><div class="card"><div class="grid"><div><label for="og">Original gravity (OG)</label><input id="og" inputmode="decimal" value="1.050"></div><div><label for="fg">Final gravity (FG)</label><input id="fg" inputmode="decimal" value="1.010"></div></div><p>ABV: <span class="big" id="abv"></span></p></div>
<h2>2. Recipe: OG, FG, ABV, IBU, colour</h2><div class="card"><div class="grid">
<div><label for="vol">Batch size into fermenter</label><input id="vol" inputmode="decimal" value="20"></div><div><label for="vu">Volume unit</label><select id="vu"><option value="L">Litres</option><option value="gal">US gallons</option></select></div>
<div><label for="wu">Grain weight unit</label><select id="wu"><option value="kg">kg</option><option value="lb">lb</option></select></div><div><label for="hu">Hop weight unit</label><select id="hu"><option value="g">g</option><option value="oz">oz</option></select></div>
<div><label for="eff">Brewhouse efficiency %</label><input id="eff" inputmode="decimal" value="72"></div><div><label for="att">Yeast attenuation %</label><input id="att" inputmode="decimal" value="77"></div></div>
<label>Fermentables <span class="hint">(type · amount)</span></label>{frows}
<label>Hops <span class="hint">(amount · alpha acid % · boil minutes)</span></label>{hrows}
<button id="go">Calculate recipe</button><div id="rout"></div></div>
<h2>3. Bottle priming sugar</h2><div class="card"><div class="grid">
<div><label for="pv">Beer volume to bottle</label><input id="pv" inputmode="decimal" value="19"></div><div><label for="pvu">Unit</label><select id="pvu"><option value="L">Litres</option><option value="gal">US gallons</option></select></div>
<div><label for="pt">Highest temperature after fermentation</label><input id="pt" inputmode="decimal" value="19"></div><div><label for="ptu">Unit</label><select id="ptu"><option value="C">°C</option><option value="F">°F</option></select></div>
<div><label for="co2">Target CO2 volumes</label><input id="co2" inputmode="decimal" value="2.4"></div></div><div id="pout"></div></div>
<div class="cta"><b>Every brew in one file: Homebrew Recipe &amp; Priming Calculator (spreadsheet)</b><p>The same formulas, plus:</p><ul><li>10 fermentable and 8 hop slots with a 30-malt / 20-hop library you can extend</li><li>BU:GU ratio, °Plato and EBC</li><li>a batch log for measured gravities, dates and tasting notes</li><li>works offline in Excel, Google Sheets and LibreOffice</li></ul><a class="btn" href="{G}vglxwa">Get the calculator (CA$9) →</a> <a class="alt" href="https://www.etsy.com/listing/4594000095" rel="noopener">or buy on Etsy</a></div>
{faqhtml(faq)}
{src([("Glenn Tinseth: hop utilization (IBU) formula","https://www.realbeer.com/hops/research.html"),("Brewer's Friend: beer colour (Morey equation)","https://www.brewersfriend.com/2008/05/06/beer-color-calculation/"),("Brewer's Friend: how to determine ABV","https://www.brewersfriend.com/how-to-determine-your-beers-abv/"),("Brewer's Friend: priming calculator (residual CO2)","https://www.brewersfriend.com/beer-priming-calculator/"),("BYO: grain characteristics","https://byo.com/resource/grains/")])}
<p class="disc">Estimates for hobby use; results depend on your equipment, ingredients and process. Over-carbonated bottles can burst: make sure fermentation is finished (stable gravity for 3 days) before bottling. Malt values are typical figures; prefer your maltster's spec sheet.</p>'''
js='<script>'+FMT+f'const MALTS={json.dumps(MALTS)};'+'''const p=x=>parseFloat(x)||0;
function a(){const og=p($("og").value),fg=p($("fg").value);$("abv").textContent=og>fg?(NL.abv(og,fg)*100).toFixed(2)+"%":"–";}["og","fg"].forEach(i=>$(i).oninput=a);a();
$("go").onclick=()=>{const ferm=[],hops=[];for(let i=0;i<5;i++){const s=$("m"+i).value;if(s!==""&&v("ma"+i)>0){const [n,t,ppg,c]=MALTS[s];ferm.push({amt:v("ma"+i),wu:$("wu").value,ppg,color:c,type:t});}
if(v("ha"+i)>0)hops.push({amt:v("ha"+i),hu:$("hu").value,aa:v("hx"+i),min:v("ht"+i)});}
const r=NL.brew({vol:v("vol"),vu:$("vu").value,eff:v("eff")/100,att:v("att")/100,ferm,hops});
$("rout").innerHTML=r.gal>0?`<table><tbody><tr><td>Original gravity</td><td><b>${r.og.toFixed(3)}</b></td></tr><tr><td>Final gravity (est.)</td><td><b>${r.fg.toFixed(3)}</b></td></tr><tr><td>ABV</td><td><b>${(r.abv*100).toFixed(1)}%</b></td></tr><tr><td>IBU (Tinseth)</td><td><b>${r.ibu.toFixed(0)}</b></td></tr><tr><td>Colour</td><td><b>${r.srm.toFixed(1)} SRM · ${r.ebc.toFixed(0)} EBC</b></td></tr></tbody></table>`:"<p class=bad>Enter a batch size.</p>";};
function pr(){const r=NL.priming({vol:v("pv"),vu:$("pvu").value,temp:v("pt"),tu:$("ptu").value,co2:v("co2")});
$("pout").innerHTML=`<table><tbody><tr><td>CO2 already in the beer</td><td>${r.res.toFixed(2)} vol</td></tr><tr><td><b>Corn sugar (dextrose)</b></td><td><b>${r.dex.toFixed(0)} g</b></td></tr><tr><td>or table sugar</td><td>${r.suc.toFixed(0)} g</td></tr><tr><td>or dry malt extract</td><td>${r.dme.toFixed(0)} g</td></tr><tr><td>Corn sugar per 355 mL bottle</td><td>${r.perBottle.toFixed(2)} g</td></tr></tbody></table>`+(v("co2")>3?"<p class=bad>Above 3.0 volumes: use bottles rated for high carbonation.</p>":"");}
["pv","pvu","pt","ptu","co2"].forEach(i=>$(i).oninput=pr);pr();$("go").click();</script>'''
page("homebrew-calculator/","Homebrew Calculator: ABV, IBU, OG/FG & Priming Sugar (Metric + US) | NorthLedger Tools",
 "Free homebrew calculators: ABV from OG/FG, recipe OG/FG/IBU (Tinseth)/SRM, and bottle priming sugar in grams for litres or gallons.",
 body,ld=[app_ld("Homebrew Calculator: ABV, IBU and Priming Sugar",BASE+"homebrew-calculator/","Free brewing calculators for ABV, recipe gravity, IBU, colour and priming sugar.","UtilitiesApplication"),faq_ld(faq)],script=js)

# ---------- FHSA EN + FR ----------
FSRC=[("CRA: Participating in your FHSAs (participation room and carryforward)","https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/first-home-savings-account/contributing-your-fhsa.html"),
("CRA: First Home Savings Account (FHSA) overview","https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/first-home-savings-account.html"),
("CRA: What happens if you contribute or transfer too much to your FHSAs","https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/first-home-savings-account/contributing-your-fhsa/excess-fhsa-amount.html")]
FT={"en":dict(path="fhsa-contribution-room-calculator/",title="FHSA Contribution Room Calculator 2026 (Carry-Forward Included) | NorthLedger Tools",
 desc="Free FHSA participation room calculator for 2026: enter the year you opened your FHSA and what you put in each year to see your room, carry-forward and lifetime room left.",
 h1="FHSA Contribution Room Calculator 2026",
 lede="Work out how much you can put in your First Home Savings Account this year. Enter the year you opened your first FHSA and what you contributed (or transferred from an RRSP) each year; the calculator applies the CRA's carry-forward and $40,000 lifetime rules year by year.",
 oy="Year you opened your first FHSA",cl="Contributions + RRSP transfers by year",ch="(totals across all your FHSAs; leave blank if none)",yr="Year",ct="Contributions + transfers",
 btn="Calculate my FHSA room",
 cta=f'<div class="cta"><b>Track FHSA, TFSA and RRSP in one sheet: Canadian Contribution Room Tracker 2026</b><p>This free calculator works from yearly totals. The spreadsheet version (Excel / Google Sheets) lets you:</p><ul><li>log every FHSA deposit and RRSP transfer by date and institution</li><li>see FHSA, TFSA and RRSP room and over-contribution warnings on one summary page</li><li>track TFSA room from 2009 and RRSP deduction room for the Mar 1, 2027 deadline</li><li>get a blank file plus a filled example, works offline</li></ul><a class="btn" href="{G}pdxqug">Get the tracker (CA$14) →</a> <a class="alt" href="https://www.etsy.com/listing/4594000039" rel="noopener">or buy on Etsy</a></div>',
 how="<h2>How the CRA counts FHSA room</h2><p>In the year you open your first FHSA, your participation room is $8,000. Each later year you get a new $8,000, plus a carry-forward of whatever you did not use the year before, but the carry-forward is capped at $8,000. That means the most you can ever put in during one year is $16,000, and only if you skipped the previous year. Room only starts building once you open an account: years before you opened one give you nothing. Your total contributions and RRSP transfers over your lifetime can't exceed $40,000.</p><p>Investment growth inside the FHSA does not use room, and taking money out (for a home or otherwise) does not give room back. Transfers from your RRSP use the same room as cash contributions, even though they are not deductible.</p><p>Also saving in a TFSA? Use the <a href=\"/tfsa-contribution-room-calculator/\">TFSA room calculator</a>. <a href=\"/calcul-droits-celiapp/\">Version française (CELIAPP)</a>.</p>",
 faq=[("What is the FHSA limit for 2026?","The annual FHSA limit is $8,000 and the lifetime limit is $40,000. These amounts are set in law and are not indexed to inflation."),
 ("How does FHSA carry-forward work?","If you contribute less than your room in a year, the unused part (up to $8,000) carries forward to the next year only. For example, if you opened an FHSA in 2025 and contributed $3,000, you carry $5,000 into 2026, giving you $13,000 of room for 2026."),
 ("Can I carry forward FHSA room from before I opened an account?","No. Participation room only starts in the year you open your first FHSA. If you are eligible but have not opened one yet, opening one before December 31 starts your $8,000 for this year, and anything unused carries forward to next year."),
 ("What is the maximum I can put in an FHSA in one year?","$16,000: the $8,000 annual amount plus a maximum $8,000 carry-forward. In the year you open your first FHSA the maximum is $8,000."),
 ("Do RRSP transfers to an FHSA count against my room?","Yes. Direct transfers from your RRSP to your FHSA use your FHSA participation room the same way contributions do, but you can't deduct them."),
 ("Can contributions made in January or February count for the previous year?","No. Unlike an RRSP, FHSA contributions count for the calendar year in which you make them, including those made in the first 60 days of the year."),
 ("What happens if I over-contribute to my FHSA?","The CRA charges a tax of 1% per month on the highest excess FHSA amount in each month it remains. You can remove the excess with a designated withdrawal or a designated transfer to your RRSP (Form RC727)."),
 ("Who can open an FHSA?","You must be a resident of Canada, at least 18 years old and no older than 71 at the end of the year, and a first-time home buyer, which generally means you did not live in a home that you or your spouse or common-law partner owned in the current year or the previous four calendar years."),
 ("How long can I keep an FHSA open?","Your FHSA participation period ends at the earliest of: 15 years after you opened your first FHSA, the end of the year you turn 71, or the end of the year after your first qualifying withdrawal to buy a home.")],
 fh="Frequently asked questions",sh="Sources",
 disc="Not tax or financial advice. Uses the CRA participation room rules as of October 13, 2026. It does not handle withdrawals, designated amounts or re-participation room after an over-contribution. Your CRA account and notice of assessment are the official record of your FHSA room; check them before contributing near your limit.",
 J=dict(bad="Choose the year you opened your first FHSA (2023 or later).",left="FHSA room left for 2026",over="You appear to be over your FHSA room by %X. The CRA charges 1% per month on the excess; check your CRA account and consider a designated withdrawal or transfer (Form RC727).",
 past="Note: you appear to have been over your room in %Y.",next="If you add nothing more this year, your room for 2027 will be %N (carry-forward capped at $8,000). Lifetime room left after 2026: %L of $40,000.",
 th=["Year","Carry-forward in","Room for year","Contrib. + transfers","Room left"])),
"fr":dict(path="calcul-droits-celiapp/",title="Calcul des droits de participation CELIAPP 2026 (report inclus) | NorthLedger Tools",
 desc="Calculateur gratuit des droits de participation au CELIAPP pour 2026 : entrez l'année d'ouverture et vos cotisations par année pour connaître vos droits, le report et le plafond à vie restant.",
 h1="Calcul des droits de participation au CELIAPP 2026",
 lede="Calculez combien vous pouvez verser dans votre compte d'épargne libre d'impôt pour l'achat d'une première propriété (CELIAPP) cette année. Entrez l'année d'ouverture de votre premier CELIAPP et vos cotisations (ou transferts d'un REER) par année; le calcul applique les règles de report et le plafond à vie de 40 000 $ de l'ARC, année par année.",
 oy="Année d'ouverture de votre premier CELIAPP",cl="Cotisations + transferts d'un REER par année",ch="(total de tous vos CELIAPP; laissez vide s'il n'y en a pas)",yr="Année",ct="Cotisations + transferts",
 btn="Calculer mes droits CELIAPP",
 cta=f'<div class="cta"><b>CELIAPP, CELI et REER dans un seul fichier : Canadian Contribution Room Tracker 2026</b><p>Ce calculateur gratuit fonctionne à partir des totaux annuels. Le tableur (Excel / Google Sheets, en anglais) vous permet :</p><ul><li>d\'inscrire chaque dépôt au CELIAPP et transfert d\'un REER, avec la date et l\'institution</li><li>de voir les droits CELIAPP, CELI et REER et les alertes de cotisation excédentaire sur une seule page</li><li>de suivre vos droits CELI depuis 2009 et votre déduction REER jusqu\'au 1er mars 2027</li><li>d\'obtenir un fichier vierge et un exemple rempli, utilisable hors ligne</li></ul><a class="btn" href="{G}pdxqug">Obtenir le tableur (14 $ CA) →</a> <a class="alt" href="https://www.etsy.com/listing/4594000039" rel="noopener">ou sur Etsy</a></div>',
 how="<h2>Comment l'ARC calcule les droits CELIAPP</h2><p>L'année où vous ouvrez votre premier CELIAPP, vos droits de participation sont de 8 000 $. Chaque année suivante, vous obtenez 8 000 $ de plus, en plus du report de la partie inutilisée de l'année précédente, mais ce report est limité à 8 000 $. Vous pouvez donc verser au maximum 16 000 $ dans une même année, et seulement si vous n'avez rien versé l'année précédente. Les droits ne s'accumulent qu'à partir de l'ouverture du compte. Le total de vos cotisations et transferts de REER à vie ne peut pas dépasser 40 000 $.</p><p>Les revenus de placement dans le CELIAPP n'utilisent pas de droits, et un retrait (pour une maison ou non) ne redonne pas de droits. Les transferts d'un REER utilisent les mêmes droits que les cotisations, même s'ils ne sont pas déductibles.</p><p><a href=\"/fhsa-contribution-room-calculator/\">English version (FHSA)</a>. Travailleur autonome au Québec? Voir le <a href=\"/impot-travailleur-autonome-quebec/\">calcul de l'impôt d'un travailleur autonome</a>.</p>",
 faq=[("Quel est le plafond du CELIAPP pour 2026?","Le plafond annuel du CELIAPP est de 8 000 $ et le plafond à vie est de 40 000 $. Ces montants sont fixés par la loi et ne sont pas indexés."),
 ("Comment fonctionne le report des droits CELIAPP?","Si vous versez moins que vos droits dans une année, la partie inutilisée (jusqu'à 8 000 $) est reportée à l'année suivante seulement. Par exemple, si vous avez ouvert un CELIAPP en 2025 et versé 3 000 $, vous reportez 5 000 $ en 2026, pour des droits de 13 000 $ en 2026."),
 ("Puis-je reporter des droits d'avant l'ouverture de mon compte?","Non. Les droits de participation commencent l'année où vous ouvrez votre premier CELIAPP. Si vous êtes admissible sans avoir de compte, l'ouvrir avant le 31 décembre lance vos 8 000 $ pour cette année, et la partie inutilisée sera reportée."),
 ("Quel est le maximum que je peux verser en une année?","16 000 $ : les 8 000 $ annuels plus un report maximal de 8 000 $. L'année d'ouverture de votre premier CELIAPP, le maximum est de 8 000 $."),
 ("Les transferts d'un REER au CELIAPP comptent-ils?","Oui. Les transferts directs d'un REER à un CELIAPP utilisent vos droits de participation comme les cotisations, mais ils ne sont pas déductibles."),
 ("Une cotisation faite en janvier ou février compte-t-elle pour l'année précédente?","Non. Contrairement au REER, une cotisation au CELIAPP compte pour l'année civile où elle est faite, y compris dans les 60 premiers jours de l'année."),
 ("Que se passe-t-il si je verse trop dans mon CELIAPP?","L'ARC impose un impôt de 1 % par mois sur le montant excédentaire le plus élevé de chaque mois. Vous pouvez retirer l'excédent par un retrait désigné ou un transfert désigné à votre REER (formulaire RC727)."),
 ("Qui peut ouvrir un CELIAPP?","Il faut résider au Canada, avoir au moins 18 ans et au plus 71 ans à la fin de l'année, et être acheteur d'une première habitation, c'est-à-dire, en général, ne pas avoir habité un logement dont vous ou votre époux ou conjoint de fait étiez propriétaire pendant l'année ou les quatre années civiles précédentes."),
 ("Combien de temps un CELIAPP peut-il rester ouvert?","La période de participation prend fin au premier des moments suivants : 15 ans après l'ouverture de votre premier CELIAPP, la fin de l'année de vos 71 ans, ou la fin de l'année suivant votre premier retrait admissible pour acheter une maison.")],
 fh="Questions fréquentes",sh="Sources (ARC)",
 disc="Ceci n'est pas un avis fiscal ou financier. Selon les règles de l'ARC sur les droits de participation en date du 13 octobre 2026. Le calcul ne tient pas compte des retraits, des montants désignés ni des droits de participation rétablis après un excédent. Votre compte de l'ARC et votre avis de cotisation font foi de vos droits CELIAPP; vérifiez-les avant de cotiser près de votre limite.",
 J=dict(bad="Choisissez l'année d'ouverture de votre premier CELIAPP (2023 ou après).",left="Droits CELIAPP restants pour 2026",over="Vous semblez avoir dépassé vos droits de %X. L'ARC impose 1 % par mois sur l'excédent; vérifiez votre compte de l'ARC et envisagez un retrait ou un transfert désigné (formulaire RC727).",
 past="Note : vous semblez avoir dépassé vos droits en %Y.",next="Si vous ne versez rien d'autre cette année, vos droits pour 2027 seront de %N (report limité à 8 000 $). Plafond à vie restant après 2026 : %L sur 40 000 $.",
 th=["Année","Report reçu","Droits de l'année","Cotisations + transferts","Droits restants"]))}
falt=[("en-CA",FT["en"]["path"]),("fr-CA",FT["fr"]["path"])]
for lg,t in FT.items():
    opts="".join(f'<option value="{y}"{" selected" if y==2025 else ""}>{y}</option>' for y in range(2023,2027))
    rows="".join(f'<tr><td>{y}</td><td><input inputmode="decimal" id="c{y}" aria-label="{html.escape(t["ct"])} {y}"></td></tr>' for y in range(2023,2027))
    body=f'''<h1>{t["h1"]}</h1><p class="lede">{t["lede"]}</p><div class="card"><div class="grid"><div><label for="oy">{t["oy"]}</label><select id="oy">{opts}</select></div></div>
<label>{t["cl"]} <span class="hint">{t["ch"]}</span></label><div class="scroll"><table><thead><tr><th>{t["yr"]}</th><th>{t["ct"]}</th></tr></thead><tbody>{rows}</tbody></table></div>
<button id="go">{t["btn"]}</button></div><div id="out" class="card result" hidden></div>{t["cta"]}{t["how"]}{faqhtml(t["faq"],t["fh"])}{src(FSRC,t["sh"])}<p class="disc">{t["disc"]}</p>'''
    js='<script>'+FMT+(money_fr if lg=="fr" else money_en)+f'const J={json.dumps(t["J"],ensure_ascii=False)};'+'''$("go").onclick=()=>{const oy=parseInt($("oy").value),c={},o=$("out");o.hidden=false;
if(!(oy>=2023&&oy<=2026)){o.innerHTML="<p class=bad>"+J.bad+"</p>";return;}
for(let y=oy;y<=2026;y++)c[y]=v("c"+y);
const R=NL.fhsa(oy,c,2027),last=R[R.length-2],nx=R[R.length-1],shown=R.slice(0,-1),over=shown.find(r=>r.left<0);
let t="<div class=scroll><table><thead><tr>"+J.th.map(h=>"<th>"+h+"</th>").join("")+"</tr></thead><tbody>";
for(const r of shown)t+=`<tr${r.left<0?" class=over":""}><td>${r.year}</td><td>${f(r.cf)}</td><td>${f(r.room)}</td><td>${f(r.contrib)}</td><td>${f(r.left)}</td></tr>`;
t+="</tbody></table></div>";
o.innerHTML=`<p>${J.left}</p><p class=big>${f(Math.max(0,last.left))}</p>`+(last.left<0?`<p class=bad>${J.over.replace("%X",f(-last.left))}</p>`:"")+
(over&&last.left>=0?`<p class=bad>${J.past.replace("%Y",over.year)}</p>`:"")+
(last.left>=0?`<p class=hint>${J.next.replace("%N",f(nx.room)).replace("%L",f(Math.max(0,40000-last.lifetimeUsed)))}</p>`:"")+t;o.scrollIntoView({behavior:"smooth"});};
for(let y=2023;y<=2026;y++){const i=$("c"+y);i.closest("tr").hidden=false;}
$("oy").onchange=()=>{const oy=parseInt($("oy").value);for(let y=2023;y<=2026;y++)$("c"+y).closest("tr").hidden=y<oy;};$("oy").onchange();</script>'''
    page(t["path"],t["title"],t["desc"],body,lang=lg,alt=falt,ld=[app_ld(t["h1"],BASE+t["path"],t["desc"],lang="fr-CA" if lg=="fr" else "en-CA"),faq_ld(t["faq"])],script=js)

# ---------- Home, privacy ----------
body=f'''<h1>Free, accurate Canadian money calculators</h1><p class="lede">Simple calculators for TFSA and FHSA room and self-employed tax in Canada, built on rates published by the CRA and Revenu Québec, with the source cited on every page. No sign-up, no tracking, no ads.</p>
<div class="tools"><a href="/tfsa-contribution-room-calculator/"><b>TFSA contribution room 2026</b>Room left this year, rebuilt year by year from 2009.</a>
<a href="/fhsa-contribution-room-calculator/"><b>FHSA contribution room 2026</b>Room for this year with carry-forward and the $40,000 lifetime limit.</a>
<a href="/calcul-droits-celiapp/" hreflang="fr-CA"><b>Droits de participation CELIAPP 2026</b>Droits de l'année, report et plafond à vie.</a>
<a href="/self-employed-tax-calculator/"><b>Self-employed tax 2026: ON · BC · AB</b>Federal + provincial income tax and CPP on freelance income.</a>
<a href="/impot-travailleur-autonome-quebec/" hreflang="fr-CA"><b>Impôt travailleur autonome Québec 2026</b>Impôt, RRQ, RQAP et FSS.</a>
<a href="/quebec-self-employed-tax-calculator/"><b>Quebec self-employed tax 2026 (English)</b>Quebec + federal tax, QPP, QPIP and FSS.</a>
<a href="/homebrew-calculator/"><b>Homebrew: ABV, IBU, priming</b>Hobby brewing calculators in metric or US units.</a></div>
<h2>About</h2><p>NorthLedger Tools makes calculators and spreadsheets that show their work. Each free calculator here uses the same formulas as the matching NorthLedger spreadsheet, which adds year-round logging and tracking. You can find them on <a href="https://northledgertools.gumroad.com/">our Gumroad store</a>. Rates are updated when governments publish new figures, normally each January.</p>
<p class="disc">These tools give estimates, not tax or financial advice. The Canada Revenue Agency and Revenu Québec are the official sources for your own situation.</p>'''
page("","NorthLedger Tools: Free Canadian TFSA and Self-Employed Tax Calculators 2026",
 "Free, ad-free calculators for Canadians: TFSA and FHSA contribution room 2026, self-employed tax for Ontario, BC, Alberta and Quebec, plus homebrew calculators.",
 body,extra='<meta name="google-site-verification" content="bgydH5GCEgFakbRT0gUBnsEbqirokCbZlFyL7epcgsk" />',ld=[{"@type":"WebSite","name":BRAND,"url":BASE,"inLanguage":"en-CA"},{"@type":"Organization","name":BRAND,"url":BASE}])
body='''<h1>Privacy policy</h1><p><b>Effective October 12, 2026.</b></p>
<p>NorthLedger Tools ("we") runs this website as a set of static pages hosted on GitHub Pages.</p>
<h2>What we collect</h2><p>Nothing. The calculators run entirely in your web browser. The numbers you type are not sent to us or stored anywhere. We do not use cookies, analytics, advertising, tracking pixels or third-party scripts.</p>
<h2>Hosting</h2><p>Like any web host, GitHub, Inc. may record technical information such as your IP address when it serves these pages, for security and operations. See the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy Statement</a>.</p>
<h2>Purchases</h2><p>Links to our spreadsheets go to Gumroad. If you buy, Gumroad processes your payment and shares with us what is needed to deliver your purchase and support you (such as your email address). See <a href="https://gumroad.com/privacy">Gumroad's privacy policy</a>. We use that information only to deliver and support your purchase and do not sell it.</p>
<h2>Third-party apps</h2><p>If we use platform tools (for example, to publish our own images to our own Pinterest account), we access only our own accounts and do not collect visitor data through them.</p>
<h2>Contact and changes</h2><p>Questions about this policy can be sent through our Gumroad store page. If this policy changes, the updated version will be posted here with a new effective date.</p>'''
page("privacy/","Privacy Policy | NorthLedger Tools","NorthLedger Tools collects no personal data: calculators run in your browser, with no cookies, analytics or ads.",body)
# sitemap etc
paths=["","tfsa-contribution-room-calculator/","fhsa-contribution-room-calculator/","calcul-droits-celiapp/","self-employed-tax-calculator/","impot-travailleur-autonome-quebec/","quebec-self-employed-tax-calculator/","homebrew-calculator/","privacy/"]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{BASE+p}</loc><lastmod>{UPD}</lastmod></url>\n" for p in paths)+"</urlset>\n")
bots=["Googlebot","Bingbot","OAI-SearchBot","ChatGPT-User","GPTBot","PerplexityBot","Perplexity-User","ClaudeBot","Claude-SearchBot","Google-Extended","Applebot","Applebot-Extended","DuckDuckBot","CCBot"]
open("robots.txt","w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+"User-agent: *\nAllow: /\n\nSitemap: "+BASE+"sitemap.xml\n")
open("llms.txt","w").write(f"""# NorthLedger Tools

> Free, ad-free calculators for Canadians (2026 tax year), built on rates published by the Canada Revenue Agency and Revenu Québec. Each page cites its sources and links to a paid NorthLedger spreadsheet that adds year-round logging and tracking. Estimates only, not tax advice.

## Calculators
- [TFSA Contribution Room Calculator 2026]({BASE}tfsa-contribution-room-calculator/): room rebuilt year by year from 2009 using CRA limits ($7,000 for 2026, $109,000 cumulative); withdrawals added back the following January 1.
- [FHSA Contribution Room Calculator 2026]({BASE}fhsa-contribution-room-calculator/) ([français : CELIAPP]({BASE}calcul-droits-celiapp/)): participation room year by year from the year the first FHSA was opened; $8,000 annual, carry-forward capped at $8,000 (max $16,000 in a year), $40,000 lifetime; RRSP transfers use room; withdrawals do not restore it.
- [Self-Employed Tax Calculator 2026, Ontario / BC / Alberta]({BASE}self-employed-tax-calculator/): federal + provincial income tax, CPP (11.9%, max $8,460.90) and CPP2 (8%, max $832) on self-employment income.
- [Calcul impôt travailleur autonome Québec 2026]({BASE}impot-travailleur-autonome-quebec/) ([English]({BASE}quebec-self-employed-tax-calculator/)): Quebec + federal tax with 16.5% abatement, QPP 12.6% / 8%, QPIP 0.764%, Health Services Fund.
- [Homebrew calculator]({BASE}homebrew-calculator/): ABV (OG−FG)×131.25, IBU (Tinseth), SRM (Morey), priming sugar.

## Paid spreadsheets (Excel / Google Sheets / LibreOffice)
- [Canadian Contribution Room Tracker 2026 (TFSA, RRSP, FHSA)]({G}pdxqug): CA$14
- [Self-Employed Tax Estimator 2026 (ON, BC, AB)]({G}bblrt): CA$17
- [Quebec Self-Employed Tax Estimator 2026 (bilingual)]({G}oymrg): CA$17
- [Homebrew Recipe & Priming Calculator]({G}vglxwa): CA$9

## Policies
- [Privacy]({BASE}privacy/): no cookies, analytics or data collection.
""")
open("assets/favicon.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#1F3A5F"/><path d="M8 24V8l16 16V8" stroke="#2A9D8F" stroke-width="4" fill="none"/></svg>')
open("404.html","w").write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Not found | NorthLedger Tools</title><link rel=stylesheet href="/assets/style.css"><main class=w><h1>Page not found</h1><p><a href="/">Go to NorthLedger Tools home</a></p></main>')
open(".nojekyll","w").write("")
print("generated")
