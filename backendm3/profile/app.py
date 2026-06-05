# ============================================
# app.py - Point d'entrée de l'application
# Membre 3 : Persistance des profils
# IFRI_MentorLink
# ============================================

from flask import Flask
from flask_mysqldb import MySQL

# Création de l'application Flask
app = Flask(__name__)

# ---- Configuration de la base de données ----
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ifri2026'
app.config['MYSQL_DB'] = 'ifri_mentorlink'

# Initialisation de MySQL
mysql = MySQL(app)

# Enregistrement des routes du profil
from routes import profile_bp
app.register_blueprint(profile_bp)

# Lancement du serveur en mode debug
if __name__ == '__main__':
    app.run(debug=True)