# 📕 MANUEL : Automatisation de la Prospection SEO (30 Jours)

Ce document explique comment utiliser le système de prospection automatisé.

## 🚀 Lancer un seul jour

Pour lancer la prospection d'un jour précis :

```bash
# Exemple pour le Jour 3 (Traiteurs prestige)
python3 prospection.py --day 3

# Mode test (1 seul brouillon pour vérifier)
python3 prospection.py --day 3 --test

# Nombre de prospects personnalisé
python3 prospection.py --day 3 --count 15
```

---

## 🔥 Lancer le BATCH (plusieurs jours d'affilée)

Le script batch enchaîne automatiquement les jours avec pause entre chaque.

```bash
# Lancer les jours 3 à 30 (10 prospects/jour, 30s de pause)
python3 scripts/run_batch.py

# Reprendre là où on s'est arrêté (skip des jours déjà faits)
python3 scripts/run_batch.py --resume

# Aperçu du plan SANS exécuter (dry run)
python3 scripts/run_batch.py --dry

# Options personnalisées
python3 scripts/run_batch.py --start 5 --end 15 --count 5 --pause 60
```

### Options du batch

| Option | Description | Défaut |
| :--- | :--- | :--- |
| `--start X` | Jour de départ | `3` |
| `--end X` | Jour de fin | `30` |
| `--count N` | Prospects par jour | `10` |
| `--pause N` | Secondes de pause entre jours | `30` |
| `--test` | 1 seul brouillon par jour | — |
| `--dry` | Affiche le plan sans envoyer | — |
| `--resume` | Saute les jours déjà complétés | — |

---

## 🛠️ Options pour un seul jour

| Option | Description | Exemple |
| :--- | :--- | :--- |
| `--day X` | **Obligatoire.** Charge la config du jour X (1 à 30). | `--day 5` |
| `--test` | Crée **un seul** brouillon (recommandé pour vérifier). | `--day 1 --test` |
| `--count N` | Définit le nombre de prospects à chercher. | `--day 1 --count 20` |

---

## 📂 Structure du Système

- **`prospection.py`** : Le moteur de scraping et d'envoi (usage journalier).
- **`scripts/run_batch.py`** : Lance automatiquement plusieurs jours d'affilée.
- **`roadmap.json`** : Configuration des 30 jours (ne pas modifier).
- **`prospection_log.csv`** : Historique des envois (anti-doublons).
- **`batch_log.json`** : Log de progression du batch (pour reprise).

---

## 📅 Roadmap des 30 Jours

| Jours | Cible |
| :--- | :--- |
| 1–2 | Domaines & lieux de mariage |
| 3–4 | Traiteurs prestige |
| 5–6 | Negafa / mises en beauté |
| 7–8 | Wedding Planners |
| 9–10 | Fleuristes mariage |
| 11–12 | DJ & Animateurs |
| 13–14 | Boutiques robes de mariée |
| 15–16 | Cake Designers |
| 17–18 | Makeup Artists |
| 19–20 | Location voitures de luxe |
| 21–22 | Orchestres mariage |
| 23–24 | Bijouteries / Joaillers |
| 25–26 | Location Photobooth |
| 27–28 | Location matériel réception |
| 29–30 | Créateurs faire-parts |
