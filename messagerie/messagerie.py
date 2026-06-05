
# === CONFIGURATION DE BASE ===
# On initialise Flask et on configure SocketIO pour accepter les requêtes de n'importe où (CORS).
# Ensuite, on crée automatiquement le dossier 'static/uploads' s'il n'existe pas, 
# c'est là qu'on va ranger toutes les images et vidéos envoyées, avec une limite de 16 Mo pour ne pas saturer le serveur.
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

#On Défini le dossier où seront stockés les fichiers reçus
DOSSIER_UPLOADS = os.path.join(os.getcwd(), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = DOSSIER_UPLOADS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite la taille à 16 Mo par fichier

#On Crée le dossier s'il n'existe pas encore
if not os.path.exists(DOSSIER_UPLOADS):
    os.makedirs(DOSSIER_UPLOADS)

# Fonction centralisée pour appeler MySQL. 
# À chaque fois qu'une route a besoin de lire ou écrire des messages, elle appelle cette fonction.
# N'oublie pas de changer le mot de passe ici si tu testes sur ta propre machine !
def connexion_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Casemiro2008",
        database="ifri_mentorlink"
    )

@app.route('/messagerie')

def afficher_messagerie():
    return render_template('messagerie.html')

@socketio.on('rejoindre')

# On assigne l'utilisateur à un canal privé unique (ex: canal_5) dès qu'il se connecte.
def gérer_connexion(donnes):
    user_id = donnes['user_id']
    join_room(f"canal_{user_id}")

@socketio.on('envoyer_message')


def gerer_nouveau_message(donnees):
    id_conversation = donnees['conversation_id']
    id_expediteur = donnees['expediteur_id']
    id_destinataire = donnees['destinataire_id']
    texte = donnees['contenu']

    # 1. Connexion à MySQL et enregistrement
    conn = connexion_db()
    curseur = conn.cursor()
    
    requete = """
        INSERT INTO messages (conversation_id, expediteur_id, contenu,lu) 
        VALUES (%s, %s, %s,%s)
    """
    valeurs = (id_conversation, id_expediteur, texte, False)
    curseur.execute(requete, valeurs)
    conn.commit()
    
    curseur.close()
    conn.close()

    # 2. Envoi de la notification en temps réel au destinataire
    donnees_notification = {
        'conversation_id': id_conversation,
        'expediteur_id': id_expediteur,
        'contenu': texte
    }
    emit('nouveau_message_recu', donnees_notification, room=f"canal_{id_destinataire}")
@socketio.on('charger_messages')
def gerer_chargement_messages(donnees):
    id_conversation = donnees['conversation_id']
    
    # 1. Connexion à la base de données
    conn = connexion_db()
    curseur = conn.cursor(dictionary=True) # dictionary=True permet de récupérer les lignes sous forme de dictionnaires faciles à envoyer
    
    # 2. Requête SQL pour récupérer l'historique par ordre chronologique
    requete = """
        SELECT id, conversation_id, expediteur_id, contenu, lu, date_envoi 
        FROM messages 
        WHERE conversation_id = %s 
        ORDER BY date_envoi ASC
    """
    
    curseur.execute(requete, (id_conversation,))
    historique = curseur.fetchall() # On récupère tous les messages
    
    # 3. Fermeture des connexions
    curseur.close()
    conn.close()
    
    # Pour éviter les bugs avec les dates (TIMESTAMP) que le JSON ne gère pas toujours bien,
    # on transforme la date en texte lisible avant l'envoi
    for msg in historique:
        if msg['date_envoi']:
            msg['date_envoi'] = msg['date_envoi'].strftime('%Y-%m-%d %H:%M:%S')
            
    # 4. On renvoie l'historique uniquement à l'utilisateur qui l'a demandé
    emit('historique_messages', {'conversation_id': id_conversation, 'messages': historique})

@socketio.on('marquer_comme_lu')

# On récupère l'historique d'une conversation spécifique.
def gerer_messages_lus(donnees):
    id_conversation = donnees['conversation_id']
    id_utilisateur_actuel = donnees['user_id']
    
    # 1. Connexion et mise à jour des messages reçus
    conn = connexion_db()
    curseur = conn.cursor()
    
    requete_update = """
        UPDATE messages 
        SET lu = TRUE 
        WHERE conversation_id = %s 
          AND expediteur_id != %s 
          AND lu = FALSE
    """
    curseur.execute(requete_update, (id_conversation, id_utilisateur_actuel))
    conn.commit()
    
    # 2. On trouve l'ID du correspondant pour la notification en temps réel
    requete_correspondant = """
        SELECT utilisateur1_id, utilisateur2_id FROM conversations WHERE id = %s
    """
    curseur.execute(requete_correspondant, (id_conversation,))
    conversation = curseur.fetchone()
    
    curseur.close()
    conn.close()
    
    if conversation:
        user1_id, user2_id = conversation
        # On détermine qui est l'autre personne
        id_correspondant = user2_id if id_utilisateur_actuel == user1_id else user1_id
        
        # 3. La ligne 126 corrigée pour cibler le canal du correspondant :
        emit('messages_lus_notification', {
            'conversation_id': id_conversation,
            'lecteur_id': id_utilisateur_actuel
        }, room=f"canal_{id_correspondant}")


@app.route('/api/upload_piece_jointe', methods=['POST'])
def uploader_piece_jointe():
    # 1.On vérifie si un fichier et un ID de message sont bien envoyés
    if 'fichier' not in request.files or 'message_id' not in request.form:
        return jsonify({'erreur': 'Données manquantes'}), 400
        
    fichier = request.files['fichier']
    message_id = request.form['message_id']
    
    if fichier.filename == '':
        return jsonify({'erreur': 'Aucun fichier sélectionné'}), 400

    if fichier:
        #On sécurise le nom du fichier pour éviter les injections de chemins (ex: ../../mon_fichier)
        nom_origine = fichier.filename
        nom_securise = secure_filename(nom_origine)
        
        #On Détecte le type de fichier (image/jpeg, video/mp4, etc.)
        type_fich = fichier.content_type
        
        #On Défini le chemin complet où le fichier sera écrit sur ton disque dur
        chemin_complet = os.path.join(app.config['UPLOAD_FOLDER'], nom_securise)
        fichier.save(chemin_complet)
        
        # Le chemin relatif, c'est ce que l'interface HTML utilisera pour afficher l'image (<img src="...">)
        chemin_relatif = f"/static/uploads/{nom_securise}"
        
        # 2.On Sauvegarde les métadonnées dans la table 'pieces_jointes' de MySQL
        conn = connexion_db()
        curseur = conn.cursor()
        
        requete = """
            INSERT INTO pieces_jointes (message_id, nom_fichier, chemin_fichier, type_fichier)
            VALUES (%s, %s, %s, %s)
        """
        
        curseur.execute(requete, (message_id, nom_origine, chemin_relatif, type_fich))
        conn.commit()
        
        curseur.close()
        conn.close()
        
        return jsonify({
            'statut': 'succès',
            'chemin': chemin_relatif,
            'type': type_fich
        }), 200

if __name__ == '__main__':
    print("Le serveur de messagerie démarre sur le port 5000...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)