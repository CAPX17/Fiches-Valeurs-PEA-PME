# Routine éditoriale hebdomadaire — Pattern C+ allégé — Sensorion (ALSEN.PA)

Tu es l'orchestrateur Claude qui exécute la routine éditoriale hebdomadaire
sur **ALSEN.PA**. Tu modifies les sections `alertes`, `pipeline`, `perspectives`
de `content/ALSEN.yaml` selon l'actualité des 7 derniers jours.

Tu opères en 5 phases avec 3 sous-agents indépendants. **Aucune validation
humaine intermédiaire.**

Durée d'exécution attendue : **15-25 minutes**.

---

## Phase 1 — Sous-agent A (générateur)

Lance un sous-agent en mode background avec ce prompt :

> Tu es un analyste financier. Lis `data/ALSEN_editorial_input.md` qui
> contient l'état actuel des sections éditoriales (alertes, pipeline,
> perspectives), les sources actuellement référencées et les **garde-fous
> d'audit** (structurels + hebdo durcis) pour Sensorion (ALSEN.PA).
>
> ⚠️ **NE LIS PAS** `content/ALSEN.yaml`, ni les fichiers
> `data/ALSEN_routine_editorial_B_*.md` (autre agent).
>
> Web search sur les **7 derniers jours uniquement** :
> - Communiqués Sensorion (sensorion.com/investors)
> - FDA / EMA / ANSM / publications scientifiques
> - Communiqués concurrents (Lilly via Akouos, Regeneron via Decibel/Otarmeni)
> - Mouvements significatifs (OPA, partenariat, levée, AG, gouvernance)
>
> Génère **0 à 3 modifications candidates** sur les sections autorisées
> (`alertes`, `pipeline`, `perspectives`). Si aucune actualité significative,
> écris explicitement « RAS » dans ton fichier.
>
> Pour CHAQUE modification candidate :
> - Section ciblée (alertes / pipeline / perspectives.X)
> - Action (AJOUTER / MODIFIER / SUPPRIMER)
> - Justification (1-3 lignes, basée sur l'actualité 7 jours)
> - Sources primaires (URL 1 + date, URL 2 + date — minimum 2)
> - Confiance (HAUTE / MOYENNE / FAIBLE)
> - Bloc YAML proposé (texte exact à insérer ou remplacer)
>
> Écris dans `data/ALSEN_routine_editorial_A_proposal.md` (mode incrémental :
> squelette d'abord, puis enrichis).

## Phase 2 — Sous-agent B (auditeur indépendant)

⚠️ **CRITIQUE : ce sous-agent NE VOIT PAS la proposition de A.**

Lance en parallèle de A (background) avec ce prompt :

> Tu es un auditeur éditorial indépendant. Tu reçois UNIQUEMENT
> `data/ALSEN_editorial_input.md`.
>
> ⚠️ Tu N'AS PAS accès aux fichiers `data/ALSEN_routine_editorial_A_*.md`,
> ni à `content/ALSEN.yaml`. Tu fais ta propre recherche depuis zéro.
>
> Génère TES propres 0-3 modifications candidates avec les mêmes consignes
> que A : sections autorisées uniquement, sources primaires datées 7 jours,
> bloc YAML exact.
>
> Web search sur les 7 derniers jours (mêmes sources prioritaires que A).
>
> Écris dans `data/ALSEN_routine_editorial_B_proposal.md` (mode incrémental).

## Phase 3 — Application T1-T6 par chaque agent

Chaque sous-agent (A et B) applique T1-T6 sur SES modifications candidates :

> **T1.** Source primaire datée < 7 jours pour modif hebdo ? OUI/NON
> **T2.** Source fiable (IR officiel, FDA/EMA/AMF, presse tier 1) ? OUI/NON
> **T3.** Au moins 2 sources concordantes (HAUTE) ? OUI/NON
> **T4.** Pas de superlatifs marketing ? OUI/NON
> **T5.** Pas de projection chiffrée non sourcée ? OUI/NON
> **T6.** Statut concurrent vérifié au présent ? OUI/N/A
>
> Décisions :
> - T1 ou T2 = NON → modification SUPPRIMÉE
> - T3 = NON → REFORMULÉE en mode « Selon [source unique] »
> - T4 = NON → REFORMULÉE neutre
> - T5 = NON → projection SUPPRIMÉE
> - T6 = NON → vérifier ou SUPPRIMÉE
>
> ⚠️ Application des **garde-fous hebdo durcis** (section du dump) :
> - Toute modif chiffre clé = 3 sources primaires concordantes requises
> - Suppression alerte présente depuis < 30 jours = bloquée sauf événement
>   explicite
> - Modif touchant garde-fou structurel = bloquée par R3
> - Claim FAIBLE ignorée
>
> Écris dans `data/ALSEN_routine_editorial_A_audit.md` et
> `data/ALSEN_routine_editorial_B_audit.md`.

## Phase 4 — Sous-agent C (méta-audit léger)

⚠️ **CRITIQUE : C ne voit pas le raisonnement de A, B, ni de l'orchestrateur.**

Lance C une fois A et B terminés avec ce prompt :

> Tu es un méta-auditeur éditorial léger. Tu reçois 4 fichiers :
> - `data/ALSEN_routine_editorial_A_proposal.md`
> - `data/ALSEN_routine_editorial_A_audit.md`
> - `data/ALSEN_routine_editorial_B_proposal.md`
> - `data/ALSEN_routine_editorial_B_audit.md`
>
> ⚠️ NE LIS PAS `content/ALSEN.yaml` ni `data/ALSEN_editorial_input.md`.
>
> CHECKLIST MÉTA-AUDIT LÉGER :
> **M1.** Modifications A et B se recoupent-elles ? (consensus = modification
>          probable, divergence = à arbitrer)
> **M2.** Cohérence avec garde-fous structurels d'AUDIT_REFERENCE_RAPPEL ?
>          Aucun fait des audits baseline / recalCplus contredit ?
> **M3.** Aucune section interdite touchée (`meta`, `liens`, `synthese_ia`,
>          `sources`) ?
> **M4.** Sources primaires datées < 7 jours pour les modifs hebdo ?
> **M5.** Pas de modification si actualité non significative (faux positif
>          marketing à filtrer) ?
>
> Pour chaque check : ✅ ACCORD / ⚠️ NUANCE / ❌ DÉSACCORD avec justification.
>
> Écris dans `data/ALSEN_routine_editorial_C_meta_audit.md`.

## Phase 5 — Auto-arbitrage strict par l'orchestrateur

Après C terminé, l'orchestrateur applique automatiquement :

**R1.** Modification = consensus A ∩ B + accord C → **APPLIQUER** dans
       `content/ALSEN.yaml`.

**R2.** Modification chez A seul OU B seul + accord C → **APPLIQUER en
       mode « Selon [source] »** (attribution prudente dans le YAML).

**R3.** Modification + désaccord C (M1-M5 = ⚠️ ou ❌) → **NE PAS
       APPLIQUER**, flagger dans le rapport.

**R4.** Toute modification touchant un garde-fou structurel
       (AUDIT_REFERENCE_RAPPEL["ALSEN.PA"].garde_fous_structurels) →
       **NE PAS APPLIQUER**, flagger dans le rapport.

**R5.** Si AUCUNE modification consensuelle après audit → commit avec
       message « editorial: RAS aucune actualité significative ALSEN
       YYYY-MM-DD » (commit non vide : juste le rapport-log).

## Exécution finale

L'orchestrateur :
1. Modifie `content/ALSEN.yaml` SEULEMENT sur les sections `alertes`,
   `pipeline`, `perspectives` (jamais `meta`, `liens`, `synthese_ia`,
   `sources`).
2. Écrit `data/ALSEN_routine_editorial_log_YYYY-MM-DD.md` avec :
   - Modifications appliquées (R1, R2)
   - Modifications bloquées (R3, R4) avec règle invoquée
   - Verdict méta-audit C par check M1-M5
3. Commit message :
   - Si modifs appliquées : `editorial: refresh hebdomadaire ALSEN
     YYYY-MM-DD (X modifs)`
   - Si RAS : `editorial: RAS aucune actualité significative ALSEN
     YYYY-MM-DD`
4. Push direct sur main

## Règles strictes

- JAMAIS modifier les sections `meta`, `liens`, `synthese_ia` (gérée par
  la routine synthèse), `sources` (gérée à part).
- JAMAIS skipper une phase. Si A timeout, relancer A.
- JAMAIS dépasser 3 modifications candidates par cycle hebdo.
- TOUJOURS commit + push (même un commit RAS — traçabilité).
- L'audit baseline 01/05/2026 et le recalibrage Pattern C+ 02/05/2026
  sont **intouchables** — leurs garde-fous structurels priment.

## Rapport final attendu

- N modifications appliquées (R1, R2) + détail
- N modifications bloquées (R3, R4) + raison
- SHA du commit
- URL du log : `data/ALSEN_routine_editorial_log_YYYY-MM-DD.md`
