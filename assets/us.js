/* NorthLedger Tools: US federal calculation engine (tax year 2026). Not tax advice.
   Sources (all 2026): IRS Rev. Proc. 2025-32 (brackets, standard deduction, QBI thresholds); IRS Pub. 15-T (2026) Worksheet 1A and
   percentage-method tables; IRS Pub. 15 (2026) (22% supplemental rate); SSA 2026 COLA fact sheet (Social Security wage base $184,500);
   IRS Form 1040-ES (2026) (self-employment tax worksheet, estimated-tax worksheet, due dates). Checked Oct 25, 2026. */
(function(root){
const M=Math.max,m=Math.min;
const SS_BASE=184500,SS_RATE=.124,MED_RATE=.029,SE_FACTOR=.9235,ADDL_MED=.009,SUPP_RATE=.22;
const STD={single:16100,mfj:32200,hoh:24150};
/* Rev. Proc. 2025-32 section 3.01 Tables 1-3: [over, base tax, rate] */
const BR={single:[[0,0,.10],[12400,1240,.12],[50400,5800,.22],[105700,17966,.24],[201775,41024,.32],[256225,58448,.35],[640600,192979.25,.37]],
 mfj:[[0,0,.10],[24800,2480,.12],[100800,11600,.22],[211400,35932,.24],[403550,82048,.32],[512450,116896,.35],[768700,206583.5,.37]],
 hoh:[[0,0,.10],[17700,1770,.12],[67450,7740,.22],[105700,16155,.24],[201750,39207,.32],[256200,56631,.35],[640600,191171,.37]]};
/* Pub. 15-T (2026) section 1, Annual Percentage Method tables: [at least, tentative amount, percent] ; std = Step 2 box NOT checked, chk = checked */
const WH={mfj:{std:[[0,0,0],[19300,0,.10],[44100,2480,.12],[120100,11600,.22],[230700,35932,.24],[422850,82048,.32],[531750,116896,.35],[788000,206583.5,.37]],
  chk:[[0,0,0],[16100,0,.10],[28500,1240,.12],[66500,5800,.22],[121800,17966,.24],[217875,41024,.32],[272325,58448,.35],[400450,103291.75,.37]]},
 single:{std:[[0,0,0],[7500,0,.10],[19900,1240,.12],[57900,5800,.22],[113200,17966,.24],[209275,41024,.32],[263725,58448,.35],[648100,192979.25,.37]],
  chk:[[0,0,0],[8050,0,.10],[14250,620,.12],[33250,2900,.22],[60900,8983,.24],[108938,20512,.32],[136163,29224,.35],[328350,96489.63,.37]]},
 hoh:{std:[[0,0,0],[15550,0,.10],[33250,1770,.12],[83000,7740,.22],[121250,16155,.24],[217300,39207,.32],[271750,56631,.35],[656150,191171,.37]],
  chk:[[0,0,0],[12075,0,.10],[20925,885,.12],[45800,3870,.22],[64925,8077.5,.24],[112950,19603.5,.32],[140175,28315.5,.35],[332375,95585.5,.37]]}};
const W4_STEP1G={mfj:12900,single:8600,hoh:8600};
const QBI={single:{thr:201750,rng:75000},hoh:{thr:201750,rng:75000},mfj:{thr:403500,rng:150000}};
const ADDL={single:200000,hoh:200000,mfj:250000};
const OT_CAP={single:12500,hoh:12500,mfj:25000},OT_PHASE={single:150000,hoh:150000,mfj:300000};
const row=(t,x)=>{let r=t[0];for(const q of t)if(x>=q[0])r=q;return r;};
function incomeTax(ti,st){ti=M(0,ti);const r=row(BR[st],ti);return r[1]+r[2]*(ti-r[0]);}
/* Pub. 15-T Worksheet 1A (annual percentage method). o: {gross (taxable wages for the period), periods, status, step2, credits(W-4 step 3, annual $), otherInc (4a), deductions (4b), extra (4c per period)} */
function withhold(o){const p=o.periods,st=o.status||'single',chk=!!o.step2;
 const w1c=(+o.taxable||0)*p,w1e=w1c+(+o.otherInc||0),w1h=(+o.deductions||0)+(chk?0:W4_STEP1G[st]),adj=M(0,w1e-w1h);
 const r=row(WH[st][chk?'chk':'std'],adj),tent=(r[1]+r[2]*(adj-r[0]))/p,after=M(0,tent-(+o.credits||0)/p);
 return {adjusted:adj,tentative:tent,withheld:after+(+o.extra||0)};}
/* Paycheck. o: {mode:'hourly'|'salary', rate, hours, otHours, salary (annual), periods, status, step2, credits, otherInc, deductions, extra, k401, s125, bonus} */
function paycheck(o){const p=o.periods,st=o.status||'single',hourly=o.mode!=='salary';
 const rate=+o.rate||0,hrs=+o.hours||0,oth=hourly?+o.otHours||0:0;
 const regular=hourly?rate*hrs:(+o.salary||0)/p,ot=rate*1.5*oth,gross=regular+ot;
 const k401=m(+o.k401||0,gross),s125=m(+o.s125||0,gross-k401),taxable=M(0,gross-k401-s125),fica=M(0,gross-s125);
 const w=withhold({taxable,periods:p,status:st,step2:o.step2,credits:o.credits,otherInc:o.otherInc,deductions:o.deductions,extra:o.extra});
 const ss=.062*fica,med=.0145*fica,net=gross-w.withheld-ss-med-k401-s125;
 const bonus=+o.bonus||0,bonusFed=SUPP_RATE*bonus,bonusFica=.0765*bonus;
 /* annualised view and qualified-overtime deduction estimate (P.L. 119-21: premium half of FLSA time-and-a-half, capped, phased out above MAGI $150k / $300k) */
 const annGross=gross*p,annTaxable=taxable*p,ti=M(0,annTaxable-STD[st]);
 const otPrem=.5*rate*oth*p,otDed=m(otPrem,OT_CAP[st]),phase=annGross>OT_PHASE[st];
 const otSaving=phase?null:incomeTax(ti,st)-incomeTax(ti-otDed,st);
 return {regular,ot,gross,k401,s125,taxable,fica,fed:w.withheld,tentative:w.tentative,adjusted:w.adjusted,ss,med,state:0,net,takeHomePct:gross>0?net/gross:0,
  bonus,bonusFed,bonusFica,bonusNet:bonus-bonusFed-bonusFica,annGross,annNet:net*p,annFed:w.withheld*p,otPrem,otDed,otSaving,otPhase:phase,
  fedPct:gross>0?w.withheld/gross:0};}
/* Self-employment tax, 1040-ES worksheet. o: {profit, wages (W-2 wages subject to Social Security), medWages (W-2 Medicare wages, default = wages), status} */
function seTax(o){const profit=+o.profit||0,wages=+o.wages||0,mw=o.medWages==null?wages:+o.medWages,st=o.status||'single';
 const se=profit>0?profit*SE_FACTOR:0,applies=se>=400,base=applies?se:0;
 const room=M(0,SS_BASE-wages),ssPart=SS_RATE*m(base,room),medPart=MED_RATE*base,tax=ssPart+medPart;
 /* Form 8959: Additional Medicare Tax 0.9% (Part I on wages over the threshold, Part II on SE income above threshold less wages) */
 const th=ADDL[st],addl=ADDL_MED*(M(0,mw-th)+M(0,base-M(0,th-mw)));
 return {se:base,ss:ssPart,med:medPart,tax,half:tax/2,addl,applies};}
/* Full year estimate, 1040-ES worksheet order. o: {profit, bizDed (SE health insurance, SEP/solo 401k etc.), wages, other (other income), adj (other adjustments), status, withheld (income tax withheld from wages), prepaid (estimated payments already made), priorTax, priorAgi} */
function estimate(o){const st=o.status||'single',profit=+o.profit||0,wages=+o.wages||0,other=+o.other||0,bizDed=+o.bizDed||0,adj=+o.adj||0;
 const s=seTax({profit,wages,status:st}),agi=M(0,wages+other+profit-s.half-bizDed-adj);
 const tiPre=M(0,agi-STD[st]);
 const qbiBase=M(0,profit-s.half-bizDed);let qbid=0;
 if(qbiBase>0){const q=QBI[st],f=tiPre<=q.thr?0:m(1,(tiPre-q.thr)/q.rng),full=.2*qbiBase;
  const lim=.2*tiPre;qbid=m(full*(1-f),lim);if(qbiBase>=1000)qbid=M(qbid,m(400,tiPre));}
 const ti=M(0,tiPre-qbid),inc=incomeTax(ti,st),total=inc+s.tax+s.addl,withheld=+o.withheld||0,prepaid=+o.prepaid||0;
 const need1=total-withheld>=1000;
 const ninety=.9*total,hasPrior=o.priorTax!=null&&o.priorTax!==''&&isFinite(+o.priorTax);
 const pct=(+o.priorAgi||0)>150000?1.1:1,priorReq=hasPrior?pct*(+o.priorTax):null;
 const required=hasPrior?m(ninety,priorReq):ninety;
 const afterW=M(0,required-withheld),payRequired=need1&&afterW>0,perQuarter=payRequired?afterW/4:0;
 const remaining=M(0,afterW-prepaid);
 return Object.assign({},s,{agi,tiPre,qbiBase,qbid,ti,inc,total,withheld,prepaid,need1,ninety,priorReq,pctPrior:pct,required,afterW,payRequired,perQuarter,remaining,
  setAsidePct:profit>0?M(0,total-withheld)/profit:0,balance:total-withheld-prepaid});}
const E={incomeTax,withhold,paycheck,seTax,estimate,STD,BR,WH,SS_BASE,SUPP_RATE};
if(typeof module!=='undefined')module.exports=E;else root.NLUS=E;
})(this);
