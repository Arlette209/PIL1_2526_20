# ============================================
# app.py - Point d'entrée de l'application
# Membre 3 : Persistance des profils
# IFRI_MentorLink
# ============================================

from flask import Flask
import pymysql

# Création de l'application Flask
app = Flask(__name__)

# ---- Configuration de la base de données ----
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ifri2026',
    'database': 'ifri_mentorlink',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    """Retourne une connexion à la base de données"""
    return pymysql.connect(**DB_CONFIG)

# Enregistrement des routes du profil
from routes import profile_bp
app.register_blueprint(profile_bp)

# Lancement du serveur en mode debug
if __name__ == '__main__':
    app.run(debug=True)