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

## Routines Claude planifiées

Deux routines Claude planifiées tournent chaque lundi matin et écrivent
directement sur `main`. Elles consomment des dumps Markdown produits à
chaque build CI dans `data/` et suivent des prompts-recettes versionnés
dans `prompts/`.

### Routine synthèse (lundi 9h00)

Régénère la section `synthese_ia` de `content/ALSEN.yaml` (score 0-10,
force du signal, texte d'analyse factuelle neutre, facteurs ± , date).
Input : `data/ALSEN_synthese_input.md`. Recette : `prompts/synthese_ALSEN.md`.

### Routine éditoriale hebdomadaire avec auto-audit (lundi 9h15)

Une seconde routine Claude planifiée chaque lundi à 9h15 (15 min après
la routine synthèse) analyse l'actualité et propose des mises à jour
éditoriales sur `content/ALSEN.yaml`. Avant tout commit, un auto-audit
strict vérifie chaque modification selon une checklist binaire (sources
primaires, cohérence avec l'audit du 01/05/2026, format YAML, etc.).
Si l'audit échoue, aucune modification n'est appliquée — un rapport
d'échec est créé à la place dans `data/ALSEN_editorial_log_[date].md`.

L'utilisateur peut consulter les rapports hebdomadaires pour comprendre
ce qui a été appliqué ou bloqué et, le cas échéant, appliquer
manuellement les modifications bloquées.

Input : `data/ALSEN_editorial_input.md` (état actuel + garde-fous audit).
Recette : `prompts/editorial_ALSEN.md`.

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
