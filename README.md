# PIL_2526_-20-
Projet intégrateur 

# PIL_2526_-20-

Projet intégrateur

##  Configuration du Backend & Stabilisation (Module 2)

Ce module a été entièrement configuré et stabilisé sous l'IDE **PyCharm** en utilisant un environnement virtuel (`venv`).

### 📦 Dépendances et Commandes de Configuration
Pour faire fonctionner la base de données locale avec l'application Flask de manière stable sous Windows, nous avons migré le connecteur SQL vers **PyMySQL** (pour éviter les erreurs critiques système de violation d'accès `0xC0000005`).

Exécuter la commande suivante dans le terminal de l'environnement virtuel pour installer la dépendance :
```bash
pip install pymysql