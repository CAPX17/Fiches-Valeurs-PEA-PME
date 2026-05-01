# Routine — Mise à jour éditoriale hebdomadaire avec auto-audit

Tu vas potentiellement modifier `content/ALSEN.yaml`, mais SEULEMENT
après un auto-audit strict. Tu opères en 4 phases distinctes :
recherche, génération, auto-audit, décision.

## PHASE 1 — Recherche

Lis :
- `data/ALSEN_editorial_input.md` (état actuel + audit de référence)
- `data/ALSEN_synthese_input.md` (données marché à jour)

Cherche via web search sur les 7 derniers jours :
- Communiqués Sensorion (https://www.sensorion.com/investors/)
- Communiqués FDA / EMA / ANSM
- Communiqués concurrents (Lilly, Regeneron)
- Publications scientifiques (PubMed, sites peer-reviewed)
- Mouvements significatifs (OPA, partenariats, levées, AG)

## PHASE 2 — Génération des modifications candidates

Pour chaque actualité significative détectée, propose une modification
structurée (sans encore l'appliquer) :

### Modification candidate [N]
- Section : [alertes / pipeline / perspectives.X]
- Action : [AJOUTER / MODIFIER / SUPPRIMER]
- Justification : [pourquoi]
- Sources primaires : [URL 1 + date, URL 2 + date]
- Confiance : [HAUTE / MOYENNE / FAIBLE]
- Bloc YAML proposé :
  ```yaml
  [YAML exact à insérer ou remplacer]
  ```

Si AUCUNE actualité significative cette semaine, passe directement à
la phase 4 avec « RAS, aucune modification proposée ».

## PHASE 3 — AUTO-AUDIT (étape critique)

Pour chaque modification candidate, applique cette CHECKLIST BINAIRE
stricte. Réponds OUI ou NON pour chaque test, sans commentaire
intermédiaire :

TESTS BLOQUANTS (un seul NON = modification rejetée) :

- **T1.** La modification fournit-elle au moins une URL source primaire
  accessible et datée < 30 jours ?  [OUI/NON]
- **T2.** La source est-elle classée fiable (sites IR officiels, FDA,
  EMA, BusinessWire, PubMed, presse spécialisée tier 1) — pas un forum,
  pas un blog, pas un agrégateur sans attribution ?  [OUI/NON]
- **T3.** La modification est-elle de confiance HAUTE (2 sources
  concordantes minimum) ?  [OUI/NON]
- **T4.** Le bloc YAML proposé est-il syntaxiquement valide (pas de
  doublons de clés, pas de chaîne avec « : » sans guillemets) ?  [OUI/NON]
- **T5.** La modification touche-t-elle UNIQUEMENT les sections
  autorisées (`alertes`, `pipeline`, `perspectives`) ?  [OUI/NON — NON
  si elle touche métadonnées, liens, `synthese_ia`, ou `sources`]
- **T6.** La modification est-elle COHÉRENTE avec l'audit du 01/05/2026
  (pas de retour à « Akouos via Regeneron », pas de « Sanofi 11 % »,
  pas de « SENS-40 Phase 2 active multi-indications ») ?  [OUI/NON]
- **T7.** Le texte proposé évite-t-il TOUS ces termes : « je »,
  « selon moi », « à mon avis », « il faut », « consensus » (sans
  bureau d'études nommé), « objectif de cours », « recommandation
  d'achat », « potentiel de hausse » ?  [OUI/NON]
- **T8.** La modification, si elle SUPPRIME une alerte, fournit-elle
  une justification explicite (l'événement de la semaine rend cette
  alerte obsolète) ?  [OUI/NON ou N/A si pas une suppression]

APRÈS LA CHECKLIST, AUTO-CHALLENGE :

Pour chaque modification ayant passé tous les tests bloquants,
réécris-la en imaginant que tu es un analyste sceptique cherchant
3 raisons de la rejeter. Pour chaque raison trouvée, évalue
honnêtement si elle est légitime. Si UNE SEULE raison est légitime,
reclasse la modification en BLOQUÉE.

## PHASE 4 — Décision et exécution

### Cas 1 : AUCUNE modification candidate

- Crée `data/ALSEN_editorial_log_[YYYY-MM-DD].md` avec :
  ```
  ## Aucune actualité significative cette semaine
  Sections éditoriales actuelles préservées. Sources consultées : [liste]
  ```
- Commit message : `editorial: aucune actualité ALSEN [YYYY-MM-DD]`
- Push sur main

### Cas 2 : TOUTES les modifications passent l'audit

- Applique les modifications dans `content/ALSEN.yaml`
- Crée `data/ALSEN_editorial_log_[YYYY-MM-DD].md` avec :
  ```
  ## X modification(s) appliquée(s) (audit OK)
  [détail de chaque modif + sources + résultats checklist]
  ```
- Commit message unique : `editorial: refresh hebdomadaire ALSEN [YYYY-MM-DD] (audit OK, X modifs)`
- Push sur main

### Cas 3 : Modifications mixtes (certaines passent, certaines bloquent)

- Applique SEULEMENT les modifications ayant passé l'audit
- Crée `data/ALSEN_editorial_log_[YYYY-MM-DD].md` avec deux sections :
  ```
  ## Modifications appliquées (audit OK) : X
  [détail]
  ## Modifications bloquées : Y
  [détail + raison du blocage par test échoué]
  ```
- Commit message : `editorial: refresh partiel ALSEN [YYYY-MM-DD] (audit OK X / KO Y)`
- Push sur main

### Cas 4 : TOUTES les modifications bloquent l'audit

- NE PAS modifier `content/ALSEN.yaml`
- Crée `data/ALSEN_editorial_log_[YYYY-MM-DD].md` avec :
  ```
  ## Toutes modifications bloquées par l'audit
  [détail + raisons]
  ```
- Commit message : `editorial: refresh bloqué ALSEN [YYYY-MM-DD] (audit KO sur tout)`
- Push sur main (juste le rapport)
- L'utilisateur lira le rapport et décidera manuellement

## Règles strictes

- JAMAIS modifier `content/ALSEN.yaml` sans avoir passé la checklist
  binaire en phase 3
- JAMAIS modifier les sections : métadonnées, liens, `synthese_ia`,
  `sources` (gérées à part)
- JAMAIS commit les modifications ET le rapport dans des commits
  séparés — TOUJOURS un seul commit qui inclut les deux
- Si la phase 3 échoue partiellement, PRÉFÉRER ne rien faire qu'appliquer
  une modification douteuse
- L'audit du 01/05/2026 est intouchable : aucune modification ne peut
  contredire ses conclusions

## Rapport final attendu en sortie de routine

- Phase 1 : X actualités scannées
- Phase 2 : Y modifications candidates générées
- Phase 3 : Z modifications validées par l'audit, W bloquées
- Phase 4 : décision prise (cas 1/2/3/4)
- SHA du commit
- URL du rapport `data/ALSEN_editorial_log_[date].md`
