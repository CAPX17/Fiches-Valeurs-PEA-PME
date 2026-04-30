# Audit de fiabilité — content/ALSEN.yaml

**Date d'audit** : 2026-05-01
**Méthode** : croisement de chaque claim factuelle avec une source primaire via web search.
**Auditeur** : Claude (Anthropic) — agent automatisé.

## Synthèse (en cours)

- Total claims auditées : ~25
- Confirmées : ~15
- À corriger : ~5
- Obsolètes : ~3
- Non vérifiables : ~2

## Détail par section

### Alertes

#### A1. Akouos / Eli Lilly vs Decibel / Regeneron
- **Claim YAML** : "concurrence (Regeneron via Akouos, Lilly via Decibel) dispose de moyens sans commune mesure"
- **Statut** : ERREUR FACTUELLE MAJEURE (inversion des deux acquisitions)
- **Source primaire** :
  - Lilly a acquis **Akouos** en octobre 2022 (~487 M$) → AK-OTOF (https://investor.lilly.com/news-releases/news-release-details/lilly-acquire-akouos-discover-and-develop-treatments-hearing)
  - Regeneron a acquis **Decibel Therapeutics** le 25/09/2023 → DB-OTO (https://investor.regeneron.com/news-releases/news-release-details/regeneron-completes-acquisition-decibel-therapeutics-adding)
- **Reformulation proposée** : "concurrence (Regeneron via Decibel, Lilly via Akouos) dispose de moyens sans commune mesure"

#### A2. Statut Decibel Therapeutics
- **Claim** : Decibel mentionnée comme entité "via Lilly"
- **Statut** : OBSOLETE — Decibel n'existe plus comme entité indépendante ; intégrée à Regeneron depuis sept. 2023.
- **Source** : https://investor.regeneron.com/news-releases/news-release-details/regeneron-completes-acquisition-decibel-therapeutics-adding (25/09/2023)

#### A3. Concurrence Regeneron OTOF (Otarmeni / DB-OTO) — 2026
- **Claim YAML** : Regeneron mentionné comme concurrent générique
- **Statut** : OBSOLETE / INCOMPLET — l'YAML omet l'événement le plus structurant 2026 :
  - Avril 2026 : FDA accelerated approval pour Otarmeni (lunsotogene parvec-cwha, ex-DB-OTO) — première thérapie génique au monde pour la perte auditive génétique (OTOF).
- **Source** : https://investor.regeneron.com/news-releases/news-release-details/otarmenitm-lunsotogene-parvec-cwha-approved-fda-first-and-only/
- **Reformulation proposée** : ajouter une alerte RISQUE concurrence dédiée :
  > "Regeneron a obtenu en avril 2026 la première AMM accélérée FDA d'une thérapie génique pour la surdité OTOF (Otarmeni, ex-DB-OTO). Sensorion (SENS-501) se retrouve concurrent direct, derrière sur la même indication ; le différenciant est l'Europe, le profil de sécurité et le tarif."

#### A4. Plateforme Pasteur — accord 27/05/2019, prolongé 31/12/2028
- **Claim** : accord-cadre signé 27/05/2019, prolongé jusqu'au 31/12/2028.
- **Statut** : CONFIRMÉ (voir D1 ci-dessous, source BusinessWire 05/01/2024)

#### A5. Sanofi 20 M€ dans tour 60 M€ janvier 2026 — détails à corriger
- **Claim YAML** : "Financement total 60 M€ bouclé en janvier 2026, dont 20 M€ apportés par Sanofi (~11 % de la capitalisation d'environ 190 M€)"
- **Statut** : CONFIRMÉ pour 60 M€ et 20 M€ ; **A CORRIGER pour la part Sanofi**
- **Source primaire** : BusinessWire 27/01/2026 (https://www.businesswire.com/news/home/20260127762736/en/) ; 214 285 714 actions nouvelles à 0,28 € (~71 % du capital pré-offre).
- **Détail à corriger** : Sanofi détient **13,9 %** post-offre (pas 11 %). Autres : Redmile 16,5 %, Artal 20,2 %, Sofinnova 12,6 %.
- **Reformulation proposée** : "Sanofi entre au capital à hauteur de ~13,9 % (20 M€ sur les 60 M€)."

#### A6. SENS-601 CTA Europe S1 2026 + IND USA fin 2026
- **Claim YAML** : "soumission CTA pour SENS-601 attendue au S1 2026, suivie d'une IND USA d'ici fin 2026. Interactions FDA + EMA actives depuis le T3 2025."
- **Statut** : CONFIRMÉ (CTA H1 2026 explicitement reconfirmé dans le PR FY2025 18/03/2026 et le PR 23/03/2026)
- **Source** : https://www.pharmiweb.com/press-release/2026-03-23/sensorion-reports-six-month-update-from-the-audiogene-phase-12-trial-of-sens-501-and-advances-gjb2
- **Note** : la formulation "interactions FDA + EMA depuis T3 2025" est vraisemblable mais n'est pas trouvée littéralement dans les communiqués primaires (les communiqués mentionnent des "regulatory interactions with the FDA and EMA"). À garder mais sourcer prudemment.

#### A7. SENS-501 Cohorte 2 — données 6 mois (23/03/2026)
- **Claim YAML** : "données 6 mois Cohorte 2 publiées le 23/03/2026 ; maintien chez 2 patients sur 3 à dose haute ; 0 EI grave sur 6 nourrissons/enfants ; relation dose-réponse Cohorte 1↔2"
- **Statut** : CONFIRMÉ
- **Source primaire** : Sensorion PR 23/03/2026, repris par PharmiWeb, Hearing Review, ClinicalTrialsArena, CGTlive (https://www.pharmiweb.com/press-release/2026-03-23/...).
- **Détail confirmé** : sustained improvements at M6 chez 2/3 patients dose haute Cohorte 2, dose-response signal entre cohortes, "no serious adverse events" sur les 6 patients traités.

#### A8. Trésorerie 47,5 M€ au 31/12/2025 — runway fin S1 2027
- **Claim YAML** : "Trésorerie 47,5 M€ au 31/12/2025 (FY2025 publié le 18/03/2026), runway jusqu'à fin S1 2027"
- **Statut** : CONFIRMÉ (montants et runway repris dans le PR FY2025 et confirmés post-financement)
- **Source** : https://live.euronext.com/en/products/equities/company-news/2026-03-18-sensorion-reports-full-year-2025-results-provides ; https://s27.q4cdn.com/232015521/files/doc_news/Sensorion-Reports-Full-Year-2025-Results-Provides-Corporate-Update-and-Announces-Release-of-Annual-Report-2026.pdf

#### A9. Stade précoce / 515 M actions post-levée
- **Claim YAML** : "~515 M actions post-levée janvier 2026"
- **Statut** : CONFIRMÉ (514,63 M actions post-offre selon Eulerpool ; 300,3 M pré-offre + 214,3 M nouvelles ≈ 514,6 M)
- **Source** : BusinessWire 27/01/2026 + Eulerpool / live.euronext.com.
- **Note** : la phrase "Phase 1/2" est correcte pour SENS-501 ; la concurrence est traitée en A1/A3.

### Pipeline

#### P1. SENS-501 (OTOF-GT) — Phase 1/2 — Cohorte 3 dose haute
- **Statut** : CONFIRMÉ. Le PR 23/03/2026 mentionne explicitement "considering a third dose level within the Audiogene trial framework". Indication "OTOF (~1 % des cas)" : à nuancer (voir E1 ci-dessous).

#### P2. SENS-601 (GJB2-GT) — Préclinique → CTA — CTA Europe S1 2026 / IND USA fin 2026
- **Statut** : CONFIRMÉ (voir A6).
- **Note** : poster ASGCT (Boston, mai 2026) annoncé dans la synthèse IA — confirmé.

#### P3. SENS-40 — SSNHL · Implant cochléaire · Cisplatine — "Phase 2b / 2a (×3)"
- **Claim YAML** : 3 indications Phase 2 simultanées
- **Statut** : VÉRIFICATION PARTIELLE — SENS-40 (seliforant) historiquement ciblait SSNHL Phase 2b ; les indications cochléaire et cisplatine relèvent de programmes plus précoces. Le PR FY2025 (mars 2026) ne met plus SENS-40 en première ligne (focus complet GT). Risque : information **obsolète ou exagérée**.
- **Source partielle** : sensorion.com/pipeline (n'a pas pu être confirmée individuellement dans cet audit). À reconfirmer auprès du R&D update SENS-40.
- **Recommandation** : reformuler "SENS-40 (seliforant) — historique Phase 2b SSNHL ; développement repriorisé après le pivot gène-thérapie. Statut programme à reconfirmer."

#### P4. Programme 3+ futur (avant 2028, accord Pasteur)
- **Statut** : CONFIRMÉ comme objectif explicite de l'accord-cadre Pasteur prolongé (BusinessWire 05/01/2024). Reste un objectif, pas un programme matérialisé.

### Perspectives — Court terme

#### CT1. AG mixte 11 mai 2026 (Paris, Square Louvois, 14h00 CET)
- **Statut** : CONFIRMÉ (BusinessWire 20/04/2026 cité en sources YAML ; date et lieu cohérents avec convocations habituelles Sensorion).
- **Note** : la convocation officielle BALO/AMF n'a pas été refetchée individuellement ; à confirmer auprès du document de convocation officiel si besoin.

#### CT2. CTA SENS-601 imminente
- **Statut** : CONFIRMÉ (S1 2026, voir A6).

#### CT3. Résistance technique 0,37 € (23,6 % Fib)
- **Statut** : NON AUDITABLE — claim technique issu de l'analyse PRT, hors périmètre de vérification factuelle externe.

#### CT4. Support court terme 0,30 €
- **Statut** : NON AUDITABLE (idem CT3).

### Perspectives — Moyen terme

#### MT1. SENS-601 IND USA d'ici fin 2026
- **Statut** : CONFIRMÉ (voir A6).

#### MT2. SENS-501 données Cohorte 3 — catalyseur clinique majeur
- **Statut** : CONFIRMÉ comme intention (PR 23/03/2026 mentionne "considering a third dose level"). Aucun calendrier précis publié — formulation correcte.

#### MT3. SENS-40 — résultats Phase 2b SSNHL
- **Statut** : INCERTAIN (voir P3). Le calendrier des "résultats Phase 2b SSNHL" sur la fenêtre 3-12 mois n'a pas été reconfirmé dans les communiqués 2025-2026. Risque d'obsolescence.

#### MT4. Trésorerie sécurisée fin S1 2027 — pas de dilution forcée
- **Statut** : CONFIRMÉ (A8).

#### MT5. 3e programme Pasteur avant 2028
- **Statut** : CONFIRMÉ comme objectif (P4).

### Perspectives — Long terme

#### LT1. Phase 2/3 SENS-501 si Cohorte 3 positive
- **Statut** : RAISONNABLE / non démentie — pas de calendrier officiel publié. Formulation conditionnelle correcte.

#### LT2. SENS-601 Phase 1 puis Phase 2 GJB2
- **Statut** : RAISONNABLE / non démentie.

#### LT3. Partenariat ou deal Big Pharma post-données pivots
- **Statut** : SPÉCULATIF — formulation conditionnelle, acceptable.

#### LT4. 3e programme Pasteur avant 2028
- **Statut** : CONFIRMÉ comme objectif (P4).

#### LT5. Consensus Boursorama 1,65 €
- **Claim YAML** : "Consensus à 1,65 € (Boursorama)"
- **Statut** : NON VÉRIFIABLE / À FLAGUER — Boursorama n'est pas une source primaire de consensus analystes (agrégateur tiers). Aucune publication d'un consensus formel d'analystes Sensorion à 1,65 € n'a été retrouvée auprès de sources primaires (Bloomberg, Refinitiv, Stockopedia, sensorion.com/IR).
- **Recommandation** : retirer le chiffre ou le reformuler "objectif de cours indicatif tiers (Boursorama, à confirmer)".

## Recommandations

### Modifications à appliquer (ordre de priorité)

1. **A1 — CRITIQUE** : corriger l'inversion Akouos/Decibel → "Regeneron via Decibel, Lilly via Akouos".
2. **A3 — CRITIQUE** : ajouter une alerte RISQUE explicite sur l'AMM FDA Otarmeni (Regeneron, avril 2026) — concurrent direct OTOF (SENS-501) sur le marché US.
3. **A5** : corriger "~11 % de la capitalisation" → "~13,9 % du capital post-offre" (Sanofi 20 M€ sur 60 M€).
4. **P3 / MT3** : revérifier ou requalifier le statut SENS-40 (Phase 2b SSNHL × 3 indications) — risque d'obsolescence après pivot GT.
5. **LT5** : retirer ou requalifier "consensus 1,65 € Boursorama" — non sourcé sur primaire.

### Claims à supprimer ou flaguer "non confirmé"

- "Cohort 3 à dose plus haute envisagée" : OK mais préciser "envisagée, calendrier non publié".
- "Interactions FDA + EMA depuis T3 2025" : laisser, mais sourcer FY2025 PR.
- "SENS-40 — 3 indications Phase 2 simultanées" : à requalifier ou supprimer.
- "Consensus 1,65 € Boursorama" : à supprimer ou requalifier.
- Mention "Decibel" comme entité indépendante via Lilly : remplacer par "Decibel (Regeneron)".

### Sources à ajouter dans la section sources du YAML

- BusinessWire 27/01/2026 : tour 60 M€ Sanofi 20 M€ (https://www.businesswire.com/news/home/20260127762736/en/)
- Sensorion PR 23/03/2026 — données 6M Audiogene SENS-501 (https://www.pharmiweb.com/press-release/2026-03-23/sensorion-reports-six-month-update-from-the-audiogene-phase-12-trial-of-sens-501-and-advances-gjb2)
- Regeneron Otarmeni FDA approval (avril 2026) (https://investor.regeneron.com/news-releases/news-release-details/otarmenitm-lunsotogene-parvec-cwha-approved-fda-first-and-only/)
- Lilly acquisition Akouos (octobre 2022) (https://investor.lilly.com/news-releases/news-release-details/lilly-acquire-akouos-discover-and-develop-treatments-hearing)
- Regeneron acquisition Decibel (septembre 2023) (https://investor.regeneron.com/news-releases/news-release-details/regeneron-completes-acquisition-decibel-therapeutics-adding)

## Note méthodologique

- L'audit a privilégié BusinessWire / Sensorion IR / Regeneron IR / Lilly IR comme sources primaires.
- Les claims techniques (résistance/support PRT) sont par nature non auditables via web search et ont été marqués comme tels.
- Le périmètre du programme **SENS-40** n'a pas pu être totalement reconfirmé via une source officielle Sensorion 2026 dans le temps imparti — la fiche IR du programme devrait être consultée.
- La part Sanofi à 13,9 % vs "~11 %" affiché dans le YAML peut s'expliquer si "11 %" se réfère à la capitalisation pré-deal ; la formulation actuelle reste néanmoins ambiguë et devrait être précisée.
- Aucune recherche complémentaire n'a été réalisée sur OMIM/GeneReviews pour la fréquence GJB2 30-40 % et OTOF ~1 % : ces ordres de grandeur sont cohérents avec la littérature classique sur les surdités congénitales non-syndromiques (GJB2/DFNB1 cause majoritaire, OTOF/DFNB9 minoritaire) — pas d'anomalie détectée mais sources non rebrindées dans cet audit.
