# 📅 Calendrier de Prospection SEO — 1 Mois (Studio Riad)

**Objectif principal :** Obtenir des réponses pour des collaborations (shooting gratuit contre recommandation).
**Objectif SEO "caché" :** Susciter la curiosité des professionnels du mariage pour qu'ils visitent `www.studioriad.com`. Ce trafic qualifié (B2B local) est un excellent signal pour Google et améliorera drastiquement ton classement SEO naturel en Île-de-France.

## ⚙️ Comment utiliser ce planning ?

1. Tous les **2 jours**, ouvre ton fichier `.env`.
2. Modifie la ligne `SEARCH_QUERY=` avec la requête du jour.
3. Modifie la ligne `SEARCH_LIMIT=15` (ou plus si tu veux).
4. Ouvre le fichier `prospection.py` et remplace le bloc `PROMPT_TEMPLATE = """..."""` par celui correspondant au jour.
5. Lance le script : `python3 prospection.py` dans ton terminal.

---

## 🗓️ Semaine 1 : Les Piliers du Mariage

### 📍 Jour 1-2 : Les Domaines et Lieux de Réception
- **Requête dans le `.env` :** `SEARCH_QUERY=domaine mariage ile de france` ou `salle de mariage ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui rédige des emails de prospection B2B bienveillants.
Rédige un e-mail court (max 150 mots) avec :
- Accroche : j'ai découvert votre superbe domaine "{nom_etablissement}" et son cadre exceptionnel.
- Présentation : photographe et vidéaste de mariage chez Studio Riad.
- Proposition : je vous propose un shooting photo/vidéo gratuit de vos salles pour vos réseaux sociaux. La mise en valeur des espaces est cruciale pour les futurs mariés.
- Contrepartie : être ajouté à votre liste de prestataires recommandés.
- Clôture : si vous voulez voir mon approche esthétique, c'est ici : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 3-4 : Les Traiteurs
- **Requête dans le `.env` :** `SEARCH_QUERY=traiteur mariage prestige ile de france` ou `traiteur halal mariage ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui rédige des emails de prospection B2B chaleureux.
Rédige un e-mail court (max 150 mots) avec :
- Accroche : je suis tombé sur l'excellence de votre service traiteur "{nom_etablissement}".
- Présentation : je suis photographe/vidéaste mariage (Studio Riad).
- Proposition : je sais à quel point le visuel de vos créations culinaires et buffets est important. Je vous propose un shooting gratuit de votre prochain cocktail/buffet pour votre com.
- Contrepartie : en échange d'une petite recommandation auprès de vos futurs mariés.
- Clôture : n'hésitez pas à jeter un oeil à ma façon de sublimer les événements : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 5-6 : Les Negafas & Zianas
- **Requête dans le `.env` :** `SEARCH_QUERY=negafa ile de france` ou `ziana paris ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui rédige des emails de prospection respectueux.
Rédige un e-mail court (max 150 mots) avec :
- Accroche : j'ai vu votre magnifique travail de mise en beauté chez "{nom_etablissement}".
- Présentation : je suis vidéaste et photographe de mariage (Studio Riad).
- Proposition : la qualité des robes et des parures mérite des images parfaites. Je vous propose un shooting gratuit de l'une de vos tenues ou d'un shooting inspiration.
- Contrepartie : un simple échange de recommandations.
- Clôture : pour voir le rendu de mes vidéos et photos de mariage : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

---

## 🗓️ Semaine 2 : L'Organisation et l'Animation

### 📍 Jour 7-8 : Les Wedding Planners
- **Requête dans le `.env` :** `SEARCH_QUERY=wedding planner paris ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui rédige des emails pour des agences d'événementiel.
Rédige un e-mail direct (max 150 mots) avec :
- Accroche : j'apprécie beaucoup l'élégance des mariages organisés par "{nom_etablissement}".
- Présentation : je suis photographe/vidéaste (Studio Riad), habitué aux mariages sur-mesure.
- Proposition : je connais vos exigences d'image. Je serais ravi de vous accompagner gratuitement sur un shooting de l'une de vos "tables d'inspiration" ou décorations.
- Contrepartie : intégrer votre short-list de photographes fiables.
- Clôture : au plaisir d'en discuter. Vous pouvez voir mon univers complet sur www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 9-10 : Les Décorateurs Floraux (Fleuristes Mariage)
- **Requête dans le `.env` :** `SEARCH_QUERY=fleuriste decoration mariage ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui écrit à des fleuristes de mariage.
Rédige un e-mail court (max 150 mots) avec :
- Accroche : le design floral de "{nom_etablissement}" a attiré mon attention.
- Présentation : photographe de mariage (Studio Riad).
- Proposition : les mariés adorent la déco, mais les fleurs fanent vite. Je vous propose d'immortaliser gratuitement l'une de vos prochaines grandes installations (arche, centres de table) pour votre portfolio.
- Contrepartie : me recommander si vos mariés cherchent un photographe.
- Clôture : portfolio et exemples de mariages sur www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 11-12 : Les DJ & Animateurs
- **Requête dans le `.env` :** `SEARCH_QUERY=dj mariage ile de france` ou `dj mariage oriental ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui écrit à des animateurs/DJ.
Rédige un e-mail cool mais pro (max 150 mots) avec :
- Accroche : belle énergie sur vos prestations chez "{nom_etablissement}".
- Présentation : vidéaste et photographe événementiel (Studio Riad).
- Proposition : c'est très dur pour un DJ d'avoir des belles vidéos de lui en pleine action. Je passe vous filmer gratuitement 30 min sur un prochain événement pour vous faire une vidéo promo.
- Contrepartie : un petit mot sur moi quand vos clients cherchent un photographe.
- Clôture : mon style vidéo (très dynamique) est visible sur www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

---

## 🗓️ Semaine 3 : Beauté et Logistique

### 📍 Jour 13-14 : Robes de Mariée & Costumes
- **Requête dans le `.env` :** `SEARCH_QUERY=boutique robe de mariee paris ile de france` ou `costume sur mesure mariage ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui écrit à des créateurs de robes/costumes.
Rédige un e-mail élégant (max 150 mots) avec :
- Accroche : la délicatesse des créations de "{nom_etablissement}" m'a beaucoup plu.
- Présentation : photographe de mariage (Studio Riad) spécialisé dans les détails.
- Proposition : je propose la réalisation d'un mini-éditorial photo gratuit de votre nouvelle collection pour sublimer les matières et les coupes sur vos réseaux.
- Contrepartie : me laisser quelques flyers en boutique ou me recommander.
- Clôture : mon regard photo est à découvrir sur www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 15-16 : Les Cake Designers / Pâtissiers
- **Requête dans le `.env` :** `SEARCH_QUERY=cake designer mariage paris ile de france` ou `piece montee mariage ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui écrit à des artisans pâtissiers.
Rédige un e-mail très bienveillant (max 150 mots) avec :
- Accroche : bluffé par la beauté de vos Wedding Cakes chez "{nom_etablissement}".
- Présentation : photographe et vidéaste événementiel (Studio Riad).
- Proposition : un gâteau de mariage est une oeuvre d'art éphémère. Je vous propose un mini-shooting gratuit en studio ou sur un événement pour des photos ultra-qualitatives de vos gâteaux texturés.
- Contrepartie : un renvoi d'ascenseur en me recommandant à vos futurs mariés.
- Clôture : rendez-vous sur www.studioriad.com pour voir ce que je fais.

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 17-18 : Maquilleuses & Coiffeuses (MUA)
- **Requête dans le `.env` :** `SEARCH_QUERY=makeup artist mariage ile de france` ou `coiffeuse mariage domicile ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui écrit à des professionnelles de la beauté.
Rédige un e-mail sympa et direct (max 150 mots) avec :
- Accroche : j'aime beaucoup le style de vos mises en beauté, "{nom_etablissement}".
- Présentation : ici Studio Riad, photographe/vidéaste mariage.
- Proposition : avoir de vraies photos pro (avant/après ou pendant les préparatifs) change tout pour vendre votre prestation. Je peux shooter un essai makeup gratuitement pour votre feed.
- Contrepartie : me glisser dans vos recommandations mariées.
- Clôture : portfolio et vidéos backstage : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

---

## 🗓️ Semaine 4 : Prestataires Additionnels

### 📍 Jour 19-20 : Location de Voitures de Prestige
- **Requête dans le `.env` :** `SEARCH_QUERY=location voiture de luxe mariage ile de france` ou `voiture ancienne mariage ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui écrit à des loueurs de véhicules.
Rédige un e-mail percutant (max 150 mots) avec :
- Accroche : superbe flotte automobile chez "{nom_etablissement}" !
- Présentation : vidéaste et photographe mariage (Studio Riad).
- Proposition : de belles images de vos véhicules en action (drones, détails cuir/carrosserie) convertissent mieux. Je réalise pour vous une courte vidéo promo gratuitement.
- Contrepartie : me recommander à vos clients (qui n'ont parfois pas encore de photographe).
- Clôture : exemple de rendus dynamiques sur mon site : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 21-22 : Groupes de Musique / Orchestres
- **Requête dans le `.env` :** `SEARCH_QUERY=orchestre mariage paris ile de france` ou `groupe de musique mariage ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui contacte des formations musicales.
Rédige un e-mail chaleureux (max 150 mots) avec :
- Accroche : j'ai vu des extraits de vos lives avec "{nom_etablissement}" et ça donne envie !
- Présentation : photographe et vidéaste de mariage (Studio Riad).
- Proposition : aujourd'hui, la vidéo est cruciale pour vendre une prestation musicale. Je vous filme gratuitement sur 2/3 morceaux lors d'un vin d'honneur pour vous faire un beau teaser.
- Contrepartie : me citer en recommandation "photographe" à vos futurs mariés.
- Clôture : pour voir ce que je crée de façon musicale et dynamique : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 23-24 : Bijouteries & Alliances
- **Requête dans le `.env` :** `SEARCH_QUERY=bijouterie alliance mariage paris` ou `createur alliance sur mesure ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui écrit à des artisans joailliers.
Rédige un e-mail élégant et poli (max 150 mots) avec :
- Accroche : admiratif de la finesse de vos créations chez "{nom_etablissement}".
- Présentation : photographe de mariage (Studio Riad), habitué aux close-up d'alliances.
- Proposition : je serais honoré de photographier gratuitement quelques-unes de vos parures/alliances en studio pour vos fiches produits ou vos réseaux, avec un éclairage macro.
- Contrepartie : petit échange de visibilité auprès des couples qui poussent votre porte.
- Clôture : mes images et mon souci du détail sont ici : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

---

## 🗓️ Semaine 5 : Les Compléments

### 📍 Jour 25-26 : Location de Photobooth
- **Requête dans le `.env` :** `SEARCH_QUERY=location photobooth borne photo mariage ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui écrit à des loueurs de box photos.
Rédige un e-mail professionnel et direct (max 150 mots) avec :
- Accroche : superbes bornes proposées par "{nom_etablissement}".
- Présentation : je suis photographe de mariage (Studio Riad) !
- Proposition : nous sommes souvent complémentaires. Plutôt qu'un shooting, je voulais savoir si vous souhaitiez créer un package "Photo + Borne" pour nos futurs mariés ?
- Contrepartie : on se recommande mutuellement pour augmenter nos ventes à tous les deux sur la saison de mariage.
- Clôture : jette un oeil à mon site pour voir si on "matche" professionnellement : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 27-28 : Loueurs de Matériel & Mobilier
- **Requête dans le `.env` :** `SEARCH_QUERY=location materiel reception mariage ile de france` ou `location tente mariage ile de france`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui contacte des prestataires logistiques.
Rédige un e-mail orienté B2B (max 150 mots) avec :
- Accroche : félicitations pour la qualité du parc matériel de "{nom_etablissement}".
- Présentation : vidéaste et photographe mariage (Studio Riad).
- Proposition : vos tentes et chaises habillent nos mariages. J'aimerais faire de belles photos grand-angle et drone d'une de vos prochaines grosses installations pour vous fournir des visuels pros pour votre site.
- Contrepartie : me garder dans vos petits papiers pour vos mariés qui cherchent.
- Clôture : visitez mon site pour voir comment je mets en valeur les lieux : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

### 📍 Jour 29-30 : Papeterie et Faire-parts
- **Requête dans le `.env` :** `SEARCH_QUERY=createur faire part mariage ile de france` ou `imprimerie papeterie mariage paris`
- **Prompt pour `prospection.py` :**
```python
PROMPT_TEMPLATE = """Tu es un assistant qui écrit à des créateurs de faire-parts.
Rédige un e-mail très doux (max 150 mots) avec :
- Accroche : le travail de typographie et papier de "{nom_etablissement}" est superbe.
- Présentation : photographe de mariage (Studio Riad), passionné par le "flatlay" (photo d'objets à plat).
- Proposition : je cherche souvent de beaux faire-parts pour mes compositions de début de journée (préparatifs). Je vous propose de photographier/mettre en scène gratuitement vos collections en studio.
- Contrepartie : en échange, on se recommande auprès de notre future clientèle mariage !
- Clôture : mon univers esthétique, si vous souhaitez regarder : www.studioriad.com

Signature :
B. Riad
www.studioriad.com | 06 15 69 28 39
(Ne mets pas de ligne d'objet en haut du texte généré.)"""
```

---
> 💡 **Le Hack SEO final :** N'oublie pas : même si l'établissement ne répond jamais à l'e-mail, la psychologie humaine fait que le responsable ira par politesse ou par curiosité cliquer sur le lien "www.studioriad.com" pour voir qui tu es. **Des centaines de clics de professionnels d'Ile-de-France sur un mois, c'est l'un des meilleurs signaux pour faire remonter ton propre site sur les requêtes Google "Photographe Mariage Ile de France" !**
