/* NorthLedger Tools calculation engine (2026). Direct port of the formulas used in the NorthLedger spreadsheets.
   Not tax advice. Rates: CRA / Revenu Québec, checked Oct 11, 2026. */
(function(root){
const FED=[[0,58523,.14],[58523,117045,.205],[117045,181440,.26],[181440,258482,.29],[258482,1e12,.33]];
const PROV={ON:[[0,53891,.0505],[53891,107785,.0915],[107785,150000,.1116],[150000,220000,.1216],[220000,1e12,.1316]],
 BC:[[0,50363,.056],[50363,100728,.077],[100728,115648,.105],[115648,140430,.1229],[140430,190405,.147],[190405,265545,.168],[265545,1e12,.205]],
 AB:[[0,61200,.08],[61200,154259,.10],[154259,185111,.12],[185111,246813,.13],[246813,370220,.14],[370220,1e12,.15]],
 QC:[[0,54345,.14],[54345,108680,.19],[108680,132245,.24],[132245,1e12,.2575]]};
const PBPA={ON:12989,BC:13216,AB:22769,QC:18952};
const YMPE=74600,YAMPE=85000,EXEMPT=3500;
const M=Math.max,m=Math.min;
const brk=(ti,t)=>t.reduce((s,[l,u,r])=>s+r*M(0,m(ti,u)-l),0);
const fbpa=ni=>ni<=181440?16452:(ni>=258482?14829:16452-(ni-181440)*1623/(258482-181440));
function ohp(ti){if(ti<=20000)return 0;if(ti<=36000)return m(300,.06*(ti-20000));if(ti<=48000)return m(450,300+.06*(ti-36000));
 if(ti<=72000)return m(600,450+.25*(ti-48000));if(ti<=200000)return m(750,600+.25*(ti-72000));return m(900,750+.25*(ti-200000));}
function calc(prov,o){const {rev=0,exp=0,emp=0,other=0,rrsp=0,fhsa=0,otherded=0,withheld=0,paid=0}=o;
 const se=rev-exp,sep=M(0,se);
 const ecpp=.0595*M(0,m(emp,YMPE)-EXEMPT),ecpp2=.04*M(0,m(emp,YAMPE)-YMPE),ei=m(emp,68900)*.0163;
 const scpp=M(0,2*.0595*M(0,m(emp+sep,YMPE)-EXEMPT)-2*ecpp),scpp2=M(0,2*.04*M(0,m(emp+sep,YAMPE)-YMPE)-2*ecpp2);
 const d222=(scpp+scpp2)/2,d22215=(ecpp+scpp/2)*.01/.0595+ecpp2+scpp2/2,base=(ecpp+scpp/2)*.0495/.0595;
 const ni=se+emp+other-d222-d22215-rrsp-fhsa-otherded,ti=M(0,ni);
 const fed=M(0,brk(ti,FED)-(fbpa(ni)+m(1501,emp)+base+ei)*.14);
 const t=PROV[prov],r1=t[0][2],pb=brk(ti,t),cred=PBPA[prov]+base+ei;let pt,x={};
 if(prov==='ON'){const b=M(0,pb-cred*r1),sur=.2*M(0,b-5818)+.36*M(0,b-7446),y=b+sur,red=M(0,m(y,600-y));
  const lift=m(M(0,y-red),M(0,m(875,.0505*emp)-.05*M(0,ni-32500)));pt=y-red-lift+ohp(ti);x={sur,red,lift,ohp:ohp(ti)};}
 else if(prov==='BC'){const b=M(0,pb-cred*r1),red=m(b,M(0,690-.0356*M(0,ni-25570)));pt=b-red;x={red};}
 else {const c=cred*r1+.02*M(0,cred-61200);pt=M(0,pb-c);}
 const bill=fed+pt+scpp+scpp2;
 return Object.assign({se,scpp,scpp2,ecpp,ei,ni,ti,fed,prov:pt,tax:fed+pt,bill,balance:bill-withheld-paid},x);}
function calcQC(o){const {rev=0,exp=0,emp=0,other=0,rrsp=0,fhsa=0,otherded=0,withheld_fed=0,withheld_qc=0,paid_fed=0,paid_qc=0}=o;
 const se=rev-exp,sep=M(0,se);
 const eq=.063*M(0,m(emp,YMPE)-EXEMPT),eq2=.04*M(0,m(emp,YAMPE)-YMPE),ei=m(emp,68900)*.013,eqpip=.0043*m(emp,103000);
 const sq=M(0,.126*M(0,m(emp+sep,YMPE)-EXEMPT)-2*eq),sq2=M(0,.08*M(0,m(emp+sep,YAMPE)-YMPE)-2*eq2);
 const sqpip=((emp+sep)>=2000&&sep>0)?.00764*M(0,m(sep,103000-m(emp,103000))):0,qpip_ded=sqpip*(.00764-.0043)/.00764;
 const f222=(sq+sq2)/2,f22215=(eq+sq/2)*.01/.063+eq2+sq2/2,fbase=(eq+sq/2)*.053/.063;
 const fni=se+emp+other-f222-f22215-qpip_ded-rrsp-fhsa-otherded,fti=M(0,fni);
 const fcred=(fbpa(fni)+m(1501,emp)+fbase+ei+eqpip+(sqpip-qpip_ded))*.14;
 const basicfed=M(0,brk(fti,FED)-fcred),abat=.165*basicfed,fed=basicfed-abat;
 const qded=sq*(.053+.02)/.126+sq2+.01*M(0,m(emp,YMPE)-EXEMPT)+eq2+qpip_ded,worker=m(1450,.06*(emp+sep));
 const qni=se+emp+other-qded-rrsp-fhsa-otherded-worker,qti=M(0,qni),qtax=M(0,brk(qti,PROV.QC)-.14*PBPA.QC);
 const fb=M(0,sep+other),fss=fb<=64355?m(150,.01*M(0,fb-18500)):m(1000,150+.01*(fb-64355));
 const qbill=qtax+sq+sq2+sqpip+fss;
 return {se,eq,sq,sq2,sqpip,qpip_ded,ei,fni,fed,abat,qded,worker,qni,qtax,fss,fedbill:fed,qcbill:qbill,bill:fed+qbill,
  bal_fed:fed-withheld_fed-paid_fed,bal_qc:qbill-withheld_qc-paid_qc};}
const TFSA={2009:5000,2010:5000,2011:5000,2012:5000,2013:5500,2014:5500,2015:10000,2016:5500,2017:5500,2018:5500,2019:6000,2020:6000,2021:6000,2022:6000,2023:6500,2024:7000,2025:7000,2026:7000};
/* by: birth year; ry: first resident year; c,w: {year:amount}. Same logic as the tracker's TFSA tab. */
function tfsa(by,ry,c={},w={}){const rows=[];let prev=null;
 for(let y=2009;y<=2026;y++){const el=(Number.isFinite(by)&&y>=by+18&&y>=(ry||0))?1:0,lim=el*TFSA[y];
  const start=prev?prev.left+prev.wd+lim:lim,ct=+c[y]||0,wd=+w[y]||0,left=start-ct;
  prev={year:y,eligible:!!el,limit:lim,start,contrib:ct,wd,left};rows.push(prev);}
 return rows;}
/* FHSA participation room (CRA formulas, simplified: no withdrawals, designations or re-participation room).
   oy: year first FHSA opened (2023+); c: {year: contributions + RRSP transfers}. */
function fhsa(oy,c={},to=2026){const rows=[];let cf=0,pr=0,cum=0,ePrev=0,ePrev2=0,cPrev=0,cfPrev=0;
 for(let y=oy;y<=to;y++){
  if(y===oy){cf=0;pr=8000;}
  else{cf=m(8000,M(0,8000+cfPrev-ePrev2-cPrev));pr=m(M(0,8000+cf-ePrev),M(0,40000-cum+ePrev));}
  const ct=+c[y]||0,left=pr-ct,ex=M(0,ePrev+ct-(8000+cf));
  rows.push({year:y,cf,room:pr,contrib:ct,left,excess:ex,lifetimeUsed:cum+ct});
  ePrev2=ePrev;ePrev=ex;cPrev=ct;cfPrev=cf;cum+=ct;}
 return rows;}
function brew(o){const {vol,vu='L',eff=.72,att=.77,ferm=[],hops=[]}=o;const gal=vu==='L'?vol/3.78541:vol;
 let pts=0,mcu=0;if(gal>0)for(const f of ferm){const lb=f.amt*(f.wu==='kg'?2.20462:1);pts+=lb*f.ppg*(f.type==='Grain'?eff:1)/gal;mcu+=lb*f.color/gal;}
 const og=1+pts/1000,fg=1+(og-1)*(1-att),abv=(og-fg)*131.25/100;let ibu=0;
 if(gal>0)for(const h of hops){const u=1.65*Math.pow(.000125,og-1)*(1-Math.exp(-.04*h.min))/4.15,oz=h.amt*(h.hu==='g'?1/28.3495:1);ibu+=u*h.aa/100*oz*7490/gal;}
 const srm=mcu<=0?0:1.4922*Math.pow(mcu,.6859);return {gal,og,fg,abv,ibu,srm,ebc:srm*1.97};}
function priming(o){const {vol,vu='L',temp,tu='C',co2}=o;const tf=tu==='C'?temp*9/5+32:temp,g=vu==='L'?vol/3.78541:vol;
 const res=3.0378-.050062*tf+.00026555*tf*tf,need=M(0,co2-res),dex=15.195*g*need;
 return {res,need,dex,suc:dex*.91,dme:dex*1.47,perBottle:g?dex/(g*3.78541/.355):0};}
function abv(og,fg){return (og-fg)*131.25/100;}
const E={calc,calcQC,tfsa,fhsa,brew,priming,abv,TFSA};
if(typeof module!=='undefined')module.exports=E;else root.NL=E;
})(this);
