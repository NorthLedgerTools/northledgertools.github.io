from guides_lib import *
IRS_SE = "https://www.irs.gov/businesses/small-businesses-self-employed/self-employment-tax-social-security-and-medicare-taxes"
IRS_ES = "https://www.irs.gov/pub/irs-pdf/f1040es.pdf"
IRS_SSE = "https://www.irs.gov/instructions/i1040sse"
WB = LIM["us_ss_wage_base"]

def se(net):
    base = net * 0.9235
    ss = 0.124 * min(base, WB); med = 0.029 * base
    return base, ss, med, ss + med, (ss + med) / 2
rows = []
for net in (20000, 60000, 100000, 150000, 250000):
    b, ss, med, tot, half = se(net)
    rows.append([money(net), money(b), money(ss, dec=2), money(med, dec=2), money(tot, dec=2), money(half, dec=2)])
setbl = table(["Net profit (Schedule C)", "× 92.35%", "Social security 12.4%", "Medicare 2.9%", "SE tax", "Deductible half"], rows, "num")
b60, ss60, med60, tot60, half60 = se(60000)
cross = WB / 0.9235

guide(lang="en", slug="us-self-employment-tax-explained", group="United States freelancers",
 title="Self-Employment Tax Explained for 2026: 15.3% on 92.35% (IRS Rules and Worked Table)",
 desc="US self-employment tax is 15.3% of 92.35% of net profit: 12.4% social security up to $184,500 plus 2.9% Medicare. Worked table at five income levels, the deductible half and the $400 filing rule.",
 h1="Self-employment tax in 2026: the 15.3% that is not 15.3% of your profit",
 short="Why SE tax is 15.3% of 92.35% of profit, a worked table and where the cap bites.",
 lede=f"Self-employment tax is the freelancer's version of FICA: 15.3% for social security and Medicare, but applied to 92.35% of your net profit, so the effective rate is about 14.1% until the {money(WB)} social security cap. On $60,000 of profit it is {money(tot60, dec=2)}.",
 body=f'''
<h2 id="formula">The formula</h2>
<ol><li>Start with net profit (Schedule C line 31, or your share of partnership income).</li>
<li>Multiply by <b>92.35%</b>. This is the self-employed way of removing the "employer half" from the base, so you are taxed like an employee-plus-employer on the same dollar.</li>
<li><b>Social security: 12.4%</b> of that amount, on up to <b>{money(WB)}</b> for 2026 (the IRS's 1040-ES worksheet uses this wage base).</li>
<li><b>Medicare: 2.9%</b> of the full amount, with no cap.</li>
<li>Add them: that is your SE tax, reported on Schedule SE. You owe it if your net earnings are $400 or more.</li>
<li>Deduct <b>half</b> of it on Schedule 1 when you calculate adjusted gross income.</li></ol>
<h2 id="table">What it comes to</h2>
{setbl}
<p>The social security part stops at {money(WB)} of the 92.35% base, which is about {money(cross)} of net profit. Above that you only pay Medicare (2.9%), and high earners may owe the 0.9% Additional Medicare Tax (Form 8959). The effective rate falls above the cap, but you are still paying income tax on top.</p>
<div class="ex"><b class="t">Worked example: $60,000 net profit</b>
$60,000 × 92.35% = {money(b60, dec=2)}. Social security: 12.4% × {money(b60, dec=2)} = {money(ss60, dec=2)}. Medicare: 2.9% × {money(b60, dec=2)} = {money(med60, dec=2)}. SE tax: <b>{money(tot60, dec=2)}</b>. The deductible half is {money(half60, dec=2)}, which lowers the income tax base. That is a 14.13% effective rate on the profit, not 15.3%.</div>
<h2 id="plan">What this means for planning</h2>
<ul><li><b>Set aside two buckets.</b> SE tax is separate from income tax: a freelancer with $60,000 profit owes about $8,478 SE tax <em>before</em> any federal income tax, and may owe state tax too.</li>
<li><b>The deduction is not a credit.</b> The deductible half reduces income tax by your marginal rate times {money(half60, dec=2)}; it does not reduce SE tax itself.</li>
<li><b>SE tax is included in estimated payments.</b> See <a href="/guides/us-estimated-tax-safe-harbors/">estimated tax safe harbors</a> for how to avoid an underpayment penalty.</li>
<li><b>Business expenses lower SE tax</b> because it is calculated on net profit, which is why tracking them matters.</li></ul>
<p>For your own numbers, our <a href="/1099-self-employment-tax-calculator/">1099 self-employment tax calculator</a> adds income tax and quarterly estimates.</p>
''',
 faq=[("What is the self-employment tax rate for 2026?", "15.3%: 12.4% social security on net earnings up to $184,500 plus 2.9% Medicare on all of them, applied to 92.35% of net profit."),
      ("Why multiply by 92.35%?", "It removes the equivalent of the employer's half of FICA from the base, so self-employed people are not taxed on tax. The result is an effective rate of about 14.13% below the cap."),
      ("Can I deduct self-employment tax?", "You deduct half of it on Schedule 1 when figuring adjusted gross income. It does not reduce the SE tax itself."),
      ("Do I owe SE tax if I earned less than $400?", "SE tax applies if net earnings from self-employment are $400 or more.")],
 sources=[("IRS: Self-employment tax (Social Security and Medicare taxes)", IRS_SE), ("IRS: Instructions for Schedule SE", IRS_SSE), ("IRS: Form 1040-ES (2026), SE tax worksheet and wage base", IRS_ES)],
 calcs=[("/1099-self-employment-tax-calculator/", "1099 self-employment tax calculator", "SE tax, income tax and quarterly estimates")],
 rel=["us-estimated-tax-safe-harbors"], cta=None)

# ======================= estimated tax =======================
def pay(prior_tax, cur_tax, agi_prior):
    pct = 1.10 if agi_prior > 150000 else 1.00
    a = 0.90 * cur_tax; b = pct * prior_tax
    return min(a, b), a, b
r1 = pay(18000, 24000, 120000); r2 = pay(18000, 24000, 180000); r3 = pay(30000, 24000, 120000)
guide(lang="en", slug="us-estimated-tax-safe-harbors", group="United States freelancers",
 title="Estimated Tax Safe Harbors for 2026: 90% vs 100% (110%) of Last Year, Due Dates, Form 1040-ES",
 desc="US freelancers avoid the underpayment penalty by paying the smaller of 90% of this year's tax or 100% (110% above $150,000 AGI) of last year's. Worked examples and the 2026 due dates.",
 h1="Estimated tax safe harbors: how little can you pay and still avoid a penalty?",
 short="The 90% / 100% / 110% rule with three worked examples and the four 2026 due dates.",
 lede="You can avoid the IRS underpayment penalty without predicting this year's income exactly: pay at least the smaller of 90% of this year's tax or 100% of last year's tax (110% if last year's AGI was above $150,000). Withholding counts too.",
 body=f'''
<h2 id="who">Who has to pay estimated tax</h2>
<p>For 2026, the IRS says you generally must pay estimated tax if you expect to owe at least <b>$1,000</b> after withholding and refundable credits, <em>and</em> you expect withholding and credits to be less than the smaller of 90% of 2026 tax or 100% of your 2025 tax (your 2025 return must cover all 12 months). If your 2025 AGI was above $150,000 ($75,000 if married filing separately), use 110% instead of 100%.</p>
<h2 id="dates">2026 due dates</h2>
{table(["Payment", "Due date"], [["1st", "April 15, 2026"], ["2nd", "June 15, 2026"], ["3rd", "September 15, 2026"], ["4th", "January 15, 2027*"]])}
<p>* You do not have to make the January payment if you file your 2026 return by February 1, 2027 and pay the balance in full. Note the quarters are not equal calendar quarters: the 2nd payment covers two months, and the 3rd covers three.</p>
<h2 id="examples">Three worked examples</h2>
{table(["", "Prior-year tax", "Expected 2026 tax", "Prior-year AGI", "90% of 2026", "100% / 110% of 2025", "Safe harbor (smaller)", "Each of 4 payments"],
 [["A", money(18000), money(24000), money(120000), money(r1[1]), money(r1[2]), money(r1[0]), money(r1[0] / 4)],
  ["B (high AGI)", money(18000), money(24000), money(180000), money(r2[1]), money(r2[2]) + " (110%)", money(r2[0]), money(r2[0] / 4)],
  ["C (income fell)", money(30000), money(24000), money(120000), money(r3[1]), money(r3[2]), money(r3[0]), money(r3[0] / 4)]], "num")}
<p><b>A:</b> paying the prior-year amount ({money(r1[0])}) is the cheaper safe harbor, so the freelancer pays {money(r1[0] / 4)} per payment and owes the other {money(24000 - r1[0])} when filing, with no underpayment penalty. <b>B:</b> with AGI above $150,000 the prior-year route is 110% of last year's tax, {money(r2[2])}. It is still below 90% of this year's tax ({money(r2[1])}), so it is the safe harbor: {money(r2[0] / 4)} per payment. <b>C:</b> income fell, so 90% of this year's tax ({money(r3[1])}) is smaller than last year's {money(30000)}.</p>
<h2 id="how">Choosing the approach</h2>
<ul><li><b>Prior-year method:</b> certainty. You know the number in January and you never have to estimate. Best when income is rising.</li>
<li><b>90% of current year:</b> lower cash out when income has fallen, but you need a decent estimate.</li>
<li><b>Annualized income:</b> if income is lumpy (a big Q4), Form 2210 Schedule AI lets you match payments to when you earned it.</li>
<li><b>Withholding:</b> withholding from a job counts as if paid evenly through the year, which helps when you also freelance.</li></ul>
<h2 id="se">Include self-employment tax</h2>
<p>Estimated tax covers income tax <em>and</em> self-employment tax (<a href="/guides/us-self-employment-tax-explained/">explained here</a>). The 1040-ES worksheet estimates both. A set-aside rule of thumb based on your actual numbers is better than a flat percentage; the <a href="/1099-self-employment-tax-calculator/">1099 calculator</a> gives a quarterly figure.</p>
<h2 id="state">State and what to do next</h2>
<p>This page covers federal rules. Many states have their own estimated tax rules and dates, which are often the same four dates but not always. Check your state's department of revenue.</p>
''',
 faq=[("How much estimated tax do I have to pay to avoid a penalty?", "The smaller of 90% of your 2026 tax or 100% of your 2025 tax (110% if your 2025 AGI was more than $150,000), counting any withholding."),
      ("When are 2026 estimated tax payments due?", "April 15, June 15 and September 15, 2026, and January 15, 2027."),
      ("Do I need to make the January 15 payment?", "Not if you file your 2026 return by February 1, 2027 and pay the full balance with it."),
      ("Do I need to pay estimated tax if I will owe less than $1,000?", "Generally no. The requirement applies when you expect to owe at least $1,000 after withholding and refundable credits.")],
 sources=[("IRS: Form 1040-ES (2026), instructions, rules and due dates", IRS_ES), ("IRS: Estimated taxes", "https://www.irs.gov/businesses/small-businesses-self-employed/estimated-taxes"),
          ("IRS: Underpayment of estimated tax by individuals (Form 2210)", "https://www.irs.gov/forms-pubs/about-form-2210")],
 calcs=[("/1099-self-employment-tax-calculator/", "1099 self-employment tax calculator", "Quarterly estimates")],
 rel=["us-self-employment-tax-explained"], cta=None)
US_LINK_KEYS = {"1099-self-employment-tax-calculator": ["us-self-employment-tax-explained", "us-estimated-tax-safe-harbors"]}
