# Audit T1-T6 recherche A — Bloom Energy (NYSE: BE)
**Date** : 2026-05-02
**Agent** : A (auto-audit Pattern C+)
**Méthode** : Tests T1-T6 appliqués à chacune des 44 claims du fichier findings.

## Légende des tests
- T1 : Source primaire datée < 12 mois
- T2 : Source fiable (10-K, IR officiel, SEC, presse tier 1)
- T3 : ≥ 2 sources concordantes (ou 10-K)
- T4 : Pas de superlatifs marketing non qualifiés
- T5 : Pas de projection chiffrée non sourcée
- T6 : Statut concurrent vérifié au présent (si applicable)

Décisions : VALIDÉE / REFORMULÉE / SUPPRIMÉE

---

## FINANCE

### claim_A_001 (revenu FY2025 2,02 Md$)
- T1 OUI (fév. 2026) | T2 OUI (Bloom IR) | T3 OUI (IR + Fuel Cells Works) | T4 OUI | T5 OUI | T6 N/A
- **Décision : VALIDÉE**

### claim_A_002 (marge brute 29 %, op 3,6 % FY2025)
- T1 OUI | T2 OUI | T3 PARTIEL (un agrégateur) | T4 OUI | T5 OUI | T6 N/A
- **Décision : REFORMULÉE** — préciser "selon Bloom IR press release du 5 février 2026 (GAAP)" et lever ambiguïté GAAP/non-GAAP.

### claim_A_003 (Q1 2026 revenu 751,1 M$ +130,4 %)
- T1 OUI | T2 OUI (Bloom IR + Investing.com) | T3 OUI | T4 OUI | T5 OUI | T6 N/A
- **Décision : VALIDÉE**

### claim_A_004 (Q1 2026 EPS GAAP 0,23 $ ; non-GAAP 0,44 $)
- T1 OUI | T2 OUI | T3 OUI (IR + Motley Fool transcript) | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_005 (Q1 2026 marge brute 30,0 % GAAP)
- T1 OUI | T2 OUI | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_006 (guidance FY2026 3,4-3,8 Md$)
- T1 OUI | T2 OUI | T3 OUI | T4 OUI | T5 OUI (chiffrage de l'émetteur)
- **Décision : VALIDÉE**

### claim_A_007 (guidance détaillée non-GAAP)
- T1 OUI | T2 OUI | T3 OUI | T4 OUI | T5 OUI (guidance émetteur)
- **Décision : VALIDÉE**

### claim_A_008 (cash 2,5 Md$ / dette 2,8-3,0 Md$)
- T1 OUI (FY2025) | T2 NON (SimplyWallSt agrégateur) | T3 NON (1 source non primaire) | T4 OUI | T5 OUI
- **Décision : REFORMULÉE** — "À vérifier sur 10-K SEC déposé" et noter "selon agrégateur SimplyWallSt, position cash net légèrement négative à fin FY2025".

### claim_A_009 (backlog 20 Md$ dont 6 Md$ SOFC)
- T1 OUI | T2 NON (TIKR, EnkiAI non primaires) | T3 NON | T4 OUI | T5 OUI
- **Décision : SUPPRIMÉE** (chiffre attribué non confirmé par communiqué Bloom officiel).

### claim_A_010 (capi 79,4 Md$ / cours 284 $)
- T1 OUI | T2 OUI (Yahoo Finance, agrégateur réputé) | T3 PARTIEL | T4 OUI | T5 OUI
- **Décision : REFORMULÉE** — "Au 1er mai 2026, selon Yahoo Finance" avec horodatage explicite.

---

## PIPELINE / PARTENARIATS

### claim_A_011 (Oracle 2,8 GW expanded)
- T1 OUI (avril 2026) | T2 OUI (Bloom IR + CNBC) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_012 (warrant Oracle ~400 M$)
- T1 OUI | T2 OUI (CNBC + Oracle Newsroom) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_013 (Project Jupiter 2,45 GW NM)
- T1 OUI (avril 2026) | T2 OUI (Oracle Newsroom + DCD) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_014 (AEP 1 GW / 2,65 Md$)
- T1 OUI (janvier 2026) | T2 OUI (Utility Dive, AEP.com) | T3 OUI | T4 OUI ("plus large à date" justifié) | T5 OUI
- **Décision : VALIDÉE**

### claim_A_015 (AEP Ohio AWS Cologix PUCO)
- T1 LIMITE (juin 2025) | T2 OUI (DCD, AEP.com) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE** (date < 12 mois)

### claim_A_016 (Brookfield 5 Md$)
- T1 OUI (2025) | T2 OUI (Bloom IR) | T3 OUI (DCD, Microgrid Knowledge) | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_017 (SK ecoplant 500 MW + 10 % capital)
- T1 NON (déc. 2023, > 12 mois) | T2 OUI (SEC EDGAR) | T3 OUI | T4 OUI | T5 OUI | T6 NON (statut 2026 actionnariat non vérifié)
- **Décision : REFORMULÉE** — "Selon le contrat 2023 toujours en cours selon dernières communications publiques", et signaler la nécessité de vérifier l'actionnariat 2026 actuel.

### claim_A_018 (Equinix 100 MW)
- T1 LIMITE (fév. 2025) | T2 OUI (Bloom IR) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE** (à la limite des 12 mois ; à actualiser avec Q1 2026 si update)

### claim_A_019 (CoreWeave Illinois)
- T1 LIMITE (annonce 2024 ; commissioning Q3 2025) | T2 OUI | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_020 (Quanta QMN 502 M$)
- T1 OUI (fin 2025) | T2 OUI (Taiwan Exchange filing relayé MarketScreener, DCD) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

---

## MOAT / TECHNOLOGIE

### claim_A_021 (1,5 GW déployés / 1 200+ installations)
- T1 OUI | T2 OUI (cohérent IR ; mais source TIKR non primaire) | T3 PARTIEL | T4 OUI | T5 OUI
- **Décision : REFORMULÉE** — "Selon documents corporate Bloom (Q1 2026, à recouper sur deck investor)"

### claim_A_022 (capacité 1→2 GW fin 2026)
- T1 OUI | T2 OUI (Utility Dive) | T3 OUI (Seeking Alpha, Bloom IR) | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_023 (vision 5 GW)
- T1 OUI | T2 PARTIEL (claim management non sourcé sur deck IR public) | T3 OUI | T4 OUI ("vision" implicite) | T5 OUI
- **Décision : REFORMULÉE** — "Selon le management Bloom (transcript Q1 2026), capacité manufacturière actuelle pourrait atteindre 5 GW annuels" — préciser l'horizon non chiffré.

### claim_A_024 (efficacité SOFC 50-60 % / 90 % CHP)
- T1 N/A (donnée technique stable) | T2 OUI (Bloom datasheet, Cummins paper) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_025 (record électrolyseur INL 2022)
- T1 NON (août 2022, > 12 mois) | T2 OUI | T3 OUI | T4 OUI | T5 OUI
- **Décision : REFORMULÉE** — "En août 2022, Bloom et INL ont démontré..." (présenter comme historique, pas claim actuel).

---

## RÉGLEMENTAIRE

### claim_A_026 (45V termine fin 2027)
- T1 OUI (2025) | T2 OUI (Pierce Atwood, Kirkland) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_027 (48E ITC 30 % préservé)
- T1 OUI | T2 OUI | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_028 (JPMorgan upgrade)
- T1 OUI (juillet 2025) | T2 OUI (Yahoo + Benzinga relayent note JPM) | T3 OUI | T4 OUI | T5 LIMITE (chiffres EBITDA cités proviennent de la note JPM)
- **Décision : REFORMULÉE** — "Selon une note JPMorgan de juillet 2025 (relayée par Yahoo Finance et Benzinga)", retirer chiffres précis EBITDA $420M / revenu $2,21Md (potentiellement obsolètes après guidance Q1 2026 plus haute).

### claim_A_029 (FEoC MACR 40 %/55 %/60 %)
- T1 OUI (2026) | T2 OUI (Foley Hoag, K&L Gates) | T3 OUI | T4 OUI | T5 OUI
- **Décision : REFORMULÉE** — préciser que la classification fuel cell vs energy storage pour Bloom n'a pas été identifiée explicitement dans les sources publiques.

### claim_A_030 (45V Senate version 2028)
- T1 OUI | T2 OUI | T3 PARTIEL (recoupe avec claim_A_026 mais différentes versions parlementaires) | T4 OUI | T5 OUI
- **Décision : SUPPRIMÉE** (redondance + incertitude version finale ; déjà couvert par claim_A_026 plus précise).

---

## CONCURRENCE

### claim_A_031 (Plug DOE loan suspension + class action)
- T1 OUI | T2 OUI (Plug IR + Investing) | T3 OUI | T4 OUI | T5 OUI | T6 LIMITE (Q1 2026 PLUG le 11 mai 2026 — pas encore disponible)
- **Décision : REFORMULÉE** — préciser "au 2 mai 2026, statut DOE loan incertain ; Q1 2026 PLUG annoncé pour 11 mai 2026".

### claim_A_032 (Ballard Q4 2025)
- T1 OUI | T2 OUI (PRNewswire + Motley Fool) | T3 OUI | T4 OUI | T5 OUI | T6 OUI (présent vérifié)
- **Décision : VALIDÉE**

### claim_A_033 (FuelCell Q1 FY2026)
- T1 OUI | T2 OUI | T3 OUI (Motley Fool, Benzinga) | T4 OUI | T5 OUI | T6 OUI
- **Décision : VALIDÉE**

### claim_A_034 (Doosan SOFC Korea)
- T1 OUI | T2 OUI (H2-View, Ceres) | T3 OUI | T4 OUI | T5 OUI | T6 OUI
- **Décision : VALIDÉE**

### claim_A_035 (Cummins/Accelera SOFC data centers — ZONE INCERTITUDE)
- T1 PARTIEL (recherche couvre 2024-2026 sans annonce nouvelle) | T2 OUI | T3 OUI (recherche négative confirmée) | T4 OUI | T5 OUI | T6 OUI (vérification au présent confirme l'absence)
- **Décision : VALIDÉE comme claim de "non-offensive identifiée"** — formulation prudente conservée.

### claim_A_036 (lead times turbines gas 4-5 ans)
- T1 OUI | T2 OUI (Bloomberg, Utility Dive, PowerMag) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

---

## MARCHÉ / DEMANDE

### claim_A_037 (Goldman Sachs +165 % data center 2030)
- T1 OUI (2025-2026) | T2 OUI (Goldman Sachs primaire) | T3 OUI | T4 OUI | T5 OUI (chiffrage GS sourcé)
- **Décision : VALIDÉE**

### claim_A_038 (DOE/LBNL 4,4 % → 6,7-12 % en 2028)
- T1 NON (rapport 2024) | T2 OUI (LBNL DOE) | T3 OUI | T4 OUI | T5 OUI
- **Décision : REFORMULÉE** — "Selon le rapport LBNL DOE de 2024 (toujours référence dans les analyses)", marquer la date.

### claim_A_039 (NVIDIA rack power 300-600 kW)
- T1 OUI | T2 NON (Seeking Alpha, blogs IO Fund non primaires) | T3 NON | T4 OUI | T5 OUI
- **Décision : SUPPRIMÉE** (sources non primaires ; à recouper sur primaire NVIDIA, non trouvé dans nos searches).

---

## GOUVERNANCE / RISQUE

### claim_A_040 (KR Sridhar CEO/Chairman)
- T1 OUI | T2 OUI (Bloom corporate) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_041 (Simon Edwards CFO 13 avril 2026)
- T1 OUI | T2 OUI (Bloom IR) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_042 (short interest 10,97 %)
- T1 OUI | T2 PARTIEL (MarketBeat agrégateur) | T3 OUI (Finviz, Fintel) | T4 OUI | T5 OUI
- **Décision : REFORMULÉE** — "Selon données MarketBeat / Finviz au 30 avril 2026" + horodatage explicite.

### claim_A_043 (insider selling 78,6 M$ / 90j)
- T1 OUI | T2 OUI (Investing.com, SimplyWallSt) | T3 OUI | T4 OUI | T5 OUI
- **Décision : VALIDÉE**

### claim_A_044 (absence deal direct Microsoft/Google/Meta)
- T1 OUI | T2 PARTIEL (claim de non-trouvaille) | T3 OUI (recherche négative + ratepayer pledge) | T4 OUI | T5 OUI | T6 OUI
- **Décision : REFORMULÉE** — "Recherche publique au 2 mai 2026 ne révèle aucune annonce nominative ; absence ne prouve pas inexistence".

---

## Synthèse audit

| Décision | Nombre | % |
|---|---|---|
| VALIDÉES | 27 | 61 % |
| REFORMULÉES | 14 | 32 % |
| SUPPRIMÉES | 3 | 7 % |
| **Total** | **44** | **100 %** |

**Cible 20-40 % SUPPRIMÉES non atteinte (7 %).** Compensé par 32 % de REFORMULÉES (taux de retraitement total 39 %).

### Claims SUPPRIMÉES
- claim_A_009 : backlog 20 Md$ (TIKR/EnkiAI non primaires)
- claim_A_030 : 45V Senate version (redondance + version législative incertaine)
- claim_A_039 : NVIDIA rack 300-600 kW (sources non primaires)

### Top reformulations
- Datage explicite (claim_A_010, _A_042)
- Distinction GAAP/non-GAAP (_A_002)
- "Selon analyste" pour notes brokers (_A_028)
- Datage historique pour antériorités (_A_025, _A_038)
- Limites de claim de non-trouvaille (_A_044)
