# ============================================
# controllers.py - Logique métier du profil
# Membre 3 : Persistance des profils
# IFRI_MentorLink
# ============================================

from models import get_profil, update_profil_db, update_competences_db, update_lacunes_db, update_disponibilites_db

def lire_profil(mysql, user_id):
    """Récupère et retourne les données du profil depuis la BDD"""
    return get_profil(mysql, user_id)

def modifier_profil_db(mysql, user_id, donnees):
    """Modifie le profil dans la base de données"""
    return update_profil_db(mysql, user_id, donnees)

def modifier_competences_db(mysql, user_id, competences):
    """Modifie les compétences dans la base de données"""
    return update_competences_db(mysql, user_id, competences)

def modifier_lacunes_db(mysql, user_id, lacunes):
    """Modifie les lacunes dans la base de données"""
    return update_lacunes_db(mysql, user_id, lacunes)

def modifier_disponibilites_db(mysql, user_id, disponibilites):
    """Modifie les disponibilités dans la base de données"""
    return update_disponibilites_db(mysql, user_id, disponibilites)