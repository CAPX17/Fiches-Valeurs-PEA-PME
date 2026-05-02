# Consolidation Pattern C+ — Sensorion (ALSEN.PA) — 2026-05-02

**Orchestrateur** : Claude (Anthropic) — synthèse des livrables A et B.
**Inputs** : `data/ALSEN_recalCplus_A_findings.md` (52 claims, agent A), `data/ALSEN_recalCplus_A_audit.md` (audit T1-T6 par A), `data/ALSEN_recalCplus_B_findings.md` (42 claims, agent B), `data/ALSEN_recalCplus_B_audit.md` (audit T1-T6 par B).
**État YAML de référence** : `content/ALSEN.yaml` au commit `bb28b55` (avant ce recalibrage).

## Synthèse chiffrée

| Mesure | Valeur |
|---|---|
| Claims YAML actuel (alertes/pipeline/perspectives factuels) | ~25 |
| Claims A post-audit (confirmées + reformulées) | 41 |
| Claims B post-audit (confirmées + reformulées) | 32 |
| **Consensus A∩B** (sujet présent et concordant chez les deux) | **24** |
| Divergence A\B (couvert par A, pas par B) | ~17 |
| Divergence B\A (couvert par B, pas par A) | ~8 |
| **Faux négatifs YAML** (consensus A∩B mais absent YAML) | **5** |
| **Faux positifs YAML** (présent YAML mais absent A et B, ou contredit) | **5** |

## Liste exhaustive des changements proposés

### CHANGEMENT 1 — AJOUT alerte GOUVERNANCE : démission CEO

**Type** : faux négatif YAML (consensus A∩B — A_040/A_041/A_042 ; B_039/B_040)
**Confiance** : HAUTE des deux côtés
**Décision proposée** : APPLIQUER (R1)

**Bloc YAML proposé** (à insérer dans `alertes:` après les RISQUE existants) :

```yaml
  - categorie: RISQUE
    titre: Transition exécutive — démission CEO Nawal Ouzren (16/02/2026)
    description: |
      Le 16 février 2026, Sensorion a annoncé le départ de Nawal Ouzren
      de ses fonctions de directrice générale et d'administratrice pour
      raisons personnelles. Amit Munshi, président du conseil
      d'administration, assure l'intérim ; le conseil a engagé une
      recherche d'un CEO permanent.

      Risque exécutif jusqu'à nomination du successeur. Ouzren reste
      consultante temporaire pour assurer la transition (source
      BusinessWire 16/02/2026).

      Sources : BusinessWire 16/02/2026, BioSpace, PharmiWeb, Morningstar.
```

### CHANGEMENT 2 — CORRECTION épidémiologie GJB2 (30-40 % → ~50 %)

**Type** : faux positif YAML (chiffre du YAML « 30 à 40 % » contredit par les deux agents)
**Sources A** : claim_A_045 (« GJB2 ≈ 50 % surdités AR non syndromiques », GeneReviews + Sensorion produit)
**Sources B** : claim_B_033 (« GJB2 jusqu'à 50 % surdités neurosensorielles AR non syndromiques prélinguales », Genetics in Medicine + OMIM)
**Confiance** : HAUTE (A et B citent références primaires concordantes : OMIM, GeneReviews, Genetics in Medicine)
**Décision proposée** : APPLIQUER (R3)

**Cible** : alerte CATALYSEUR « SENS-601 — CTA Europe S1 2026 imminent ».
**Avant** : *« Le gène GJB2 (connexine 26) est responsable de 30 à 40 % de l'ensemble des surdités génétiques dans le monde, soit un marché adressable 30 à 40 fois plus large que celui d'OTOF (SENS-501, ~1 % des cas). »*
**Après** : *« Le gène GJB2 (connexine 26) est la cause génétique unique la plus fréquente de surdité congénitale ; selon GeneReviews/OMIM, GJB2 explique jusqu'à 50 % des surdités neurosensorielles non syndromiques autosomiques récessives prélinguales. SENS-601 adresse ainsi un marché bien plus large que celui d'OTOF (SENS-501, qui concerne 1 à 8 % des surdités congénitales non syndromiques selon GeneReviews). »*

### CHANGEMENT 3 — CORRECTION épidémiologie OTOF (~1 % → 1-8 %)

**Type** : faux positif YAML (chiffre « ~1 % » trop étroit)
**Sources A** : claim_A_044 (« OTOF = 1-8 % des surdités congénitales non syndromiques », GeneReviews + PMC review)
**Sources B** : claim_B_031 (« OTOF 1-8 % des surdités congénitales non syndromiques », GeneReviews + CGTlive)
**Confiance** : HAUTE
**Décision proposée** : APPLIQUER (R3) — couvert dans le changement 2 ci-dessus pour l'alerte CATALYSEUR.

**Cibles supplémentaires** :
- `pipeline[0].indication: Surdité congénitale OTOF (~1 % des cas)` → `Surdité congénitale OTOF (1-8 % des surdités congénitales non syndromiques)`
- `pipeline[1].indication: Surdité congénitale GJB2 (30-40 % des cas)` → `Surdité congénitale GJB2 (jusqu'à 50 % des surdités AR non syndromiques prélinguales)`

### CHANGEMENT 4 — AJOUT précision dilution janvier 2026 (71 %)

**Type** : faux négatif YAML partiel (le YAML mentionne « ~515 M actions post-levée » mais pas le pourcentage de dilution)
**Sources A** : claim_A_023 (« émission représente ~71 % du capital antérieur », BusinessWire 27/01/2026)
**Sources B** : claim_B_021 (« 214 285 714 actions, ~71 % du capital social existant », Investing.com + BusinessWire)
**Confiance** : HAUTE (A∩B + source primaire BusinessWire)
**Décision proposée** : APPLIQUER (R1)

**Cible** : alerte FINANCE « Sanofi 20 M€ dans le tour de 60 M€ » et alerte RISQUE « Stade précoce ».

**Ajout dans l'alerte FINANCE Sanofi** : compléter avec « L'émission de 214 285 714 actions nouvelles à 0,28 € représente ~71 % du capital antérieur, induisant une dilution majeure pour les actionnaires non participants (BusinessWire 27/01/2026). »

### CHANGEMENT 5 — AJOUT alerte CATALYSEUR : désignations FDA SENS-501

**Type** : faux négatif YAML (consensus A∩B, absent YAML)
**Sources A** : claim_A_037 (Orphan Drug + Rare Pediatric Disease, T4 2022, BusinessWire + BiopharmaReporter)
**Sources B** : claim_B_036 (Orphan Drug + Rare Pediatric Disease, novembre 2022, BusinessWire + CGTlive)
**Confiance** : HAUTE — fait structurel acquis
**Décision proposée** : APPLIQUER (R1) sous forme d'enrichissement de l'alerte SENS-501 existante (PIPELINE / Cohorte 2)

**Ajout dans l'alerte PIPELINE Cohorte 2 SENS-501** (en fin de description) :
*« SENS-501 dispose des désignations Orphan Drug FDA et Rare Pediatric Disease (FDA, T4 2022) ainsi que d'une désignation Orphan Drug EMA, conférant des avantages réglementaires (exclusivité de marché potentielle) et un voucher éligible en cas d'AMM. »*

### CHANGEMENT 6 — REFORMULATION garde-fou Pasteur (« 25 ans d'expertise »)

**Type** : faux positif YAML potentiel (formulation marketing non sourcée)
**Sources** : A_004 et B_002 mentionnent Christine Petit (Institut Pasteur, Collège de France, Prix Kavli 2018) sans le « 25 ans d'expertise mondiale ».
**Confiance** : HAUTE pour la reformulation (sources primaires Institut Pasteur)
**Décision proposée** : APPLIQUER (R3) — passage en formulation neutre sourcée

**Cible** : alerte MOAT « Plateforme Institut Pasteur ».
**Avant** : *« Pr Christine Petit, 25 ans d'expertise mondiale en génétique auditive »*
**Après** : *« Pr Christine Petit (Institut Pasteur, Pr au Collège de France, Prix Kavli 2018) préside le Conseil scientifique de Sensorion depuis 2018 et dirige le laboratoire Auditory Therapies Innovation Lab à l'Institut de l'Audition »*

### CHANGEMENT 7 — REFORMULATION garde-fou Pasteur (« clause de résiliation OPA »)

**Type** : faux positif YAML probable (claim non sourcée par A ni B)
**Sources A** : aucune mention spécifique d'une clause de résiliation
**Sources B** : aucune mention spécifique d'une clause de résiliation
**Confiance** : NON CONFIRMABLE — A et B n'ont pas trouvé de source primaire pour cette clause
**Décision proposée** : APPLIQUER (R2) — suppression de la mention non sourcée

**Cible** : alerte MOAT « Plateforme Institut Pasteur ».
**Avant** : *« Clause de résiliation en cas de changement de contrôle non agréé : protection contre OPA hostile. »*
**Après** : (suppression complète de la phrase) — la mention sur l'option de licence exclusive reste, sourcée par le communiqué Institut Pasteur de janvier 2024.

### CHANGEMENT 8 — REFORMULATION « interactions FDA + EMA depuis T3 2025 »

**Type** : faux positif YAML (date T3 2025 non sourcée)
**Sources A** : aucune source ne confirme T3 2025 spécifiquement
**Sources B** : aucune source ne confirme T3 2025 spécifiquement
**Confiance** : NON CONFIRMABLE
**Décision proposée** : APPLIQUER (R2) — suppression du « depuis T3 2025 »

**Cible** : alerte CATALYSEUR « SENS-601 ».
**Avant** : *« Interactions réglementaires FDA + EMA actives depuis le T3 2025. »*
**Après** : *« Interactions réglementaires en cours avec la FDA et l'EMA en vue des soumissions CTA et IND (Sensorion PR 23/03/2026). »*

### CHANGEMENT 9 — REFORMULATION « 3e programme avant 2028 »

**Type** : faux positif YAML (consensus A∩B insuffisant)
**Sources A** : claim_A_001/A_002/A_003 décrivent l'option de licence exclusive et les **deux** programmes générés (SENS-501, SENS-601), sans confirmer de 3e programme
**Sources B** : claim_B_004 dit explicitement « **Deux** programmes de thérapie génique sont conduits sous l'accord Pasteur »
**Confiance** : NON CONFIRMABLE pour le 3e programme
**Décision proposée** : APPLIQUER (R2) — suppression ou prudente reformulation des mentions « 3ᵉ programme »

**Cibles** :
- alerte MOAT : *« Deux programmes déjà générés (SENS-501, SENS-601), un troisième explicitement attendu avant 2028 »* → *« Deux programmes générés à ce stade (SENS-501, SENS-601). L'accord-cadre prolongé jusqu'à fin 2028 laisse la possibilité de programmes additionnels, non confirmés publiquement à ce jour. »*
- `pipeline[3]` : « Programme 3+ (futur) — Émergence avant 2028 (accord Pasteur) » → SUPPRIMER ou requalifier en « Optionnels — accord Pasteur prolongé jusqu'au 31/12/2028 »
- `perspectives.moyen_terme.points` : « 3ᵉ programme issu de la plateforme Pasteur possible avant 2028 » → SUPPRIMER (non sourcé)
- `perspectives.long_terme.points` : « Plateforme Pasteur — émergence d'un 3ᵉ programme avant 2028 » → SUPPRIMER

### CHANGEMENT 10 — CORRECTION nominale « SENS-40 » → « SENS-401 »

**Type** : faux positif YAML (typo)
**Sources A** : claim_A_017 « SENS-401 (arazasétron) », confirmée. claim_A_018 idem.
**Sources B** : claim_B_017 « SENS-401 (arazasetron) » — 3 indications.
**Confiance** : HAUTE — consensus A∩B sur le nom correct
**Décision proposée** : **R6 — NE PAS APPLIQUER automatiquement** (touche le garde-fou figé `AUDIT_REFERENCE_RAPPEL["ALSEN.PA"]` qui mentionne « SENS-40 »). À flaguer pour décision méta-audit.

### CHANGEMENT 11 — ENRICHISSEMENT alerte SENS-501 (étude implant cochléaire SENS-401 / Cochlear Limited)

**Type** : information complémentaire (consensus partiel)
**Sources A** : claim_A_018 (Phase 2a SENS-401 implant cochléaire avec Cochlear Limited, critère principal atteint en 2024)
**Sources B** : claim_B_017 (mentionne implant cochléaire dans 3 indications SENS-401)
**Confiance** : MOYENNE — A est précis avec Cochlear Limited et critère principal, B le mentionne sans détail
**Décision proposée** : NE PAS APPLIQUER en confiance moyenne (R5) — laisser à un audit ultérieur

### CHANGEMENT 12 — REFORMULATION concurrence Big Pharma

**Type** : enrichissement (consensus A∩B sur AK-OTOF)
**Sources A** : claim_A_032 (reformulée — Lilly AK-OTOF Phase 1/2 NCT05821959, données janv 2024, pas d'update 2025-2026 récent)
**Sources B** : claim_B_029 (reformulée — AK-OTOF en cours, NCT05821959, fin estimée octobre 2028 selon clinicaltrials.gov)
**Confiance** : MOYENNE/HAUTE — fact NCT05821959 + fin 2028 confirmé
**Décision proposée** : APPLIQUER (R3) — préciser AK-OTOF avec calendrier ClinicalTrials.gov

**Cible** : alerte RISQUE « Stade précoce ».
**Ajout** : *« AK-OTOF (Lilly via Akouos) est en essai Phase 1/2 NCT05821959, fin estimée octobre 2028 (clinicaltrials.gov) ; aucun update clinique majeur 2025-2026 n'a été publiquement diffusé. »*

## Garde-fous figés à AJOUTER dans `AUDIT_REFERENCE_RAPPEL["ALSEN.PA"]`

(à proposer au méta-auditeur C, application R1 si validé)

1. **Démission CEO Nawal Ouzren le 16/02/2026** ; Amit Munshi (président CA) assure l'intérim. Toute mise à jour future doit refléter le statut intérim jusqu'à nomination d'un CEO permanent.
2. **Épidémiologie corrigée** : OTOF = 1-8 % des surdités congénitales non syndromiques (GeneReviews) ; GJB2 = jusqu'à 50 % des surdités AR non syndromiques prélinguales (OMIM, Genetics in Medicine). Toute formulation antérieure « 30-40 % GJB2 / ~1 % OTOF » est interdite.
3. **Dilution janvier 2026 = ~71 %** du capital antérieur (214 285 714 actions à 0,28 €).
4. **Dénomination correcte du programme petite molécule = SENS-401** (et non SENS-40), arazasétron, indications SSNHL Phase 2b achevée + implant cochléaire Phase 2a + cisplatine Phase 2 (CIO achevée T1 2026 selon Sensorion FY2025 PR).

## Désaccords / claims à examiner par le méta-auditeur C

- Changement 10 (SENS-40 → SENS-401) : touche un garde-fou figé. R6 dit de ne pas appliquer ; mais c'est une simple correction nominale (typo) avec consensus A∩B fort. **Question pour C** : peut-on l'appliquer en mettant à jour parallèlement le garde-fou ?
- Changement 11 (Cochlear Limited) : confiance moyenne, R5 dit de ne pas appliquer. **Question pour C** : suffisamment important pour un examen complémentaire ?
- Garde-fou n°4 ci-dessus dépend du changement 10.
