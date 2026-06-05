# ============================================
# controllers.py - Logique métier du profil
# Membre 3 : Persistance des profils
# IFRI_MentorLink
# ============================================

from models import get_profil

def lire_profil(mysql, user_id):
    """Récupère et retourne les données du profil depuis la BDD"""
    return get_profil(mysql, user_id)