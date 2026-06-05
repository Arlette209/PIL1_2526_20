# PIL_2526_-20-
Projet intégrateur 

# Module 4 : Algorithme de Matching et Gestion du Mentorat
**Membre 4 :** Daniel AHOUANSOU  
**Rôle :** Algorithme & Traitement de métier 

---

## 1. Présentation du Module
Ce module gère la mise en relation (matching) automatisée entre les étudiants demandeurs d'aide et les mentors disponibles sur la plateforme **IFRI MentorLink**. Il fournit une API REST robuste pour publier et récupérer les offres et les demandes, ainsi qu'un algorithme de calcul de pertinence pour associer les profils.

## 2. Structure de l'Espace de Travail (`Daniel_Workspace/`)
Tous les composants du module sont centralisés de manière autonome dans ce dossier afin d'éviter tout conflit avec le reste de l'équipe :
* `app_M4.py` : Point d'entrée de l'application Flask, configuration du serveur, encodage UTF-8 et gestion des règles CORS.
* `backend_M4/` : Package Python contenant la logique métier.
  * `matching.py` : Contrôleur principal contenant les routes API (`/offres`, `/demandes`, `/matching`) et l'algorithme de score.
  * `__init__.py` : Fichier d'initialisation du package Python.
* `ifri_mentorlink.sql` & `TP_MATCHING.sql` : Scripts d'initialisation de la base de données relationnelle et jeux de données de test.

## 3. Fonctionnement de l'Algorithme de Matching
L'algorithme filtre d'abord les mentors qui possèdent au moins une compétence recherchée par le demandeur. Ensuite, il évalue chaque profil sur un total de **100 points** selon les critères du cahier des charges :

1. **Format du Mentorat (Score de base) :**
   * Format `PRESENTIEL` : `+50 points`
   * Format `EN_LIGNE` / `EN LIGNE` : `+40 points`
2. **Bonus de Filière (Croisement) :**
   * Si le mentor appartient à la **même filière** que le demandeur (ex: GL - GL) : `+20 points`
   * Si les filières sont différentes : `+0 point`

*Le score final est plafonné à 100 points et la liste des mentors trouvés est triée par **ordre décroissant** (du score le plus élevé au plus bas).*

### Exemple de comportement (Données de test) :
Pour un demandeur en filière **GL** :
* **Mentor Jean (Présentiel + Même filière GL)** : Score = 50 + 20 = **70 points** (Proposé en 1ère position).
* **Mentor Marie (En Ligne + Filière IA)** : Score = 40 + 0 = **40 points** (Proposé en 2ème position).

## 4. Guide de Lancement et Déploiement

### Prérequis
* Python installed (avec l'environnement virtuel `venv` configuré à la racine)
* Serveur MySQL actif avec la base `ifri_mentorlink` importée.

### Commandes de démarrage
1. Accéder à l'espace de travail :
   ```bash
   cd Daniel_Workspace