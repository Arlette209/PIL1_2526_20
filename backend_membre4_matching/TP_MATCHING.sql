USE ifri_mentorlink;

-- Décrocher temporairement les contraintes pour vider proprement si besoin
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE mentorat;
TRUNCATE TABLE utilisateurs;
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================================
-- 1. INSERTION DE 4 ÉTUDIANTS DE TEST
-- =====================================================================
INSERT INTO utilisateurs (id, role_id, filiere_id, niveau_id, nom, prenom, email, telephone, mot_de_passe, bio)
VALUES
-- Utilisateur 1 : Toi (Demandeur en GL - Licence 3)
(1, 2, 2, 3, 'AHOUANSOU', 'Daniel', 'daniel@ifri.uac.bj', '+22901000001', 'hash_pwd_1', 'Passionné de cybersécurité et dev.'),

-- Utilisateur 2 : Mentor potentiel A (Même filière : GL - Licence 3)
(2, 2, 2, 3, 'SOGLO', 'Jean', 'jean.soglo@ifri.uac.bj', '+22901000002', 'hash_pwd_2', 'Excellent en développement backend.'),

-- Utilisateur 3 : Mentor potentiel B (Filière différente : IA - Licence 3)
(3, 2, 1, 3, 'KPADONOU', 'Marie', 'marie.kpadonou@ifri.uac.bj', '+22901000003', 'hash_pwd_3', 'Spécialiste des bases de données et python.'),

-- Utilisateur 4 : Étudiant C (En GL, mais n'offre pas la bonne compétence)
(4, 2, 2, 3, 'HOUNGBE', 'Alain', 'alain@ifri.uac.bj', '+22901000004', 'hash_pwd_4', 'A l\'aise en réseau.');


-- =====================================================================
-- 2. INSERTION DES COMPÉTENCES DE TEST (Si elles n'existent pas)
-- =====================================================================
INSERT IGNORE INTO competences (id, nom) VALUES 
(1, 'Algèbre linéaire'),
(2, 'Bases de données relationnelles'),
(3, 'Réseaux informatiques');


-- =====================================================================
-- 3. CRÉATION DES ANNONCES DE MENTORAT
-- =====================================================================

-- Daniel (id: 1) a des lacunes et publie une DEMANDE en 'Bases de données relationnelles' (id: 2)
INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut)
VALUES (1, 'DEMANDE', 2, 'LES_DEUX', 'Besoin d\'aide pour optimiser des requêtes SQL complexes.', 'OUVERTE');

-- Jean (id: 2, Filière GL comme Daniel) offre son aide (OFFRE) sur les 'Bases de données relationnelles' (id: 2)
INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut)
VALUES (2, 'OFFRE', 2, 'PRESENTIEL', 'Je peux aider sur le SQL et la modélisation.', 'OUVERTE');

-- Marie (id: 3, Filière IA) offre AUSSI son aide (OFFRE) sur les 'Bases de données relationnelles' (id: 2)
INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut)
VALUES (3, 'OFFRE', 2, 'EN_LIGNE', 'Dispo pour des séances Zoom sur le SQL.', 'OUVERTE');

-- Alain (id: 4) offre une compétence en Réseaux (id: 3) -> Il ne doit pas matcher avec Daniel
INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut)
VALUES (4, 'OFFRE', 3, 'LES_DEUX', 'Aide en routage et commutation.', 'OUVERTE');