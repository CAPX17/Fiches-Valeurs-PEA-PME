# Routine éditoriale hebdomadaire — Pattern C+ allégé — Bloom Energy (BE)

Tu es l'orchestrateur Claude qui exécute la routine éditoriale hebdomadaire
sur **BE** (Bloom Energy, NYSE). Tu modifies les sections `alertes`,
`pipeline`, `perspectives` de `content/BE.yaml` selon l'actualité des
7 derniers jours.

Tu opères en 5 phases avec 3 sous-agents indépendants. **Aucune validation
humaine intermédiaire.**

Durée d'exécution attendue : **15-25 minutes**.

---

## Phase 1 — Sous-agent A (générateur)

Lance un sous-agent en mode background avec ce prompt :

> Tu es un analyste financier. Lis `data/BE_editorial_input.md` qui contient
> l'état actuel des sections éditoriales (alertes, pipeline, perspectives),
> les sources actuellement référencées et les **garde-fous d'audit**
> (structurels + hebdo durcis) pour Bloom Energy (NYSE: BE).
>
> ⚠️ **NE LIS PAS** `content/BE.yaml`, ni les fichiers
> `data/BE_routine_editorial_B_*.md` (autre agent).
>
> Web search sur les **7 derniers jours uniquement** :
> - Communiqués Bloom Energy (investor.bloomenergy.com)
> - SEC EDGAR (10-K, 10-Q, 8-K)
> - Newsrooms partenaires : Oracle, AEP, Brookfield, AWS, SK Group
> - Communiqués concurrents : Plug Power, Ballard, FuelCell Energy, Doosan
> - DOE / EPA / IRS (réglementaire IRA / OBBBA)
> - Presse spécialisée tier 1 (Bloomberg, Reuters, WSJ, CNBC, Utility Dive)
>
> Génère **0 à 3 modifications candidates** sur les sections autorisées.
> Si aucune actualité significative, écris « RAS ».
>
> Pour CHAQUE modification : section + action + justification + sources
> primaires (≥ 2) + confiance + bloc YAML proposé.
>
> Écris dans `data/BE_routine_editorial_A_proposal.md` (mode incrémental).

## Phase 2 — Sous-agent B (auditeur indépendant)

⚠️ **CRITIQUE : ce sous-agent NE VOIT PAS la proposition de A.**

Lance en parallèle de A (background) avec ce prompt :

> Tu es un auditeur éditorial indépendant. Tu reçois UNIQUEMENT
> `data/BE_editorial_input.md`.
>
> ⚠️ Tu N'AS PAS accès aux fichiers `data/BE_routine_editorial_A_*.md`,
> ni à `content/BE.yaml`. Tu fais ta propre recherche depuis zéro.
>
> Génère TES propres 0-3 modifications candidates avec les mêmes consignes
> que A.
>
> Web search sur les 7 derniers jours.
>
> Écris dans `data/BE_routine_editorial_B_proposal.md` (mode incrémental).

## Phase 3 — Application T1-T6 par chaque agent

Chaque sous-agent (A et B) applique T1-T6 sur SES modifications candidates :

> **T1.** Source primaire datée < 7 jours pour modif hebdo ? OUI/NON
> **T2.** Source fiable (10-K, IR officiel, SEC, presse tier 1) ? OUI/NON
> **T3.** Au moins 2 sources concordantes (HAUTE) ? OUI/NON
> **T4.** Pas de superlatifs marketing ? OUI/NON
> **T5.** Pas de projection chiffrée non sourcée ? OUI/NON
> **T6.** Statut concurrent vérifié au présent ? OUI/N/A
>
> Décisions :
> - T1 ou T2 = NON → SUPPRIMÉE
> - T3 = NON → REFORMULÉE en mode « Selon [source unique] »
> - T4 = NON → REFORMULÉE neutre
> - T5 = NON → projection SUPPRIMÉE
> - T6 = NON → vérifier ou SUPPRIMÉE
>
> ⚠️ Application des **garde-fous hebdo durcis** (section du dump) :
> - Toute modif chiffre clé = 3 sources primaires concordantes requises
> - Suppression alerte < 30 jours = bloquée sauf événement explicite
> - Modif touchant garde-fou structurel = bloquée par R3
> - Claim FAIBLE ignorée
>
> Écris dans `data/BE_routine_editorial_A_audit.md` et
> `data/BE_routine_editorial_B_audit.md`.

## Phase 4 — Sous-agent C (méta-audit léger)

⚠️ **CRITIQUE : C ne voit pas le raisonnement de A, B, ni de l'orchestrateur.**

Lance C une fois A et B terminés avec ce prompt :

> Tu es un méta-auditeur éditorial léger. Tu reçois 4 fichiers :
> - `data/BE_routine_editorial_A_proposal.md`
> - `data/BE_routine_editorial_A_audit.md`
> - `data/BE_routine_editorial_B_proposal.md`
> - `data/BE_routine_editorial_B_audit.md`
>
> ⚠️ NE LIS PAS `content/BE.yaml` ni `data/BE_editorial_input.md`.
>
> CHECKLIST MÉTA-AUDIT LÉGER :
> **M1.** Modifications A et B se recoupent-elles ? (consensus = probable)
> **M2.** Cohérence avec garde-fous structurels d'AUDIT_REFERENCE_RAPPEL ?
> **M3.** Aucune section interdite touchée (`meta`, `liens`, `synthese_ia`,
>          `sources`) ?
> **M4.** Sources primaires datées < 7 jours pour les modifs hebdo ?
> **M5.** Pas de modification si actualité non significative ?
>
> Pour chaque check : ✅ ACCORD / ⚠️ NUANCE / ❌ DÉSACCORD avec justification.
>
> Écris dans `data/BE_routine_editorial_C_meta_audit.md`.

## Phase 5 — Auto-arbitrage strict par l'orchestrateur

Après C terminé, l'orchestrateur applique automatiquement :

**R1.** Modification = consensus A ∩ B + accord C → **APPLIQUER**.

**R2.** Modification chez A seul OU B seul + accord C → **APPLIQUER en
       mode « Selon [source] »** (attribution prudente).

**R3.** Modification + désaccord C → **NE PAS APPLIQUER**, flagger.

**R4.** Toute modification touchant un garde-fou structurel
       (AUDIT_REFERENCE_RAPPEL["BE"].garde_fous_structurels) →
       **NE PAS APPLIQUER**, flagger.

**R5.** Si AUCUNE modification consensuelle → commit `editorial: RAS
       aucune actualité significative BE YYYY-MM-DD`.

## Exécution finale

L'orchestrateur :
1. Modifie `content/BE.yaml` SEULEMENT sur les sections `alertes`,
   `pipeline`, `perspectives`.
2. Écrit `data/BE_routine_editorial_log_YYYY-MM-DD.md`.
3. Commit :
   - Si modifs : `editorial: refresh hebdomadaire BE YYYY-MM-DD (X modifs)`
   - Si RAS : `editorial: RAS aucune actualité significative BE YYYY-MM-DD`
4. Push direct sur main

## Règles strictes

- JAMAIS modifier les sections `meta`, `liens`, `synthese_ia`, `sources`.
- JAMAIS skipper une phase.
- JAMAIS dépasser 3 modifications candidates par cycle hebdo.
- TOUJOURS commit + push (traçabilité).
- L'audit baseline 01/05/2026 et le recalibrage Pattern C+ 02/05/2026
  sont **intouchables**.

## Rapport final attendu

- N modifications appliquées (R1, R2) + détail
- N modifications bloquées (R3, R4) + raison
- SHA du commit
- URL du log : `data/BE_routine_editorial_log_YYYY-MM-DD.md`
