# ============================================
# models.py - Accès aux données du profil
# Membre 3 : Persistance des profils
# IFRI_MentorLink
# ============================================

def get_profil(mysql, user_id):
    """Récupère le profil complet d'un utilisateur depuis la base de données"""
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT u.id, u.nom, u.prenom, u.email, u.telephone, 
               u.bio, u.photo_profil, f.nom as filiere, n.nom as niveau
        FROM utilisateurs u
        JOIN filieres f ON u.filiere_id = f.id
        JOIN niveaux n ON u.niveau_id = n.id
        WHERE u.id = %s
    """, (user_id,))
    user = cur.fetchone()
    
    cur.execute("""
        SELECT c.nom FROM competences c
        JOIN utilisateur_competences uc ON c.id = uc.competence_id
        WHERE uc.utilisateur_id = %s
    """, (user_id,))
    competences = [row[0] for row in cur.fetchall()]
    
    cur.execute("""
        SELECT c.nom FROM competences c
        JOIN utilisateur_lacunes ul ON c.id = ul.competence_id
        WHERE ul.utilisateur_id = %s
    """, (user_id,))
    lacunes = [row[0] for row in cur.fetchall()]
    
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


def update_profil_db(mysql, user_id, donnees):
    """Met à jour le profil d'un utilisateur dans la base de données"""
    cur = mysql.connection.cursor()
    
    cur.execute("""
        UPDATE utilisateurs 
        SET nom = COALESCE(%s, nom),
            prenom = COALESCE(%s, prenom),
            email = COALESCE(%s, email),
            telephone = COALESCE(%s, telephone),
            bio = COALESCE(%s, bio)
        WHERE id = %s
    """, (
        donnees.get('nom'),
        donnees.get('prenom'),
        donnees.get('email'),
        donnees.get('telephone'),
        donnees.get('bio'),
        user_id
    ))
    
    mysql.connection.commit()
    cur.close()
    
    return get_profil(mysql, user_id)


def update_competences_db(mysql, user_id, competences):
    """Met à jour les compétences d'un utilisateur dans la base de données"""
    cur = mysql.connection.cursor()
    
    cur.execute("DELETE FROM utilisateur_competences WHERE utilisateur_id = %s", (user_id,))
    
    for competence in competences:
        cur.execute("SELECT id FROM competences WHERE nom = %s", (competence,))
        result = cur.fetchone()
        
        if result:
            competence_id = result[0]
        else:
            cur.execute("INSERT INTO competences (nom) VALUES (%s)", (competence,))
            competence_id = cur.lastrowid
        
        cur.execute("""
            INSERT INTO utilisateur_competences (utilisateur_id, competence_id)
            VALUES (%s, %s)
        """, (user_id, competence_id))
    
    mysql.connection.commit()
    cur.close()
    
    return get_profil(mysql, user_id)["competences"]


def update_lacunes_db(mysql, user_id, lacunes):
    """Met à jour les lacunes d'un utilisateur dans la base de données"""
    cur = mysql.connection.cursor()
    
    cur.execute("DELETE FROM utilisateur_lacunes WHERE utilisateur_id = %s", (user_id,))
    
    for lacune in lacunes:
        cur.execute("SELECT id FROM competences WHERE nom = %s", (lacune,))
        result = cur.fetchone()
        
        if result:
            competence_id = result[0]
        else:
            cur.execute("INSERT INTO competences (nom) VALUES (%s)", (lacune,))
            competence_id = cur.lastrowid
        
        cur.execute("""
            INSERT INTO utilisateur_lacunes (utilisateur_id, competence_id)
            VALUES (%s, %s)
        """, (user_id, competence_id))
    
    mysql.connection.commit()
    cur.close()
    
    return get_profil(mysql, user_id)["lacunes"]


def update_disponibilites_db(mysql, user_id, disponibilites):
    """Met à jour les disponibilités d'un utilisateur dans la base de données"""
    cur = mysql.connection.cursor()
    
    cur.execute("DELETE FROM disponibilites WHERE utilisateur_id = %s", (user_id,))
    
    for dispo in disponibilites:
        cur.execute("""
            INSERT INTO disponibilites (utilisateur_id, jour, heure_debut, heure_fin)
            VALUES (%s, %s, %s, %s)
        """, (user_id, dispo["jour"], dispo["debut"], dispo["fin"]))
    
    mysql.connection.commit()
    cur.close()
    
    return get_profil(mysql, user_id)["disponibilites"]