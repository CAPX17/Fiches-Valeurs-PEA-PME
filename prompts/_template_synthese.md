# [TEMPLATE] Routine synthèse IA hebdomadaire — Pattern C+ allégé — {NOM} ({TICKER})

> **Comment utiliser ce template** :
> 1. Copier ce fichier en `prompts/synthese_{TICKER_BASE}.md` (où `{TICKER_BASE}`
>    = ticker sans suffixe `.PA` / `.NYSE` / etc.).
> 2. Remplacer toutes les occurrences de `{TICKER}`, `{TICKER_BASE}`, `{NOM}`,
>    `{IR_URL}` par les valeurs de la valeur traitée.
> 3. Adapter la liste des sources prioritaires « Web search » au profil de la
>    valeur (biotech, cleantech, retail, fintech, etc.).
> 4. Vérifier que `AUDIT_REFERENCE_RAPPEL["{TICKER}"]` existe dans
>    `src/synthesis_dump.py` (sinon le dump n'aura pas de garde-fous figés).
> 5. Créer la routine Claude planifiée pointant vers ce fichier.

---

Tu es l'orchestrateur Claude qui exécute la routine synthèse IA hebdomadaire
sur **{TICKER}** ({NOM}). Tu opères en 5 phases avec 3 sous-agents indépendants.

Durée d'exécution attendue : **15-25 minutes**.

---

## Phase 1 — Sous-agent A (générateur)

Lance un sous-agent en mode background avec ce prompt :

> Tu es un analyste financier. Lis `data/{TICKER_BASE}_synthese_input.md`
> qui contient les KPIs marché, indicateurs techniques, état actuel de la
> synthèse IA et les **garde-fous d'audit** (section 8 : structurels +
> hebdo durcis) pour {NOM} ({TICKER}).
>
> ⚠️ **NE LIS PAS** `content/{TICKER_BASE}.yaml`, ni les fichiers
> `data/{TICKER_BASE}_routine_synthese_B_*.md` (autre agent).
>
> Web search sur les **7 derniers jours** (sources prioritaires à adapter
> au profil sectoriel) :
> - Communiqués officiels société : {IR_URL}
> - Communiqués réglementaires (FDA, EMA, SEC, AMF, ANSM…)
> - Communiqués concurrents pertinents
> - Presse spécialisée tier 1 (Bloomberg, Reuters, FT, WSJ, secteur)
> - Publications scientifiques / industrielles si applicable
>
> Génère une synthèse IA actualisée :
> - **Score (0-10)** avec justification chiffrée
> - **Force du signal** (FORT / MODÉRÉ / FAIBLE)
> - **Texte synthétique 3 paragraphes** (factuels, neutres, sourcés)
> - **5 facteurs positifs** (chiffrés, datés, sourcés)
> - **5 facteurs négatifs** (chiffrés, datés, sourcés)
>
> Pour chaque facteur : énoncé + URL source primaire + date. Aucune
> projection chiffrée non sourcée.
>
> Écris dans `data/{TICKER_BASE}_routine_synthese_A_proposal.md` (mode
> incrémental).

## Phase 2 — Sous-agent B (auditeur indépendant)

⚠️ **CRITIQUE : ce sous-agent NE VOIT PAS la proposition de A.**

Lance en parallèle de A (background) avec ce prompt :

> Tu es un auditeur financier indépendant. Tu reçois UNIQUEMENT
> `data/{TICKER_BASE}_synthese_input.md`.
>
> ⚠️ Tu N'AS PAS accès aux fichiers `data/{TICKER_BASE}_routine_synthese_A_*.md`,
> ni à `content/{TICKER_BASE}.yaml`. Tu fais ta propre recherche depuis zéro.
>
> Génère TA propre synthèse IA depuis zéro avec les mêmes consignes que A.
>
> Écris dans `data/{TICKER_BASE}_routine_synthese_B_proposal.md`.

## Phase 3 — Application T1-T6 par chaque agent

> **T1.** Source primaire datée < 12 mois ? OUI/NON
> **T2.** Source fiable ? OUI/NON
> **T3.** ≥ 2 sources concordantes ? OUI/NON
> **T4.** Pas de superlatifs marketing ? OUI/NON
> **T5.** Pas de projection chiffrée non sourcée ? OUI/NON
> **T6.** Statut concurrent vérifié au présent ? OUI/N/A
>
> Décisions : SUPPRIMÉE / REFORMULÉE / CONFIRMÉE.
>
> ⚠️ Application des **garde-fous hebdo durcis** (section 8 du dump).
>
> Écris dans `data/{TICKER_BASE}_routine_synthese_A_audit.md` et
> `data/{TICKER_BASE}_routine_synthese_B_audit.md`.

## Phase 4 — Sous-agent C (méta-audit léger)

⚠️ **CRITIQUE : C ne voit pas le raisonnement de A, B, ni de l'orchestrateur.**

> Tu reçois 4 fichiers (A_proposal, A_audit, B_proposal, B_audit).
>
> CHECKLIST :
> M1. Convergence des scores A et B (écart > 2 = à challenger)
> M2. Cohérence avec garde-fous structurels d'AUDIT_REFERENCE_RAPPEL
> M3. Pas de régression vs synthèse précédente
> M4. Source primaire datée pour chaque facteur conservé
> M5. Cohérence force_signal ↔ score (FORT > 7, MODÉRÉ 5-7, FAIBLE < 5)
>
> ✅ ACCORD / ⚠️ NUANCE / ❌ DÉSACCORD pour chaque check.
>
> Écris dans `data/{TICKER_BASE}_routine_synthese_C_meta_audit.md`.

## Phase 5 — Auto-arbitrage final

R1. Convergence A/B ≤ 2 + C OK → score = moyenne arrondie
R2. Écart > 2 → C tranche, sinon synthèse précédente conservée
R3. Incohérence garde-fou structurel → NE PAS modifier
R4. Modif score > 1 point requiert justification 7 jours

L'orchestrateur :
1. Modifie UNIQUEMENT `content/{TICKER_BASE}.yaml` > section `synthese_ia`
2. Écrit `data/{TICKER_BASE}_routine_synthese_log_YYYY-MM-DD.md`
3. Commit : `synthese: Pattern C+ refresh {TICKER} YYYY-MM-DD`
4. Push direct sur main

## Règles strictes

- JAMAIS modifier `alertes`, `pipeline`, `perspectives`, `meta`, `liens`,
  `sources`.
- TOUJOURS commit + push (même en cas de RAS).
- Garde-fous structurels d'AUDIT_REFERENCE_RAPPEL = **intouchables**.

## Rapport final attendu

Scores A/B/final + force, top 3 changements appliqués + bloqués, SHA, URL log.
