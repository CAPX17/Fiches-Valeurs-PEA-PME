# Méta-audit C — Sensorion (ALSEN.PA)
**Date** : 2026-05-02
**Agent** : C (méta-auditeur indépendant, Pattern C+)
**Inputs** : A_findings, A_audit, B_findings, B_audit, consolidation_draft.

---

## Synthèse globale

- **M1** (consensus A∩B équivalents) : ⚠️ NUANCE
- **M2** (divergences vraiment incompatibles) : ⚠️ NUANCE
- **M3** (faux négatifs YAML légitimes) : ✅ ACCORD (avec une réserve)
- **M4** (faux positifs YAML légitimes) : ⚠️ NUANCE
- **M5** (claims importantes oubliées) : ❌ DÉSACCORD
- **M6** (ratio consensus/divergence cohérent) : ⚠️ NUANCE

**Ratio nuance/désaccord : 5 / 6 ≈ 83 %** (largement au-dessus de la cible 30 %).

---

## Détail des 6 tests

### M1 — Consensus A∩B équivalents
**Verdict global** : ⚠️ NUANCE

**Détails** :
- **Démission CEO (date)** : ⚠️ NUANCE — A dit « 17 février 2026 » (claim_A_040) ; B dit « 16 février 2026 » (claim_B_039). Ce n'est *pas* le même jour. Les sources B (BusinessWire 20260216462062) sont datées du 16/02 ; les sources A (BioSpace, PharmiWeb « 2026-02-17 ») relaient avec un jour de décalage (différence fuseau horaire / date PR vs date relai). La consolidation tranche pour le 16/02 sans expliciter le conflit de date.
- **Trésorerie 31/12/2025** : ⚠️ NUANCE — A annonce **47,5 M€** (claim_A_024) ; B annonce **47,3 M€** (claim_B_022). Écart de 0,2 M€ non commenté par la consolidation. Probablement arrondi différent ou inclusion/exclusion du dépôt court terme de 10,2 M€ ; à vérifier sur le PR FY2025.
- **Épidémiologie GJB2** : ✅ ACCORD — A « ≈ 50 % » + B « jusqu'à 50 % » : équivalence acceptable, l'orchestrateur a bien retenu la formulation B « jusqu'à 50 % ».
- **Épidémiologie OTOF 1-8 %** : ✅ ACCORD — claim_A_044 et claim_B_031 strictement convergentes, GeneReviews commun.
- **Dilution 71 %** : ✅ ACCORD — A_023 et B_021 chiffrent identiquement, sources concordantes.
- **Approbation FDA Otarmeni** : ✅ ACCORD — A_028 et B_027 totalement alignées.
- **Patients dosés** : ⚠️ NUANCE — A dit « 5 patients dosés (cohorte 1=2, cohorte 2=3) » (claim_A_008) ; B dit « 6 patients à travers les 2 premières cohortes » (claim_B_012) et « 6 patients traités » (claim_B_016). **Incohérence numérique 5 vs 6** non remarquée par la consolidation. Probable lecture B qui inclut un patient supplémentaire de cohorte 1 (3 vs 2 ?) ou décalage temporel entre les sources. Critique pour les futures alertes.
- **SENS-501 dose cohortes** : ✅ ACCORD — A_009 et B_013 identiques.

### M2 — Divergences vraiment incompatibles
**Verdict global** : ⚠️ NUANCE

**Détails** :
- **CEO ouzren consultante (B_041 supprimée par B, A_042 confirmée par A)** : ⚠️ NUANCE — B a supprimé la claim B_041 (« Ouzren reste consultante temporaire ») pour cause de T3 fail (source unique BusinessWire). A confirme A_042 sur les mêmes sources (BioSpace + PharmiWeb relayant la même PR BusinessWire). C'est **la même information** corroborée par les **mêmes sources**, mais B applique une politique stricte « source unique = supprimée » alors que A admet le PR officiel comme suffisant. Politique d'audit divergente, pas véritable contradiction factuelle. La consolidation utilise A_042 dans CHANGEMENT 1 sans signaler que B a écarté ce point — choix éditorial discutable.
- **Pasteur option licence exclusive** : ❌ DÉSACCORD non résolu — A_002 (reformulée puis supprimée en politique stricte selon le récap final A) vs B_003 (supprimée). **Les deux ont fini par écarter cette claim**, et pourtant la consolidation maintient cette mention dans CHANGEMENT 7 (« la mention sur l'option de licence exclusive reste, sourcée par le communiqué Institut Pasteur de janvier 2024 »). **Incohérence majeure** : le draft conserve une affirmation que les deux audits ont in fine retirée.
- **Lilly AK-OTOF / patient 11 ans** : ⚠️ NUANCE — A a supprimé claim_A_033 (« 1er patient 11 ans audition restaurée ») pour donnée datée (>12 mois) ; B a reformulé claim_B_029 mais en gardant les 30 jours / 11 ans. Donc B retient l'info, A la rejette. La consolidation suit B (CHANGEMENT 12 mentionne fin 2028 mais omet le patient 11 ans) — choix raisonnable mais non explicité.
- **Couverture des 3 indications SENS-401** : ⚠️ NUANCE — Seul B (B_017) couvre les **3** indications structurées (SSNHL Phase 2b, implant cochléaire Phase 2a, cisplatine Phase 2). A couvre A_017 (NOTOXIS cisplatine) et A_018 (Cochlear) séparément, sans mentionner SSNHL Phase 2b. Ce n'est pas une contradiction mais un **gap de couverture A** non flaggé.

### M3 — Faux négatifs YAML légitimes
**Verdict global** : ✅ ACCORD (avec une réserve)

**Détails** :
- **Démission CEO (CHANGEMENT 1)** : ✅ ACCORD — Vraiment absent du YAML, consensus solide A∩B, importance évidente.
- **Désignations FDA SENS-501 (CHANGEMENT 5)** : ⚠️ NUANCE — Je n'ai pas le YAML actuel sous les yeux (consigne explicite « ne lis pas content/ALSEN.yaml »), donc je ne peux pas vérifier si la désignation Orphan/RPDD est *réellement* absente. Selon la consolidation elle l'est, mais c'est un fait connu et structurel (T4 2022) probablement déjà mentionné quelque part. Le caractère « faux négatif » dépend d'un appel orchestrateur non vérifiable ici.
- **Dilution 71 % (CHANGEMENT 4)** : ✅ ACCORD — Précision quantitative manifestement utile, consensus solide.
- **Épidémiologie corrigée (CHANGEMENTS 2 et 3)** : ✅ ACCORD — Présentés comme faux *positifs* (correction de chiffre erroné), pas faux négatifs. Légitimes.

### M4 — Faux positifs YAML légitimes
**Verdict global** : ⚠️ NUANCE

**Détails** :
- **« 25 ans d'expertise mondiale » (CHANGEMENT 6)** : ✅ ACCORD pour suppression — formulation marketing non sourçable, le remplacement est plus précis et neutre.
- **« Clause de résiliation OPA » (CHANGEMENT 7)** : ⚠️ NUANCE — Critère « non confirmable par A et B » appliqué assez sévèrement. Une clause contractuelle de change-of-control est **typique** des accords Pasteur-spinoff et l'absence de mention publique est attendue (ce sont des clauses non publiques). Supprimer purement la mention va dans le sens « pas de source = on retire », mais on perd potentiellement une information vraie. Recommandation : reformuler en « selon les communications historiques de la société » plutôt que supprimer (mais pour ça il faudrait corroboration).
- **« Interactions FDA + EMA depuis T3 2025 » (CHANGEMENT 8)** : ✅ ACCORD pour reformulation — date T3 2025 effectivement non sourcée par A ni B ; le remplacement « interactions en cours en vue des soumissions CTA et IND » est correct.
- **« 3e programme avant 2028 » (CHANGEMENT 9)** : ⚠️ NUANCE — B_004 dit explicitement « **deux** programmes » mais cela ne signifie pas qu'un troisième ne pourra pas émerger : c'est un état des lieux à la date des sources (mars 2026), pas une exclusion. La suppression complète des mentions « 3e programme » dans les perspectives moyen/long terme est trop sévère ; une reformulation prudente (« optionnel sous l'accord prolongé jusqu'à fin 2028 ») suffirait. Le draft propose justement cette option en alternative — bien, mais pour le pipeline[3] il propose « SUPPRIMER ou requalifier » avec OU exclusif, ce qui est ambigu.
- **Cohorte 3 / 3e niveau de dose** : la consolidation ne mentionne pas explicitement cet enrichissement comme correction du YAML alors que A_011 et B_009 sont en consensus. À vérifier.

### M5 — Claims importantes oubliées
**Verdict global** : ❌ DÉSACCORD

**Claims importantes manquant à la consolidation** :
- **claim_B_028** (indication précise Otarmeni : >90 dB HL, mutations bialléliques OTOF, sans implant cochléaire ipsilatéral préalable) : critère essentiel pour analyser l'overlap concurrentiel direct avec SENS-501. **Totalement omis** par le draft.
- **claim_B_034 + claim_A_048** (1 nouveau-né sur 500 atteint de surdité congénitale) : consensus A∩B, donnée d'épidémiologie clé pour dimensionner le marché. Pas mentionné dans les changements.
- **claim_A_010 / claim_B_015** (gains de 60-70 dB HL chez 2/3 des patients cohorte 2 à 6 mois) : donnée d'efficacité clinique **fondamentale** sur le programme phare ; consensus solide ; absence de mention dans les 12 changements proposés. C'est très étonnant.
- **claim_B_042** (présentation JPM 15/01/2026) : événement gouvernance/comm qui s'inscrit dans la chronologie pré-démission Ouzren ; non couvert par A (gap de couverture A) et non discuté dans la consolidation comme divergence B\A à valoriser.
- **claim_A_028 / claim_B_027** (approbation Otarmeni) — la consolidation l'utilise dans CHANGEMENT 12 mais comme contexte secondaire ; or c'est *l'événement concurrentiel le plus matériel des 6 derniers mois*. Il mérite un changement dédié (ajout d'alerte RISQUE/CONCURRENCE majeure), pas seulement une mention dans AK-OTOF.
- **claim_A_001** (date d'expiration extension partenariat = 31/12/2028) : précision factuelle utilisée dans CHANGEMENT 9 mais qui mériterait un garde-fou propre (la date est citée dans le garde-fou n°2 « 30-40 % GJB2 » de manière indirecte mais pas comme garde-fou autonome).

### M6 — Ratio consensus/divergence cohérent
**Verdict global** : ⚠️ NUANCE

**Analyse** :
- Annoncé : 24 consensus A∩B, 17 divergences A\B, 8 divergences B\A.
- Vérification grossière par dénombrement thématique :
  - **Vrais consensus identifiables** sur lecture : MOAT Pasteur 2024 (A_001/B_001), Petit chair SAB (A_004/B_002), 2 programmes Pasteur (A_003/B_004), SENS-501 dual AAV OTOF DFNB9 (A_006/B_011), NCT06370351 (A_007/B_012), dose cohortes (A_009/B_013), gains 60-70 dB (A_010/B_015), pas d'EI grave (~A_008/B_016), cohorte 3 envisagée (A_011/B_009), CTA H1 2026 (A_014/B_006), IND fin 2026 (A_014/B_007), ASGCT (A_015/B_008), AGM 11 mai (A_039/B_010), placement 60 M€ (A_019/B_019), Sanofi 13,9 % / 20 M€ (A_020/B_019), participants tour (A_022/B_020), 214 M actions / 71 % (A_023/B_021), trésorerie ~47 M€ (A_024/B_022), runway H1 2027 (A_025/B_023), Otarmeni FDA (A_028/B_027), Otarmeni gratuit US (A_031/B_028), AK-OTOF NCT (A_032/B_029), GeneReviews OTOF 1-8 % (A_044/B_031), GJB2 ~50 % (A_045/B_033), 1/500 (A_048/B_034), ODD/RPDD SENS-501 (A_037/B_036), démission CEO (A_040/B_039), Munshi intérim (A_041/B_040), SENS-401 cisplatine/CIO (~A_017/B_017-B_018).
  - On compte facilement **28-30** consensus, pas 24. **Le chiffre de 24 sous-estime le consensus**.
- **Divergences A\B = 17 annoncé** : les claims uniques à A vraiment matérielles incluent A_002 (option licence — mais B_003 la couvre aussi), A_005 (Petit IdA 2019-2021), A_012 (DMC déc 2025), A_018 (Cochlear), A_021 (détail des % détenteurs), A_026 (HY2025), A_027 (Meyka, supprimée), A_029 (DB-OTO origin), A_030 (CHORD 80%/42%), A_033/A_034/A_035/A_036 (concurrents divers), A_038 (CTA Audiogene 2024), A_043 (otoferlin science), A_046/A_047 (connexin science). Soit **~14-15** claims uniques à A, dont plusieurs supprimées par A. **Chiffre de 17 plausible.**
- **Divergences B\A = 8 annoncé** : B_018 (CIO achevée T1 2026), B_024 (publication FY2025 18/03/2026), B_025 (perte nette), B_026 (capi Boursorama), B_028 (indication Otarmeni précise), B_032 (auditory neuropathy), B_035 (vecteur GJB2 propriétaire), B_037 (EMA ODD 2022), B_038 (ODD SENS-401 EMA/FDA), B_042 (JPM). Soit **~10** claims, plus que les 8 annoncés.
- **Conclusion** : le décompte est globalement plausible mais **sous-estime le consensus** et **sous-estime B\A**. La répartition n'est pas grossièrement fausse, mais elle pourrait masquer des claims B\A importantes (B_028 indication Otarmeni précise, B_042 JPM, B_038 ODD SENS-401) que la consolidation a fait passer à la trappe.

---

## Verdicts par changement (1 à 12)

1. **CHANGEMENT 1 — Ajout alerte démission CEO** : ⚠️ NUANCE — Le contenu est correct et bien sourcé, mais la **date 16/02/2026 vs 17/02/2026** (cf. M1) doit être tranchée explicitement par référence à la PR primaire BusinessWire 20260216462062. Le draft choisit 16/02 sans signaler le conflit avec A_040 qui dit 17/02.

2. **CHANGEMENT 2 — Correction GJB2 30-40 % → ~50 %** : ✅ ACCORD — Consensus A∩B sur sources de référence (GeneReviews, OMIM, Genetics in Medicine). Reformulation rigoureuse.

3. **CHANGEMENT 3 — Correction OTOF ~1 % → 1-8 %** : ✅ ACCORD — Idem, sources scientifiques convergentes, fourchette plus précise.

4. **CHANGEMENT 4 — Précision dilution 71 %** : ✅ ACCORD — Source primaire BusinessWire, consensus A∩B, ajout factuel utile.

5. **CHANGEMENT 5 — Désignations FDA SENS-501** : ⚠️ NUANCE — Le contenu est exact (consensus A_037/B_036 sur ODD + RPDD nov 2022). Mais A et B ont noté T1 fail (info > 12 mois) acceptée par exception « fait structurel ». Le draft ne signale pas que la mention « voucher éligible en cas d'AMM » est une **inférence** de l'orchestrateur, non explicitement présente dans A_037 ni B_036. À nuancer.

6. **CHANGEMENT 6 — Reformulation « 25 ans d'expertise »** : ✅ ACCORD — Substitution d'une formulation marketing par une formulation factuelle vérifiable. Bien.

7. **CHANGEMENT 7 — Suppression « clause de résiliation OPA »** : ⚠️ NUANCE — Suppression sévère ; et incohérence avec la décision de **conserver** la mention « option de licence exclusive » alors que **A_002 et B_003 ont toutes deux été supprimées/écartées** par les audits respectifs (A_002 supprimée en politique stricte d'A, B_003 supprimée par B). La consolidation devrait soit supprimer aussi la mention licence exclusive, soit conserver les deux avec attribution prudente. Asymétrie non justifiée.

8. **CHANGEMENT 8 — Reformulation « FDA + EMA T3 2025 »** : ✅ ACCORD — Date T3 2025 non sourcée, remplacement neutre justifié.

9. **CHANGEMENT 9 — Reformulation « 3e programme avant 2028 »** : ⚠️ NUANCE — La reformulation MOAT « Deux programmes générés à ce stade ... possibilité de programmes additionnels » est bonne. Mais la suppression brutale dans pipeline[3] ET dans `perspectives.moyen_terme` ET dans `perspectives.long_terme` est excessive. Le 3e programme reste une **possibilité légitime** avec l'extension du contrat à 2028 ; il ne s'agit pas d'une affirmation contredite par les sources, juste d'une affirmation non encore confirmée. Une reformulation conditionnelle suffit.

10. **CHANGEMENT 10 — SENS-40 → SENS-401** : ⚠️ NUANCE — Voir réponse Q1 ci-dessous. Correction nominale légitime, mais la procédure R6 (« ne pas appliquer auto, touche garde-fou figé ») doit être respectée formellement.

11. **CHANGEMENT 11 — Cochlear Limited** : ⚠️ NUANCE — Le draft propose de ne pas appliquer (R5 confiance moyenne). Or la claim A_018 est confirmée par A avec 5 critères OUI ; B_017 mentionne aussi l'implant cochléaire avec Cochlear Ltd. C'est plus solide que « confiance moyenne ». Voir réponse Q2 ci-dessous.

12. **CHANGEMENT 12 — Précision AK-OTOF** : ✅ ACCORD — Calendrier ClinicalTrials.gov (fin estimée octobre 2028) est factuel et bien attribué. Mention « pas d'update 2025-2026 » utile pour positionner la course.

---

## Réponses aux 3 questions de l'orchestrateur

### Q1 — Changement 10 (SENS-40 → SENS-401) : peut-on l'appliquer malgré R6 ?

**Réponse : ✅ OUI, mais avec procédure formelle.**

C'est une simple correction typographique avec consensus A∩B fort (8 sources distinctes citent SENS-401, aucune ne mentionne « SENS-40 » comme nom de programme — il n'existe pas). La règle R6 vise à protéger les garde-fous contre des modifications introduites par dérive, **pas à figer une typo**. Procédure recommandée :
1. Mettre à jour simultanément la claim YAML ET le garde-fou `AUDIT_REFERENCE_RAPPEL["ALSEN.PA"]` dans le même commit.
2. Documenter dans le commit message que la modification du garde-fou est une **correction de coquille**, pas un changement de fond.
3. Ne pas considérer cette modification comme un « précédent » pour assouplir R6 sur d'autres points.

### Q2 — Changement 11 (Cochlear Limited) : suffisamment important pour examen complémentaire ?

**Réponse : ✅ OUI, à appliquer avec attribution prudente.**

A_018 est une claim **confirmée** (5/5 OUI) chez A, avec deux sources tier-1 (BusinessWire FY2024 PR + Hearing Health Matters). B la mentionne sans détail (B_017) mais ne la contredit pas. Le critère « confiance moyenne » dans la consolidation est trop sévère. Recommandation : ajouter une mention courte dans l'alerte SENS-401 actuelle, du type :

> *« L'étude Phase 2a SENS-401 dans l'implantation cochléaire (en partenariat avec Cochlear Limited, australien, leader mondial des implants cochléaires) a atteint en 2024 son critère principal pharmacocinétique : présence de SENS-401 dans la périlymphe à des taux compatibles avec une efficacité thérapeutique potentielle chez 100 % des patients prélevés (Sensorion FY2024 PR, 13/03/2025). »*

L'enjeu stratégique (partenariat industriel avec un leader mondial des implants cochléaires) justifie l'inclusion.

### Q3 — Garde-fou n°4 (sur SENS-401) : dépend de la réponse à Q1

**Réponse : ✅ OUI, applicable** — sous réserve d'appliquer Q1. Le garde-fou n°4 codifie la dénomination correcte SENS-401 + arazasétron + 3 indications. Il est cohérent avec les claims A_017, A_018, B_017, B_018 (consensus A∩B robuste). À intégrer dans le même commit que la correction Q1 pour éviter toute fenêtre d'incohérence.

---

## Évaluation des 4 garde-fous proposés

### Garde-fou 1 — Démission CEO Nawal Ouzren le 16/02/2026 + Munshi intérim
**Verdict** : ⚠️ NUANCE — Date 16/02 vs 17/02 doit être figée explicitement par référence à la PR BusinessWire 20260216462062 (date primaire = 16/02/2026 en heure US). Sinon contenu OK. Préciser aussi « jusqu'à nomination CEO permanent » comme fait évolutif (à reviewer à chaque audit ultérieur).

### Garde-fou 2 — Épidémiologie OTOF (1-8 %) / GJB2 (jusqu'à 50 %)
**Verdict** : ✅ ACCORD — Sources primaires concordantes (GeneReviews, OMIM, Genetics in Medicine), consensus A∩B, formulation prudente (« jusqu'à 50 % » et fourchette OTOF). Excellent garde-fou.

### Garde-fou 3 — Dilution janvier 2026 = ~71 % (214 285 714 actions à 0,28 €)
**Verdict** : ✅ ACCORD — Données chiffrées précises, sources primaires (BusinessWire 27/01/2026), consensus A∩B. Garde-fou solide.

### Garde-fou 4 — Dénomination SENS-401 + arazasétron + 3 indications
**Verdict** : ⚠️ NUANCE — Contenu correct (consensus B_017 sur 3 indications), MAIS :
- L'indication SSNHL Phase 2b achevée n'est mentionnée que par B (claim_B_017), A ne la couvre pas.
- L'indication CIO Phase 2 achevée T1 2026 vient d'une **source unique** (claim_B_018 reformulée) — corroboration faible.
- Recommandation : reformuler le garde-fou en « SENS-401 (arazasétron, petite molécule) — historiquement étudié dans 3 indications : SSNHL (Phase 2b achevée selon BioSpace 18/03/2026), implant cochléaire (Phase 2a en partenariat Cochlear Limited, critère pharmacocinétique atteint en 2024), cisplatine/CIO (Phase 2 NOTOXIS achevée au T1 2026 selon Sensorion FY2025 PR) ».

---

## Recommandations finales pour la phase 6 (application auto)

### Changements à APPLIQUER fermement
- **CHANGEMENT 2** (épidémio GJB2 jusqu'à 50 %)
- **CHANGEMENT 3** (épidémio OTOF 1-8 %)
- **CHANGEMENT 4** (dilution 71 %)
- **CHANGEMENT 6** (reformulation Christine Petit, factuelle)
- **CHANGEMENT 8** (suppression « depuis T3 2025 » non sourcée)
- **CHANGEMENT 10** (SENS-40 → SENS-401, avec mise à jour synchronisée du garde-fou — voir Q1)
- **CHANGEMENT 12** (précision AK-OTOF / NCT05821959 / fin oct. 2028)

### Changements à APPLIQUER avec amendement
- **CHANGEMENT 1** (démission CEO) : trancher la date à 16/02/2026 (PR primaire BusinessWire) et signaler le décalage avec A_040 dans le commit.
- **CHANGEMENT 5** (désignations FDA) : retirer la mention « voucher éligible en cas d'AMM » (inférence orchestrateur non sourcée par A ni B).
- **CHANGEMENT 9** (3e programme) : reformulation MOAT acceptable ; ne PAS supprimer entièrement les mentions dans `perspectives.moyen_terme` et `pipeline[3]` — les requalifier en « optionnel sous accord prolongé jusqu'au 31/12/2028, non confirmé publiquement ».
- **CHANGEMENT 11** (Cochlear Limited) : APPLIQUER (cf. Q2), pas reporter à un audit ultérieur.

### Changements à NE PAS APPLIQUER tels quels
- **CHANGEMENT 7** (suppression mention « OPA hostile ») : OK pour supprimer la clause de résiliation OPA, MAIS retirer aussi (ou requalifier) la mention « option de licence exclusive » — A_002 et B_003 ont toutes deux été supprimées/écartées par les audits ; conserver l'une et supprimer l'autre est asymétrique et non défendable.

### Garde-fous à intégrer dans AUDIT_REFERENCE_RAPPEL
- **Garde-fou 2** (épidémio) : intégration ferme.
- **Garde-fou 3** (dilution 71 %) : intégration ferme.
- **Garde-fou 1** (démission CEO) : intégration avec date 16/02/2026 figée explicitement.
- **Garde-fou 4** (SENS-401) : intégration avec libellé enrichi proposé ci-dessus (3 indications avec sources distinctes pour chaque, attribution prudente sur SSNHL et CIO).

### Claims importantes à intégrer EN PLUS (oubliées par la consolidation, cf. M5)
- **Indication précise Otarmeni** (B_028) : >90 dB HL, mutations bialléliques OTOF, sans implant ipsilatéral préalable — à intégrer dans une alerte RISQUE/CONCURRENCE dédiée Otarmeni, distincte de l'enrichissement AK-OTOF (CHANGEMENT 12).
- **Gains audiométriques cohorte 2 SENS-501** (A_010/B_015) : 60-70 dB HL chez 2/3 des patients à 6 mois — donnée d'efficacité majeure, mériterait d'enrichir l'alerte PIPELINE Cohorte 2 existante.
- **1 nouveau-né sur 500** (A_048/B_034) : épidémio générale utile pour le marché total adressable.
- **Trancher l'incohérence 5 vs 6 patients dosés** (A_008 « 5 patients » vs B_012/B_016 « 6 patients ») : à clarifier avant tout enrichissement de l'alerte PIPELINE.

---

**Fin du méta-audit C.**
