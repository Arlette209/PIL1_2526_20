# Rapport journalier – Membre 3
**Date : 05 juin 2026**

## Ce que j'ai fait aujourd'hui

J'ai terminé l'implémentation des endpoints PUT pour `/profile`, 
`/competences`, `/lacunes` et `/disponibilites`, ce qui permet 
maintenant de modifier les données directement dans la base de données 
MySQL.

J'ai également ajouté la fonctionnalité d'upload de photo de profil 
via l'endpoint `POST /profile/<user_id>/photo`.

Au départ j'avais connecté mon système à la base de données avec 
flask_mysqldb, mais après concertation avec l'équipe, on a décidé 
d'utiliser pymysql comme les autres membres. J'ai donc migré tout 
mon code vers pymysql pour assurer la cohérence du projet.

J'ai aussi participé à la réunion d'équipe pour faire le point sur 
l'avancement de chacun.

## Difficultés rencontrées

J'ai rencontré quelques difficultés notamment lors de la migration 
vers pymysql et le débogage des endpoints PUT, mais j'ai réussi à 
les résoudre.

## Ce qui reste à faire

- Attendre que tous les membres terminent leurs modules
- Le Membre 1 fusionnera tous les codes en un seul projet
- Rédiger le rapport final en HTML avec toute l'équipe