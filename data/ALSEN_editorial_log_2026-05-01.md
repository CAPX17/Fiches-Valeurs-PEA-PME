# Rapport éditorial hebdomadaire — Sensorion (ALSEN.PA)

**Date d'exécution** : 2026-05-01  
**Routine** : editorial_ALSEN.md  
**Fenêtre de recherche** : 24 avril – 1er mai 2026  

---

## 1 modification appliquée (audit OK)

### MC-1 — Alerte RISQUE Regeneron : date précise + free pricing US

**Section** : alertes  
**Action** : MODIFIER  
**Champ modifié** : `titre` + `description` (alerte RISQUE Otarmeni/Regeneron)

**Avant :**
```
titre: Concurrent approuvé FDA sur OTOF — Otarmeni (Regeneron) avril 2026
[...] Regeneron a obtenu en avril 2026 [...]
Source : communiqué Regeneron / FDA, avril 2026.
```

**Après :**
```
titre: Concurrent approuvé FDA sur OTOF — Otarmeni (Regeneron) 23 avril 2026
[...] Regeneron a obtenu le 23 avril 2026 [...]
Regeneron a annoncé concomitamment qu'Otarmeni sera fourni gratuitement
aux patients américains éligibles ; le prix hors États-Unis n'était pas
encore fixé au 24 avril 2026.
Sources : Regeneron IR / FDA, 23/04/2026 ; CNBC, 24/04/2026.
```

**Justification** : Deux faits nouveaux confirmés dans la fenêtre 7 jours —
(1) date exacte de l'AMM FDA = 23 avril 2026 (vs mention générique "avril 2026") ;
(2) Regeneron fournira Otarmeni gratuitement aux patients US (accord gouvernement US
annoncé simultanément à l'AMM), avec prix international non encore fixé au 24/04.

**Sources primaires :**
- investor.regeneron.com — communiqué AMM + free pricing, 23/04/2026
- cnbc.com/2026/04/24/regeneron-otarmeni-gene-therapy-hearing-loss.html — 24/04/2026
- globenewswire.com/news-release/2026/04/29/... — Regeneron Q1 2026 (confirme la gratuité US)

**Résultats checklist binaire :**

| Test | Résultat |
|------|----------|
| T1. URL source primaire datée < 30 jours | OUI |
| T2. Source fiable (IR officiel / presse tier 1) | OUI |
| T3. Confiance HAUTE (≥2 sources concordantes) | OUI |
| T4. YAML syntaxiquement valide | OUI |
| T5. Sections autorisées uniquement | OUI |
| T6. Cohérent avec l'audit 01/05/2026 | OUI |
| T7. Termes interdits absents | OUI |
| T8. N/A (pas une suppression) | N/A |

**Auto-challenge :**
- Raison 1 : "Gratuité US non pertinente pour biotech européenne" → PAS LÉGITIME
- Raison 2 : "Date précise cosmétique" → PAS LÉGITIME (combinée au free pricing)
- Raison 3 : "Incohérence avec 'accès remboursement'" → PAS LÉGITIME (texte précise hors-US)

**Verdict** : VALIDÉE ✓

---

## Sources consultées (Phase 1)

| Source | Date | Pertinence |
|--------|------|------------|
| businesswire.com — AG documents availability | 20-21/04/2026 | Hors fenêtre 7j, déjà capturée |
| pharmiweb.com — AG documents | 21/04/2026 | Hors fenêtre 7j, déjà capturée |
| investor.regeneron.com — Otarmeni AMM + free pricing | 23/04/2026 | → MC-1 |
| FDA.gov / HHS.gov — Otarmeni AMM | 23/04/2026 | Confirme MC-1 |
| bloomberg.com — Regeneron Otarmeni free | 23/04/2026 | Confirme MC-1 |
| cnbc.com — Regeneron overseas price | 24/04/2026 | → MC-1 (fenêtre 7j) |
| globenewswire.com — Regeneron Q1 2026 | 29/04/2026 | Confirme MC-1 |
| sensorion.com/investors — derniers communiqués | scan 01/05/2026 | Aucune release 24-30/04 |
| asgct.org — dates conférence 2026 | scan 01/05/2026 | Mai 11-15, source >30j |
| biospace.com, pharmiweb.com, pharmixweb.com — SENS-501/601 | mars 2026 | Hors fenêtre, déjà capturée |

**Total sources scannées** : ~15 articles/pages

---

## Actualités NON retenues (raison)

- **Lilly / Seamless Therapeutics $1.12B deal** : annoncé 28/01/2026, hors fenêtre 7 jours
- **ASGCT poster SENS-601** : annoncé dans communiqué 23/03/2026 (>30 jours), T1 échouerait
- **Regeneron Q1 2026 résultats** : aucune donnée commerciale Otarmeni nouvelle (approval trop récent pour Q1), confirme seulement le free pricing déjà capturé dans MC-1
- **Precisions techniques Fib/MA** : sections interdites (synthese_ia)

---

## Bilan de la routine

- **Phase 1** : ~15 sources scannées, 1 actualité significative dans la fenêtre 7 jours
- **Phase 2** : 1 modification candidate générée (MC-1)
- **Phase 3** : 1 validée par l'audit (8/8 tests OK + auto-challenge négatif), 0 bloquée
- **Phase 4** : Cas 2 — modification appliquée dans content/ALSEN.yaml
- **Sections modifiées** : alertes (1 alerte RISQUE)
- **Sections préservées** : pipeline, perspectives, synthese_ia, sources (sauf ajout CNBC 24/04)
- **Garde-fous audit 01/05/2026** : intacts (Lilly=Akouos, Regeneron=Decibel/Otarmeni, Sanofi 13,9 %, SENS-40 historique Phase 2b)
