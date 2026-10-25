from guides_lib import *

T = {int(k): v for k, v in LIM["tfsa_by_year"].items()}
CRA = "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/"
TFSA_EXCESS = (CRA + "tax-free-savings-account/owing-tax/excess.html")
TFSA_PAY = (CRA + "tax-free-savings-account/owing-tax/pay.html")
TFSA_ROOM = (CRA + "tax-free-savings-account/contributing/calculate-room.html")
TFSA_WD = (CRA + "tax-free-savings-account/withdraw.html")
ITA207 = "https://laws-lois.justice.gc.ca/eng/acts/I-3.3/section-207.01.html"

# ======================= 1. TFSA over-contribution =======================
rows = []
for ex in (500, 1000, 2000, 5000, 10000):
    rows.append([money(ex)] + [money(ex * 0.01 * m) for m in (1, 2, 4, 7, 12)])
cost_tbl = table(["Highest excess in the month", "Fixed in 1 month", "2 months", "4 months", "7 months", "12 months"], rows, "num")

guide(lang="en", slug="tfsa-over-contribution-penalty", group="Registered accounts (TFSA, RRSP, FHSA)",
 title="TFSA Over-Contribution Penalty: How the 1% Monthly Tax Is Calculated (CRA Rules)",
 desc="The CRA taxes excess TFSA amounts at 1% per month on the highest excess in each month. Worked examples, a cost-of-delay table, how to report on RC243 and what to do first.",
 h1="TFSA over-contribution penalty: how the 1% a month is calculated",
 short="The 1% monthly tax, the CRA's own examples, a cost-of-delay table and how to fix it.",
 lede="Go over your TFSA room and the CRA taxes the excess at 1% per month, counted on the highest excess you held in each month. Because every month counts in full, the date you fix it matters more than most people expect.",
 body=f'''
<h2 id="what">What counts as an over-contribution</h2>
<p>Your TFSA room for a year is the annual limit plus unused room carried forward from earlier years plus withdrawals you made in the <em>previous</em> year, minus what you have already contributed (see <a href="{TFSA_ROOM}">the CRA's room page</a>). If your contributions in a year push past that number, the part above it is an <b>excess TFSA amount</b>.</p>
<p>The CRA lists three common ways it happens: miscalculating your room, re-contributing a withdrawal in the same year without enough room, and contributing to several TFSAs without tracking the combined total. The room belongs to you, not to each account, so two TFSAs at two banks share one limit.</p>
<h2 id="tax">How the 1% tax is calculated</h2>
<p>The tax is 1% of the <b>highest</b> excess amount in your account during each month it remains. Two details trip people up:</p>
<ul><li><b>Whole months.</b> A single day in a month is a full month of tax. Fixing it on the 30th costs the same as fixing it on the 1st.</li>
<li><b>Highest, not average.</b> If you remove part of the excess mid-month, that month is still taxed on the larger figure. The smaller figure applies from the next month.</li></ul>
<p>The CRA's own examples show it. Over-contribute $2,000 in June and withdraw it in September and you pay $20 for each of June, July, August and September: $80. Withdraw it later in June and you owe $20. Over-contribute $6,000 in August, withdraw $4,000 in mid-September and the last $2,000 in October: $60 for August, $60 for September and $20 for October, which is $140.</p>
<div class="ex"><b class="t">Worked example: the same-year re-deposit</b>
Sam contributed the full $7,000 for 2026 in January, took out $5,000 in March for a car repair, and put $5,000 back in June, thinking the withdrawal freed up the room. It did not: withdrawals are added back to your room on January 1 of the <em>next</em> year, not straight away. In June Sam is $5,000 over.
<ul><li>Fixed in June: 1% × $5,000 = <b>$50</b></li><li>Fixed in September (June, July, August, September): 4 × $50 = <b>$200</b></li><li>Left in the account the whole year: it keeps costing $50 every month</li></ul></div>
<h2 id="cost">What delay costs</h2>
<p>1% a month sounds small, but it is a flat charge on the excess for every month it stays. The table shows the tax for different excess sizes and fix times (excess held at one level the whole time).</p>
{cost_tbl}
<p>The point of the table is the first column pair: small excesses cost little, but a large one left for a year costs 12% of the amount with no benefit to you.</p>
<h2 id="fix">What to do first</h2>
<ol><li><b>Withdraw the excess</b> from the account as soon as you know. The CRA says to do this "as soon as possible" and not to wait for a notice. You do not need to call the CRA; your institution reports the withdrawal.</li>
<li><b>Work out the highest excess in each month</b> it was there (our <a href="/tfsa-contribution-room-calculator/">TFSA room calculator</a> shows your room by year, and your own deposit and withdrawal dates give the rest).</li>
<li><b>File a TFSA Return (Form RC243) with Schedule A (RC243-SCH-A)</b> and pay what you owe by <b>June 30 of the year after</b> the tax applies. Tax from 2026 is due June 30, 2027. You can submit through "Submit documents" in your CRA account.</li>
<li><b>Ask for relief if it was a genuine mistake.</b> The CRA may waive or cancel the tax if it arose from a reasonable error and you withdrew the excess to fix it. You request this in a letter explaining what happened.</li></ol>
<p>The CRA checks TFSA contributions once a year and typically notifies people in late spring. Institutions report to the CRA by the end of February, so an excess can sit for several months before you hear about it, and the 1% meter runs the whole time.</p>
<h2 id="deliberate">Deliberate over-contributions</h2>
<p>The CRA warns that an excess caused by a <em>deliberate</em> over-contribution may be taxed as an "advantage" at the 100% advantage rate instead of 1% a month. The Income Tax Act defines a deliberate over-contribution in s.207.01. An honest miscalculation is the 1% case; knowingly contributing far beyond your room to exploit tax-free growth is the case to avoid.</p>
<h2 id="prevent">How to avoid it</h2>
<ul><li>Treat the CRA account figure as a starting point: it is updated once a year in spring and does not include this year's deposits. Compare it with your institution's records.</li>
<li>Keep a log of every deposit and withdrawal by date and institution. A TFSA transfer made directly between institutions is not a contribution; withdrawing and redepositing yourself is.</li>
<li>Do not re-contribute a withdrawal in the same calendar year unless you still have unused room without counting it.</li></ul>
''',
 faq=[("Is the TFSA over-contribution tax 1% of the whole balance?", "No. It is 1% of the highest excess amount in each month the excess stays in the account, not of your total TFSA balance."),
      ("If I withdraw the excess on the last day of the month, do I still owe that month?", "Yes. The CRA's own example confirms the 1% applies for the month of the over-contribution even if you remove it later in the same month."),
      ("When do I pay the TFSA over-contribution tax?", "File Form RC243 with Schedule A and pay by June 30 of the year after the year the tax applies. For tax arising in 2026, that is June 30, 2027."),
      ("Can the CRA cancel the tax?", "It may waive or cancel it if it arose from a reasonable error, looking at how much the transaction led to other tax and how much you withdrew to correct it. You send a letter through your CRA account or by mail.")],
 sources=[("CRA: If you owe tax on excess TFSA amounts", TFSA_EXCESS), ("CRA: If you have to pay tax on a TFSA (RC243, waivers)", TFSA_PAY),
          ("CRA: Calculate your TFSA contribution room", TFSA_ROOM), ("CRA: Withdrawing from a TFSA", TFSA_WD), ("Income Tax Act s.207.01 (definitions, deliberate over-contribution)", ITA207)],
 calcs=[("/tfsa-contribution-room-calculator/", "TFSA contribution room calculator", "Room rebuilt year by year from 2009")],
 rel=["how-the-tfsa-limit-is-set", "surcotisation-celi"], cta="tracker",
 alt=[("en-CA", "guides/tfsa-over-contribution-penalty/"), ("fr-CA", "guides-fr/surcotisation-celi/")])

# ======================= 2. How the TFSA limit is set =======================
cum = {}
run = 0
for y in sorted(T): run += T[y]; cum[y] = run
tbl1 = table(["Year", "Annual limit", "Cumulative since 2009"], [[str(y), money(T[y]), money(cum[y])] for y in sorted(T)], "num")
tot = sum(T.values())
since = []
for y in (2009, 2012, 2015, 2018, 2020, 2022, 2024, 2026):
    since.append([f"Eligible from {y}" + (" (or earlier)" if y == 2009 else ""), money(sum(v for k, v in T.items() if k >= y))])
tbl2 = table(["If you were 18+ and a resident since", "Total room through 2026 (nothing contributed)"], since, "num")
nxt = LIM.get("tfsa_next")
nxt_txt = ("<b>Not yet announced as of October 25, 2026.</b> The CRA publishes the next year's limit in the fall. Numbers floating around before then are guesses: we will update this page and the calculator on the day the CRA confirms it."
           if not nxt else f"The CRA has announced the 2027 limit: {money(nxt)}.")
guide(lang="en", slug="how-the-tfsa-limit-is-set", group="Registered accounts (TFSA, RRSP, FHSA)",
 title="How the TFSA Annual Limit Is Set and Your Total Room Since 2009 (CRA Table)",
 desc="The TFSA dollar limit is $5,000 indexed to inflation and rounded to the nearest $500. Full year-by-year table 2009-2026, total room by start year, and how withdrawals are added back.",
 h1="How the TFSA limit is set, and how much room you have in total",
 short="The indexation rule, every year's limit since 2009 and total room by start year.",
 lede=f"The TFSA annual limit is not a political announcement each year. It is $5,000 indexed to inflation and rounded to the nearest $500, which is why it moves in $500 steps. If you have been eligible since 2009, your total room through 2026 is {money(tot)}.",
 body=f'''
<h2 id="rule">The rule behind the number</h2>
<p>Under the Income Tax Act (s.207.01), the TFSA dollar limit is $5,000 for 2009, indexed each year after 2009 using the same inflation factor as the tax brackets (s.117.1) and rounded to the nearest $500. The Act sets $10,000 for 2015 as a one-off. That explains the zig-zag in the table below: the limit only changes when accumulated inflation crosses a rounding step.</p>
<h2 id="table">Every limit since 2009</h2>
{tbl1}
<p>Check: the 18 annual limits add up to {money(tot)}. That is the CRA's cumulative figure for someone eligible since 2009.</p>
<h2 id="since">Total room by when you became eligible</h2>
<p>You start accruing room in the calendar year you turn 18, as long as you are a resident of Canada with a SIN. If you became eligible later than 2009, your lifetime total is the sum from your first year. Nothing contributed:</p>
{tbl2}
<p>These are totals before any contributions or withdrawals. Your actual room is that total, minus everything you have contributed, plus withdrawals from previous years.</p>
<h2 id="withdrawals">What withdrawals do to room</h2>
<p>A TFSA withdrawal does not create room right away. It is added back on <b>January 1 of the next calendar year</b>. That timing is the source of most accidental over-contributions (see <a href="/guides/tfsa-over-contribution-penalty/">the penalty guide</a>). Withdrawing $5,000 in March 2026 means $5,000 of extra room from January 1, 2027, not before.</p>
<h2 id="next">What about next year's limit?</h2>
<p>{nxt_txt}</p>
<h2 id="cra">Checking your own number</h2>
<p>Your CRA account shows your room as of the CRA's last annual update, which happens in spring. It does not include this year's deposits and withdrawals. The safe method is the CRA figure plus your own records since: use <a href="/tfsa-contribution-room-calculator/">the calculator</a> to rebuild room from your first eligible year.</p>
''',
 faq=[("How is the TFSA limit decided?", "By formula: $5,000 for 2009, indexed to inflation each year and rounded to the nearest $500, with $10,000 for 2015 set in the Act."),
      ("What is the total TFSA room if I have been eligible since 2009?", f"{money(tot)} through 2026 (the sum of the annual limits), before subtracting anything you contributed."),
      ("When do TFSA withdrawals get added back to my room?", "On January 1 of the following calendar year, not immediately."),
      ("Is the 2027 TFSA limit announced?", "Not as of October 25, 2026. The CRA announces it in the fall; we will update when it is official.")],
 sources=[("Income Tax Act s.207.01 (TFSA dollar limit definition)", ITA207), ("CRA: Calculate your TFSA contribution room", TFSA_ROOM), ("CRA: Withdrawing from a TFSA", TFSA_WD),
          ("CRA: TFSA overview", CRA + "tax-free-savings-account.html")],
 calcs=[("/tfsa-contribution-room-calculator/", "TFSA contribution room calculator", "Room rebuilt year by year from 2009")],
 rel=["tfsa-over-contribution-penalty", "fhsa-and-home-buyers-plan"], cta="tracker")

# ======================= 3. FHSA + HBP =======================
FH = CRA + "first-home-savings-account/"
HBP = CRA + "rrsps-related-plans/what-home-buyers-plan/"
fh_rows = [["Year you open your first FHSA", "$8,000", "$0", "$8,000"], ["Year 2, nothing contributed in year 1", "$8,000", "$8,000", "$16,000"],
           ["Year 2, the full $8,000 contributed in year 1", "$8,000", "$0", "$8,000"], ["Year 4, nothing contributed in years 1 to 3", "$8,000", "$8,000 (capped)", "$16,000"]]
fh_tbl = table(["Situation", "Annual limit", "Carry-forward", "Room that year"], fh_rows, "num")
hbp_rows = []
for amt in (15000, 30000, 45000, 60000):
    hbp_rows.append([money(amt), money(amt / 15, dec=0), "15 years"])
hbp_tbl = table(["HBP withdrawal", "Minimum yearly repayment (÷ 15)", "Repayment period"], hbp_rows, "num")
guide(lang="en", slug="fhsa-and-home-buyers-plan", group="Registered accounts (TFSA, RRSP, FHSA)",
 title="FHSA + Home Buyers' Plan: Using Both for Your First Home (CRA Rules, 2026)",
 desc="How the FHSA and the RRSP Home Buyers' Plan work together: $8,000 a year and $40,000 lifetime, qualifying-withdrawal conditions, the $60,000 HBP, repayment rules and traps.",
 h1="FHSA and the Home Buyers' Plan: can you use both?",
 short="Two first-home programs, one home: limits, conditions and repayment traps.",
 lede="You can use an FHSA qualifying withdrawal and an RRSP Home Buyers' Plan withdrawal for the same home, if you meet each program's conditions at the time of each withdrawal. They behave very differently afterwards: FHSA money is never repaid; HBP money must go back into your RRSP over 15 years.",
 body=f'''
<h2 id="compare">The two programs side by side</h2>
{table(["", "FHSA", "RRSP Home Buyers' Plan"],
 [["What it is", "A registered account you contribute to (deductible)", "A temporary loan from your own RRSP"],
  ["Limit", "$8,000 a year, $40,000 lifetime", "Up to $60,000 withdrawn"],
  ["Tax on the way out", "None, if it is a qualifying withdrawal", "None at withdrawal"],
  ["Repay it?", "No", "Yes, over 15 years into your RRSP"],
  ["Effect on RRSP room", "RRSP-to-FHSA transfers use FHSA room and are not deductible", "Repayments do not affect your RRSP deduction limit"]])}
<h2 id="room">How FHSA room builds up</h2>
<p>Participation room is $8,000 for the year you open your first FHSA. Unused room carries forward, but the carry-forward is capped at $8,000, so the most you can add in one year is $16,000. Lifetime is $40,000. Your room is reduced by RRSP-to-FHSA transfers, and a taxable withdrawal does not restore it unless the CRA's re-participation rules apply.</p>
{fh_tbl}
<h2 id="qualifying">What a qualifying FHSA withdrawal needs</h2>
<p>All of these, per the CRA:</p>
<ul><li>You are a first-time buyer for the withdrawal: you did not live in a home you owned (or jointly owned) as your main residence in the current year before the withdrawal (not counting the 30 days just before) or the previous four calendar years.</li>
<li>You have a written agreement to buy or build a qualifying home in Canada, with the acquisition or completion date before <b>October 1 of the year after</b> the withdrawal.</li>
<li>You did not acquire the home more than 30 days before the withdrawal.</li>
<li>You are a Canadian resident from the first withdrawal until you acquire the home.</li>
<li>You intend to occupy it as your main home within one year of buying or building it.</li>
<li>You give your issuer Form RC725.</li></ul>
<p>If any condition fails, the amount is a taxable withdrawal and is added to your income for that year. There is no minimum holding period for contributions before a qualifying withdrawal. Once you make a qualifying withdrawal, close the FHSA by December 31 of the following year.</p>
<h2 id="hbp">How the Home Buyers' Plan works</h2>
<p>An eligible first-time buyer can withdraw up to $60,000 from RRSPs without it being taxed, then repay it over 15 years. Each year the minimum is your balance divided by the years left. Repay nothing and that year's minimum is added to your income. Repay more and later minimums shrink.</p>
{hbp_tbl}
<div class="callout"><b>Check the start date of repayment.</b> The CRA's repayment page grants a temporary three-year deferral only to people whose <em>first</em> HBP withdrawal was made between January 1, 2022 and December 31, 2025 (repayments start in the fifth year after the withdrawal). For earlier withdrawals the repayments start the second year after. We read the CRA's page as not extending the relief to 2026 withdrawals; confirm your own start year on your HBP statement or with the CRA before you plan around it.</div>
<p>To repay, you contribute to an RRSP in the repayment year or the first 60 days after, then designate it as a repayment on Schedule 7. You cannot repay an HBP into an FHSA. And RRSP contributions made in the 89 days before an HBP withdrawal may not be deductible if they exceed what remains in the RRSP; plan the timing.</p>
<h2 id="both">Using both for the same home</h2>
<p>The CRA confirms that you can make an HBP withdrawal and a qualifying FHSA withdrawal for the same qualifying home, as long as you meet all conditions at the time of each. Couples can each use their own FHSA and HBP. A sensible order is to use FHSA first (no repayment), and then the HBP only for the amount you need, since each dollar of HBP creates a 15-year repayment schedule.</p>
<h2 id="traps">Traps to avoid</h2>
<ul><li><b>Excess FHSA amounts cost 1% a month</b> on the highest excess, and a qualifying withdrawal does not clear one.</li>
<li><b>Moving FHSA money to a TFSA is a taxable withdrawal</b> plus a TFSA contribution: only direct transfers to an RRSP, RRIF or another FHSA avoid tax.</li>
<li><b>Re-contributing a qualifying withdrawal</b> is a new, non-deductible contribution.</li></ul>
''',
 faq=[("Can I use the FHSA and the Home Buyers' Plan together?", "Yes. The CRA says you can use both for the same qualifying home as long as you meet the conditions at the time of each withdrawal."),
      ("How much can I take out under the HBP?", "Up to $60,000 from your RRSPs, repaid over 15 years."),
      ("Do I have to repay an FHSA qualifying withdrawal?", "No. Unlike the HBP, qualifying FHSA withdrawals are not repaid."),
      ("What is the FHSA carry-forward limit?", "Unused participation room carries forward up to $8,000, so the most you can contribute in a year is $16,000. The lifetime limit is $40,000.")],
 sources=[("CRA: Withdrawals and transfers out of your FHSAs", FH + "withdrawals-transfers-out-your-fhsas.html"), ("CRA: Participating in your FHSAs", FH + "contributing-your-fhsa.html"),
          ("CRA: How to participate in the Home Buyers' Plan", HBP + "participate-home-buyers-plan.html"), ("CRA: How to repay the amounts withdrawn under the HBP", HBP + "repay-funds-withdrawn-rrsp-s-under-home-buyers-plan.html")],
 calcs=[("/fhsa-contribution-room-calculator/", "FHSA contribution room calculator", "Year-by-year participation room"), ("/rrsp-tax-refund-calculator/", "RRSP tax refund calculator", "What a contribution saves")],
 rel=["rrsp-deduction-limit-explained", "celiapp-et-regime-d-accession-a-la-propriete"], cta="tracker",
 alt=[("en-CA", "guides/fhsa-and-home-buyers-plan/"), ("fr-CA", "guides-fr/celiapp-et-regime-d-accession-a-la-propriete/")])

# ======================= 4. RRSP deduction limit =======================
RP = CRA + "rrsps-related-plans/"
rl = LIM["rrsp_limit"]
need26 = rl["2026"] / 0.18
need27 = rl["2027"] / 0.18
inc_rows = [[money(x), money(min(x * 0.18, rl["2026"]))] for x in (30000, 60000, 90000, 120000, 150000, 187834)]
inc_tbl = table(["Earned income in 2025", "New RRSP room for 2026 (18%, capped)"], inc_rows, "num")
guide(lang="en", slug="rrsp-deduction-limit-explained", group="Registered accounts (TFSA, RRSP, FHSA)",
 title="RRSP Deduction Limit Explained: 18% Rule, 2026 & 2027 Limits, Over-Contribution",
 desc="How your RRSP deduction limit is built (18% of last year's earned income, capped), the 2026 and 2027 dollar limits, the March 1 deadline and the $2,000 buffer before the 1% monthly tax.",
 h1="RRSP deduction limit explained: 18%, the cap and the $2,000 buffer",
 short="How room is built, the 2026 and 2027 limits and when over-contributing costs money.",
 lede=f"Your RRSP room for 2026 is 18% of your 2025 earned income up to {money(rl['2026'])}, plus unused room from earlier years, minus pension adjustments. The 2027 maximum is already set at {money(rl['2027'])}. And the penalty only starts once you are more than $2,000 over.",
 body=f'''
<h2 id="build">How your RRSP room is built</h2>
<p>Your RRSP deduction limit for a year is: <b>18% of the previous year's earned income (up to the dollar limit)</b>, plus any unused room carried forward, minus your pension adjustment, plus any pension adjustment reversal. Your notice of assessment shows the exact figure for the next contribution year.</p>
<p>Two points often confused: the room is based on <em>last year's</em> earned income, so your 2025 earnings create room used for the 2026 tax year; and "earned income" is mainly employment income and net self-employment income, not investment income or most capital gains.</p>
<h2 id="limits">The dollar limits</h2>
{table(["Tax year", "Dollar limit", "Earned income needed to reach it"],
 [["2024", money(rl["2024"]), money(rl["2024"] / 0.18)], ["2025", money(rl["2025"]), money(rl["2025"] / 0.18)],
  ["2026", money(rl["2026"]), money(need26)], ["2027", money(rl["2027"]) + " (set by the CRA)", money(need27)]], "num")}
<p>With 2025 earned income of about {money(need26)} you earn the full {money(rl['2026'])}. Below that, room is just 18%:</p>
{inc_tbl}
<h2 id="deadline">The deadline</h2>
<p>Contributions made in the first 60 days of a year can be deducted on the prior year's return. For 2026 the deadline is <b>{LIM["rrsp_deadline"]}</b>. A contribution after that date counts for 2027.</p>
<h2 id="example">Worked example: inside the buffer and past it</h2>
<div class="ex"><b class="t">Priya's numbers</b>
2025 earned income: $72,000. Unused room carried forward: $4,000. No pension adjustment.<br>
2026 room: $4,000 + 18% × $72,000 ($12,960) = <b>$16,960</b>.
<ul><li>She contributes $18,500 by March 1, 2027: $1,540 over. Because the CRA allows a lifetime $2,000 cushion, <b>no tax</b> applies, but she cannot deduct the extra $1,540 until she earns more room.</li>
<li>She contributes $21,000: $4,040 over. The cushion covers $2,000, leaving $2,040 over it, so the 1% tax is <b>$20.40 a month</b> (about $245 over a year) until she withdraws the excess or new room absorbs it.</li></ul></div>
<p>Report the tax on Form T1-OVP; the CRA's deadline is 90 days after the end of the year the excess relates to (March 31, 2027 for 2026). Withdrawing the excess promptly stops further months of tax.</p>
<p>The $2,000 buffer is cumulative: it applies to your total over-contributions over time, not each year. And over-contributions inside the buffer still produce no deduction, so they save no tax; they just earn tax-sheltered growth. That is a reason not to aim for it.</p>
<h2 id="refund">Why this matters for your refund</h2>
<p>A deduction is worth your marginal rate. Use <a href="/rrsp-tax-refund-calculator/">the RRSP refund calculator</a> to see the saving at your income and province, then check that the contribution fits inside your room first. Contribute above room and you get no refund on the excess.</p>
<h2 id="hbp">Special case: HBP and FHSA</h2>
<p>Repayments under the Home Buyers' Plan do not reduce your RRSP deduction limit, and direct transfers from an FHSA to an RRSP generally do not affect RRSP room. See <a href="/guides/fhsa-and-home-buyers-plan/">FHSA and the Home Buyers' Plan</a>.</p>
''',
 faq=[("What is the RRSP limit for 2026?", f"{money(rl['2026'])}, reached with 2025 earned income of about {money(need26)}. The 2027 limit is {money(rl['2027'])}."),
      ("What is the RRSP contribution deadline for the 2026 tax year?", f"{LIM['rrsp_deadline']}."),
      ("Can I over-contribute to my RRSP without penalty?", "Up to a cumulative $2,000 over your limit, with no tax. Beyond that, the tax is 1% per month on the excess above the cushion. Over-contributions within the buffer cannot be deducted."),
      ("Where do I find my RRSP deduction limit?", "On your latest notice of assessment and in your CRA account, which shows the limit for the current year.")],
 sources=[("CRA: RRSP contributions and deduction limit", RP + "rrsp-contributions.html"), ("CRA: Tax on RRSP over-contributions", RP + "contributing-a-rrsp-prpp/excess-rrsp-contribution.html"),
          ("CRA: RRSP, PRPP and SPP limits (2024–2027)", RP + "contributing-a-rrsp-prpp/contributions-limit.html")],
 calcs=[("/rrsp-tax-refund-calculator/", "RRSP tax refund calculator", "Tax with and without the deduction")],
 rel=["fhsa-and-home-buyers-plan", "date-limite-reer-et-plafond-de-cotisation"], cta="tracker")

# ======================= 5. Self-employed CPP =======================
YMPE, EX, R1, CEIL, R2 = LIM["cpp_ympe"], LIM["cpp_exemption"], LIM["cpp_rate_total"], LIM["cpp2_ceiling"], LIM["cpp2_rate_total"]
def cpp(net):
    base = R1 * max(0, min(net, YMPE) - EX); c2 = R2 * max(0, min(net, CEIL) - YMPE)
    return base, c2
rows = []
for net in (10000, 30000, 50000, 74600, 80000, 90000):
    b, c2 = cpp(net); t = b + c2
    basepct = 0.099 * max(0, min(net, YMPE) - EX); enh = 0.02 * max(0, min(net, YMPE) - EX) + c2
    ded = basepct / 2 + enh; cred = basepct / 2
    rows.append([money(net), money(b, dec=2), money(c2, dec=2), money(t, dec=2), money(ded, dec=2), money(cred, dec=2)])
cpp_tbl = table(["Net self-employment income", "CPP (11.9%)", "CPP2 (8%)", "Total you pay", "Deduction, line 22200", "Credit base, line 31000"], rows, "num")
CPPSRC = CRA + "about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/"
guide(lang="en", slug="self-employed-cpp-explained", group="Self-employed and freelancers",
 title="Self-Employed CPP in 2026: Both Shares, CPP2, and How It Is Deducted (Line 22200)",
 desc="Self-employed Canadians pay both halves of CPP: 11.9% on earnings from $3,500 to $74,600, plus 8% CPP2 to $85,000. Worked table of what you pay and how it is split between deduction and credit.",
 h1="Self-employed CPP in 2026: you pay both halves, and it is deducted two ways",
 short="11.9% plus CPP2, a worked table, and how Schedule 8 splits it into deduction and credit.",
 lede=f"If you work for yourself you pay the employee and the employer half of CPP, 11.9% of net self-employment income between {money(EX)} and {money(YMPE)}, plus 8% on the next {money(CEIL-YMPE)} (CPP2). The maximum for 2026 is {money(cpp(CEIL)[0] + cpp(CEIL)[1], dec=2)}. It is not all deducted the same way.",
 body=f'''
<h2 id="rates">The 2026 rates and ceilings</h2>
{table(["", "Employee (each half)", "Self-employed pays", "Applies to net earnings"],
 [["Base CPP", "5.95%", "11.9%", f"{money(EX)} to {money(YMPE)} (maximum {money(R1*(YMPE-EX), dec=2)})"],
  ["CPP2 (second additional)", "4%", "8%", f"{money(YMPE)} to {money(CEIL)} (maximum {money(R2*(CEIL-YMPE), dec=2)})"]], "num")}
<p>"Net earnings" means business income after expenses. Contributions are calculated on <code>Schedule 8</code> of your return, and you pay them with your income tax balance. If you also have an employer, your employer's CPP counts toward the same ceilings, so you only pay the remainder on self-employment income. Quebec residents pay QPP instead; see <a href="/guides/how-we-check-our-numbers/">how we check our numbers</a> and <a href="/impot-travailleur-autonome-quebec/">the Quebec calculator</a>.</p>
<h2 id="table">What you pay at different incomes</h2>
{cpp_tbl}
<p>The last two columns are the split described below, computed from the CRA's rules: the base CPP is half credit and half deduction, and the enhanced part is fully deductible.</p>
<h2 id="deduction">Why it is split into a deduction and a credit</h2>
<p>Because you pay both halves, the tax system treats the employer half as a business cost and the employee half as a personal credit. On Schedule 8:</p>
<ul><li><b>Line 31000 credit.</b> The base CPP split in half: the employee-share of the base contribution gets a non-refundable credit at the lowest federal rate (14% for 2026).</li>
<li><b>Line 22200 deduction.</b> The other half of the base CPP <em>plus all</em> of the enhanced (first additional) and CPP2 contributions is deducted from your income.</li></ul>
<div class="ex"><b class="t">Worked example at $50,000 net</b>
Total CPP is $5,533.50. Of that, base CPP is 9.9% × $46,500 = $4,603.50 and the enhanced part is 2% × $46,500 = $930.00. The credit base is half of base CPP: <b>$2,301.75</b> (line 31000). The deduction is the other $2,301.75 plus $930.00 = <b>$3,231.75</b> (line 22200). The income tax saving from the deduction depends on your marginal rate; the credit saves 14% of $2,301.75 federally, about $322.</div>
<h2 id="planning">Planning points</h2>
<ul><li><b>It is a flat cost, not a bracket.</b> Whether you earn $30,000 or $74,600 you pay 11.9% on the part above $3,500, so the first dollar above the exemption costs 11.9 cents in CPP before any income tax.</li>
<li><b>CPP stops mattering above $85,000.</b> Beyond the CPP2 ceiling your marginal rate no longer includes CPP, which is why set-aside percentages fall as income rises.</li>
<li><b>It builds a pension.</b> Unlike income tax, CPP contributions raise your future retirement benefit, which is worth remembering when you see the total.</li>
<li><b>Include it in instalments.</b> The CRA's instalment calculations add CPP payable to net tax owing, so CPP is part of what you pay quarterly. See <a href="/guides/which-tax-instalment-method/">which instalment method to use</a>.</li></ul>
''',
 faq=[("How much CPP do self-employed people pay in 2026?", f"11.9% of net self-employment income between {money(EX)} and {money(YMPE)} (up to {money(R1*(YMPE-EX), dec=2)}), plus 8% of income from {money(YMPE)} to {money(CEIL)} for CPP2 (up to {money(R2*(CEIL-YMPE), dec=2)})."),
      ("Is self-employed CPP tax deductible?", "Partly in each way: half of the base contribution is a credit (line 31000), and the other half of the base plus all enhanced and CPP2 contributions are a deduction (line 22200)."),
      ("Do Quebec self-employed workers pay CPP?", "No. They pay the Quebec Pension Plan, at 12.6% up to $74,600 and 8% on the next $10,400, with a maximum of $9,791."),
      ("Do I still pay CPP if I have a job and a side business?", "Contributions from both sources count toward the same yearly maximum. If your employer already took the maximum, you do not owe more on the business income.")],
 sources=[("CRA: Line 22200, deduction for CPP or QPP contributions on self-employment income", CPPSRC + "line-22200-deduction-cpp-qpp-contributions-on-self-employment-other-earnings.html"),
          ("CRA: Line 31000, base CPP or QPP contributions on self-employment income", CPPSRC + "line-31000-cpp-qpp-contributions-on-self-employment-other-earnings.html"),
          ("CRA: The Canada Pension Plan enhancement (self-employed)", "https://www.canada.ca/en/revenue-agency/news/2023/05/the-canada-pension-plan-enhancement--businesses-individuals-and-self-employed-what-it-means-for-you.html")],
 calcs=[("/self-employed-tax-calculator/", "Self-employed tax calculator (ON, BC, AB)", "Income tax plus CPP and CPP2"), ("/freelancer-tax-set-aside-calculator/", "Tax set-aside calculator", "What % of each payment to save")],
 rel=["which-tax-instalment-method", "how-we-check-our-numbers"], cta="se")

# ======================= 6. Instalment method =======================
INS = "https://www.canada.ca/en/revenue-agency/services/payments/payments-cra/individual-payments/income-tax-instalments/"
INS_OPT = "https://www.canada.ca/en/revenue-agency/services/payments/payments-cra/individual-payments/income-tax-instalments/options-calculate.html"
INS_WHO = "https://www.canada.ca/en/revenue-agency/services/payments/payments-cra/individual-payments/income-tax-instalments/who-pays-instalments.html"
guide(lang="en", slug="which-tax-instalment-method", group="Self-employed and freelancers",
 title="Which Tax Instalment Method to Use: No-Calculation, Prior-Year or Current-Year (CRA)",
 desc="The CRA gives three ways to calculate tax instalments. A worked comparison shows why the prior-year method avoids interest but defers the cash, how interest and the penalty work, and Quebec's $1,800 rule.",
 h1="Which tax instalment method should you use? A worked comparison",
 short="No-calculation vs prior-year vs current-year, with a worked example and the penalty rules.",
 lede="The CRA offers three ways to work out your quarterly instalments. They are all acceptable, but they put your cash out at different times, and instalment interest is measured against whichever method would have cost you the least.",
 body=f'''
<h2 id="who">Who has to pay instalments</h2>
<p>You generally have to pay by instalments if your net tax owing is more than <b>$3,000</b> for the current year <em>and</em> in either of the two previous years (<b>$1,800</b> for residents of Quebec, as of December 31). Self-employed people, landlords and people with investment or pension income without enough withholding are the usual cases. The CRA mails reminders (Form INNS1) in February, for March and June, and in August, for September and December.</p>
<p>Payments are due <b>March 15, June 15, September 15 and December 15</b>.</p>
<h2 id="methods">The three methods</h2>
{table(["Method", "How it works", "Good for"],
 [["No-calculation", "Pay the amounts printed on the CRA's reminder. If you only got the August reminder, pay the amount in box 2 on September 15 and December 15.", "Steady income; no effort"],
  ["Prior-year", "Add your net tax owing from last year's return, plus CPP payable and any voluntary EI, and pay according to that figure (in the fall-start case, 75% on Sept 15 and 25% on Dec 15).", "Income that grew this year"],
  ["Current-year", "Estimate this year's net tax owing plus CPP and EI and pay that.", "Income that dropped this year"]])}
<div class="ex"><b class="t">Worked example: a growing freelancer</b>
Aisha freelances in Ontario. Her 2025 net tax owing plus CPP was $9,200. In 2026 her net income is $60,000; the same engine behind <a href="/self-employed-tax-calculator/">our calculator</a> puts her 2026 bill (income tax plus CPP) at about <b>$14,603</b>.
<ul><li><b>Prior-year method:</b> pays about $9,200 in the year (a quarter each), then owes the remaining ≈ $5,403 when she files. No instalment interest, because she paid what the method required. The cash is due April 30, 2027.</li>
<li><b>Current-year method:</b> pays $14,603 across four payments (≈ $3,651 each) and owes almost nothing at filing.</li></ul>
The first is easier on cash in the year and costs nothing in interest if paid on time; the second leaves nothing for April. Neither is "right": the question is whether you would rather hold the money until April, and whether you will actually keep it separate. A <a href="/freelancer-tax-set-aside-calculator/">set-aside percentage</a> solves the second problem.</div>
<h2 id="interest">How interest and the penalty work</h2>
<p>Instalment interest applies if you were required to pay, got a reminder showing an amount, and paid late, not at all, or too little. It is compounded daily at the prescribed rate. The CRA compares what you paid with what you should have paid, using <b>the payment calculation option that results in the least interest</b>, and charges the difference if it is more than $25. That is why paying according to any of the three methods keeps you clear.</p>
<p>A penalty applies only if your instalment interest for the year is more than $1,000. It is half of the interest above the greater of $1,000 or 25% of the interest you would have owed with no instalments. The CRA's example: actual interest $2,500, no-payment interest $3,200: penalty = ($2,500 − $1,000) ÷ 2 = <b>$750</b>.</p>
<p>You can reduce interest by overpaying the next instalment or paying it early; the credit interest is not refundable and only offsets instalment interest for the same year.</p>
<h2 id="quebec">If you live in Quebec</h2>
<p>You deal with two governments. Revenu Québec sends its own reminder (Form TPZ-1026.A) when your net tax owing passed $1,800, and you pay it separately from the CRA, on the same four dates. The CRA's threshold for Quebec residents is also $1,800. Our <a href="/quebec-tax-instalments-calculator/">Quebec instalments calculator</a> estimates each side, and the French guide <a href="/guides-fr/acomptes-provisionnels-quelle-methode/">acomptes provisionnels : quelle méthode</a> covers the Revenu Québec rules.</p>
<h2 id="tips">Practical rules</h2>
<ul><li>Pay on the due date: the CRA treats the processing date of a bank payment as the payment date, so allow time.</li>
<li>If income drops mid-year, re-run the current-year estimate: it can justify smaller later instalments. Keep your working in case the CRA asks.</li>
<li>Write down which method you chose for each year: your "least interest" comparison uses all three, and a note makes April easier.</li></ul>
''',
 faq=[("What are the instalment due dates?", "March 15, June 15, September 15 and December 15."),
      ("What is the instalment threshold?", "Net tax owing above $3,000 for the current year and either of the two previous years; for Quebec residents, $1,800."),
      ("Which instalment method has the lowest interest risk?", "Any of the three avoids interest if you pay what the method requires; the CRA measures interest against the option that would have cost you the least."),
      ("Do I need to pay instalments if I did not get a reminder?", "You are still responsible if you meet the threshold, but instalment interest only applies when you received a reminder showing an amount to pay.")],
 sources=[("CRA: Options to calculate instalments", INS_OPT), ("CRA: Interest and penalty charges on instalments", INS + "interest-penalty-charges.html"),
          ("CRA: Who has to pay instalments (English)", INS_WHO), ("Revenu Québec: Versement des acomptes provisionnels", "https://www.revenuquebec.ca/fr/citoyens/declaration-de-revenus/payer-ou-etre-rembourse/acomptes-provisionnels/versement-des-acomptes-provisionnels/")],
 calcs=[("/freelancer-tax-set-aside-calculator/", "Tax set-aside calculator", "Includes quarterly instalments"), ("/quebec-tax-instalments-calculator/", "Quebec instalments calculator", "Revenu Québec and CRA, side by side")],
 rel=["self-employed-cpp-explained", "gst-hst-small-supplier-freelancers", "acomptes-provisionnels-quelle-methode"], cta="se")

# ======================= 7. GST/HST small supplier =======================
GST = "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/when-register-charge.html"
q = [("Q1", 4000), ("Q2", 9000), ("Q3", 11000), ("Q4", 8000)]
guide(lang="en", slug="gst-hst-small-supplier-freelancers", group="Self-employed and freelancers",
 title="GST/HST Small Supplier Rule for Freelancers: The $30,000 Test, Explained with Examples",
 desc="Freelancers do not have to register for GST/HST until taxable revenue passes $30,000. How the single-quarter and four-quarter tests work, the 29-day deadline, and the exceptions like ride-sharing.",
 h1="The $30,000 GST/HST small supplier rule for freelancers",
 short="How the quarter and four-quarter tests work, when you must start charging, and the exceptions.",
 lede="You can skip GST/HST registration while you are a small supplier: no more than $30,000 of taxable revenue in a single calendar quarter or over four consecutive quarters. The tricky part is that the test is rolling, and the day you cross it you must charge tax on the sale that crosses it.",
 body=f'''
<h2 id="test">The two tests</h2>
<p>For most businesses, the CRA looks at your <b>total revenue (before expenses) from worldwide taxable supplies</b>, including zero-rated supplies and those of associated persons. It excludes financial services, sales of capital property and goodwill. A calendar quarter runs January–March, April–June, July–September or October–December.</p>
{table(["If you exceed $30,000...", "You stop being a small supplier...", "You must..."],
 [["in a single calendar quarter", "on the day of the sale that takes you over", "charge GST/HST on that sale, and register within 29 days"],
  ["over the previous four consecutive quarters (not in one quarter)", "at the end of the month after the quarter in which you exceed", "charge from the first sale after that, and register within 29 days"]])}
<div class="ex"><b class="t">Worked example</b>
A designer's revenue by quarter: Q1 {money(4000)}, Q2 {money(9000)}, Q3 {money(11000)}, Q4 {money(8000)}: total {money(32000)} over the four quarters, but no single quarter above $30,000. She becomes a non-small supplier at the end of the month <em>after</em> Q4 (end of January). She charges tax from her first sale after that date.
<br><br>If she lands one $35,000 contract in a quarter, she crosses the line on the day of that sale, and she must charge GST/HST on that contract itself.</div>
<h2 id="practical">What it means in practice</h2>
<ul><li><b>Watch two numbers, not one.</b> Track revenue per calendar quarter and a running four-quarter total. Our <a href="/self-employed-tax-calculator/">self-employed calculator</a> deals with income tax; the GST/HST test is separate and uses gross revenue, not profit.</li>
<li><b>You cannot recover tax you did not charge.</b> If you cross the line and fail to charge, you owe the GST/HST yourself.</li>
<li><b>Registering early can make sense.</b> Voluntary registration lets you claim input tax credits on business purchases. Your effective date is usually the day you ask (or up to 30 days earlier). The trade-off is that you must charge clients and file returns.</li></ul>
<h2 id="exceptions">Exceptions</h2>
<ul><li><b>Taxi and commercial ride-sharing drivers</b> must register and charge GST/HST from their first fare, even when under $30,000.</li>
<li><b>Non-residents</b> selling cross-border digital services or hosting certain events follow different registration rules.</li>
<li><b>Quebec:</b> you register for GST and QST with Revenu Québec, and the small-supplier rules apply to both taxes. See the Revenu Québec page below.</li></ul>
<h2 id="after">After you register</h2>
<p>Charge the tax on invoices, keep receipts for input tax credits, and file returns on the schedule your filing period sets. The tax you collect is not your income: the set-aside percentage for income tax and CPP is separate, so keep GST/HST money in its own account.</p>
''',
 faq=[("When do I have to register for GST/HST as a freelancer?", "When your taxable revenue exceeds $30,000 in a single calendar quarter, or over four consecutive quarters. You register within 29 days of the effective date."),
      ("Is the $30,000 profit or revenue?", "Revenue before expenses from taxable supplies, not profit."),
      ("Do I have to charge GST/HST on the sale that takes me over $30,000?", "Yes, if you pass the limit in a single quarter. Your registration is effective no later than the day of that sale."),
      ("Do Uber drivers need to register?", "Yes. Commercial ride-sharing and taxi drivers must register from their first fare regardless of the $30,000 limit.")],
 sources=[("CRA: When to register for and start charging the GST/HST", GST), ("CRA: GST/HST for commercial ride-sharing drivers", "https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/gi-196/gst-hst-commercial-ride-sharing-services.html"),
          ("Revenu Québec: Petit fournisseur (TPS/TVQ)", "https://www.revenuquebec.ca/fr/citoyens/taxes/biens-et-services-taxables-detaxes-ou-exoneres/tps-et-tvq/autres-situations/petit-fournisseur/")],
 calcs=[("/freelancer-tax-set-aside-calculator/", "Tax set-aside calculator", "Income tax and CPP, separate from GST/HST")],
 rel=["which-tax-instalment-method", "self-employed-cpp-explained"], cta="se")

# ======================= 8. Methodology =======================
import json as _j
OFF = _j.load(open("validation/rq_official_2026.json"))
pick = [r for r in OFF["contrib"] if r[0] in (20000, 50000, 60000, 80000, 100000)]
cmp_rows = []
import subprocess
eng = _j.loads(subprocess.check_output(["node", "-e", "const E=require('./assets/engine.js');const o=%s;console.log(JSON.stringify(o.map(r=>{const x=E.calcQC({rev:r[0]});return [r[0],x.sq+x.sq2,x.sqpip,x.fss]})))" % _j.dumps(pick)]))
for (net, rrq, rqap, fss), (_, e1, e2, e3) in zip(pick, eng):
    cmp_rows.append([money(net), money(rrq) + " / " + money(round(e1)), money(rqap) + " / " + money(round(e2)), money(fss) + " / " + money(round(e3))])
cmp_tbl = table(["Net business income", "QPP: Revenu Québec / us", "QPIP: Revenu Québec / us", "Health Services Fund: Revenu Québec / us"], cmp_rows, "num")
guide(lang="en", slug="how-we-check-our-numbers", group="About our numbers",
 title="How We Check Our Numbers: Calculators Tested Against Revenu Québec's Official Tables",
 desc="Our tax calculators are tested against 110 figures from Revenu Québec's published 2026 self-employed tables, with zero differences above $1. How the test works, what it does not cover and how to report a mistake.",
 h1="How we check our numbers: 110 official figures, zero differences",
 short="Our calculators compared to Revenu Québec's published 2026 tables, row by row.",
 lede="A tax calculator is only useful if it matches the official numbers. We compare ours with Revenu Québec's own 2026 estimation tables for self-employed workers. In the latest run, 110 official figures matched our engine to the dollar.",
 body=f'''
<h2 id="test">What we compare</h2>
<p>Revenu Québec publishes two 2026 tables for self-employed workers: provincial and federal income tax at 22 levels of taxable income, and QPP, QPIP and Health Services Fund contributions at 22 levels of net business income. That is 44 tax figures (22 rows, provincial and federal) and 66 contribution figures (22 rows, three contributions). Our test runs the same calculation engine that powers the Quebec calculators on this site and compares each result with the published value, rounded to the dollar.</p>
{cmp_tbl}
<p>Sample rows above. In the full run of 110 figures (the tax table's 44 plus the contribution table's 66), the largest difference was $0. The test file and the official figures are published in our repository (<code>validation/</code>) so anyone can re-run them with <code>node validation/rq_check.js</code>.</p>
<h2 id="how">Why it matters</h2>
<p>Quebec self-employed tax involves federal tax with the 16.5% abatement, QPP with an employee and an employer share, QPIP, and the Health Services Fund. Mistakes in any one of these (for instance treating QPP as CPP) show up as dollars. Testing against the official table catches them.</p>
<h2 id="not">What the test does not prove</h2>
<ul><li>Revenu Québec says its tables are an overview and not an official calculation. They describe a single filer with no other credits; real returns vary.</li>
<li>The tables cover Quebec. For Ontario, BC and Alberta we use the published federal and provincial brackets, rates and credits, but we are not aware of an equivalent official table of results to test against, so treat those estimates with a little more caution.</li>
<li>Our calculators estimate for one person with no family credits. They are for planning, not filing.</li></ul>
<h2 id="process">Our process for the rest of the content</h2>
<ol><li>Every number is taken from an official page (CRA, Revenu Québec, Retraite Québec, IRS, the Income Tax Act) and the source is cited on the page.</li>
<li>Guides are drafted with the help of AI tools, then each figure is checked against its source.</li>
<li>When a limit changes (January for most), we update the calculators and guides together and show the date checked.</li>
<li>If we cannot confirm a number from an official source, we say so rather than guess. As of October 25, 2026, that applies to the 2027 TFSA limit.</li></ol>
<h2 id="report">Found an error?</h2>
<p>Tell us through our Gumroad store messages and we will check it against the source and fix it, with the date of the correction on the page.</p>
''',
 faq=[("How accurate are the Quebec calculators?", "In our latest test, 110 of 110 figures from Revenu Québec's 2026 self-employed tables matched to the dollar."),
      ("Do you test Ontario, BC and Alberta too?", "Those are checked against CRA brackets and worked examples; there is no official results table equivalent to Revenu Québec's to test against."),
      ("Can I re-run the test?", "Yes. The repository includes validation/rq_check.js and the official figures; run it with Node.")],
 sources=[("Revenu Québec: Travailleurs autonomes, tables d'impôt et de cotisations (2026)", OFF["url"]), ("Retraite Québec: Travail et cotisations (RRQ)", "https://www.retraitequebec.gouv.qc.ca/fr/programmes/regime-rentes-quebec/travail-et-cotisations")],
 calcs=[("/quebec-self-employed-tax-calculator/", "Quebec self-employed tax calculator", "Federal + Quebec, QPP, QPIP, FSS"), ("/impot-travailleur-autonome-quebec/", "Calcul impôt travailleur autonome Québec", "Version française")],
 rel=["self-employed-cpp-explained"], cta="qc")
