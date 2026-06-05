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

@profile_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """GET /profile/<user_id> → Retourne toutes les infos du profil"""
    from app import mysql
    profil = lire_profil(mysql, user_id)
    if not profil:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404
    return jsonify(profil)


# ------ ENDPOINT COMPETENCES ------

@profile_bp.route('/competences/<int:user_id>', methods=['GET'])
def get_competences(user_id):
    """GET /competences/<user_id> → Retourne les compétences"""
    from app import mysql
    profil = lire_profil(mysql, user_id)
    if not profil:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404
    return jsonify({"competences": profil["competences"]})


# ------ ENDPOINT DISPONIBILITES ------

@profile_bp.route('/disponibilites/<int:user_id>', methods=['GET'])
def get_disponibilites(user_id):
    """GET /disponibilites/<user_id> → Retourne les disponibilités"""
    from app import mysql
    profil = lire_profil(mysql, user_id)
    if not profil:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404
    return jsonify({"disponibilites": profil["disponibilites"]})


# ------ ENDPOINT LACUNES ------

@profile_bp.route('/lacunes/<int:user_id>', methods=['GET'])
def get_lacunes(user_id):
    """GET /lacunes/<user_id> → Retourne les lacunes"""
    from app import mysql
    profil = lire_profil(mysql, user_id)
    if not profil:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404
    return jsonify({"lacunes": profil["lacunes"]})