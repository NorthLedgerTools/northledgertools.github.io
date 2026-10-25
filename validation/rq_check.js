// Compares assets/engine.js with Revenu Québec's published 2026 self-employed estimation tables.
// Usage: node validation/rq_check.js   (exit code 1 if any row differs by more than $1)
const E = require('../assets/engine.js');
const T = require('./rq_official_2026.json');
let bad = 0, rows = 0, maxd = 0;
const rnd = Math.round;
function chk(label, got, want) {
  rows++; const d = Math.abs(rnd(got) - want); maxd = Math.max(maxd, d);
  if (d > 1) { bad++; console.log('DIFF', label, 'engine', got.toFixed(2), 'RQ', want); }
}
for (const [ti, prov, fed] of T.tax) {
  const r = E.calcQC({ other: ti });
  chk('prov tax @' + ti, r.qtax, prov); chk('fed tax @' + ti, r.fed, fed);
}
for (const [net, rrq, rqap, fss] of T.contrib) {
  const r = E.calcQC({ rev: net });
  chk('RRQ @' + net, r.sq + r.sq2, rrq); chk('RQAP @' + net, r.sqpip, rqap); chk('FSS @' + net, r.fss, fss);
}
console.log(`${rows} official figures compared, ${bad} differ by more than $1, largest difference $${maxd}`);
process.exit(bad ? 1 : 0);
