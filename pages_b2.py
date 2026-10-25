# ===== Batch 2 (2026-10-25): UK VAT calculator, UK Flat Rate Scheme comparison, California paycheck, French self-employed (ON/BC/AB) =====
import re as _re
B2UPD="2026-10-25"
money_gb='const f=x=>(x<0?"-":"")+"£"+Math.abs(x).toLocaleString("en-GB",{minimumFractionDigits:2,maximumFractionDigits:2});'
UKJS=open("assets/uk.js",encoding="utf-8").read()
FRS_SECT=json.loads(_re.search(r"const FRS=(\[.*?\]);",UKJS,_re.S).group(1))

# ---------- UK VAT calculator ----------
VAT_SRC=[("GOV.UK: VAT rates (standard 20%, reduced 5%, zero 0%)","https://www.gov.uk/vat-rates"),
("GOV.UK: Register for VAT, when to register (£90,000 threshold, 30-day rules, effective dates)","https://www.gov.uk/register-for-vat"),
("GOV.UK: Cancel your VAT registration (deregistration threshold £88,000)","https://www.gov.uk/register-for-vat/cancel-your-registration"),
("GOV.UK: Charge, reclaim and record VAT","https://www.gov.uk/charge-reclaim-record-vat"),
("HMRC: VAT Notice 700, The VAT Guide (VAT-inclusive prices, rounding, taxable turnover)","https://www.gov.uk/guidance/vat-guide-notice-700"),
("GOV.UK: VAT Flat Rate Scheme for small businesses","https://www.gov.uk/vat-flat-rate-scheme")]
vfaq=[("How do I add 20% VAT to a price?","Multiply the net (ex-VAT) price by 1.2. £100 + 20% VAT = £120, of which £20 is VAT. For the 5% reduced rate multiply by 1.05; the zero rate adds nothing, but zero-rated sales still count towards your taxable turnover."),
("How do I take VAT out of a price that already includes it?","Divide the VAT-inclusive price by 1.2 for the standard rate to get the net price. £120 ÷ 1.2 = £100, so the VAT is £20. Equivalent shortcut: the VAT is one-sixth (the 'VAT fraction') of a price that includes 20% VAT, and one-twenty-first of a price that includes 5% VAT. Do not take 20% off the gross price: 20% of £120 is £24, which is wrong."),
("What are the UK VAT rates in 2026?","Standard rate 20% (most goods and services), reduced rate 5% (for example children's car seats and home energy) and zero rate 0% (for example most food and children's clothes). Some supplies are exempt from VAT, such as postage stamps and financial and property transactions, and some are outside the scope of VAT altogether."),
("What is the VAT registration threshold?","£90,000 of VAT-taxable turnover. You must register if your total taxable turnover over the last 12 months goes over £90,000, or if you expect it to go over £90,000 in the next 30 days alone. You can register voluntarily below the threshold. You can ask to cancel registration if your taxable turnover falls below £88,000."),
("How is the 12-month turnover test applied?","It is a rolling test, not a tax-year test: at the end of every month, add up your taxable turnover for the previous 12 months. If it is over £90,000, you must apply to register within 30 days of the end of that month, and your registration takes effect from the first day of the second month after you went over. For example, if you pass £90,000 during July, you must register by 30 August and the effective date is 1 September."),
("What is the '30-day' rule?","If you realise at any point that your taxable turnover will go over £90,000 within the next 30 days alone (for example a big contract), you must register by the end of that 30-day period and your effective date is the day you realised. If you realise on 1 May, you apply by 30 May and the effective date is 1 May."),
("What counts as taxable turnover?","The total value of everything you sell that is not VAT-exempt or outside the scope of VAT. It includes zero-rated, reduced-rated and standard-rated sales, goods you hire or loan to customers, business goods used for private reasons, bartered or gifted goods, and some services bought from overseas under the reverse charge. Exempt sales do not count."),
("What happens if I register late?","You owe VAT on sales from the date you should have registered, even if you did not charge it to customers, and you may face a penalty depending on the amount and how late you are. If you will exceed the threshold, apply on time."),
("Is this the right calculator for Flat Rate Scheme VAT?","No. The Flat Rate Scheme replaces output-minus-input accounting with a flat percentage of your VAT-inclusive turnover, which depends on your trade sector. Use our Flat Rate Scheme calculator to compare it with standard accounting."),
("Why can a total on an invoice differ by a penny?","VAT on an invoice can be worked out per line or on the invoice total, and each method rounds to the nearest penny. This calculator rounds half a penny upwards on each line and adds the lines; HMRC accepts either method if you apply it consistently, provided the VAT you show matches the VAT you account for.")]
vbody=f'''<h1>UK VAT Calculator 2026: Add or Remove VAT, and Check Your Registration Date</h1>
<p class="lede">Add 20%, 5% or 0% VAT to a price, or take it out of a VAT-inclusive total, to the penny. Then check whether you have to register: enter the month your 12-month taxable turnover passed £90,000, or the day you realised it would, and get the registration deadline and effective date.</p>
<div class="card"><h2>Add or remove VAT</h2><div class="grid">
<div><label for="am">Amount (£)</label><input id="am" inputmode="decimal" placeholder="100"></div>
<div><label for="md">What is the amount?</label><select id="md"><option value="add">Price without VAT (add VAT)</option><option value="remove">Price including VAT (remove VAT)</option></select></div>
<div><label for="rt">VAT rate</label><select id="rt"><option value="20">Standard rate 20%</option><option value="5">Reduced rate 5%</option><option value="0">Zero rate 0%</option></select></div></div>
<button id="go">Calculate VAT</button><div id="out" class="result card" hidden></div>
<details><summary>Invoice with several VAT rates</summary><p class="hint">Enter the amounts for each line on the same basis (all without VAT, or all with VAT) as selected above.</p><div class="grid">
<div><label for="l1">Line 1 amount (£)</label><input id="l1" inputmode="decimal"></div><div><label for="r1">Line 1 rate</label><select id="r1"><option value="20">20%</option><option value="5">5%</option><option value="0">0%</option></select></div>
<div><label for="l2">Line 2 amount (£)</label><input id="l2" inputmode="decimal"></div><div><label for="r2">Line 2 rate</label><select id="r2"><option value="20">20%</option><option value="5">5%</option><option value="0">0%</option></select></div>
<div><label for="l3">Line 3 amount (£)</label><input id="l3" inputmode="decimal"></div><div><label for="r3">Line 3 rate</label><select id="r3"><option value="20">20%</option><option value="5">5%</option><option value="0">0%</option></select></div></div>
<button id="gl">Total the invoice</button><div id="outl" class="result card" hidden></div></details></div>
<div class="card"><h2>Do I need to register for VAT?</h2><div class="grid">
<div><label for="rtp">What happened?</label><select id="rtp"><option value="over">My taxable turnover for the last 12 months went over £90,000 at the end of a month</option><option value="fwd">I realised my turnover will go over £90,000 in the next 30 days</option></select></div>
<div id="gm"><label for="mo">Month it went over</label><select id="mo"></select></div>
<div id="gy"><label for="yr">Year</label><input id="yr" inputmode="numeric" value="2026"></div>
<div id="gd" hidden><label for="dt">Date you realised</label><input id="dt" type="date"></div>
<div><label for="tv">Your taxable turnover, last 12 months (£, optional)</label><input id="tv" inputmode="decimal"></div></div>
<button id="rg">Work out my deadline</button><div id="outr" class="result card" hidden></div></div>
<h2>How to add and remove VAT</h2>
<div class="scroll"><table><thead><tr><th>Rate</th><th>Net → gross</th><th>Gross → net</th><th>VAT fraction of the gross price</th></tr></thead><tbody>
<tr><td>Standard 20%</td><td>× 1.2</td><td>÷ 1.2</td><td>1/6 (£120 contains £20 VAT)</td></tr>
<tr><td>Reduced 5%</td><td>× 1.05</td><td>÷ 1.05</td><td>1/21 (£105 contains £5 VAT)</td></tr>
<tr><td>Zero 0%</td><td>× 1</td><td>÷ 1</td><td>no VAT, but counts towards taxable turnover</td></tr></tbody></table></div>
<p>Take care with the reverse direction: to find the net price from a gross price at 20%, divide by 1.2 (or multiply by 5/6). Taking 20% off the gross figure leaves you short on the VAT you owe HMRC. Prices in the UK for consumers normally show VAT-inclusive amounts, while invoices between VAT-registered businesses show the net price, the VAT and the total separately.</p>
<h2>The registration rules, step by step</h2>
<p>There are two separate triggers and each has its own deadline. The <b>backward-looking test</b> compares your taxable turnover for the previous 12 months with £90,000 at the end of every calendar month, a rolling test that does not follow the tax year. Once it is passed you have 30 days from the end of that month to apply, and HMRC treats you as VAT-registered from the first day of the second month after the month you went over. The <b>forward-looking test</b> applies if you can see that turnover in the next 30 days alone will exceed £90,000: you must apply by the end of that period and your effective date is the day you realised. Whichever applies first governs, and from the effective date you must charge VAT on your sales whether or not your certificate has arrived. If you only make VAT-exempt or out-of-scope supplies you do not have to register.</p>
<p>Once registered, a business may use the <a href="/vat-flat-rate-scheme-calculator/">Flat Rate Scheme</a> if it expects taxable turnover of £150,000 or less (excluding VAT) over the next 12 months. Our <a href="/vat-flat-rate-scheme-calculator/">Flat Rate Scheme calculator</a> shows whether it would cost you less than standard VAT accounting.</p>
{faqhtml(vfaq)}
{src(VAT_SRC)}
<p class="disc">Not tax or accounting advice. Rates and thresholds as published on GOV.UK on 25 October 2026 (the £90,000 registration and £88,000 deregistration thresholds, and the 20%, 5% and 0% rates). Registration dates are calculated from the GOV.UK rules for a business that is not already registered and has not applied for an exception; they do not cover group registrations, takeovers or the special rules for non-UK businesses. HMRC has the final say on your effective date of registration.</p>'''
vjs='<script>'+FMT+money_gb+'''const MN=["January","February","March","April","May","June","July","August","September","October","November","December"];
$("mo").innerHTML=MN.map((m,i)=>`<option value="${i+1}">${m}</option>`).join("");$("mo").value=String(new Date().getMonth()+1);
const dfmt=s=>new Date(s+"T00:00:00Z").toLocaleDateString("en-GB",{timeZone:"UTC",day:"numeric",month:"long",year:"numeric"});
const rows=(a,b,c,r)=>`<table><tbody><tr><td>Price without VAT</td><td>${f(a)}</td></tr><tr><td>VAT at ${r}%</td><td>${f(b)}</td></tr><tr><td><b>Price including VAT</b></td><td><b>${f(c)}</b></td></tr></tbody></table>`;
$("go").onclick=()=>{const o=$("out");o.hidden=false;const a=v("am"),r=parseFloat($("rt").value);if(!(a>0)){o.innerHTML="<p class=bad>Enter an amount first.</p>";return;}
const x=NLUK.vat(a,r,$("md").value);o.innerHTML=`<p>${$("md").value==="add"?"Price including VAT":"Price without VAT"}</p><p class=big>${f($("md").value==="add"?x.gross:x.net)}</p>`+rows(x.net,x.vat,x.gross,r);};
$("gl").onclick=()=>{const o=$("outl");o.hidden=false;const ls=[1,2,3].map(i=>({amount:v("l"+i),rate:parseFloat($("r"+i).value)})).filter(l=>l.amount>0);if(!ls.length){o.innerHTML="<p class=bad>Enter at least one line.</p>";return;}
const s=NLUK.sumLines(ls,$("md").value);o.innerHTML=`<p>Invoice total including VAT</p><p class=big>${f(s.gross)}</p><table><tbody><tr><td>Total without VAT</td><td>${f(s.net)}</td></tr><tr><td>Total VAT</td><td>${f(s.vat)}</td></tr><tr><td><b>Total including VAT</b></td><td><b>${f(s.gross)}</b></td></tr></tbody></table>`;};
$("rtp").onchange=()=>{const w=$("rtp").value==="fwd";$("gm").hidden=$("gy").hidden=w;$("gd").hidden=!w;};
$("rg").onclick=()=>{const o=$("outr");o.hidden=false;let r,h;const tv=v("tv");
if($("rtp").value==="over"){const y=parseInt($("yr").value),m=parseInt($("mo").value);if(!(y>2000&&y<2100)){o.innerHTML="<p class=bad>Enter a valid year.</p>";return;}r=NLUK.regAfterCrossing(y,m);
 h=`<p>Apply for VAT registration by</p><p class=big>${dfmt(r.deadline)}</p><table><tbody><tr><td>Month your 12-month turnover went over £90,000</td><td>${MN[m-1]} ${y}</td></tr><tr><td>Deadline to register (30 days after the end of that month)</td><td>${dfmt(r.deadline)}</td></tr><tr><td>Effective date of registration (first day of the second month after)</td><td>${dfmt(r.effective)}</td></tr></tbody></table><p class=hint>You must charge VAT from the effective date, even if you register at the deadline.</p>`;}
else{const d=$("dt").value;if(!d){o.innerHTML="<p class=bad>Choose the date you realised.</p>";return;}const p=d.split("-").map(Number);r=NLUK.regForward(p[0],p[1],p[2]);
 h=`<p>Apply for VAT registration by</p><p class=big>${dfmt(r.deadline)}</p><table><tbody><tr><td>Date you realised turnover will pass £90,000 within 30 days</td><td>${dfmt(d)}</td></tr><tr><td>Deadline to register (end of that 30-day period)</td><td>${dfmt(r.deadline)}</td></tr><tr><td>Effective date of registration (the day you realised)</td><td>${dfmt(r.effective)}</td></tr></tbody></table><p class=hint>From the effective date you owe VAT on your sales.</p>`;}
if(tv>0)h+=`<p class=hint>Your last-12-month taxable turnover of ${f(tv)} is ${tv>NLUK.THRESHOLD?f(tv-NLUK.THRESHOLD)+" over":f(NLUK.THRESHOLD-tv)+" under"} the £90,000 threshold.</p>`;
o.innerHTML=h;};</script>'''
page("uk-vat-calculator/","UK VAT Calculator 2026: Add or Remove VAT (20%, 5%, 0%) and Registration Deadline | NorthLedger Tools",
 "Free UK VAT calculator for 2026: add or remove 20%, 5% or 0% VAT to the penny, plus your VAT registration deadline and effective date from the £90,000 threshold rules.",
 vbody,loc="en-GB",ld=[app_ld("UK VAT Calculator 2026",BASE+"uk-vat-calculator/","Adds or removes UK VAT at 20%, 5% and 0% and works out the VAT registration deadline and effective date.",lang="en-GB",cur="GBP"),faq_ld(vfaq)],
 libs='<script src="/assets/uk.js"></script>',script=vjs,upd=B2UPD)

# ---------- UK VAT Flat Rate Scheme ----------
FRS_SRC=[("GOV.UK: VAT Flat Rate Scheme, how much you pay (sector percentages)","https://www.gov.uk/vat-flat-rate-scheme/how-much-you-pay"),
("GOV.UK: VAT Flat Rate Scheme, who can join (£150,000 to join)","https://www.gov.uk/vat-flat-rate-scheme/who-can-join"),
("GOV.UK: VAT Flat Rate Scheme, if your circumstances change (£230,000 to leave)","https://www.gov.uk/vat-flat-rate-scheme/if-your-circumstances-change"),
("HMRC: VAT Notice 733, Flat Rate Scheme for small businesses (limited cost business, 1% first-year reduction, capital goods over £2,000)","https://www.gov.uk/guidance/flat-rate-scheme-for-small-businesses-vat-notice-733--2"),
("GOV.UK: VAT rates","https://www.gov.uk/vat-rates")]
ffaq=[("How does the VAT Flat Rate Scheme work?","Instead of charging 20% to customers and reclaiming the VAT on your purchases, you still charge your customers the normal VAT and show it on your invoices, but you pay HMRC a fixed percentage of your VAT-inclusive turnover. The percentage depends on your trade sector. You keep the difference between the VAT you collected and what you pay HMRC, and generally you cannot reclaim VAT on purchases, except capital assets over £2,000 including VAT."),
("Who can join the Flat Rate Scheme in 2026?","You can join if you expect your VAT taxable turnover (excluding VAT) to be £150,000 or less over the next 12 months. You must leave if, on the anniversary of joining, your turnover for the last 12 months was more than £230,000 including VAT (or you expect it to be in the next 12 months), or if you expect your total income in the next 30 days alone to be more than £230,000 including VAT."),
("What is the limited cost business rate of 16.5%?","If you spend very little on goods you use in the business, you must use 16.5% instead of your sector rate. A limited cost business spends less than 2% of its VAT-inclusive flat rate turnover on relevant goods, or more than 2% but less than £1,000 a year (£250 a quarter). Relevant goods exclude capital expenditure, vehicles and fuel (unless you are a transport business), food and drink for you or staff, and goods bought for resale (unless that is your main business). Services do not count at all, which is why many contractors fall into it."),
("What is the 1% first-year discount?","If it is within the first 12 months from the date you registered for VAT, you can deduct 1 percentage point from your flat rate percentage. It also applies to the limited cost rate, so 16.5% becomes 15.5%. The discount ends on the first anniversary of VAT registration, even if you joined the scheme later."),
("Do exempt sales and zero-rated sales count?","Yes: the flat rate is applied to your total VAT-inclusive turnover, which includes zero-rated, reduced-rated and standard-rated sales and any exempt income. That is why the scheme is often poor value for a business with a lot of zero-rated sales, since it pays the flat rate on those sales while standard accounting would pay no output VAT on them."),
("How does the calculator decide if the scheme saves money?","For the period you choose it computes VAT you would pay with standard accounting (VAT you charge on 20% and 5% sales, minus VAT you can reclaim on your purchases) and compares it with the flat rate percentage multiplied by VAT-inclusive turnover. A positive difference means the scheme costs you less in that period."),
("Which sector rate should I use if I do several things?","HMRC says to use the percentage for your main business activity, measured by turnover. If you cannot find a sector that fits, 'Any other activity not listed elsewhere' applies. If your business changes the sector, you must update the percentage."),
("When do I have to use 16.5% even if my sector rate is lower?","Whenever the limited cost test is met for the return period. The test must be carried out for each return, so the same business can pay its sector rate in a quarter with equipment purchases and 16.5% in a quarter without them."),
("Is the scheme better for me than standard VAT accounting?","It depends on your sector rate, your sales mix and your purchases. It tends to suit businesses with few VAT-bearing costs and mostly standard-rated sales, but it often costs more for a business with high VAT-bearing costs or many zero-rated sales, or one forced into the 16.5% limited cost rate. This calculator compares a single period; check a typical quarter and a quarter with unusual spending.")]
sec_rows="".join(f"<tr><td>{html.escape(n)}</td><td>{r:g}%</td></tr>" for n,r in FRS_SECT)
sec_opts="".join(f'<option value="{r:g}"{" selected" if n=="Management consultancy" else ""}>{html.escape(n)} ({r:g}%)</option>' for n,r in FRS_SECT)
fbody=f'''<h1>VAT Flat Rate Scheme Calculator 2026: Compare with Standard VAT Accounting</h1>
<p class="lede">Choose your trade sector and enter one VAT period of sales and purchases. The calculator applies the HMRC flat rate, checks whether you are a 16.5% limited cost business, applies the 1% first-year discount if it applies, and compares the payment with what you would owe under standard VAT accounting.</p>
<div class="card"><div class="grid">
<div><label for="sc">Trade sector (HMRC flat rate)</label><select id="sc">{sec_opts}</select></div>
<div><label for="pd">VAT period</label><select id="pd"><option value="q">One quarter</option><option value="y">One year</option></select></div>
<div><label for="s20">Standard-rated sales, excluding VAT (£)</label><input id="s20" inputmode="decimal" placeholder="20000"></div>
<div><label for="s5">Reduced-rate (5%) sales, excluding VAT (£)</label><input id="s5" inputmode="decimal"></div>
<div><label for="s0">Zero-rated sales (£)</label><input id="s0" inputmode="decimal"></div>
<div><label for="ex">Exempt sales (£)</label><input id="ex" inputmode="decimal"></div>
<div><label for="pv">VAT you could reclaim on purchases, standard accounting (£)</label><input id="pv" inputmode="decimal" placeholder="1500"></div>
<div><label for="gd">Spend on relevant goods, including VAT (£) <span class="hint">goods only: not services, vehicles or fuel, food, capital items</span></label><input id="gd" inputmode="decimal" placeholder="600"></div>
<div><label for="fy">Within 12 months of VAT registration?</label><select id="fy"><option value="0">No</option><option value="1">Yes (1% discount)</option></select></div></div>
<button id="go">Compare the two methods</button></div><div id="out" class="card result" hidden></div>
<h2>How the Flat Rate Scheme payment is worked out</h2>
<p>Flat rate payment = flat rate percentage × VAT-inclusive turnover. VAT-inclusive turnover is the money you receive for sales that includes VAT on standard and reduced-rate sales, plus zero-rated and exempt sales. For example, a consultant with £1,000 of standard-rated sales invoices £1,200 including 20% VAT. At a sector rate of 14%, the payment to HMRC is £168 and the consultant keeps £32 of the VAT collected. Under standard accounting the payment would be £200 less whatever VAT was paid on purchases.</p>
<h3>The limited cost business test</h3>
<p>A business is a <i>limited cost business</i> if its spend on relevant goods in the period is below 2% of its VAT-inclusive flat rate turnover, or above 2% but under £1,000 a year (£250 a quarter). It then pays 16.5% regardless of sector. This calculator runs that test for the period you enter. For example, a business with £10,000 of quarterly turnover that spends £225 on relevant goods is a limited cost business, because £225 is more than 2% (£200) but under £250; the same business spending £260 pays its sector rate.</p>
<h3>Joining and leaving</h3>
<p>You can join if your expected taxable turnover for the next 12 months, excluding VAT, is £150,000 or less. You must leave if your VAT-inclusive turnover for the 12 months to your anniversary of joining was more than £230,000 (or you expect it to be in the next 12 months), or you expect more than £230,000 in the next 30 days alone. HMRC also lets a business that spends big on one-off capital items (over £2,000 including VAT) reclaim that VAT outside the scheme.</p>
<p>New to VAT? Start with the <a href="/uk-vat-calculator/">UK VAT calculator</a> to add or remove VAT and to find your registration date.</p>
<h2>All 2026 flat rate percentages</h2>
<div class="scroll"><table><thead><tr><th>Type of business</th><th>Flat rate</th></tr></thead><tbody>{sec_rows}</tbody></table></div>
<p class="hint">Percentages as published by HMRC on GOV.UK. The 1% first-year reduction and the 16.5% limited cost rate are explained above.</p>
{faqhtml(ffaq)}
{src(FRS_SRC)}
<p class="disc">Not tax or accounting advice. Compares one VAT period using HMRC's published flat rate percentages and rules as of 25 October 2026. It assumes VAT on your purchases is fully reclaimable under standard accounting, ignores partial exemption (relevant if you make exempt sales), capital goods adjustments, bad-debt relief and cash accounting timing, and does not check your eligibility to join or leave. Confirm your sector and rate with HMRC before applying.</p>'''
fjs='<script>'+FMT+money_gb+'''$("go").onclick=()=>{const o=$("out");o.hidden=false;const q=$("pd").value==="q",s20=v("s20"),s5=v("s5"),s0=v("s0"),ex=v("ex");
if(!(s20+s5+s0+ex>0)){o.innerHTML="<p class=bad>Enter your sales for the period.</p>";return;}
const r=NLUK.frs({s20,s5,s0,exempt:ex,purchVat:v("pv"),goods:v("gd"),rate:parseFloat($("sc").value),firstYear:$("fy").value==="1",annual:!q});
const per=q?4:1,exAnn=(s20+s5+s0)*per;
let h=`<p>${r.diff>0?"The Flat Rate Scheme costs you less by":r.diff<0?"Standard VAT accounting costs you less by":"The two methods cost the same"}</p><p class=big>${f(Math.abs(r.diff))}</p><p class=hint>for this ${q?"quarter":"year"}${r.diff>0?"":""}. Positive means you pay HMRC less under the scheme.</p>`;
h+=`<table><tbody><tr><td>VAT-inclusive turnover</td><td>${f(r.incl)}</td></tr><tr><td>Flat rate used${r.lct?" (limited cost business)":""}</td><td>${r.rate.toFixed(1)}%</td></tr><tr><td><b>Pay HMRC under the Flat Rate Scheme</b></td><td><b>${f(r.flat)}</b></td></tr><tr><td>VAT charged on your standard and reduced-rate sales</td><td>${f(r.standard+v("pv"))}</td></tr><tr><td>Less VAT reclaimed on purchases</td><td>${f(-v("pv"))}</td></tr><tr><td><b>Pay HMRC under standard accounting</b></td><td><b>${f(r.standard)}</b></td></tr></tbody></table>`;
if(r.lct)h+=`<p><b>Limited cost business:</b> your spend on relevant goods (${f(v("gd"))}) is under ${f(r.limit)} (2% of VAT-inclusive turnover) or under ${f(r.abs)}, so 16.5%${$("fy").value==="1"?" less 1% = 15.5%":""} applies instead of your sector rate of ${parseFloat($("sc").value).toFixed(1)}%.</p>`;
else h+=`<p>Your spend on relevant goods (${f(v("gd"))}) is above both limits (${f(r.limit)} and ${f(r.abs)}), so your sector rate applies${$("fy").value==="1"?", less the 1% first-year discount":""}.</p>`;
if(exAnn>150000)h+=`<p class=bad>At this level your yearly turnover excluding VAT (about ${f(exAnn)}) is above the £150,000 limit for joining the scheme.</p>`;
if(r.incl*per>230000)h+=`<p class=bad>VAT-inclusive turnover of ${f(r.incl*per)} a year is above the £230,000 level at which you must leave the scheme.</p>`;
o.innerHTML=h;o.scrollIntoView({behavior:"smooth"});};</script>'''
page("vat-flat-rate-scheme-calculator/","VAT Flat Rate Scheme Calculator 2026: Sector Rates, 16.5% Limited Cost Test | NorthLedger Tools",
 "Free UK VAT Flat Rate Scheme calculator: pick your sector, apply the 16.5% limited cost test and 1% first-year discount, and compare against standard VAT accounting.",
 fbody,loc="en-GB",ld=[app_ld("VAT Flat Rate Scheme Calculator 2026",BASE+"vat-flat-rate-scheme-calculator/","Compares UK VAT Flat Rate Scheme payments with standard VAT accounting, including the limited cost business test.",lang="en-GB",cur="GBP"),faq_ld(ffaq)],
 libs='<script src="/assets/uk.js"></script>',script=fjs,upd=B2UPD)

# ---------- California paycheck ----------
CA_SRC=[("California EDD: 2026 Withholding Schedules, Method B (Exact Calculation), Tables 1 to 28","https://edd.ca.gov/siteassets/files/pdf_pub_ctr/26methb.pdf"),
("California EDD: 2026 Withholding Schedules, Method A (Wage Bracket)","https://edd.ca.gov/siteassets/files/pdf_pub_ctr/26metha.pdf"),
("California EDD: Contribution rates, withholding schedules (SDI 1.3% on all wages in 2026)","https://edd.ca.gov/en/payroll_taxes/rates_and_withholding/"),
("California EDD: 2026 California Employer's Guide, DE 44 (supplemental wages 10.23% and 6.6%)","https://edd.ca.gov/siteassets/files/pdf_pub_ctr/de44.pdf"),
("California EDD: Taxability of Employee Benefits, DE 231EB (401(k) and cafeteria plans)","https://edd.ca.gov/siteassets/files/pdf_pub_ctr/de231eb.pdf"),
("California EDD: DE 4, Employee's Withholding Allowance Certificate","https://edd.ca.gov/en/payroll_taxes/forms_and_publications/"),
("California DIR: Overtime (daily, weekly and seventh-day rules)","https://www.dir.ca.gov/dlse/faq_overtime.htm"),
("California DIR: Minimum wage ($16.90 from January 1, 2026)","https://www.dir.ca.gov/dlse/minimum_wage.htm"),
("California Department of Finance: minimum wage rises to $17.40 on January 1, 2027","https://dof.ca.gov/media/docs/whats-new/Minimum-Wage-Increase-Notification-Governor-and-Legislative-Letter.pdf"),
("IRS Pub. 15-T (2026) (federal withholding, Worksheet 1A)","https://www.irs.gov/pub/irs-pdf/p15t.pdf"),
("IRS Pub. 15 (2026) (Social Security 6.2% to $184,500, Medicare 1.45%, 22% supplemental rate)","https://www.irs.gov/publications/p15")]
cafaq=[("What comes out of a California paycheck in 2026?","Federal income tax (from your Form W-4 and the IRS Pub. 15-T tables), Social Security 6.2% up to $184,500 for the year, Medicare 1.45%, California personal income tax withholding (from your DE 4 and the EDD's 2026 schedules), and California State Disability Insurance (SDI) of 1.3% of all wages. Pre-tax items like a 401(k) or health premiums reduce some of these."),
("What is California SDI and is there a wage cap?","SDI is the employee-paid payroll tax that funds State Disability Insurance and Paid Family Leave benefits. The 2026 rate is 1.3% of every dollar of wages. Since January 1, 2024 there is no wage ceiling, so higher earners keep paying it all year; before 2024 it stopped at an annual wage limit."),
("How does California decide how much income tax to withhold?","The employer uses the DE 4 you filled in (not the federal W-4 allowances, which no longer exist) together with the EDD's withholding schedules. The exact method subtracts a standard deduction for your pay period, applies the 2026 withholding rate table for your filing status (rates from 1.1% up to 14.63%), then subtracts a credit for each regular allowance. If your pay is at or below the low-income exemption for your pay period, nothing is withheld."),
("What are DE 4 allowances and what are 'estimated deduction' allowances?","Regular allowances give a fixed tax credit each (for example $3.24 per allowance on a weekly paycheck in 2026). Additional allowances for estimated deductions (such as itemized deductions) reduce the wages subject to withholding by a fixed amount per allowance instead of giving a credit. Married employees with two or more regular allowances and head-of-household filers use the larger standard deduction and low-income exemption."),
("How is overtime paid in California?","California requires daily overtime, which is more generous than the federal weekly rule for most non-exempt employees: time-and-a-half for hours over 8 up to 12 in a day, over 40 in a workweek, and the first 8 hours on the seventh consecutive day of a workweek; double time for hours over 12 in a day and over 8 on the seventh consecutive day. The helper above applies those rules to one week of daily hours."),
("How are bonuses and other supplemental wages taxed?","If your employer pays a bonus or stock option separately from regular wages, California withholding is a flat 10.23% with no allowances, and federal withholding is a flat 22%. Other separate supplemental wages, such as commissions and overtime pay, are withheld at 6.6% by California. If the bonus is paid together with regular pay, it is added to the paycheck and taxed on the regular schedule instead. Social Security, Medicare (7.65%) and SDI (1.3%) apply as usual."),
("Does California tax 401(k) contributions on my paycheck?","Pre-tax 401(k) deferrals reduce your California income tax withholding, like federal, but they are still subject to SDI. Section 125 cafeteria plan deductions (for example health insurance premiums) are exempt from California income tax withholding and from SDI, and from Social Security and Medicare."),
("What is California's minimum wage in 2026?","$16.90 an hour for all employers from January 1, 2026, with higher minimums for fast food and healthcare facility employees and in many cities and counties. The Department of Finance has certified an increase to $17.40 on January 1, 2027."),
("Why is my pay stub different from this estimate?","Payroll systems may use the wage-bracket tables instead of the exact method (differences of a few cents), annualize irregular pay, include post-tax deductions, garnishments or local taxes, or apply a different DE 4. Pre-tax deductions beyond 401(k) and Section 125, tips, and wages above the Social Security base later in the year are not modelled. Check your pay stub."),
("Is overtime pay tax-free in California?","No. Overtime is wages for California withholding. A new federal deduction for the premium part of qualified overtime exists for tax years 2025 to 2028, but it is claimed on the federal return, not on your paycheck, and this page does not model any state treatment of it.")]
cabody=f'''<h1>California Paycheck Calculator 2026: Take-Home Pay with SDI, Overtime and Bonus</h1>
<p class="lede">Find your take-home pay in California for 2026: federal tax from the IRS tables, California income tax using the EDD's exact-calculation withholding schedule and your DE 4 allowances, Social Security, Medicare and the 1.3% State Disability Insurance. There is a helper for California's daily overtime and double-time rules.</p>
<div class="card"><div class="grid">
<div><label for="md">Paid</label><select id="md"><option value="hourly">Hourly</option><option value="salary">Salary</option></select></div>
<div><label for="pf">Pay frequency</label><select id="pf"><option value="52">Weekly</option><option value="26" selected>Every two weeks</option><option value="24">Twice a month</option><option value="12">Monthly</option></select></div>
<div id="g1"><label for="rt">Hourly rate</label><input id="rt" inputmode="decimal" placeholder="25"></div>
<div id="g2"><label for="hr">Regular hours this paycheck</label><input id="hr" inputmode="decimal" placeholder="80"></div>
<div id="g3"><label for="oh">Overtime hours (1.5×)</label><input id="oh" inputmode="decimal" placeholder="0"></div>
<div id="g5"><label for="dh">Double-time hours (2×)</label><input id="dh" inputmode="decimal" placeholder="0"></div>
<div id="g4" hidden><label for="sl">Annual salary</label><input id="sl" inputmode="decimal" placeholder="85000"></div>
<div><label for="fs">Federal filing status (W-4)</label><select id="fs"><option value="single">Single or married filing separately</option><option value="mfj">Married filing jointly</option><option value="hoh">Head of household</option></select></div>
<div><label for="cs">California filing status (DE 4)</label><select id="cs"><option value="single">Single, dual income married, or married with multiple employers</option><option value="married">Married (one income)</option><option value="hoh">Unmarried head of household</option></select></div>
<div><label for="ra">DE 4 regular allowances</label><input id="ra" inputmode="numeric" value="0"></div>
<div><label for="ea">DE 4 additional allowances for estimated deductions</label><input id="ea" inputmode="numeric" value="0"></div>
<div><label for="k4">401(k) / pre-tax retirement per paycheck</label><input id="k4" inputmode="decimal"></div>
<div><label for="s1">Pre-tax health, dental (Section 125) per paycheck</label><input id="s1" inputmode="decimal"></div>
<div><label for="bn">Bonus <span class="hint">(paid separately; optional)</span></label><input id="bn" inputmode="decimal"></div></div>
<details><summary>Federal Form W-4 details and extra withholding (optional)</summary><div class="grid">
<div><label for="s2">Step 2 box checked (two jobs)?</label><select id="s2"><option value="0">No</option><option value="1">Yes</option></select></div>
<div><label for="s3">Step 3: credits (annual $)</label><input id="s3" inputmode="decimal"></div>
<div><label for="s4a">Step 4(a): other income (annual $)</label><input id="s4a" inputmode="decimal"></div>
<div><label for="s4b">Step 4(b): deductions (annual $)</label><input id="s4b" inputmode="decimal"></div>
<div><label for="s4c">Step 4(c): extra federal withholding per paycheck</label><input id="s4c" inputmode="decimal"></div>
<div><label for="cx">Extra California withholding per paycheck (DE 4)</label><input id="cx" inputmode="decimal"></div></div></details>
<details><summary>Overtime helper: hours worked each day of one workweek</summary><p class="hint">Enter hours for seven days of one workweek. For a two-week pay period, run it once per week and add the results. Overtime is based on hours actually worked.</p><div class="grid">
{"".join(f'<div><label for="d{i}">Day {i+1}</label><input id="d{i}" inputmode="decimal"></div>' for i in range(7))}</div>
<button id="oth">Work out regular, overtime and double-time hours</button><div id="hout" class="result card" hidden></div></details>
<button id="go">Calculate my California paycheck</button></div>
<div id="out" class="card result" hidden></div>
<h2>What comes out of a California paycheck</h2>
<div class="scroll"><table><thead><tr><th>Item</th><th>2026 rule</th></tr></thead><tbody>
<tr><td>California income tax</td><td>EDD Method B (exact calculation) using your DE 4 filing status and allowances</td></tr>
<tr><td>State Disability Insurance (SDI)</td><td>1.3% of all wages, no wage cap</td></tr>
<tr><td>Federal income tax</td><td>Per your W-4 and the IRS Pub. 15-T tables</td></tr>
<tr><td>Social Security</td><td>6.2% of wages up to $184,500 for the year</td></tr>
<tr><td>Medicare</td><td>1.45% of all wages (+0.9% over $200,000)</td></tr>
<tr><td>Bonus (paid separately)</td><td>California 10.23%, federal 22%</td></tr>
<tr><td>Other supplemental pay (e.g. commissions)</td><td>California 6.6% when paid separately</td></tr>
<tr><td>Minimum wage</td><td>$16.90 an hour statewide ($17.40 from January 1, 2027); local rates can be higher</td></tr></tbody></table></div>
<h2>California overtime in plain English</h2>
<p>Unlike the federal rule, California counts overtime by the day as well as by the week. A non-exempt employee is owed 1.5 times the regular rate for hours over 8 and up to 12 in a workday, for hours over 40 in a workweek, and for the first 8 hours on the seventh consecutive day worked in a workweek. Double time applies to hours over 12 in a day and to hours over 8 on the seventh consecutive day. Hours already paid as daily overtime are not counted again towards the 40-hour weekly rule. The helper above applies exactly these rules to one workweek; enter the totals it gives in the pay fields.</p>
<p>Texas, by comparison, has no state income tax and no daily overtime: see the <a href="/texas-paycheck-calculator/">Texas paycheck calculator</a>. Self-employed in the US? Use the <a href="/1099-self-employment-tax-calculator/">1099 self-employment tax calculator</a>.</p>
<h2>How the California income tax is figured</h2>
<p>This follows the EDD's Method B steps. If your gross wages for the period are at or below the low-income exemption for your pay period and filing status, no tax is withheld. Otherwise, subtract the estimated-deduction amount for any additional allowances, subtract the standard deduction for the period, look up the tax in the withholding rate table for your filing status, and subtract the allowance credit. For example, the EDD's own sample of a biweekly paycheck of $1,600 for a married employee with three allowances, one of them for estimated deductions, works out to $2.38 of California tax, and this calculator returns the same figure.</p><p>One quirk to know about: the EDD's Method A wage-bracket tables are not always identical to Method B. For a biweekly paycheck for a married employee with two or more allowances, the Method A table appears to apply the single-person standard deduction ($219) instead of the $439 that Method B's Table 3 gives (which is exactly double the single amount and consistent with every other pay period). This calculator follows Method B, so for that one filing status and pay period it can differ from the Method A table by up to roughly $20 per paycheck. Your employer's payroll software may use either method.</p>
{faqhtml(cafaq)}
{src(CA_SRC)}
<p class="disc">Not tax advice or payroll advice. Estimate of 2026 withholding for one regular paycheck for an employee with one job, using the EDD 2026 Method B schedules, the IRS Pub. 15-T (2026) percentage method and the rates above, as of October 25, 2026. It does not model post-tax deductions, garnishments, tips, local taxes, wages above the Social Security base later in the year, additional Medicare tax withholding, or California's separate tax-return calculation. Your employer's pay stub is the official figure.</p>'''
CAJ=dict(bad="Enter your pay details first.",below="Your rate is below California's $16.90 statewide minimum wage for 2026 (local minimums may be higher).")
cajs='<script>'+FMT+money_en+f'const J={json.dumps(CAJ)};'+'''const md=$("md");md.onchange=()=>{const h=md.value==="salary";["g1","g2","g3","g5"].forEach(i=>$(i).hidden=h);$("g4").hidden=!h;};
$("oth").onclick=()=>{const d=[0,1,2,3,4,5,6].map(i=>v("d"+i)),r=NLCA.hours(d),o=$("hout");o.hidden=false;
$("hr").value=r.reg;$("oh").value=r.ot;$("dh").value=r.dt;md.value="hourly";md.onchange();
o.innerHTML=`<p>For this workweek: <b>${r.reg}</b> regular hours, <b>${r.ot}</b> overtime hours (1.5×), <b>${r.dt}</b> double-time hours (2×). These were entered in the pay fields above.</p>`;};
$("go").onclick=()=>{const o=$("out");o.hidden=false;const h=md.value==="salary";
const inp={mode:md.value,rate:v("rt"),hours:v("hr"),otHours:v("oh"),dtHours:v("dh"),salary:v("sl"),periods:parseInt($("pf").value),fedStatus:$("fs").value,step2:$("s2").value==="1",credits:v("s3"),otherInc:v("s4a"),deductions:v("s4b"),fedExtra:v("s4c"),caStatus:$("cs").value,reg:parseInt($("ra").value)||0,est:parseInt($("ea").value)||0,caExtra:v("cx"),k401:v("k4"),s125:v("s1"),bonus:v("bn")};
if(!((h&&inp.salary>0)||(!h&&inp.rate>0&&(inp.hours>0||inp.otHours>0||inp.dtHours>0)))){o.innerHTML="<p class=bad>"+J.bad+"</p>";return;}
const r=NLCA.paycheck(inp),n=v("bn");
let t=`<p>Take-home pay per paycheck</p><p class=big>${f(r.net)}</p><p class=hint>${(100*r.takeHomePct).toFixed(1)}% of your ${f(r.gross)} gross pay. About ${f(r.annNet)} a year if every paycheck matched this one.</p>`;
if(!h&&inp.rate>0&&inp.rate<NLCA.MIN_WAGE)t+=`<p class=bad>${J.below}</p>`;
const extra=[];if(r.ot>0)extra.push(f(r.ot)+" overtime");if(r.dt>0)extra.push(f(r.dt)+" double time");
t+="<table><tbody>"+[["Gross pay"+(extra.length?" (includes "+extra.join(" and ")+")":""),r.gross],["Federal income tax",-r.fed],["Social Security (6.2%)",-r.ss],["Medicare (1.45%)",-r.med],["California income tax"+(r.ca.exempt?" (below low-income exemption)":""),-r.caTax],["California SDI (1.3%)",-r.sdi],["401(k) / pre-tax retirement",-r.k401],["Pre-tax health (Section 125)",-r.s125],["Take-home pay",r.net]].map(x=>`<tr><td>${x[0]}</td><td>${f(x[1])}</td></tr>`).join("")+"</tbody></table>";
if(n>0)t+=`<h3>Bonus of ${f(n)}, paid separately</h3><p>Federal income tax at the flat 22%: ${f(r.bonusFed)}. California income tax at 10.23%: ${f(r.bonusCa)}. Social Security and Medicare (7.65%): ${f(r.bonusFica)}. SDI (1.3%): ${f(r.bonusSdi)}. <b>You keep ${f(r.bonusNet)}.</b></p>`;
t+=`<p class=hint>California takes ${f(r.stateTotal)} from this paycheck (income tax plus SDI).</p>`;
o.innerHTML=t;o.scrollIntoView({behavior:"smooth"});};</script>'''
page("california-paycheck-calculator/","California Paycheck Calculator 2026: SDI, Overtime & Bonus Take-Home Pay | NorthLedger Tools",
 "Free 2026 California paycheck calculator: take-home pay with EDD state withholding (DE 4 allowances), 1.3% SDI, daily overtime and double time, 401(k) and bonus.",
 cabody,loc="en-US",ld=[app_ld("California Paycheck Calculator 2026",BASE+"california-paycheck-calculator/","Calculates 2026 take-home pay in California with state withholding, SDI, overtime and bonuses.",lang="en-US",cur="USD"),faq_ld(cafaq)],
 libs='<script src="/assets/us.js"></script><script src="/assets/ca.js"></script>',script=cajs,upd=B2UPD)

# ---------- French: self-employed tax Ontario / BC / Alberta ----------
SEFR_PATH="impot-travailleur-autonome-ontario-cb-alberta/"
SEFR_SRC=[("ARC : Taux d'imposition des particuliers au Canada (en anglais)","https://www.canada.ca/en/revenue-agency/services/tax/individuals/tax-rates-brackets.html"),
("ARC : Taux de cotisation, maximums et exemptions du RPC (en anglais)","https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/payroll/payroll-deductions-contributions/canada-pension-plan-cpp/cpp-contribution-rates-maximums-exemptions.html"),
("ARC : T4127, Formules pour le calcul des retenues sur la paie (juillet 2026) (en anglais)","https://www.canada.ca/en/revenue-agency/services/forms-publications/payroll/t4127-payroll-deductions-formulas/t4127-jul.html"),
("ARC : Acomptes provisionnels d'impôt sur le revenu (en anglais)","https://www.canada.ca/en/revenue-agency/services/payments/payments-cra/individual-payments/income-tax-instalments.html"),
("Ontario : Crédit d'impôt pour les personnes et les familles à faible revenu (RFR) (en anglais)","https://www.ontario.ca/page/low-income-workers-tax-credit"),
("Colombie-Britannique : taux d'imposition des particuliers (en anglais)","https://www2.gov.bc.ca/gov/content/taxes/income-taxes/personal/tax-rates"),
("ARC : T4032AB, tables de retenues sur la paie, renseignements généraux (en anglais)","https://www.canada.ca/en/revenue-agency/services/forms-publications/payroll/t4032-payroll-deductions-tables/t4032ab-jan/t4032ab-january-general-information.html")]
sefaq=[("Combien un travailleur autonome paie-t-il au RPC en 2026?","Le travailleur autonome paie à la fois la part de l'employé et celle de l'employeur : 11,9 % des gains nets de travail autonome entre 3 500 $ et 74 600 $ (maximum 8 460,90 $), plus la deuxième cotisation supplémentaire (RPC2) de 8 % sur les gains entre 74 600 $ et 85 000 $ (maximum 832 $). Si vous avez aussi un revenu d'emploi, les cotisations déjà versées par votre employeur réduisent le montant à payer."),
("Les cotisations au RPC d'un travailleur autonome sont-elles déductibles?","En partie. La moitié « employeur » des cotisations de base, la partie bonifiée et toutes les cotisations au RPC2 sont déduites du revenu (ligne 22200 de la déclaration), et la part « employé » de base donne un crédit d'impôt non remboursable. Ce calculateur applique les deux."),
("Quand l'impôt sur le revenu de travail autonome de 2026 est-il exigible?","Pour l'année d'imposition 2026, les travailleurs autonomes ont jusqu'au 15 juin 2027 pour produire leur déclaration, mais tout solde dû doit être payé au plus tard le 30 avril 2027 pour éviter les intérêts."),
("Dois-je verser des acomptes provisionnels?","Vous devrez peut-être verser des acomptes trimestriels (15 mars, 15 juin, 15 septembre et 15 décembre) si votre impôt net à payer dépasse 3 000 $ en 2026 et en 2025 ou en 2024. L'ARC envoie des rappels d'acomptes lorsqu'ils sont requis."),
("Qu'est-ce qui n'est pas inclus dans cette estimation?","La TPS/TVH, les cotisations d'AE pour prestations spéciales (facultatives pour les travailleurs autonomes), les gains en capital, les dividendes et leurs crédits, les revenus de pension, les frais de scolarité, les frais médicaux, les dons, les crédits pour conjoint et autres crédits, l'Allocation canadienne pour les travailleurs et les crédits remboursables. Saisissez uniquement le bénéfice net de l'entreprise après dépenses."),
("Quels taux de 2026 sont utilisés?","Les tranches fédérales de 14 %, 20,5 %, 26 %, 29 % et 33 % (le taux le plus bas est de 14 % pour 2026), le montant personnel de base fédéral jusqu'à 16 452 $, ainsi que les tranches et montants personnels de base 2026 de l'Ontario, de la Colombie-Britannique (taux le plus bas de 5,60 %) et de l'Alberta (nouvelle première tranche de 8 %), tels que publiés par l'ARC et les provinces.")]
sefrbody=f'''<h1>Calcul de l'impôt d'un travailleur autonome 2026 (Ontario, C.-B., Alberta)</h1>
<p class="lede">Estimez votre impôt fédéral et provincial de 2026 ainsi que le RPC et le RPC2 sur vos revenus de pigiste ou d'entreprise, y compris la surtaxe et la prime-santé de l'Ontario, la réduction d'impôt de la Colombie-Britannique et la tranche de 8 % de l'Alberta.</p>
<div class="card"><div class="grid">
<div><label for="prov">Province de résidence au 31 décembre 2026</label><select id="prov"><option value="ON">Ontario</option><option value="BC">Colombie-Britannique</option><option value="AB">Alberta</option></select></div>
<div><label for="rev">Revenus bruts de travail autonome</label><input id="rev" inputmode="decimal" placeholder="60 000"></div>
<div><label for="exp">Dépenses d'entreprise</label><input id="exp" inputmode="decimal" placeholder="8 000"></div>
<div><label for="emp">Revenu d'emploi (T4), s'il y a lieu</label><input id="emp" inputmode="decimal"></div>
<div><label for="oth">Autres revenus imposables <span class="hint">(intérêts, etc.)</span></label><input id="oth" inputmode="decimal"></div>
<div><label for="rrsp">Déduction REER</label><input id="rrsp" inputmode="decimal"></div>
<div><label for="fhsa">Déduction CELIAPP</label><input id="fhsa" inputmode="decimal"></div>
<div><label for="wh">Impôt retenu à la source <span class="hint">(T4, case 22)</span></label><input id="wh" inputmode="decimal"></div>
<div><label for="paid">Acomptes déjà versés pour 2026</label><input id="paid" inputmode="decimal"></div></div>
<button id="go">Estimer mon impôt 2026</button></div><div id="out" class="card result" hidden></div>
<div class="cta"><b>Suivez tout au long de l'année : tableur Self-Employed Tax Estimator 2026 (ON · BC · AB)</b><p>Mêmes formules que cette page (le tableur est en anglais), plus :</p><ul><li>un journal mensuel des revenus et dépenses pour que l'estimation se mette à jour au fil de l'année</li><li>un montant suggéré à mettre de côté à chaque paiement et les dates d'acomptes</li><li>chaque taux dans un onglet modifiable, avec sa source officielle</li><li>fichier vierge + exemple rempli; fonctionne dans Excel, Google Sheets et LibreOffice</li></ul><a class="btn" href="{G}bblrt">Obtenir le tableur (17 $ CA) →</a> <a class="alt" href="https://www.etsy.com/listing/4594017328" rel="noopener">ou l'acheter sur Etsy</a></div>
<h2>Comment le calcul fonctionne</h2><p>Le revenu net de travail autonome (revenus moins dépenses) s'ajoute à vos autres revenus. Le RPC et le RPC2 sur les gains de travail autonome sont calculés aux taux des travailleurs autonomes, moins ce qui a déjà été versé par votre emploi. Les montants déductibles du RPC, du REER et du CELIAPP réduisent le revenu imposable. L'impôt fédéral utilise les tranches et crédits de 2026 (montant personnel de base, montant canadien pour emploi, crédits pour le RPC et l'AE). L'impôt provincial ajoute les règles de votre province : surtaxe, réduction d'impôt, crédit RFR et prime-santé de l'Ontario; réduction d'impôt de la Colombie-Britannique; tranches 2026 de l'Alberta.</p>
<p>Vous résidez au Québec? Utilisez plutôt le <a href="/impot-travailleur-autonome-quebec/">calculateur pour travailleurs autonomes du Québec (RRQ, RQAP, FSS)</a>. Pour estimer la réserve à mettre de côté sur chaque paiement, voyez aussi l'outil <a href="/freelancer-tax-set-aside-calculator/">de réserve d'impôt pour pigistes</a> (en anglais).</p>
{faqhtml(sefaq,"Questions fréquentes")}
{src(SEFR_SRC,"Sources")}
<p class="disc">Ceci n'est pas un avis fiscal. Estimation simplifiée pour 2026 selon les taux publiés au 12 octobre 2026, pour une personne seule sans autres crédits. Votre impôt réel dépend de votre déclaration complète. Pour produire votre déclaration, utilisez un logiciel certifié ou un professionnel.</p>'''
sefrjs='<script>'+FMT+money_fr+'''$("go").onclick=()=>{const p=$("prov").value,r=NL.calc(p,{rev:v("rev"),exp:v("exp"),emp:v("emp"),other:v("oth"),rrsp:v("rrsp"),fhsa:v("fhsa"),withheld:v("wh"),paid:v("paid")});
const se=Math.max(0,r.se),o=$("out");o.hidden=false;
const rows=[["Revenu net de travail autonome",r.se],["Revenu imposable",r.ti],["Impôt fédéral",r.fed],["Impôt provincial"+(p==="ON"?" (dont prime-santé de l'Ontario "+f(r.ohp)+")":""),r.prov],["RPC (travailleur autonome)",r.scpp],["RPC2",r.scpp2],["Total impôt + RPC",r.bill],["Moins impôt retenu et acomptes versés",-(v("wh")+v("paid"))]];
o.innerHTML=`<p>${r.balance>=0?"Solde estimé à payer pour 2026":"Remboursement estimé pour 2026"}</p><p class=big>${f(Math.abs(r.balance))}</p>`+
`<p class=hint>Cela représente environ ${(100*r.bill/Math.max(1,se+v("emp")+v("oth"))).toFixed(1).replace(".",",")} % de votre revenu total en impôt et RPC. Solde dû le 30 avril 2027.</p>`+
(r.tax-v("wh")>3000?"<p class=hint>Votre impôt net à payer dépasse 3 000 $ : si c'était aussi le cas en 2024 ou en 2025, l'ARC s'attend à des acomptes trimestriels.</p>":"")+
"<table><tbody>"+rows.map(([a,b])=>`<tr><td>${a}</td><td>${f(b)}</td></tr>`).join("")+"</tbody></table>";o.scrollIntoView({behavior:"smooth"});};</script>'''
SEALT=[("en-CA","self-employed-tax-calculator/"),("fr-CA",SEFR_PATH)]
page(SEFR_PATH,"Calcul d'impôt travailleur autonome 2026 : Ontario, C.-B., Alberta (RPC inclus) | NorthLedger Tools",
 "Calculateur gratuit 2026 : impôt fédéral et provincial et RPC/RPC2 d'un travailleur autonome en Ontario, en Colombie-Britannique et en Alberta. Solde à payer estimé.",
 sefrbody,lang="fr",alt=SEALT,ld=[app_ld("Calcul de l'impôt d'un travailleur autonome 2026 (ON, C.-B., AB)",BASE+SEFR_PATH,"Estime l'impôt fédéral et provincial 2026 et le RPC des travailleurs autonomes en Ontario, en Colombie-Britannique et en Alberta.",lang="fr-CA"),faq_ld(sefaq)],script=sefrjs,upd=B2UPD)
