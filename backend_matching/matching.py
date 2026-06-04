import pymysql
from flask import Blueprint, request, jsonify, current_app

matching_bp = Blueprint('matching', __name__)


def obtenir_connexion():
    """Etablir la connexion avec la base de données MySQL locale"""
    return pymysql.connect(
        host=current_app.config.get('MYSQL_HOST', 'localhost'),
        user=current_app.config.get('MYSQL_USER', 'root'),
        password=current_app.config.get('MYSQL_PASSWORD', '@Advent7JR'),
        database=current_app.config.get('MYSQL_DB', 'ifri_mentorlink'),
        cursorclass=pymysql.cursors.DictCursor
    )


@matching_bp.route('/matching', methods=['GET'])
def calculer_matching():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"status": "error",
                        "message": "Le paramètre user_id est manquant."
                        }), 400

    conn = None
    cursor = None

    try:
        conn = obtenir_connexion()
        cursor = conn.cursor()

        query_user = """SELECT m.*, u.filiere_id, u.niveau_id
                        FROM mentorat m
                                 JOIN utilisateurs u ON m.utilisateur_id = u.id
                        WHERE m.utilisateur_id = %s
                          AND m.statut = 'OUVERTE'
                     """
        cursor.execute(query_user, (user_id,))
        besoins_user = cursor.fetchall()

        if not besoins_user:
            return jsonify({
                "status": "success",
                "message": "Aucune demande ou offre active trouvée pour cet utilisateur.",
                "matches": []
            }), 200

        mon_mentorat = besoins_user[0]
        mon_type = mon_mentorat['type']

        type_partenaire_recherche = 'OFFRE' if mon_type == 'DEMANDE' else 'DEMANDE'

        query_partners = """
                         SELECT m.id as mentorat_id,
                                m.utilisateur_id,
                                m.format,
                                m.description,
                                u.nom,
                                u.prenom,
                                u.photo_profil,
                                u.filiere_id,
                                u.niveau_id,
                         FROM mentorat m
                                  JOIN utilisateurs u ON m.utilisateur_id = u.id
                                  JOIN filieres f ON u.filiere_id = f.id
                                  JOIN niveaux n ON u.niveau_id = n.id
                         WHERE m.type = %s
                           AND m.competence_id = %s
                           AND m.statut = 'OUVERTE'
                           AND m.utilisateur_id != %s \
                         """
        cursor.execute(query_partners, (type_partenaire_recherche, mon_mentorat['competence_id'], user_id))
        partenaires_potentiels = cursor.fetchall()

        liste_matchs = []

        for p in partenaires_potentiels:
            score = 0.0
            raison = []

            score += 50.0
            raison.append("Partage la même compétence cible")

            if p['filiere_id'] == mon_mentorat['filiere_id']:
                score += 25.0
                raison.append(f"Même filière d'étude ({p['filiere_nom']})")

            if (p['format'] == mon_mentorat['format'] or
                    p['format'] == 'LES DEUX' or
                    mon_mentorat['format'] == 'LES DEUX'):
                score += 25.0
                raison.append("Format d'apprentissage compatible")

            liste_matchs.append({
                "partenaire_id": p['utilisateur_id'],
                "nom_prenom": f"{p['nom']} {p['prenom']}",
                "photo_profil": p['photo_profil'],
                "filiere": p['filiere_nom'],
                "niveau": p['niveau_nom'],
                "format_propose": p['format'],
                "description": p['description'],
                "score_compatibilite": score,
                "raison": raison
            })

        liste_matchs = sorted(liste_matchs, key=lambda x: x['score_compatibilite'], reverse=True)

        return jsonify({
            "status": "success",
            "total_matches": len(liste_matchs),
            "matches": liste_matchs
        }), 200

    except Exception as err:
        import traceback
        error_complete = traceback.format_exc()
        return jsonify({
            "status": "error",
            "message": f"Erreur lors de l'exécution du matching :{str(err)}",
            "traceback": error_complete
        }), 500
    finally:
        if cursor is not None and not isinstance(cursor, type(obtenir_connexion())):
            try:
                cursor.close()
            except:
                pass

        if conn is not None and conn.open:
            try:
                conn.close()
            except:
                pass
