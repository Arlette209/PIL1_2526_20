import pymysql
from flask import Blueprint, request, jsonify
from sqlalchemy import except_

matching_bp = Blueprint('matching_bp', __name__)


def get_db_connection():
    """Etablir la connexion avec la base de données MySQL locale"""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="@Advent7JR",
        database="ifri_mentorlink",
        cursorclass=pymysql.cursors.DictCursor
    )


# 1. GESTION DES OFFRES
@matching_bp.route('/offres', methods=['POST', 'GET'])
def gerer_offres():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                data = request.json

                # Insérer une offre
                query = """INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut) \
                           VALUES (%s, 'OFFRE', %s, %s, %s, 'OUVERTE')
                        """
                cursor.execute(query, (
                    data.get('utilisateur_id'),
                    data.get('competence_id'),
                    data.get('format', 'LES DEUX'),
                    data.get('description', '')
                ))
                conn.commit()
                return jsonify({
                    "message": "Offre de mentorat publié avec succès !"
                }), 201
            else:
                # Récupérer des offres
                query = """
                        SELECT m.id, 
                               m.utilisateur_id,
                               u.nom,
                               u.prenom,
                               n.nom  AS niveau,
                               f.code AS filiere,
                               c.nom  AS competence, m.format, m.description,
                               m.date_publication
                        FROM mentorat m
                                 JOIN utilisateurs u ON m.utilisateur_id = u.id
                                 JOIN niveaux n ON u.niveau_id = n.id
                                 JOIN filieres f ON u.filiere_id = f.id
                                 JOIN competences c ON m.competence_id = c.id
                        WHERE m.type = 'OFFRE'
                          AND m.statut = 'OUVERTE'
                        """
                cursor.execute(query)
                offres = cursor.fetchall()
                return jsonify(offres), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    finally:
        conn.close()


# 2. GESTION DES DEMANDES

@matching_bp.route('/demandes', methods=['POST', 'GET'])
def gerer_demandes():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                data = request.json

                # Insérer une demande dans la tabe mentorat
                query = """
                        INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut)
                        VALUES (%s, 'DEMANDE', %s, %s, %s, 'OUVERTE')
                        """

                cursor.execute(query, (
                    data.get('utilisateur_id'),
                    data.get('competence_id'),
                    data.get('format', 'LES DEUX'),
                    data.get('description', '')
                ))
                conn.commit()
                return jsonify({
                    "message": "Demande d'aide pour avoir un Mentorat publié avec succès !"
                }), 201
            else:
                # Récupérer des demandes
                query = """
                        SELECT m.id
                             , m.utilisateur_id
                             , u.nom
                             , u.prenom
                             , n.nom  AS niveau
                             , f.code AS filiere
                             , c.nom  AS competence, m.format, m.description
                             , m.date_publication
                        FROM mentorat m
                                 JOIN utilisateurs u ON m.utilisateur_id = u.id
                                 JOIN niveaux n ON u.niveau_id = n.id
                                 JOIN filieres f ON u.filiere_id = f.id
                                 JOIN competences c ON m.competence_id = c.id
                        WHERE m.type = 'DEMANDE'
                          AND m.statut = 'OUVERTE'
                        """

                cursor.execute(query)
                demandes = cursor.fetchall()
                return jsonify(demandes), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    finally:
        conn.close()


# 3. L'algorithme de matching : Score, Compatiblilité

@matching_bp.route('/matching', methods=['GET'])
def executer_matching():
    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({
            "error": "Le paramètre user_id est manquant."
        }), 400

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:

            # Récupérer la filière du demandeur d'aide
            query_filiere_user = "SELECT filiere_id FROM utilisateurs WHERE id = %s"
            cursor.execute(query_filiere_user, (user_id))
            user_info = cursor.fetchone()

            # Extraire et sécuriser l'id de la filière
            user_filiere_id = user_info['filiere_id'] if user_info else None

            # Récupérer les demandes de l'utilisateur connecté
            query_besoins = "SELECT competence_id FROM mentorat WHERE utilisateur_id = %s AND type = 'DEMANDE' AND statut = 'OUVERTE'"
            cursor.execute(query_besoins, (user_id,))
            mes_demandes = cursor.fetchall()

            if not mes_demandes:
                return jsonify({
                    "message": "Aucune demande active pour cet utilisateur. Veuillez ajoutez des demandes d'aides d'abord.",
                    "matches": []
                }), 200

            # Prendre les ID des compétences recherches
            competence_ids = [d['competence_id'] for d in mes_demandes]

            # Trouver les mentors qui disposent de ces compétences
            format_string = ','.join(['%s'] * len(competence_ids))

            # Récupération de l'ID de la filière du mentor
            query_mentors = f""" SELECT 
                                    m.utilisateur_id AS mentor_id, 
                                    u.nom, u.prenom, 
                                    n.nom AS niveau, 
                                    u.filiere_id AS mentor_filiere_id, 
                                    f.code AS filiere, 
                                    m.competence_id, 
                                    c.nom AS competence_nom,
                                    m.format
                                 FROM mentorat m
                                 JOIN utilisateurs u ON m.utilisateur_id = u.id
                                 JOIN niveaux n ON u.niveau_id = n.id
                                 JOIN filieres f ON u.filiere_id = f.id
                                 JOIN competences c ON m.competence_id = c.id
                                 WHERE m.type = 'OFFRE'
                                    AND m.statut = 'OUVERTE'
                                    AND m.competence_id IN ({format_string})
                                    AND m.utilisateur_id != %s
                            """


            # Fusion des IDs de concaténation et de l'ID utilisateur dans un seul tuples imutables pour injecter de manières sécurisée dans les paramètres (%s) de la requête SQL
            params = list(competence_ids) + [user_id]
            cursor.execute(query_mentors, params)

            mentors = cursor.fetchall()
            liste_matchings = []

            # structure de calcul : Score
            for mentor in mentors:
                score_de_base = 0
                score_de_filiere = 0

                format_mentor = mentor.get('format', 'AUTRE')

                # Croisement des formats
                if format_mentor == 'PRESENTIEL':
                    score_de_base += 50
                elif mentor['format'] == 'EN_LIGNE' or mentor['format'] == 'EN LIGNE':
                    score_de_base += 40

                # Croisement des filieres
                if mentor.get('mentor_filiere_id') == user_filiere_id:
                    score_de_filiere += 20

                liste_matchings.append({
                    "mentor_id": mentor['mentor_id'],
                    "nom": mentor['nom'],
                    "prenom": mentor['prenom'],
                    "competence": mentor['competence_nom'],
                    "filiere": mentor['filiere'],
                    "niveau": mentor['niveau'],
                    "score": min(score_de_base + score_de_filiere, 100.00),
                    "status": "PROPOSE"
                })

            # Triage des résultats du score
            liste_matchings = sorted(liste_matchings, key=lambda x: x['score'], reverse=True)

            return jsonify({
                "user_id_demandeur": user_id,
                "matches_trouves": liste_matchings
            }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    finally:
        conn.close()
