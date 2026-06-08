from concurrent.interpreters import list_all

import pymysql
from flask import Blueprint, request, jsonify
from sqlalchemy import except_

matching_bp = Blueprint('matching_bp', __name__)


def get_db_connection():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="@Advent7JR",
            database="ifri_mentorlink",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Erreur de connexion à la pase de données IFRI_MENTORLINK : {e}")
        return None


# 1. GESTION DES OFFRES
@matching_bp.route('/', methods=['GET'])
def index():
    """Route d'index pour tester la connectivité du module"""
    return jsonify({
        "statut": "success",
        "message": "Le serveur de matching (Membre 4) est fonctionnel et écoute sur le réseau local"
    }), 200


@matching_bp.route('/offres', methods=['GET'])
def get_all_offres():
    """Route secondaire pour l'équipe : Récupérer toutes les offres de mentorat ouvertes"""
    connection = get_db_connection()
    if not connection:
        return jsonify({
            "statut": "error",
            "message": "Impossible de se connecter à la base de donées"
        }), 500

    with connection.cursor() as cursor:
        try:
            # 🔥 CORRECTION : n.id rejoint maintenant 'niveaux' (au lieu de niveau) et o.statut est corrigé (au lieu de o.satut)
            query = """SELECT o.id,
                              u.nom,
                              u.prenom,
                              f.code AS filiere,
                              n.nom  AS niveau,
                              c.nom  AS competence,
                              o.format,
                              o.description
                       FROM mentorat o
                                JOIN utilisateurs u ON o.utilisateur_id = u.id
                                JOIN filieres f ON u.filiere_id = f.id
                                JOIN niveaux n ON u.niveau_id = n.id
                                JOIN competences c ON o.competence_id = c.id
                       WHERE o.type = 'OFFRE'
                         AND o.statut = 'OUVERTE'
                    """
            cursor.execute(query)
            offres = cursor.fetchall()
            return jsonify(offres), 200
        except Exception as e:
            return jsonify({
                "statut": "error",  # 🔥 CORRECTION : le statut passe à 'error' en cas d'exception
                "message": str(e)
            }), 500
        finally:
            connection.close()


@matching_bp.route('/matching', methods=['GET'])
def execute_matching():
    """Route principale de l'algorithme de matching
        Paramètre attendu : l'ID de l'apprenant qui fait la demande (user_id)
    """
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({
            "statut": "error",
            "message": "Le paramètre user_id est obligatoire"
        }), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({
            "statut": "error",
            "message": "Erreur de connexion à la base de données"
        }), 500

    with connection.cursor() as cursor:
        try:
            # Récupérer le profil de l'apprenant connecté
            query_apprenant = """ SELECT filiere_id, niveau_id
                                  FROM utilisateurs
                                  WHERE id = %s
                              """
            cursor.execute(query_apprenant, (user_id,))
            apprenant = cursor.fetchone()

            if not apprenant:
                return jsonify({
                    "statut": "error",
                    "message": "Apprenant introuvable."
                }), 404

            filiere_id_app = apprenant['filiere_id']
            niveau_id_app = apprenant['niveau_id']

            # Récupérer les compétences dont cet apprenant est à la recherche
            query_demandes = """ SELECT competence_id
                                 FROM mentorat
                                 WHERE utilisateur_id = %s
                                   AND type = 'DEMANDE'
                                   AND statut = 'OUVERTE'
                             """

            cursor.execute(query_demandes, (user_id,))
            demandes = cursor.fetchall()

            if not demandes:
                return jsonify({
                    "statut": "success",  # 🔥 CORRECTION : 'success' au lieu de 'error' car le traitement est normal
                    "message": "Cet apprenant n'a aucune demande de mantorat active.",
                    "matchings": []
                }), 200

            # Extraires les IDs de compétences recherchés
            liste_competences_recherchees = [d['competence_id'] for d in demandes]

            # Trouver les offres de mentor qui correspondent à au moins une competence demandée et dont le niveau du mentor est supérieur à celle de l'apprenant

            # 🔥 CORRECTION : .join() prend des parenthèses () et non des crochets []
            format_strings = ','.join(['%s'] * len(liste_competences_recherchees))
            query_mentors = f""" SELECT 
                    o.id AS offre_id,
                    o.format AS offre_format,
                    o.description AS offre_description,
                    o.competence_id AS offre_competence_id,
                    m.id AS mentor_id,
                    m.nom AS mentor_nom,
                    m.prenom AS mentor_prenom,
                    m.filiere_id AS mentor_filiere_id,
                    f.code AS mentor_filiere_code,
                    m.niveau_id AS mentor_niveau_id,
                    n.nom AS mentor_niveau_nom,
                    c.nom AS competence_nom
                FROM mentorat o
                JOIN utilisateurs m ON o.utilisateur_id = m.id
                JOIN filieres f ON m.filiere_id = f.id
                JOIN niveaux n ON m.niveau_id = n.id
                JOIN competences c ON o.competence_id = c.id
                WHERE o.type = 'OFFRE' 
                  AND o.statut = 'OUVERTE'
                  AND o.competence_id IN ({format_strings})
                  AND m.niveau_id >= %s
                    """

            # Préparation des requêtes pour la requête SQL
            params = liste_competences_recherchees + [niveau_id_app]
            cursor.execute(query_mentors, params)
            offres_mentors = cursor.fetchall()

            # Phase de calcul du score
            matchings_calcules = []

            for offre in offres_mentors:
                score = 0.0

                # Le critère 1 est le format du mentorat : 50 Points
                if offre['offre_format'] == 'PRESENTIEL':
                    score += 50.0
                elif offre['offre_format'] == 'EN_LIGNE':
                    score += 40.0
                elif offre['offre_format'] == 'LES_DEUX':
                    score += 45.0  # 🔥 CORRECTION : '+=' pour éviter d'écraser la valeur de score initiale

                # Le critère 2 est l'alignement de filière : 20 Points
                if offre['mentor_filiere_id'] == filiere_id_app:
                    score += 20.0

                # Le critère 3 est l'expertise et écart de niveau : 10 Points
                if offre['mentor_niveau_id'] > niveau_id_app:
                    ecart = offre['mentor_niveau_id'] - niveau_id_app
                    score += min(10.0, float(ecart) * 2.5)  # 🔥 SÉCURISATION : float() sur l'écart numérique
                else:
                    score += 5.0

                # Le critère 4 sont les compétences communes additionnelles communes : 20 Points
                query_bonus_comp = """SELECT COUNT(*) AS nb_communs
                                      FROM utilisateur_competences uc
                                      WHERE uc.utilisateur_id = %s
                                        AND uc.competence_id IN (SELECT competence_id
                                                                 FROM utilisateur_lacunes
                                                                 WHERE utilisateur_id = %s)
                                   """

                cursor.execute(query_bonus_comp, (offre['mentor_id'], user_id))
                result_bonus = cursor.fetchone()

                if isinstance(result_bonus, dict) and 'nb_communs' in result_bonus:
                    nb_communs = result_bonus['nb_communs']

                    if nb_communs > 0:
                        # 🔥 CORRECTION : Remplacement de la chaîne 'nb_communs' par la variable numérique nb_communs
                        score += min(20.0, float(nb_communs) * 5.0)

                # structuration de la réponse
                matchings_calcules.append({
                    "offre_id": offre['offre_id'],
                    "mentor_id": offre['mentor_id'],
                    "nom": offre['mentor_nom'],
                    "prenom": offre['mentor_prenom'],
                    "filiere": offre['mentor_filiere_code'],
                    "niveau": offre['mentor_niveau_nom'],
                    "competence_principale": offre['competence_nom'],
                    "format": offre['offre_format'],
                    "description": offre['offre_description'],
                    "score_pertinence": round(score, 2)
                })

            # Tri des profils par ordre décroissant
            matchings_calcules.sort(key=lambda x: x['score_pertinence'], reverse=True)

            return jsonify({
                "statut": "success",
                "apprenant_id": int(user_id),
                "total_matchs_trouves": len(matchings_calcules),
                "matchings": matchings_calcules
            }), 200

        except Exception as e:
            return jsonify({
                "statut": "error",
                "message": f"Erreur SQL/Python : {str(e)}"
            }), 500
        finally:
            connection.close()
