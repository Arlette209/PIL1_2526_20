# ============================================
# routes.py - Endpoints de l'API profil
# Membre 3 : Persistance des profils
# IFRI_MentorLink
# ============================================

from flask import Blueprint, jsonify, request
from controllers import lire_profil

# Création du blueprint pour les routes du profil
profile_bp = Blueprint('profile', __name__)


# ------ ENDPOINT PROFIL COMPLET ------

@profile_bp.route('/profile/<int:user_id>', methods=['GET', 'PUT'])
def handle_profile(user_id):
    """
    GET /profile/<user_id> → Retourne toutes les infos du profil
    PUT /profile/<user_id> → Modifie les infos du profil
    """
    from app import mysql
    from controllers import modifier_profil_db
    
    if request.method == 'GET':
        profil = lire_profil(mysql, user_id)
        if not profil:
            return jsonify({"erreur": "Utilisateur non trouvé"}), 404
        return jsonify(profil)
    
    elif request.method == 'PUT':
        donnees = request.get_json()
        profil = modifier_profil_db(mysql, user_id, donnees)
        return jsonify({
            "message": "Profil mis à jour avec succès",
            "profil": profil
        })


# ------ ENDPOINT COMPETENCES ------

@profile_bp.route('/competences/<int:user_id>', methods=['GET', 'PUT'])
def handle_competences(user_id):
    """
    GET /competences/<user_id> → Retourne les compétences
    PUT /competences/<user_id> → Modifie les compétences
    """
    from app import mysql
    from controllers import modifier_competences_db
    
    if request.method == 'GET':
        profil = lire_profil(mysql, user_id)
        if not profil:
            return jsonify({"erreur": "Utilisateur non trouvé"}), 404
        return jsonify({"competences": profil["competences"]})
    
    elif request.method == 'PUT':
        donnees = request.get_json()
        competences = modifier_competences_db(mysql, user_id, donnees["competences"])
        return jsonify({
            "message": "Compétences mises à jour",
            "competences": competences
        })


# ------ ENDPOINT DISPONIBILITES ------

@profile_bp.route('/disponibilites/<int:user_id>', methods=['GET', 'PUT'])
def handle_disponibilites(user_id):
    """
    GET /disponibilites/<user_id> → Retourne les disponibilités
    PUT /disponibilites/<user_id> → Modifie les disponibilités
    """
    from app import mysql
    from controllers import modifier_disponibilites_db
    
    if request.method == 'GET':
        profil = lire_profil(mysql, user_id)
        if not profil:
            return jsonify({"erreur": "Utilisateur non trouvé"}), 404
        return jsonify({"disponibilites": profil["disponibilites"]})
    
    elif request.method == 'PUT':
        donnees = request.get_json()
        disponibilites = modifier_disponibilites_db(mysql, user_id, donnees["disponibilites"])
        return jsonify({
            "message": "Disponibilités mises à jour",
            "disponibilites": disponibilites
        })


# ------ ENDPOINT LACUNES ------

@profile_bp.route('/lacunes/<int:user_id>', methods=['GET', 'PUT'])
def handle_lacunes(user_id):
    """
    GET /lacunes/<user_id> → Retourne les lacunes
    PUT /lacunes/<user_id> → Modifie les lacunes
    """
    from app import mysql
    from controllers import modifier_lacunes_db
    
    if request.method == 'GET':
        profil = lire_profil(mysql, user_id)
        if not profil:
            return jsonify({"erreur": "Utilisateur non trouvé"}), 404
        return jsonify({"lacunes": profil["lacunes"]})
    
    elif request.method == 'PUT':
        donnees = request.get_json()
        lacunes = modifier_lacunes_db(mysql, user_id, donnees["lacunes"])
        return jsonify({
            "message": "Lacunes mises à jour",
            "lacunes": lacunes
        })