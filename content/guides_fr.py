from guides_lib import *
import json as _j, subprocess
T = {int(k): v for k, v in LIM["tfsa_by_year"].items()}
CF = "https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/"
RF = "https://www.revenuquebec.ca/fr/citoyens/"
rl = LIM["rrsp_limit"]

# ============ FR 1. acomptes provisionnels ============
RQ_ACC = RF + "declaration-de-revenus/payer-ou-etre-rembourse/acomptes-provisionnels/versement-des-acomptes-provisionnels/"
CRA_QUI = "https://www.canada.ca/fr/agence-revenu/services/paiements/paiements-arc/paiements-particuliers/impots-acomptes-provisionnels/qui-paie-acomptes-provisionnels.html"
eng = _j.loads(subprocess.check_output(["node", "-e", "const E=require('./assets/engine.js');const r=E.calcQC({rev:60000});console.log(JSON.stringify({q:r.qcbill/4,f:r.fedbill/4,qt:r.qcbill,ft:r.fedbill}))"]))
guide(lang="fr", slug="acomptes-provisionnels-quelle-methode", group="Travailleurs autonomes (Québec)",
 title="Acomptes provisionnels au Québec : quelle méthode choisir (ARC et Revenu Québec)",
 desc="Deux gouvernements, deux séries d'acomptes : seuil de 1 800 $, dates du 15 mars au 15 décembre, méthodes sans calcul, année précédente ou année courante, intérêts et pénalités, avec un exemple chiffré pour 60 000 $.",
 h1="Acomptes provisionnels au Québec : quelle méthode choisir?",
 short="Seuil de 1 800 $, deux paiements distincts, trois méthodes et un exemple chiffré.",
 lede="Au Québec, vous payez vos acomptes à deux endroits : Revenu Québec et l'Agence du revenu du Canada. Le seuil est le même (1 800 $), les dates aussi, mais les montants et les formulaires sont distincts. Voici comment choisir une méthode sans payer d'intérêts inutiles.",
 body=f'''
<h2 id="qui">Qui doit verser des acomptes</h2>
<p>L'ARC indique que les résidents du Québec doivent payer par acomptes provisionnels si leur impôt net à payer dépasse <b>1 800 $</b> pour l'année en cours <em>et</em> aussi pour 2024 ou 2025 (3 000 $ ailleurs au Canada). La province de résidence au 31 décembre détermine le seuil. Revenu Québec applique lui aussi 1 800 $ et envoie le formulaire TPZ-1026.A en février et en août si votre impôt net à payer de 2024 dépassait ce montant (en août seulement, pour les versements de septembre et de décembre, si seul celui de 2025 le dépassait). Ce seuil de 1 800 $ se mesure sur l'impôt net à payer : les cotisations ne sont pas comptées dans le test, mais elles s'ajoutent ensuite aux montants à verser.</p>
<p>Les versements se font quatre fois par année : <b>15 mars, 15 juin, 15 septembre et 15 décembre</b>. Revenu Québec précise que ces acomptes servent à payer votre impôt <em>et certaines cotisations</em> : pour un travailleur autonome, les cotisations au RRQ, au RQAP, au Fonds des services de santé et au régime d'assurance médicaments s'ajoutent à l'impôt.</p>
<h2 id="deux">Deux gouvernements, deux paiements</h2>
{table(["", "Revenu Québec", "ARC (fédéral)"],
 [["Seuil", "1 800 $", "1 800 $ (résidents du Québec)"], ["Rappel", "TPZ-1026.A (février et août)", "INNS1 (février : mars et juin; août : septembre et décembre)"],
  ["Ce que vous payez", "Impôt du Québec + RRQ + RQAP + FSS + assurance médicaments", "Impôt fédéral (après l'abattement du Québec)"], ["Dates", "15 mars, 15 juin, 15 sept., 15 déc.", "Les mêmes"],
  ["Si le montant dépasse 10 000 $", "Paiement électronique obligatoire depuis 2024", "—"]])}
<p>Les montants de rappel arrivent par courrier ou dans Mon dossier. Si vous ne recevez pas le TPZ-1026.A, la responsabilité de déterminer vos versements vous revient : Revenu Québec propose le formulaire TP-1026 pour le calcul.</p>
<h2 id="methodes">Les trois méthodes de l'ARC</h2>
{table(["Méthode", "Comment faire", "Convient si"],
 [["Sans calcul", "Payer les montants inscrits sur le rappel. Si vous n'avez reçu que le rappel d'août, payer le montant de la case 2 le 15 septembre et le 15 décembre.", "Revenu stable"],
  ["Année précédente", "Prendre l'impôt net à payer de 2025, plus les cotisations au RPC à payer et la cotisation volontaire à l'assurance-emploi. Départ en septembre : 75 % le 15 septembre et 25 % le 15 décembre.", "Revenu en hausse"],
  ["Année courante", "Estimer l'impôt net à payer de 2026, avec les mêmes ajouts. Départ en septembre : 75 % et 25 %.", "Revenu en baisse"]])}
<p>Note : la ligne « cotisations au RPC » s'applique aux résidents des autres provinces; pour un résident du Québec, ce sont les cotisations au RRQ qui entrent dans le calcul de Revenu Québec.</p>
<div class="ex"><b class="t">Exemple : revenu net d'entreprise de 60 000 $ en 2026</b>
Avec le moteur de <a href="/impot-travailleur-autonome-quebec/">notre calculateur</a>, la facture estimée est de {money(eng["qt"], "fr", 0)} pour Revenu Québec (impôt 4 938 $, RRQ 7 119 $, RQAP 458 $, FSS 150 $) et de {money(eng["ft"], "fr", 0)} pour l'ARC. Par trimestre : environ <b>{money(eng["q"], "fr", 0)}</b> à Revenu Québec et <b>{money(eng["f"], "fr", 0)}</b> à l'ARC, soit près de 4 218 $ chaque 15 mars, juin, septembre et décembre. Ces chiffres supposent une personne seule sans autres revenus ni crédits : consultez votre rappel pour vos montants réels.</div>
<h2 id="interets">Intérêts et pénalités</h2>
<p>Revenu Québec exige des intérêts capitalisés quotidiennement sur tout versement en retard ou partiel, plus un intérêt supplémentaire de 10 % par année sur la partie manquante si vous avez versé moins de 75 % du montant exigé. Si vous payez à temps les montants inscrits sur votre TPZ-1026.A, vous n'avez pas d'intérêts à payer, même s'ils s'avèrent insuffisants. À l'ARC, l'intérêt sur acomptes s'applique si vous deviez en payer, avez reçu un rappel indiquant un montant et avez payé en retard ou trop peu. Il est composé quotidiennement au taux prescrit; l'ARC le calcule selon l'option de calcul qui produit le moins d'intérêts, et ne l'exige que s'il dépasse 25 $. Une pénalité ne s'ajoute que si les intérêts de l'année dépassent 1 000 $ : c'est la moitié de l'excédent par rapport au plus élevé de 1 000 $ ou de 25 % des intérêts qui auraient été exigés sans aucun acompte. Exemple de l'ARC : intérêts de 2 500 $ et de 3 200 $ sans acompte donnent une pénalité de (2 500 − 1 000) ÷ 2 = 750 $.</p>
<h2 id="conseils">Conseils pratiques</h2>
<ul><li>Si votre revenu a augmenté, la méthode de l'année précédente garde les intérêts à zéro, mais vous devrez le solde en avril : mettez le reste de côté.</li>
<li>La date de réception est celle du traitement par l'institution financière : prévoyez quelques jours.</li>
<li>Si vous cessez ou réduisez le travail autonome, refaites l'estimation de l'année courante avant le versement suivant.</li></ul>
<p>Notre <a href="/acomptes-provisionnels-travailleur-autonome-quebec/">calculateur d'acomptes</a> estime les deux montants. Ce guide complète <a href="/guides/which-tax-instalment-method/">la version anglaise</a>, qui traite surtout des règles hors Québec.</p>
''',
 faq=[("Quel est le seuil d'acomptes provisionnels au Québec?", "1 800 $ d'impôt net à payer pour l'année en cours et pour 2024 ou 2025, à Revenu Québec comme à l'ARC."),
      ("Quelles sont les dates des acomptes?", "Le 15 mars, le 15 juin, le 15 septembre et le 15 décembre."),
      ("Dois-je payer à Revenu Québec et à l'ARC?", "Oui, séparément : Revenu Québec pour l'impôt du Québec et certaines cotisations, l'ARC pour l'impôt fédéral."),
      ("Quelle méthode évite les intérêts?", "L'ARC mesure l'intérêt selon l'option qui coûte le moins : payer selon l'une des trois méthodes, à temps, vous met à l'abri.")],
 sources=[("Revenu Québec : Versement des acomptes provisionnels", RQ_ACC), ("ARC : Qui doit payer par acomptes provisionnels", CRA_QUI),
          ("ARC : Intérêts et pénalités sur les acomptes (en anglais)", "https://www.canada.ca/en/revenue-agency/services/payments/payments-cra/individual-payments/income-tax-instalments/interest-penalty-charges.html")],
 calcs=[("/acomptes-provisionnels-travailleur-autonome-quebec/", "Acomptes provisionnels, travailleur autonome Québec", "Revenu Québec et ARC"), ("/impot-travailleur-autonome-quebec/", "Calcul impôt travailleur autonome Québec", "Impôt, RRQ, RQAP, FSS")],
 rel=["cotisations-travailleur-autonome-quebec-2026"], cta="qc")

# ============ FR 2. cotisations ============
OFF = _j.load(open("validation/rq_official_2026.json"))
pick = [r for r in OFF["contrib"] if r[0] in (10000, 20000, 30000, 40000, 60000, 80000, 100000, 181440)]
rows = [[money(n, "fr"), money(a, "fr"), money(b, "fr"), money(c, "fr"), money(a + b + c, "fr")] for n, a, b, c in pick]
ctbl = table(["Revenu net d'entreprise", "RRQ", "RQAP", "FSS", "Total à payer"], rows, "num")
guide(lang="fr", slug="cotisations-travailleur-autonome-quebec-2026", group="Travailleurs autonomes (Québec)",
 title="Cotisations du travailleur autonome au Québec en 2026 : RRQ, RQAP et FSS expliqués",
 desc="Taux et plafonds 2026 du RRQ (12,6 %, maximum 9 791 $), du RQAP (0,764 %) et du Fonds des services de santé, avec la table officielle de Revenu Québec à huit niveaux de revenu.",
 h1="Cotisations du travailleur autonome au Québec en 2026 : RRQ, RQAP et FSS",
 short="Taux, plafonds et table officielle des cotisations selon le revenu net d'entreprise.",
 lede="Un salarié ne paie qu'une partie de ses cotisations; un travailleur autonome les paie en totalité. En 2026, à 60 000 $ de revenu net d'entreprise, Revenu Québec prévoit 7 119 $ de RRQ, 458 $ de RQAP et 150 $ au Fonds des services de santé : 7 727 $ en tout, avant l'impôt.",
 body=f'''
<h2 id="taux">Les taux et plafonds de 2026</h2>
{table(["Cotisation", "Taux", "S'applique à", "Maximum"],
 [["RRQ, régime de base + première cotisation supplémentaire", "10,6 % + 2 % = 12,6 %", "Revenu de 3 500 $ à 74 600 $", "8 958,60 $"],
  ["RRQ, deuxième cotisation supplémentaire", "8 %", "De 74 600 $ à 85 000 $", "832 $"],
  ["Total RRQ", "", "", "9 791 $"],
  ["RQAP (travailleur autonome)", "0,764 %", "Jusqu'à 103 000 $", "786,92 $"],
  ["Fonds des services de santé (FSS)", "selon le revenu", "Progressive, à partir de 18 500 $", "1 000 $"]])}
<p>Le travailleur autonome paie les deux parts du RRQ, celle du salarié et celle de l'employeur, d'où 12,6 % au lieu de la moitié. Revenu Québec précise que les cotisations se calculent sur le <b>revenu net d'entreprise</b>, alors que l'impôt se calcule sur le revenu imposable (après, par exemple, la déduction pour REER).</p>
<h2 id="table">La table de Revenu Québec</h2>
<p>Voici des lignes de la table d'estimation 2026 de Revenu Québec pour une personne qui n'a que du revenu de travail autonome :</p>
{ctbl}
<p>Observez trois choses : le RRQ plafonne à 9 791 $ vers 85 000 $ de revenu, le RQAP à 787 $ au-dessus de 103 000 $, et le FSS monte jusqu'à 1 000 $. Au-delà de 85 000 $, le total des cotisations ne bouge presque plus, ce qui explique pourquoi le pourcentage à mettre de côté diminue quand le revenu augmente.</p>
<h2 id="exemple">Exemple : 60 000 $ de revenu net</h2>
<div class="ex">RRQ : 12,6 % × (60 000 − 3 500) = 7 119 $. RQAP : 0,764 % × 60 000 = 458,40 $, arrondi à 458 $. FSS : 150 $. Total : <b>7 727 $</b>, soit environ 12,9 % du revenu net, avant l'impôt. Ces montants sont identiques à ceux de la table de Revenu Québec.</div>
<h2 id="deduction">Ce qui est déductible</h2>
<p>Une partie de la cotisation au RRQ et au RQAP peut être déduite de votre revenu, et le reste donne droit à un crédit d'impôt non remboursable. Les règles précises sont dans les formulaires de Revenu Québec et de l'ARC; notre <a href="/impot-travailleur-autonome-quebec/">calculateur</a> les applique pour estimer votre impôt et il est testé sur les tables officielles (voir <a href="/guides/how-we-check-our-numbers/">comment nous vérifions nos chiffres</a>, en anglais).</p>
<h2 id="acomptes">Et les acomptes?</h2>
<p>Ces cotisations font partie de ce que vous payez par acomptes à Revenu Québec : voir <a href="/guides-fr/acomptes-provisionnels-quelle-methode/">acomptes provisionnels : quelle méthode choisir</a>.</p>
''',
 faq=[("Quel est le taux du RRQ pour un travailleur autonome en 2026?", "12,6 % du revenu net d'entreprise entre 3 500 $ et 74 600 $, puis 8 % entre 74 600 $ et 85 000 $. Maximum : 9 791 $."),
      ("Combien paie-t-on au RQAP comme travailleur autonome?", "0,764 % du revenu jusqu'à 103 000 $, soit au plus 786,92 $ en 2026."),
      ("Pourquoi paie-t-on plus qu'un salarié?", "Parce que le travailleur autonome assume à la fois la part du salarié et celle de l'employeur."),
      ("Les cotisations se calculent-elles sur le revenu imposable?", "Non : elles se calculent sur le revenu net d'entreprise, alors que l'impôt se calcule sur le revenu imposable.")],
 sources=[("Revenu Québec : Travailleurs autonomes, tables d'impôt et de cotisations", OFF["url"]), ("Revenu Québec : Cotisation du travailleur autonome au RRQ", RF + "declaration-de-revenus/payer-ou-etre-rembourse/paiement-des-cotisations/cotisations-du-travailleur-autonome-ou-du-membre-dune-societe-de-personnes/cotisation-du-travailleur-autonome-ou-du-membre-dune-societe-de-personnes-au-regime-de-rentes-du-quebec/"),
          ("Retraite Québec : Travail et cotisations", "https://www.retraitequebec.gouv.qc.ca/fr/programmes/regime-rentes-quebec/travail-et-cotisations")],
 calcs=[("/impot-travailleur-autonome-quebec/", "Calcul impôt travailleur autonome Québec", "Impôt, RRQ, RQAP, FSS")],
 rel=["acomptes-provisionnels-quelle-methode"], cta="qc")

# ============ FR 3. CELIAPP + RAP ============
FRC = CF + "compte-epargne-libre-impot-achat-premiere-propriete/"
hbp_rows = [[money(a, "fr"), money(a / 15, "fr"), "15 ans"] for a in (15000, 30000, 45000, 60000)]
guide(lang="fr", slug="celiapp-et-regime-d-accession-a-la-propriete", group="Comptes enregistrés (CELI, REER, CELIAPP)",
 title="CELIAPP et RAP : utiliser les deux pour votre première propriété (règles de l'ARC, 2026)",
 desc="Comment le CELIAPP et le Régime d'accession à la propriété (REER) se combinent : 8 000 $ par an et 40 000 $ à vie, conditions du retrait admissible, RAP de 60 000 $ et remboursement.",
 h1="CELIAPP et RAP : peut-on utiliser les deux pour la même propriété?",
 short="Deux programmes, une propriété : plafonds, conditions et pièges de remboursement.",
 lede="Oui, un retrait admissible du CELIAPP et un retrait du RAP (REER) peuvent servir pour la même habitation, si vous respectez les conditions de chaque programme à chaque retrait. Après coup, ils diffèrent : le CELIAPP ne se rembourse pas; le RAP se rembourse à votre REER en 15 ans.",
 body=f'''
<h2 id="compare">Les deux programmes côte à côte</h2>
{table(["", "CELIAPP", "RAP (REER)"],
 [["Nature", "Compte enregistré où l'on cotise (déductible)", "Emprunt temporaire dans son propre REER"], ["Limite", "8 000 $ par an, 40 000 $ à vie", "Jusqu'à 60 000 $"],
  ["Impôt au retrait", "Aucun si le retrait est admissible", "Aucun au moment du retrait"], ["À rembourser?", "Non", "Oui, sur 15 ans, dans un REER"],
  ["Effet sur les droits REER", "Transferts REER vers CELIAPP : pas déductibles, ils utilisent des droits CELIAPP", "Les remboursements sont des cotisations désignées, non déductibles"]])}
<h2 id="droits">Comment les droits de participation au CELIAPP s'accumulent</h2>
<p>Vos droits sont de 8 000 $ l'année où vous ouvrez votre premier CELIAPP. Les droits inutilisés se reportent, jusqu'à 8 000 $, donc le maximum en une année est de 16 000 $. Le plafond à vie est de 40 000 $. Les transferts d'un REER vers le CELIAPP utilisent des droits.</p>
<h2 id="retrait">Conditions du retrait admissible</h2>
<ul><li>Vous êtes un acheteur d'une première habitation : vous n'avez pas habité, comme résidence principale, une habitation que vous déteniez (seul ou avec un autre) pendant l'année en cours avant le retrait (sauf les 30 jours précédents) ni pendant les 4 années civiles précédentes.</li>
<li>Vous avez une entente écrite pour acheter ou construire une habitation admissible au Canada, avec une date d'acquisition ou d'achèvement avant le <b>1er octobre de l'année suivant le retrait</b>.</li>
<li>Vous n'avez pas acquis l'habitation plus de 30 jours avant le retrait.</li>
<li>Vous êtes résident du Canada du premier retrait jusqu'à l'acquisition.</li>
<li>Vous prévoyez l'occuper comme résidence principale dans l'année suivant l'achat ou la construction.</li>
<li>Vous remettez le formulaire RC725 à votre émetteur.</li></ul>
<p>Si une condition n'est pas remplie, le retrait est imposable et s'ajoute à votre revenu. Après un retrait admissible, fermez le CELIAPP au plus tard le 31 décembre de l'année suivante.</p>
<h2 id="rap">Le Régime d'accession à la propriété</h2>
<p>Un acheteur admissible peut retirer jusqu'à 60 000 $ de ses REER sans impôt, puis rembourser sur 15 ans. Chaque année, le minimum est le solde divisé par le nombre d'années restantes; sans remboursement, ce minimum est ajouté à votre revenu.</p>
{table(["Retrait RAP", "Remboursement annuel minimum (÷ 15)", "Période"], hbp_rows, "num")}
<div class="callout"><b>Vérifiez la date de départ.</b> La page de l'ARC accorde un allègement de trois ans seulement aux personnes dont le <em>premier</em> retrait RAP a eu lieu entre le 1er janvier 2022 et le 31 décembre 2025 (remboursement dès la cinquième année suivante). Pour les autres, le remboursement commence la deuxième année suivante. Confirmez votre propre date sur votre relevé RAP ou auprès de l'ARC.</div>
<h2 id="pieges">Pièges à éviter</h2>
<ul><li>Un excédent de CELIAPP coûte 1 % par mois et un retrait admissible ne l'efface pas.</li>
<li>Un transfert CELIAPP vers CELI est un retrait imposable plus une cotisation au CELI : seuls les transferts directs vers un REER, un FERR ou un autre CELIAPP sont sans impôt.</li>
<li>Recotiser un retrait admissible crée une nouvelle cotisation non déductible.</li></ul>
<p>Calculez vos droits avec <a href="/calcul-droits-celiapp/">le calculateur CELIAPP</a>. Version anglaise : <a href="/guides/fhsa-and-home-buyers-plan/">FHSA and the Home Buyers' Plan</a>.</p>
''',
 faq=[("Peut-on utiliser le CELIAPP et le RAP ensemble?", "Oui, pour la même habitation admissible, si vous remplissez les conditions à chaque retrait."),
      ("Combien peut-on retirer par le RAP?", "Jusqu'à 60 000 $ de vos REER, à rembourser sur 15 ans."),
      ("Faut-il rembourser un retrait admissible du CELIAPP?", "Non, contrairement au RAP."),
      ("Quel est le report maximal des droits du CELIAPP?", "Les droits inutilisés se reportent jusqu'à 8 000 $; le maximum annuel est donc de 16 000 $, et le plafond à vie de 40 000 $.")],
 sources=[("ARC : Retraits et transferts de vos CELIAPP", FRC + "retraits-transferts-vos-celiapp.html"), ("ARC : Définitions pour les CELIAPP", FRC + "definitions.html"),
          ("ARC : How to repay the amounts withdrawn under the HBP (en anglais)", "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/rrsps-related-plans/what-home-buyers-plan/repay-funds-withdrawn-rrsp-s-under-home-buyers-plan.html"),
          ("ARC : How to participate in the Home Buyers' Plan (en anglais)", "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/rrsps-related-plans/what-home-buyers-plan/participate-home-buyers-plan.html")],
 calcs=[("/calcul-droits-celiapp/", "Calcul des droits CELIAPP", "Droits de participation année par année"), ("/calcul-remboursement-reer/", "Calcul du remboursement REER", "Économie d'impôt")],
 rel=["date-limite-reer-et-plafond-de-cotisation"], cta="tracker",
 alt=[("en-CA", "guides/fhsa-and-home-buyers-plan/"), ("fr-CA", "guides-fr/celiapp-et-regime-d-accession-a-la-propriete/")])

# ============ FR 4. REER ============
need26 = rl["2026"] / 0.18
inc_rows = [[money(x, "fr"), money(min(x * 0.18, rl["2026"]), "fr")] for x in (30000, 60000, 90000, 120000, 150000, 187834)]
guide(lang="fr", slug="date-limite-reer-et-plafond-de-cotisation", group="Comptes enregistrés (CELI, REER, CELIAPP)",
 title="REER : plafond de déduction 2026 et 2027, date limite du 1er mars et cotisation excédentaire",
 desc="Votre plafond REER est 18 % du revenu gagné de l'année précédente, jusqu'à 33 810 $ pour 2026 (35 390 $ pour 2027). Date limite, marge de 2 000 $ et impôt de 1 % par mois.",
 h1="REER : plafond de cotisation, date limite et marge de 2 000 $",
 short="Comment les droits se calculent, plafonds 2026 et 2027, et quand l'excédent coûte de l'argent.",
 lede=f"Vos droits REER pour 2026 sont 18 % de votre revenu gagné de 2025, jusqu'à {money(rl['2026'], 'fr')}, plus les droits inutilisés des années passées, moins le facteur d'équivalence. Le plafond de 2027 est déjà fixé à {money(rl['2027'], 'fr')}. Et la pénalité ne s'applique qu'au-delà de 2 000 $ de dépassement.",
 body=f'''
<h2 id="calcul">Comment se calculent vos droits</h2>
<p>Votre plafond de déduction REER = <b>18 % du revenu gagné de l'année précédente (jusqu'au plafond en dollars)</b> + droits inutilisés reportés − facteur d'équivalence + facteur d'équivalence rectifié. Votre avis de cotisation indique le montant exact pour la prochaine année. Le revenu gagné de 2025 sert donc à 2026, et il comprend surtout le revenu d'emploi et le revenu net de travail autonome, pas les revenus de placement.</p>
<h2 id="plafonds">Les plafonds en dollars</h2>
{table(["Année d'imposition", "Plafond", "Revenu gagné nécessaire"],
 [["2024", money(rl["2024"], "fr"), money(rl["2024"] / 0.18, "fr")], ["2025", money(rl["2025"], "fr"), money(rl["2025"] / 0.18, "fr")], ["2026", money(rl["2026"], "fr"), money(need26, "fr")], ["2027", money(rl["2027"], "fr"), money(rl["2027"] / 0.18, "fr")]], "num")}
{table(["Revenu gagné en 2025", "Nouveaux droits pour 2026 (18 %, plafonnés)"], inc_rows, "num")}
<h2 id="date">La date limite</h2>
<p>Les cotisations des 60 premiers jours d'une année peuvent être déduites de l'année précédente. Pour 2026, la date limite est le <b>{LIM["rrsp_deadline_fr"]}</b>.</p>
<h2 id="exemple">Exemple : dans la marge et au-delà</h2>
<div class="ex"><b class="t">Le cas de Priya</b>Revenu gagné 2025 : 72 000 $. Droits inutilisés : 4 000 $. Droits 2026 : 4 000 $ + 18 % × 72 000 $ (12 960 $) = <b>16 960 $</b>.
<ul><li>Cotisation de 18 500 $ : dépassement de 1 540 $. La marge cumulative de 2 000 $ s'applique : <b>aucun impôt</b>, mais le dépassement n'est pas déductible.</li>
<li>Cotisation de 21 000 $ : dépassement de 4 040 $, dont 2 040 $ au-delà de la marge. Impôt de 1 % par mois : <b>20,40 $ par mois</b> (environ 245 $ par an), jusqu'au retrait de l'excédent.</li></ul></div>
<p>L'impôt s'inscrit sur le formulaire T1-OVP, dans les 90 jours suivant la fin de l'année (le 31 mars 2027 pour 2026). Les remboursements du RAP n'affectent pas votre plafond de déduction.</p>
<p>Voyez l'économie d'impôt avec <a href="/calcul-remboursement-reer/">le calculateur de remboursement REER</a>, après avoir vérifié que votre cotisation respecte vos droits.</p>
''',
 faq=[("Quel est le plafond REER pour 2026?", f"{money(rl['2026'], 'fr')}, atteint avec un revenu gagné de 2025 d'environ {money(need26, 'fr')}. Le plafond de 2027 est de {money(rl['2027'], 'fr')}."),
      ("Quelle est la date limite REER pour l'année 2026?", f"Le {LIM['rrsp_deadline_fr']}."),
      ("Peut-on dépasser son plafond REER sans pénalité?", "De 2 000 $ au total, sans impôt. Au-delà, l'impôt est de 1 % par mois. Le dépassement dans la marge n'est pas déductible."),
      ("Où trouver mon plafond REER?", "Sur votre dernier avis de cotisation et dans votre compte de l'ARC.")],
 sources=[("ARC : Effet de vos cotisations sur le maximum déductible au titre des REER", CF + "reer-regimes-connexes/cotiser-a-reer-a-rpac-a/effet-vos-cotisations-maximum-deductible-votre-reer-rpac.html"),
          ("ARC : Cotisations excédentaires", CF + "reer-regimes-connexes/cotiser-a-reer-a-rpac-a/consequences-cotisations-excedentaires-a-votre-reer-rpac.html"),
          ("ARC : Guide T4040, REER et autres régimes enregistrés pour la retraite", "https://www.canada.ca/fr/agence-revenu/services/formulaires-publications/publications/t4040/reer-autres-regimes-enregistres-retraite.html")],
 calcs=[("/calcul-remboursement-reer/", "Calcul du remboursement REER", "Impôt avec et sans déduction")],
 rel=["celiapp-et-regime-d-accession-a-la-propriete"], cta="tracker",
 alt=[("en-CA", "guides/rrsp-deduction-limit-explained/"), ("fr-CA", "guides-fr/date-limite-reer-et-plafond-de-cotisation/")])

# ============ FR 5. surcotisation CELI ============
cost = table(["Excédent le plus élevé du mois", "Corrigé en 1 mois", "2 mois", "4 mois", "7 mois", "12 mois"],
             [[money(x, "fr")] + [money(x * .01 * m, "fr") for m in (1, 2, 4, 7, 12)] for x in (500, 1000, 2000, 5000, 10000)], "num")
guide(lang="fr", slug="surcotisation-celi", group="Comptes enregistrés (CELI, REER, CELIAPP)",
 title="Surcotisation au CELI : comment l'impôt de 1 % par mois est calculé (règles de l'ARC)",
 desc="L'ARC impose 1 % par mois sur le montant excédentaire le plus élevé de chaque mois. Exemples de l'ARC, tableau du coût du retard, déclaration RC243 et marche à suivre.",
 h1="Surcotisation au CELI : comment fonctionne le 1 % par mois",
 short="L'impôt de 1 % par mois, les exemples de l'ARC, le coût du retard et la marche à suivre.",
 lede="Si vous dépassez vos droits de cotisation au CELI, l'ARC impose l'excédent à 1 % par mois, calculé sur le montant excédentaire le plus élevé de chaque mois. Comme chaque mois compte en entier, la date de correction compte plus qu'on ne le croit.",
 body=f'''
<h2 id="quoi">Ce qu'est une surcotisation</h2>
<p>Vos droits pour une année = limite annuelle + droits inutilisés + retraits de l'année précédente − cotisations déjà versées. Si vos cotisations dépassent ce total, l'excédent est un <b>montant excédentaire</b>. L'ARC cite trois causes courantes : mal calculer ses droits, recotiser un retrait la même année sans droits suffisants, et cotiser à plusieurs CELI sans suivre le total. Les droits vous appartiennent, pas à chaque compte.</p>
<h2 id="calcul">Comment l'impôt se calcule</h2>
<p>Impôt = 1 % du montant excédentaire <b>le plus élevé</b> de chaque mois où il reste dans le compte. Deux pièges : un seul jour dans un mois compte comme un mois complet; et c'est le plus haut montant du mois, pas la moyenne.</p>
<p>Exemples de l'ARC : surcotisation de 2 000 $ en juin, retirée en septembre : 20 $ par mois pour juin, juillet, août et septembre, soit 80 $; retirée plus tard en juin, 20 $. Surcotisation de 6 000 $ en août, 4 000 $ retirés à la mi-septembre, le reste en octobre : 60 $ pour août, 60 $ pour septembre et 20 $ pour octobre, soit 140 $.</p>
<div class="ex"><b class="t">Exemple : le redépôt la même année</b>Sam cotise la limite de 7 000 $ en janvier 2026, retire 5 000 $ en mars, puis les redépose en juin en croyant que le retrait a libéré des droits. Les retraits ne sont ajoutés à vos droits que le 1er janvier de l'année suivante. Sam a donc 5 000 $ d'excédent en juin :
<ul><li>corrigé en juin : 1 % × 5 000 $ = <b>50 $</b></li><li>corrigé en septembre (juin à septembre) : 4 × 50 $ = <b>200 $</b></li></ul></div>
<h2 id="cout">Le coût du retard</h2>
{cost}
<h2 id="corriger">Que faire</h2>
<ol><li><b>Retirez l'excédent</b> dès que possible; ne attendez pas l'avis de l'ARC. Vous n'avez pas à l'appeler : votre institution transmet la preuve de retrait.</li>
<li><b>Produisez une déclaration CELI (formulaire RC243)</b>, avec l'annexe A (RC243-SCH-A), et payez au plus tard le <b>30 juin de l'année suivante</b> (le 30 juin 2027 pour l'impôt de 2026).</li>
<li><b>Demandez une renonciation</b> si c'est une erreur raisonnable : l'ARC peut renoncer à l'impôt ou l'annuler selon les circonstances.</li></ol>
<p>L'ARC examine les cotisations une fois par an et avise souvent à la fin du printemps. Les émetteurs lui transmettent leurs données à la fin de février : l'excédent peut durer des mois avant que vous soyez informé, et le 1 % continue de courir. Une surcotisation intentionnelle peut être imposée au taux de 100 % applicable à un avantage.</p>
<h2 id="eviter">Comment l'éviter</h2>
<ul><li>Le montant affiché dans votre compte de l'ARC date de la dernière mise à jour annuelle du printemps : il ne tient pas compte de vos dépôts de l'année. Comparez avec les dossiers de votre institution.</li>
<li>Tenez un journal de chaque dépôt et retrait par date et institution.</li>
<li>Ne recotisez pas un retrait la même année si vous n'avez pas déjà les droits sans lui.</li></ul>
<p>Reconstituez vos droits avec <a href="/calcul-droits-celi/">le calculateur CELI</a>. Version anglaise : <a href="/guides/tfsa-over-contribution-penalty/">TFSA over-contribution penalty</a>.</p>
''',
 faq=[("L'impôt de 1 % porte-t-il sur tout le solde du CELI?", "Non, seulement sur le montant excédentaire le plus élevé de chaque mois."),
      ("Si je retire l'excédent le dernier jour du mois, dois-je payer ce mois?", "Oui, l'exemple de l'ARC confirme que le 1 % s'applique pour le mois de la surcotisation."),
      ("Quand dois-je payer l'impôt?", "Produisez le RC243 avec l'annexe A et payez au plus tard le 30 juin de l'année suivante."),
      ("L'ARC peut-elle annuler l'impôt?", "Elle peut y renoncer ou l'annuler s'il découle d'une erreur raisonnable.")],
 sources=[("ARC : Si vous cotisez en trop à un CELI", CF + "compte-epargne-libre-impot/cotiser/en-trop.html"), ("ARC : Si vous devez payer de l'impôt sur les montants excédentaires d'un CELI", CF + "compte-epargne-libre-impot/devoir-impot/montant-excedentaire.html"),
          ("ARC : Formulaire RC243, Déclaration CELI", "https://www.canada.ca/fr/agence-revenu/services/formulaires-publications/formulaires/rc243.html")],
 calcs=[("/calcul-droits-celi/", "Calcul des droits CELI", "Droits reconstitués depuis 2009"), ("/calcul-droits-celiapp/", "Calcul des droits CELIAPP", "Droits de participation")],
 rel=["celiapp-et-regime-d-accession-a-la-propriete"], cta="tracker",
 alt=[("en-CA", "guides/tfsa-over-contribution-penalty/"), ("fr-CA", "guides-fr/surcotisation-celi/")])
