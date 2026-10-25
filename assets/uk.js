/* NorthLedger Tools: UK VAT engine (rates and thresholds as of 25 Oct 2026). Not tax advice.
   Sources: GOV.UK VAT rates (20% / 5% / 0%); GOV.UK When to register for VAT (threshold GBP 90,000; 30-day rules); GOV.UK VAT Flat Rate Scheme
   (eligibility GBP 150,000, leave at GBP 230,000 incl. VAT, sector rates table); HMRC VAT Notice 733 (limited cost business 16.5%: relevant goods under 2% of
   VAT-inclusive flat-rate turnover or under GBP 1,000 a year; 1% first-year reduction; capital goods over GBP 2,000 handled outside the scheme). */
(function(root){
const THRESHOLD=90000,DEREG=88000,FRS_JOIN=150000,FRS_LEAVE=230000,LCT_RATE=16.5,LCT_PCT=2,LCT_ABS=1000,FIRST_YEAR_CUT=1;
const FRS=[["Accountancy or book-keeping", 14.5], ["Advertising", 11.0], ["Agricultural services", 11.0], ["Any other activity not listed elsewhere", 12.0], ["Architect, civil and structural engineer or surveyor", 14.5], ["Boarding or care of animals", 12.0], ["Business services not listed elsewhere", 12.0], ["Catering services including restaurants and takeaways", 12.5], ["Computer and IT consultancy or data processing", 14.5], ["Computer repair services", 10.5], ["Entertainment or journalism", 12.5], ["Estate agency or property management services", 12.0], ["Farming or agriculture not listed elsewhere", 6.5], ["Film, radio, television or video production", 13.0], ["Financial services", 13.5], ["Forestry or fishing", 10.5], ["General building or construction services", 9.5], ["Hairdressing or other beauty treatment services", 13.0], ["Hiring or renting goods", 9.5], ["Hotel or accommodation", 10.5], ["Investigation or security", 12.0], ["Labour-only building or construction services", 14.5], ["Laundry or dry-cleaning services", 12.0], ["Lawyer or legal services", 14.5], ["Library, archive, museum or other cultural activity", 9.5], ["Management consultancy", 14.0], ["Manufacturing fabricated metal products", 10.5], ["Manufacturing food", 9.0], ["Manufacturing not listed elsewhere", 9.5], ["Manufacturing yarn, textiles or clothing", 9.0], ["Membership organisation", 8.0], ["Mining or quarrying", 10.0], ["Packaging", 9.0], ["Photography", 11.0], ["Post offices", 5.0], ["Printing", 8.5], ["Publishing", 11.0], ["Pubs", 6.5], ["Real estate activity not listed elsewhere", 14.0], ["Repairing personal or household goods", 10.0], ["Repairing vehicles", 8.5], ["Retailing food, confectionery, tobacco, newspapers or children’s clothing", 4.0], ["Retailing pharmaceuticals, medical goods, cosmetics or toiletries", 8.0], ["Retailing not listed elsewhere", 7.5], ["Retailing vehicles or fuel", 6.5], ["Secretarial services", 13.0], ["Social work", 11.0], ["Sport or recreation", 8.5], ["Transport or storage, including couriers, freight, removals and taxis", 10.0], ["Travel agency", 10.5], ["Veterinary medicine", 11.0], ["Wholesaling agricultural products", 8.0], ["Wholesaling food", 7.5], ["Wholesaling not listed elsewhere", 8.5]];
const bp=r=>Math.round(r*100);
/* integer pence maths, round half up. mode 'add': amount is the net price; 'remove': amount is the VAT-inclusive price. rate in percent. */
function vat(amount,rate,mode){const n=Math.round(amount*100),b=bp(rate);let net,v,gross;
 if(mode==='remove'){gross=n;net=Math.floor((2*gross*10000+(10000+b))/(2*(10000+b)));v=gross-net;}
 else{net=n;v=Math.floor((2*net*b+10000)/20000);gross=net+v;}
 return {net:net/100,vat:v/100,gross:gross/100};}
function sumLines(lines,mode){let net=0,v=0,gross=0;const rows=lines.map(l=>{const r=vat(l.amount,l.rate,mode);net+=Math.round(r.net*100);v+=Math.round(r.vat*100);gross+=Math.round(r.gross*100);return r;});
 return {rows,net:net/100,vat:v/100,gross:gross/100};}
const iso=d=>d.toISOString().slice(0,10);
/* Turnover went over GBP 90,000 in the 12 months to the end of month (year,month 1-12): register within 30 days of the end of that month; effective from the 1st of the second month after. */
function regAfterCrossing(year,month){const eom=new Date(Date.UTC(year,month,0)),dl=new Date(eom.getTime()+30*864e5),edr=new Date(Date.UTC(year,month+1,1));return {deadline:iso(dl),effective:iso(edr)};}
/* Expect to go over in the next 30 days: register by the end of that 30-day period; effective the day you realised. */
function regForward(year,month,day){const d=new Date(Date.UTC(year,month-1,day));return {deadline:iso(new Date(d.getTime()+29*864e5)),effective:iso(d)};}
/* Flat Rate Scheme vs standard accounting for one VAT period. o: {s20,s5,s0 (sales ex VAT), exempt (exempt sales), purchVat (VAT on purchases reclaimable under standard accounting),
   goods (VAT-inclusive spend on relevant goods), rate (sector %), firstYear (bool), annual (bool: period is a full year; otherwise a quarter)} */
function frs(o){const s20=+o.s20||0,s5=+o.s5||0,s0=+o.s0||0,ex=+o.exempt||0,pv=+o.purchVat||0,goods=+o.goods||0;
 const out20=Math.round(s20*20)/100,out5=Math.round(s5*5)/100;
 const incl=Math.round((s20*120+s5*105+s0*100+ex*100))/100;
 const standard=out20+out5-pv;
 const abs=o.annual===false?LCT_ABS/4:LCT_ABS;
 const lct=goods<LCT_PCT/100*incl||goods<abs;
 const base=lct?LCT_RATE:+o.rate,rate=Math.max(0,base-(o.firstYear?FIRST_YEAR_CUT:0));
 const flat=Math.round(incl*rate)/100;
 return {incl,standard,lct,limit:Math.max(LCT_PCT/100*incl,0),abs,rate,base,flat,diff:standard-flat};}
const E={vat,sumLines,regAfterCrossing,regForward,frs,FRS,THRESHOLD,DEREG,FRS_JOIN,FRS_LEAVE,LCT_RATE};
if(typeof module!=='undefined')module.exports=E;else root.NLUK=E;
})(this);
