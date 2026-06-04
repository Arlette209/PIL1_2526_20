# PIL_2526_-20-
Projet intégrateur 

# PIL_2526_-20-

### 📄 Rapport Technique

Voici une version complète et détaillée. Elle intègre toute la démarche de configuration, la résolution des bugs critiques, la logique de l'algorithme de matching et le test d'interconnexion en réseau local que j'ai réalisé.

# Rapport Technique : Module 2 - Algorithme de Matching (Backend)

## 1. Environnement de Développement et Configuration
Le développement de ce module a été entièrement réalisé sous l'IDE **PyCharm Professional** en s'appuyant sur un environnement virtuel (`venv`) isolé. Cette configuration garantit la portabilité du code et évite les conflits de dépendances système.

* **Langage :** Python 3.14
* **Framework :** Flask (pour la création de l'API REST)
* **IDE :** PyCharm

---

## 2. Gestion Critique de la Base de Données (Migration PyMySQL)
Initialement, le projet devait utiliser le connecteur standard `mysql.connector`. Cependant, lors de la liaison avec le serveur Flask sous l'environnement Windows, le système rencontrait un crash critique persistant :
* **Erreur système :** Violation d'accès (Exit code `0xC0000005`).

La solution qui a été apportée pour remédier à ce problème est que l'architecture a été migrée vers la bibliothèque PyMySQL. Ce connecteur en Python pur a offert une stabilité parfaite. 
L'installation dans le `venv` a été complétée via le terminal de PyCharm avec la commande :
```bash
pip install pymysql

```

---

## 3. Optimisation du Code et Résolution des Bugs de Flux

Pendant la phase d'implémentation dans `matching.py`, deux corrections majeures ont permis de finaliser la route :

1. **Initialisation de l'objet curseur :** Correction de la ligne `cursor = conn.cursor()` (ajout des parenthèses) pour instancier un véritable curseur de base de données au lieu de manipuler par erreur l'objet fonction. Cela a résolu l'erreur `AttributeError: 'function' object has no attribute 'execute'`.
2. **Gestion sécurisée du cycle de vie SQL :** Structuration rigoureuse des blocs `try/except/finally` afin de garantir que chaque requête s'exécute proprement et que le curseur ainsi que la connexion soient systématiquement fermés, évitant que Flask ne renvoie une réponse vide (`None`).

---

## 4. Logique de l'Algorithme et Format d'API

La route `/matching` (méthode `GET`) prend en paramètre un `user_id` :

1. Elle vérifie le statut du mentorat de l'utilisateur (Filière, Niveau, et s'il s'agit d'une **DEMANDE** ou d'une **OFFRE**).
2. Elle inverse la recherche (si l'utilisateur a une Demande, l'algorithme cherche une Offre correspondante).
3. En cas d'absence de profil actif ou correspondant, le backend ne plante plus et retourne une structure JSON standardisée (Code `200 OK`) prête pour l'intégration Front-end :

```json
{
  "status": "success",
  "message": "Aucune demande ou offre active trouvée pour cet utilisateur.",
  "matches": []
}

```

---

## 5. Test d'Interconnexion et Déploiement Réseau (Multi-machines)

Pour valider l'utilisabilité de l'API par le reste de l'équipe (notamment pour l'intégration avec le développeur Front-end), un test en conditions réelles d'interconnexion a été mené.

* **Configuration réseau :Le serveur Flask a été configuré pour écouter sur toutes les interfaces réseau locales en modifiant le point d'entrée : `app.run(host='0.0.0.0', port=5000)`.
* Protocole de test : Un deuxième ordinateur a été connecté au même réseau Wi-Fi que la machine principale de développement.
* Résultat : En ciblant l'adresse IPv4 locale du serveur (ex: `http://<IP_LOCALE>:5000/matching?user_id=1`), le second ordinateur a pu interroger l'API avec succès et recevoir instantanément la structure JSON sans aucune perte de paquets ni blocage du pare-feu. L'API est donc officiellement prête à être partagée et consommée par l'application cliente.

```

---