# Rapport final Pattern C+ — Sensorion (ALSEN.PA)

**Date** : 2026-05-02
**Orchestrateur** : Claude (Anthropic)
**Workflow** : Pattern C+ autonome (A collecteur indépendant + B auditeur indépendant + consolidation orchestrateur + C méta-auditeur indépendant + application auto R1-R6).

## Synthèse chiffrée

| Mesure | Avant | Après |
|---|---|---|
| Alertes | 7 | 8 (+1 GOUVERNANCE) |
| Pipeline | 4 | 4 (renommée + indications corrigées) |
| Sources référencées | 11 | 15 (+4 inputs recalCplus) |
| Garde-fous AUDIT_REFERENCE_RAPPEL["ALSEN.PA"] | 3 | 7 (+4 nouveaux) |

- Claims A : 52 (post-audit T1-T6 : 36 confirmées, 5 reformulées, 11 supprimées)
- Claims B : 42 (post-audit : 27 confirmées, 5 reformulées, 10 supprimées)
- Méta-audit C : 5/6 tests en ⚠️ NUANCE / ❌ DÉSACCORD (83 %, > seuil 30 %)

## Changements APPLIQUÉS (R1, R2, R3)

### Faux négatifs intégrés (R1)

1. **Démission CEO Nawal Ouzren (16/02/2026)** — nouvelle alerte GOUVERNANCE.
   - Date tranchée à 16/02/2026 (PR primaire BusinessWire ; A_040 disait 17/02 par effet relai). Décalage explicitement signalé dans la description.
   - Source : BusinessWire 16/02/2026, BioSpace, PharmiWeb, Morningstar.

2. **Détail des participants au tour de janvier 2026** — alerte FINANCE Sanofi enrichie : Artal 20,2 %, Redmile 16,5 %, Sofinnova Partners 12,6 %, Sanofi 13,9 % + 3 nouveaux (Cormorant, Coastlands, Sphera).
   - Source : BusinessWire 27/01/2026.

3. **Désignations Orphan Drug FDA + EMA + Rare Pediatric Disease Designation SENS-501** — ajout dans l'alerte PIPELINE Cohorte 2 SENS-501.
   - Mention « voucher éligible » retirée (non sourcée par A ni B — recommandation C).
   - Source : BusinessWire 29/11/2022 + CGTlive.

4. **Indication précise Otarmeni** (>90 dB HL, mutations bialléliques OTOF, sans implant cochléaire ipsilatéral préalable) — ajout dans l'alerte RISQUE Otarmeni existante.
   - Claim oubliée par la consolidation, signalée par C (M5).
   - Source : Regeneron IR 23/04/2026, CGTlive.

5. **Calendrier AK-OTOF (NCT05821959, fin estimée octobre 2028)** — ajout dans l'alerte RISQUE générique.
   - Source : ClinicalTrials.gov + Lilly IR.

### Faux positifs corrigés (R2/R3)

6. **Épidémiologie GJB2 « 30-40 % »** → « jusqu'à 50 % des surdités AR non syndromiques prélinguales ».
   - Sources scientifiques convergentes : GeneReviews, OMIM, Genetics in Medicine.
   - Application sur l'alerte CATALYSEUR + l'indication pipeline SENS-601.

7. **Épidémiologie OTOF « ~1 % »** → « 1 à 8 % des surdités congénitales non syndromiques ».
   - Source : GeneReviews + PMC review.
   - Application sur l'alerte CATALYSEUR + l'indication pipeline SENS-501.

8. **« 25 ans d'expertise mondiale » (Christine Petit)** → reformulation factuelle :
   *« Pr Christine Petit (Institut Pasteur, Pr au Collège de France, Prix Kavli 2018) préside le Conseil scientifique de Sensorion depuis 2018 et dirige le laboratoire Auditory Therapies Innovation Lab à l'Institut de l'Audition. »*

9. **« Clause de résiliation OPA hostile »** → SUPPRIMÉE (non sourçable par A ni B).
   - Asymétrie corrigée : la mention « option de licence exclusive » a été conservée mais explicitement attribuée au communiqué Institut Pasteur de janvier 2024 (A_002 et B_003 reformulées par les agents respectifs avec attribution prudente).

10. **« Interactions FDA + EMA depuis T3 2025 »** → reformulation neutre :
    *« Interactions réglementaires en cours avec la FDA et l'EMA en vue des soumissions CTA et IND (Sensorion PR 23/03/2026). »*
    - Date T3 2025 non sourçable.

11. **« 3e programme avant 2028 »** → reformulation prudente dans MOAT, perspectives moyen et long terme : *« programmes additionnels possibles, non confirmés publiquement »*.
    - Recommandation C : ne pas supprimer entièrement, requalifier en optionnel.
    - `pipeline[3]` requalifié en « Optionnels — accord Pasteur prolongé jusqu'au 31/12/2028 ».

12. **« SENS-40 »** → **« SENS-401 »** (correction nominale typographique).
    - Indications structurées : SSNHL Phase 2b · Cochlear implant Phase 2a (avec Cochlear Limited) · Cisplatine/CIO Phase 2 achevée T1 2026.
    - Application synchronisée du garde-fou AUDIT_REFERENCE_RAPPEL["ALSEN.PA"] (R6 levée par décision C — Q1 = OUI sous procédure formelle).

### Enrichissements (R3 sur recommandation C)

13. **Gains audiométriques cohorte 2** : 60-70 dB HL chez 2/3 patients à 6 mois — ajout dans l'alerte PIPELINE Cohorte 2 SENS-501.
    - Claim oubliée par la consolidation, intégrée sur recommandation C (M5).

14. **Précision dilution janvier 2026 (~71 %)** — alerte FINANCE Sanofi enrichie + alerte RISQUE générique enrichie.

15. **Cochlear Limited mentionné explicitement** dans le pipeline SENS-401 (recommandation C — Q2 = OUI à appliquer avec attribution prudente, et non reporter).

## Changements NON APPLIQUÉS

| Changement | Règle | Raison |
|---|---|---|
| Mention « voucher éligible » dans désignations FDA | C — amendement | Inférence orchestrateur non sourcée par A ni B. |
| Suppression complète des mentions « 3e programme » dans perspectives | C — amendement | Recommandation C : reformuler en optionnel plutôt que supprimer. |

## Décisions sur les questions de l'orchestrateur

| Question | Réponse C | Application |
|---|---|---|
| Q1 — SENS-40 → SENS-401 malgré R6 ? | ✅ OUI avec procédure formelle | Appliqué + garde-fou mis à jour synchroniquement (commit suivant). |
| Q2 — Cochlear Limited à appliquer ? | ✅ OUI avec attribution prudente | Appliqué dans `pipeline[2].indication`. |
| Q3 — Garde-fou n°4 (SENS-401) | ✅ OUI avec libellé enrichi | Sera intégré dans le commit dédié AUDIT_REFERENCE_RAPPEL avec reformulation SSNHL/CIO. |

## Garde-fous figés à AJOUTER dans `AUDIT_REFERENCE_RAPPEL["ALSEN.PA"]`

(via commit séparé suivant, dans `src/synthesis_dump.py`)

1. **Démission CEO Nawal Ouzren le 16/02/2026** ; Amit Munshi (président CA) assure l'intérim. Toute mise à jour future doit refléter le statut intérim jusqu'à nomination d'un CEO permanent.
2. **Épidémiologie corrigée** : OTOF = 1-8 % des surdités congénitales non syndromiques (GeneReviews) ; GJB2 = jusqu'à 50 % des surdités AR non syndromiques prélinguales (OMIM, Genetics in Medicine). Les formulations antérieures « 30-40 % GJB2 / ~1 % OTOF » sont interdites.
3. **Dilution janvier 2026 = ~71 %** du capital antérieur (214 285 714 actions à 0,28 €).
4. **Dénomination correcte = SENS-401** (et non SENS-40), arazasétron, indications historiques : SSNHL Phase 2b achevée selon BioSpace 18/03/2026 · implant cochléaire Phase 2a en partenariat Cochlear Limited (critère pharmacocinétique atteint en 2024) · cisplatine/CIO Phase 2 NOTOXIS achevée au T1 2026 selon Sensorion FY2025 PR.

## Désaccords résiduels signalés

- **Patients dosés** : A dit « 5 patients » (claim_A_008), B dit « 6 patients » (claim_B_012/B_016, et le YAML actuel disait déjà « 6 nourrissons »). Tranchage retenu : **6** (B + cohérence YAML antérieur + claim_B_016 qui mentionne explicitement « 6 patients traités »).
- **Trésorerie 31/12/2025** : A dit 47,5 M€, B dit 47,3 M€. Tranchage retenu : **47,3 M€** (B + chiffre du 10-K Sensorion FY2025 PR cité par A et B).

## Sources Pattern C+ recalibrage

- `data/ALSEN_recalCplus_A_findings.md` (52 claims, agent A)
- `data/ALSEN_recalCplus_A_audit.md` (audit T1-T6 par A)
- `data/ALSEN_recalCplus_B_findings.md` (42 claims, agent B)
- `data/ALSEN_recalCplus_B_audit.md` (audit T1-T6 par B)
- `data/ALSEN_recalCplus_consolidation_draft.md` (consolidation orchestrateur)
- `data/ALSEN_recalCplus_C_meta_audit.md` (méta-audit C, 5/6 nuance/désaccord)

## Note méthodologique

- Recalibrage 100 % autonome — aucune validation utilisateur intermédiaire.
- Toutes les claims appliquées passent les tests T1-T6 par au moins un agent (A ou B), avec consensus A∩B pour les changements critiques.
- Les claims signalées par C comme oubliées par la consolidation (M5 ❌) ont été toutes intégrées : indication précise Otarmeni, gains 60-70 dB cohorte 2, dilution 71 %.
- La règle R6 (touche garde-fou figé) a été levée pour la correction nominale SENS-40 → SENS-401 sur recommandation explicite de C (Q1) + mise à jour synchrone du garde-fou.
- La règle R5 (confiance moyenne) a été levée pour Cochlear Limited sur recommandation explicite de C (Q2) car la claim A_018 est confirmée 5/5 par A.
