# 📘 **Documentation Technique - Module Matching et Gestion du Mentorat (Membre 4)**

**PIL_2526_-20-**
**Projet Intégrateur (IFRI MentorLink)**
**Membre 4 : Daniel AHOUANSOU Rôle : Algorithme de Matching & Logique Métier Backend**

## **1. Structure Détaillée de l'Espace de Travail (backend_membre4_matching/)**

Tous les composants de ce module sont entièrement centralisés et isolés de manière autonome dans ce répertoire afin de garantir une intégration propre sur le dépôt GitHub de l'équipe et d'éviter tout conflit de fusion (merge conflict) :

backend_membre4_matching/
│
├── app_M4.py               # Point d'entrée principal de l'application Flask
├── TP_MATCHING.sql         # Script d'initialisation de la BDD et jeux de données tests
│
└── matching/               # Package Python contenant le cœur du module
    ├── init.py             # Initialisation du package pour les imports Python
    ├── matching.py         # Contrôleur, routes de l'API (Blueprint) et requêtes SQL
    └── README_Matching.md  # La présente documentation technique

**Rôle précis des fichiers :**
app_M4.py : Point d'entrée principal de l'application Flask, configuration globale du serveur (port 5000), encodage UTF-8 et gestion de la sécurité via Flask-CORS.
TP_MATCHING.sql : Script d'initialisation de la base de données relationnelle locale et jeu de données de test (insertions de profils fictifs).
matching/matching.py : Contrôleur principal contenant les routes d'API (Blueprints), les requêtes de jointures SQL et l'algorithme de scoring.
matching/README_Matching.md : La présente documentation technique.

## **2. Fonctionnement Approfondi de l'Algorithme de Matching**

L'algorithme extrait dynamiquement les données relationnelles et évalue chaque profil de mentor potentiel pour un apprenant donné. Le score final est calculé de manière cumulative sur un total de 100 points maximum.

**Étape 1 : Le Pré-filtrage par Compétences**
Avant de calculer les scores, l'algorithme utilise des requêtes SQL avec jointures internes (INNER JOIN) pour ne retenir que les mentors possédant au moins une compétence en commun avec celles recherchées dans la demande de l'apprenant.

**Étape 2 : Le Calcul des Scores Évaluatifs**
Sur les profils filtrés, l'algorithme applique le barème de scoring suivant :
Format du Mentorat (Score de base - Max 50 points) : Si le mentor propose un format en PRESENTIEL : +50 points
Si le mentor propose un format EN_LIGNE ou EN LIGNE : +40 points
Bonus de Filière Académique (Max 20 points) : L'algorithme compares la filière de l'apprenant et celle du mentor.
Si les filières correspondent exactement (ex: Génie Logiciel - Génie Logiciel) : +20 points
Si les filières sont différentes (ex: Génie Logiciel - Sécurité Informatique) : +0 point
Poids des Compétences Communes (Max 30 points) : Chaque correspondance exacte (exact match) sur une compétence technique ajoute des points supplémentaires au score global de l'algorithme.

**Étape 3 : Le Mécanisme de Tri et Classement**
Une fois les scores individuels calculés, l'algorithme effectue un tri par ordre décroissant (du score le plus élevé au plus bas). Les mentors les plus pertinents par rapport au profil académique et aux besoins de l'apprenant sont placés en tête de liste dans la structure de données JSON.

## **3. Endpoints de l'API REST & Spécifications des Réponses JSON**

Le serveur backend écoute par défaut sur le port 5000.

💡 **NOTA BENE POUR L'ÉQUIPE :**
Pour des tests individuels sur mon propre machine, j'utilise l'adresse "localhost".
Pour interconnecter le Frontend (Membre 1/2) avec ce Backend, vous devez obligatoirement vous connecter au même réseau Wi-Fi que moi et utiliser mon adresse IP réseau actuelle (ex: 192.168.1.103).

### **3.1. Vérification du Statut du Serveur**
URL (Local) : GET http://localhost:5000/
URL (Réseau Équipe) : GET http://192.168.1.103:5000/
Description : Route d'index permettant de valider la connectivité réseau.
Code de retour HTTP : 200 OK
Format de la réponse : { "status": "success", "message": "Le serveur Flask du Module 4 (Matching) est en ligne et prêt !" }

### **3.2. Récupération des Offres de Mentorat**
URL (Local) : GET http://localhost:5000/offres
URL (Réseau Équipe) : GET http://192.168.1.103:5000/offres
Description : Renvoie la liste brute de toutes les offres de mentorat actives.
Code de retour HTTP : 200 OK

### **3.3. Récupération des Demandes d'Aide**
URL (Local) : GET http://localhost:5000/demandes
URL (Réseau Équipe) : GET http://192.168.1.103:5000/demandes
Description : Renvoie la liste de toutes les requêtes de soutien postées par les apprenants.
Code de retour HTTP : 200 OK

### **3.4. Exécution de l'Algorithme de Matching Classé**
URL (Local) : GET http://localhost:5000/matching?user_id=1
URL (Réseau Équipe) : GET http://192.168.1.103:5000/matching?user_id=1
Paramètre requis : user_id (L'identifiant unique de l'apprenant).
Description : Traite les besoins de l'étudiant spécifié, exécute la logique de scoring SQL et retourne la liste des mentors classés par ordre de pertinence.
Code de retour HTTP : 200 OK

## **4. Guide de Lancement et Connexion Réseau (Équipe)**

**Prérequis Systèmes**
Python 3.x installé globalement sur la machine.
Environnement virtuel Python (venv) activé.
Serveur de base de données démarré avec la base ifri_mentorlink.

**Procédure d'Interconnexion :**
Nous devons connecter toutes les machines de l'équipe (Frontend et Backend) sur le même point d'accès Wi-Fi.
Maintenant, moi je lance le serveur depuis mon terminal avec : python backend_membre4_matching/app_M4.py
On note l'adresse IP qui s'affiche dans la console de démarrage (ex: Running on http://192.168.1.103:5000).
Les membres du Frontend doivent simplement utiliser cette IP dans leurs configurations pour envoyer les requêtes vers mon serveur.

⚠️ **NOTE SUR LA BASE DE DONNÉES LOCALES :** Les identifiants de connexion MySQL présents dans le code de connexion (matching.py) correspondent à ma configuration locale. Si vous récupérez ce code pour exécuter le serveur sur votre propre machine, veillez à modifier la chaîne de connexion avec vos propres identifiants (Utilisateur root et mot de passe local).