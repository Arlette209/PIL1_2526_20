# Rapport journalier – Membre 3
**Date : 04 juin 2026**

## Ce que j'ai fait aujourd'hui

J'ai commencé par installer tous les outils nécessaires pour accomplir 
ma tâche : Python, Flask, MySQL Workbench, Postman, Git et GitHub.

Ensuite j'ai créé la structure de mon module back-end avec les fichiers 
`app.py`, `models.py`, `controllers.py` et `routes.py`. J'ai développé 
les endpoints GET pour `/profile`, `/competences`, `/lacunes` et 
`/disponibilites` qui permettent de récupérer les informations du profil 
d'un utilisateur.

J'ai aussi connecté mon application Flask à la base de données MySQL en 
utilisant le schéma SQL fourni par le Membre 1. J'ai testé mes endpoints 
avec Postman et le navigateur pour vérifier qu'ils fonctionnent correctement.

Enfin j'ai fait mon premier commit et push sur le dépôt GitHub du groupe.

## Difficultés rencontrées

J'ai rencontré quelques difficultés notamment avec la configuration de Git 
et la connexion entre Flask et MySQL, mais j'ai réussi à les résoudre.

## Prochaines étapes

- Implémenter les endpoints PUT pour modifier les données dans la vraie 
base de données
- Gérer l'upload des photos de profil
-Récupérer le code  du membre 2 pour intégrer l'authentification
-Adapter mes endpoints pour utiliser le user_id de l'utilisateur connecté