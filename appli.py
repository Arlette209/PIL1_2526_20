from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
import pymysql
from functools import wraps

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'cle_secrete_pour_mentorlink_ifri'


def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',       
        password='015058',  
        database='ifri_mentorlink',
        cursorclass=pymysql.cursors.DictCursor
    )


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Accès refusé. Veuillez vous connecter."}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API opérationnelle"})

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return jsonify({
        "message": f"Bienvenue sur ton espace privé, ID utilisateur : {session['user_id']}"
    })


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')
    filiere = data.get('filiere')
    niveau = data.get('niveau')
    
    if not all([nom, prenom, email, mot_de_passe, filiere, niveau]):
        return jsonify({"error": "Veuillez remplir tous les champs"}), 400

    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        sql_check = "SELECT id_utilisateur FROM Utilisateurs WHERE email = %s"
        cursor.execute(sql_check, (email,))
        if cursor.fetchone():
            return jsonify({"error": "Cet email est déjà utilisé"}), 400
        
        hashed_password = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')
        
        sql_insert = """
            INSERT INTO Utilisateurs (nom, prenom, email, mot_de_passe, filiere, niveau) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert, (nom, prenom, email, hashed_password, filiere, niveau))
        connection.commit()
        return jsonify({"message": "Inscription réussie !"}), 201

    except Exception as e:
        return jsonify({"error": f"Erreur serveur : {str(e)}"}), 500
    finally:
        if connection is not None:
            connection.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')
    
    if not email or not mot_de_passe:
        return jsonify({"error": "Veuillez remplir tous les champs"}), 400

    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        sql = "SELECT * FROM Utilisateurs WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Identifiants incorrects"}), 401
            
        if bcrypt.check_password_hash(user['mot_de_passe'], mot_de_passe):
            session['user_id'] = user['id_utilisateur']
            session['user_nom'] = user['nom']
            
            return jsonify({
                "message": "Connexion réussie !",
                "utilisateur": {
                    "id": user['id_utilisateur'],
                    "nom": user['nom'],
                    "prenom": user['prenom'],
                    "filiere": user['filiere'],
                    "niveau": user['niveau']
                }
            }), 200
        else:
            return jsonify({"error": "Identifiants incorrects"}), 401
            
    except Exception as e:
        return jsonify({"error": f"Erreur serveur : {str(e)}"}), 500
    finally:
        if connection is not None:
            connection.close()


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Déconnexion réussie"}), 200


@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    nouveau_mot_de_passe = data.get('nouveau_mot_de_passe')
    
    if not email or not nouveau_mot_de_passe:
        return jsonify({"error": "Veuillez remplir tous les champs"}), 400
        
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
    
        
        sql_check = "SELECT id_utilisateur FROM Utilisateurs WHERE email = %s"
        cursor.execute(sql_check, (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Aucun compte associé à cet email"}), 404
            
        
        new_hashed_password = bcrypt.generate_password_hash(nouveau_mot_de_passe).decode('utf-8')
        
        
        sql_update = "UPDATE Utilisateurs SET mot_de_passe = %s WHERE email = %s"
        cursor.execute(sql_update, (new_hashed_password, email))
        connection.commit()
        
        return jsonify({"message": "Mot de passe réinitialisé avec succès !"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erreur serveur : {str(e)}"}), 500
    finally:
        if connection is not None:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)