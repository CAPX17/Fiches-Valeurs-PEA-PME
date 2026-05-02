# Fiches-Valeurs

Générateur statique de fiches d'analyse pour actions cotées (PEA-PME et
hors PEA-PME), hébergé gratuitement via GitHub Pages. Les données
factuelles (cours, capitalisation, indicateurs techniques) sont
rafraîchies quotidiennement depuis yfinance ; le contenu éditorial
(thèse, alertes, pipeline, perspectives) est versionné en YAML pour
une édition simple et un audit historique propre.

L'index d'accueil regroupe les fiches en deux sections (PEA-PME / Hors
PEA-PME) selon le champ `cadre_fiscal` du YAML.

Première fiche disponible : **Sensorion (ALSEN.PA)** — biotech Euronext
Growth Paris spécialisée en thérapies géniques auditives.

URL publique attendue après activation de GitHub Pages :
**https://capx17.github.io/Fiches-Valeurs-PEA-PME/**

---

## Objectif

- Mettre à disposition une fiche d'analyse lisible, à jour, et reproductible
  pour chaque valeur suivie.
- Séparer strictement le **factuel** (auto, yfinance) du **subjectif**
  (éditorial, YAML versionné).
- Conserver un historique git propre des changements éditoriaux : chaque
  modification de thèse est une diff YAML traçable.
- Zéro coût d'hébergement : GitHub Pages + GitHub Actions sur les minutes
  gratuites des dépôts publics.

---

## Stack technique

- **Python 3.11**
- **yfinance** — récupération cours, capitalisation, range 52 semaines,
  historique 1 an
- **pandas** + **pandas-ta** (avec fallback pandas pur) — RSI(14),
  MACD(12,26,9), MA50/200, niveaux Fibonacci
- **Jinja2** — moteur de templating HTML
- **PyYAML** — chargement du contenu éditorial
- **GitHub Actions** — régénération automatique quotidienne
- **GitHub Pages** — hébergement statique gratuit

---

## Architecture du dépôt

```
Fiches-Valeurs-PEA-PME/
├── content/                  # Contenu éditorial (YAML, versionné)
│   └── ALSEN.yaml            # Fiche Sensorion (thèse, alertes, pipeline...)
├── src/                      # Code Python
│   ├── fetcher.py            # Wrapper yfinance + cache SQLite local
│   ├── indicators.py         # RSI, MACD, MA, Fibonacci (avec fallback)
│   └── renderer.py           # Construction du contexte Jinja
├── templates/                # Templates Jinja
│   └── fiche.html            # Template unique de fiche
├── static/                   # Assets statiques (source)
│   └── style.css
├── docs/                     # Sortie publiée par GitHub Pages
│   ├── index.html            # Régénéré par CI
│   └── style.css             # Copié depuis static/
├── tests/                    # Tests + fixtures
│   ├── render_fixture.py     # Rendu hors-ligne avec valeurs source
│   └── fixtures/
├── .github/workflows/
│   └── generate.yml          # Pipeline CI (manuel + cron quotidien)
├── generate.py               # Point d'entrée (ticker → docs/index.html)
├── requirements.txt
└── README.md
```

---

## Édition d'une fiche (`content/ALSEN.yaml`)

Chaque valeur suivie a son propre fichier `content/<SYMBOLE>.yaml`. Le YAML
est strict : aucune extrapolation par rapport à la source documentée
(toujours citée en commentaire d'en-tête).

Sections principales :

| Section | Rôle |
|---|---|
| `ticker`, `isin`, `nom`, `marche`, `secteur`, `ville` | Identification |
| `pea_pme_eligible` | Booléen — affiché en badge |
| `liens` | Boursorama, Euronext, page IR |
| `alertes` | Cartes éditoriales, ordre = ordre d'affichage |
| `pipeline` | Programmes confirmés uniquement |
| `perspectives` | Court / moyen / long terme |
| `avis` | Note 0-10, intensité, texte personnel |
| `sources` | Liste explicite des sources citées |

### Structure d'une alerte

```yaml
alertes:
  - categorie: MOAT          # MOAT / CATALYSEUR / RISQUE / FINANCE / PIPELINE
    titre: Titre court de la carte
    description: |
      Texte multi-lignes, markdown léger autorisé.
      Doit pouvoir être rattaché à une source listée plus bas.
```

### Structure d'un programme pipeline

```yaml
pipeline:
  - programme: SENS-501 (OTOF-GT)
    indication: Surdité congénitale OTOF (~1 % des cas)
    stade: Phase 1/2
    stade_class: p1           # p1 / p2 / preclin / disc (couleurs CSS)
    prochaine_etape: Cohorte 3 (dose haute) · données durabilité
```

### Génération locale

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python generate.py --ticker ALSEN.PA
# Sortie : docs/index.html + docs/style.css
```

Option `--no-cache` pour ignorer le cache yfinance local (`.cache/`).

---

## Workflow GitHub Actions

Fichier : `.github/workflows/generate.yml`

Trois déclencheurs :

1. **Manuel** — bouton « Run workflow » dans l'onglet *Actions* du dépôt
   (`workflow_dispatch`).
2. **Push sur `main`** — uniquement si les fichiers utiles changent
   (code, templates, content, requirements).
3. **Cron quotidien** — `0 18 * * *` UTC, soit ~20:00 Paris été /
   ~19:00 Paris hiver, peu après la clôture Euronext (17:30 Paris).

Étapes du job :

1. Checkout du dépôt
2. Setup Python 3.11 (avec cache pip)
3. Installation des dépendances
4. `python generate.py` — régénère `docs/index.html` et `docs/style.css`
5. Si `docs/` a changé : commit auto par `github-actions[bot]` avec
   `[skip ci]` dans le message pour éviter une boucle de déclenchement,
   puis push direct sur `main`.

Un `concurrency.group: generate-fiche` empêche deux runs simultanés.

---

## Activation de GitHub Pages

À effectuer **une seule fois** par le propriétaire du dépôt :

1. Aller dans **Settings → Pages**.
2. Source : **Deploy from a branch**.
3. Branch : **`main`** / Folder : **`/docs`**.
4. **Save**.

Après quelques secondes, GitHub publie le site à l'URL :

> https://capx17.github.io/Fiches-Valeurs-PEA-PME/

Chaque commit auto sur `main` déclenche un redéploiement Pages
automatique (sans action manuelle).

---

## Note sur le range Fibonacci dynamique

Les niveaux Fibonacci affichés (23,6 % / 38,2 % / 50 % / 61,8 % / 78,6 %)
sont calculés dynamiquement à partir du **range 52 semaines yfinance live**
(`high_52w` − `low_52w`). Les valeurs en euros peuvent donc évoluer entre
deux régénérations si un nouveau plus haut ou plus bas annuel est touché.

Les seuils éditoriaux mentionnés dans le YAML (par exemple
*« résistance technique immédiate à 0,37 € (23,6 % Fib) »*) reflètent
l'instantané de la source d'origine et ne sont pas recalculés
automatiquement — ils restent volontairement figés pour traçabilité.

---

## Routines Claude planifiées (Pattern C+ allégé)

Deux routines Claude planifiées tournent chaque lundi matin **par fiche**
et écrivent directement sur `main`. Elles consomment des dumps Markdown
produits à chaque build CI dans `data/` et suivent des prompts-recettes
versionnés dans `prompts/`.

Toutes les routines appliquent le **Pattern C+ allégé** : sous-agent A
(générateur), sous-agent B (auditeur indépendant aveugle), sous-agent C
(méta-audit léger), puis auto-arbitrage R1-R5 par l'orchestrateur.
Aucune validation humaine intermédiaire — les conclusions des audits
baseline (`data/<TICKER>_audit_*.md`) et des recalibrages Pattern C+
(`data/<TICKER>_recalCplus_*.md`) constituent des **garde-fous figés**
intouchables, codifiés dans `AUDIT_REFERENCE_RAPPEL` (voir
`src/synthesis_dump.py`).

### Routine synthèse (lundi 9h00)

Régénère la section `synthese_ia` du YAML d'une fiche (score 0-10,
force du signal, texte 3 paragraphes, 5 facteurs +/-, date).
Input : `data/<TICKER>_synthese_input.md`.
Recette : `prompts/synthese_<TICKER>.md`.
Durée : 15-25 minutes.

### Routine éditoriale (lundi 9h15)

Modifie les sections `alertes`, `pipeline`, `perspectives` selon
l'actualité 7 jours (max 3 modifications par cycle).
Input : `data/<TICKER>_editorial_input.md` (état actuel + garde-fous
structurels + garde-fous hebdo durcis).
Recette : `prompts/editorial_<TICKER>.md`.
Durée : 15-25 minutes.

### Architecture des garde-fous

`AUDIT_REFERENCE_RAPPEL[ticker]` (dans `src/synthesis_dump.py`) contient
deux listes par ticker :

- **`garde_fous_structurels`** : faits stables issus des audits baseline
  + recalibrages Pattern C+. Toute modification les contredisant est
  bloquée par R3/R6 du méta-audit C.
- **`garde_fous_hebdo_durcis`** : règles procédurales communes (3 sources
  primaires concordantes pour un chiffre clé, suppression d'alerte
  < 30 jours bloquée, claim FAIBLE ignorée, modif score IA > 1 point
  exigeant justification 7 jours).

Ces deux blocs sont injectés UNIQUEMENT pour le ticker courant dans les
dumps `_synthese_input.md` et `_editorial_input.md` — pas de pollution
croisée entre fiches.

### Procédure : créer ou mettre à jour les routines Claude

Dans Claude (claude.ai/web ou app), pour chaque routine planifiée :

1. **Pour ALSEN** (existant) : mettre à jour les 2 routines Claude
   existantes en remplaçant leur prompt par le contenu actuel des
   fichiers :
   - `prompts/synthese_ALSEN.md` (routine synthèse, planifiée lundi 9h00)
   - `prompts/editorial_ALSEN.md` (routine éditoriale, planifiée lundi 9h15)

2. **Pour BE** (à créer) : créer 2 nouvelles routines planifiées avec
   les contenus de :
   - `prompts/synthese_BE.md` (lundi 9h00 ou autre créneau)
   - `prompts/editorial_BE.md` (lundi 9h15)

3. **Pour une nouvelle fiche** (futures valeurs) :
   - Créer `content/<TICKER>.yaml` (cf. structure d'une fiche).
   - Ajouter une entrée `AUDIT_REFERENCE_RAPPEL["<TICKER>"]` dans
     `src/synthesis_dump.py` (au moins les garde-fous baseline ; les
     hebdo durcis utilisent `HEBDO_DURCIS_DEFAULTS`).
   - Copier `prompts/_template_synthese.md` en
     `prompts/synthese_<TICKER>.md` et remplacer les `{TICKER}`,
     `{TICKER_BASE}`, `{NOM}`, `{IR_URL}`.
   - Idem pour `prompts/_template_editorial.md`.
   - Créer les 2 routines Claude planifiées correspondantes.

### Surveillance

Chaque cycle hebdo produit un fichier-log dans `data/` :
- `data/<TICKER>_routine_synthese_log_<date>.md`
- `data/<TICKER>_routine_editorial_log_<date>.md`

Ces logs détaillent les modifications appliquées (R1, R2) et bloquées
(R3, R4) avec la règle invoquée. Consultables via GitHub.

---

## Roadmap

- [x] Pipeline complet pour Sensorion (ALSEN.PA)
- [x] Régénération quotidienne via GitHub Actions
- [ ] Extension à d'autres valeurs (PEA-PME et hors PEA-PME, un YAML
      par valeur dans `content/`)
- [ ] Index multi-fiches sur la home `docs/index.html`
- [ ] Page d'historique éditorial (diff git rendu en HTML)

---

## Disclaimer

Ce dépôt n'est **ni une recommandation d'investissement, ni un conseil
en investissement** au sens des dispositions du Code monétaire et
financier. Les analyses publiées reflètent une opinion personnelle, sont
fournies à titre purement informatif et pédagogique, et peuvent être
erronées ou obsolètes. Investir en actions comporte un risque de perte
en capital pouvant aller jusqu'à la totalité du montant investi, en
particulier sur les compartiments small / micro-caps (notamment PEA-PME)
et sur les valeurs technologiques ou biotech.

Faites vos propres recherches (DYOR) et, si nécessaire, consultez un
conseiller en investissement financier (CIF) agréé.
