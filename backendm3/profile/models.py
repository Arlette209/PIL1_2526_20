# ============================================
# models.py - Accès aux données du profil
# Membre 3 : Persistance des profils
# IFRI_MentorLink
# ============================================

def get_profil(mysql, user_id):
    """Récupère le profil complet d'un utilisateur depuis la base de données"""
    cur = mysql.connection.cursor()
    
    # Récupérer les infos de base de l'utilisateur
    cur.execute("""
        SELECT u.id, u.nom, u.prenom, u.email, u.telephone, 
               u.bio, u.photo_profil, f.nom as filiere, n.nom as niveau
        FROM utilisateurs u
        JOIN filieres f ON u.filiere_id = f.id
        JOIN niveaux n ON u.niveau_id = n.id
        WHERE u.id = %s
    """, (user_id,))
    user = cur.fetchone()
    
    # Récupérer les compétences
    cur.execute("""
        SELECT c.nom FROM competences c
        JOIN utilisateur_competences uc ON c.id = uc.competence_id
        WHERE uc.utilisateur_id = %s
    """, (user_id,))
    competences = [row[0] for row in cur.fetchall()]
    
    # Récupérer les lacunes
    cur.execute("""
        SELECT c.nom FROM competences c
        JOIN utilisateur_lacunes ul ON c.id = ul.competence_id
        WHERE ul.utilisateur_id = %s
    """, (user_id,))
    lacunes = [row[0] for row in cur.fetchall()]
    
    # Récupérer les disponibilités
    cur.execute("""
        SELECT jour, heure_debut, heure_fin FROM disponibilites
        WHERE utilisateur_id = %s
    """, (user_id,))
    disponibilites = [{"jour": row[0], "debut": str(row[1]), "fin": str(row[2])} 
                      for row in cur.fetchall()]
    
    cur.close()
    
    if not user:
        return None
    
    return {
        "id": user[0],
        "nom": user[1],
        "prenom": user[2],
        "email": user[3],
        "telephone": user[4],
        "bio": user[5],
        "photo": user[6],
        "filiere": user[7],
        "niveau": user[8],
        "competences": competences,
        "lacunes": lacunes,
        "disponibilites": disponibilites
    }