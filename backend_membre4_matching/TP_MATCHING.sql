DROP DATABASE IF EXISTS ifri_mentorlink;
CREATE DATABASE ifri_mentorlink;
USE ifri_mentorlink;

-- 1. Table des rôles
CREATE TABLE roles(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO roles(nom) VALUES ('ADMIN'), ('UTILISATEUR');

-- 2. Table des filières
CREATE TABLE filieres(
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL
);

INSERT INTO filieres(code, nom) VALUES
('IA', 'Intelligence Artificielle'),
('GL', 'Génie Logiciel'),
('IM', 'Internet et Multimédia'),
('SI', 'Systèmes Informatiques'),
('SEIOT', 'Systèmes Embarqués et IoT');

-- 3. Table des niveaux académiques
CREATE TABLE niveaux(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO niveaux(nom) VALUES
('Licence 1'),
('Licence 2'),
('Licence 3'),
('Master 1'),
('Master 2');

-- 4. Table des utilisateurs
CREATE TABLE utilisateurs(
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    filiere_id INT NOT NULL,
    niveau_id INT NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    photo_profil VARCHAR(255),
    bio TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(role_id) REFERENCES roles(id),
    FOREIGN KEY(filiere_id) REFERENCES filieres(id),
    FOREIGN KEY(niveau_id) REFERENCES niveaux(id)
);

-- 5. Table des compétences globales
CREATE TABLE competences(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

-- 6. Tables d'association pour les profils
CREATE TABLE utilisateur_competences(
    utilisateur_id INT,
    competence_id INT,
    PRIMARY KEY(utilisateur_id, competence_id),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY(competence_id) REFERENCES competences(id) ON DELETE CASCADE
);

CREATE TABLE utilisateur_lacunes(
    utilisateur_id INT,
    competence_id INT,
    PRIMARY KEY(utilisateur_id, competence_id),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY(competence_id) REFERENCES competences(id) ON DELETE CASCADE
);

-- 7. Table des disponibilités hebdomadaires
CREATE TABLE disponibilites(
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    jour ENUM('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'),
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- 8. Table centrale des offres et demandes (Annonces)
CREATE TABLE mentorat(
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    type ENUM('OFFRE', 'DEMANDE') NOT NULL,
    competence_id INT NOT NULL,
    format ENUM('PRESENTIEL', 'EN_LIGNE', 'LES_DEUX') DEFAULT 'LES_DEUX',
    description TEXT,
    statut ENUM('OUVERTE', 'EN_COURS', 'TERMINEE') DEFAULT 'OUVERTE',
    date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id),
    FOREIGN KEY(competence_id) REFERENCES competences(id)
);

-- 9. Table des Matchings générés par l'algorithme
CREATE TABLE matchings(
    id INT AUTO_INCREMENT PRIMARY KEY,
    mentor_id INT NOT NULL,
    mentore_id INT NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    statut ENUM('PROPOSE', 'ACCEPTE', 'REFUSE') DEFAULT 'PROPOSE',
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(mentor_id) REFERENCES utilisateurs(id),
    FOREIGN KEY(mentore_id) REFERENCES utilisateurs(id)
);

-- 10. Tables de messagerie
CREATE TABLE conversations(
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur1_id INT NOT NULL,
    utilisateur2_id INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(utilisateur1_id) REFERENCES utilisateurs(id),
    FOREIGN KEY(utilisateur2_id) REFERENCES utilisateurs(id)
);

CREATE TABLE messages(
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    expediteur_id INT NOT NULL,
    contenu TEXT NOT NULL,
    lu BOOLEAN DEFAULT FALSE,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY(expediteur_id) REFERENCES utilisateurs(id)
);

CREATE TABLE pieces_jointes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    message_id INT NOT NULL,
    nom_fichier VARCHAR(255),
    chemin_fichier VARCHAR(255),
    type_fichier VARCHAR(100),
    date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(message_id) REFERENCES messages(id) ON DELETE CASCADE
);

-- 11. Tables de suivi des sessions et évaluations
CREATE TABLE sessions_mentorat(
    id INT AUTO_INCREMENT PRIMARY KEY,
    mentor_id INT NOT NULL,
    mentore_id INT NOT NULL,
    date_session DATETIME NOT NULL,
    duree INT NOT NULL,
    mode ENUM('PRESENTIEL', 'EN_LIGNE'),
    compte_rendu TEXT,
    statut ENUM('PLANIFIEE', 'TERMINEE', 'ANNULEE') DEFAULT 'PLANIFIEE',
    FOREIGN KEY(mentor_id) REFERENCES utilisateurs(id),
    FOREIGN KEY(mentore_id) REFERENCES utilisateurs(id)
);

CREATE TABLE evaluations(
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    mentor_id INT NOT NULL,
    auteur_id INT NOT NULL,
    note INT CHECK(note BETWEEN 1 AND 5),
    commentaire TEXT,
    date_evaluation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions_mentorat(id),
    FOREIGN KEY(mentor_id) REFERENCES utilisateurs(id),
    FOREIGN KEY(auteur_id) REFERENCES utilisateurs(id)
);

-- 12. Table des notifications
CREATE TABLE notifications(
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    titre VARCHAR(255),
    contenu TEXT,
    est_lue BOOLEAN DEFAULT FALSE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Indexations pour l'optimisation des performances des requêtes
CREATE INDEX idx_email ON utilisateurs(email);
CREATE INDEX idx_telephone ON utilisateurs(telephone);
CREATE INDEX idx_matching_score ON matchings(score);
CREATE INDEX idx_messages_date ON messages(date_envoi);
CREATE INDEX idx_session_date ON sessions_mentorat(date_session);

-- =====================================================================
-- 1. INSERTION DES COMPÉTENCES DE TEST
-- =====================================================================
INSERT INTO competences (nom) VALUES
('Programmation Python'),
('Développement Web avec Flask'),
('Bases de données SQL & MySQL'),
('Sécurité des Réseaux'),
('Analyse de Données et IA'),
('Modélisation UML & Génie Logiciel'),
('Développement d''applications IoT');

-- =====================================================================
-- 2. INSERTION DES UTILISATEURS DE TEST (Mot de passe générique : 'pass123')
-- =====================================================================
-- Note : role_id 2 = UTILISATEUR. Les filieres et niveaux suivent tes structures.

-- Apprenant Réf (ID 1) : Daniel - L1 Génie Logiciel (filiere 2, niveau 1)
INSERT INTO utilisateurs (role_id, filiere_id, niveau_id, nom, prenom, email, telephone, mot_de_passe, bio) VALUES
(2, 2, 1, 'AHOUANSOU', 'Daniel', 'daniel@ifri.bj', '90000001', 'pass123', 'Étudiant en L1 GL, cherche à maîtriser le développement backend.');

-- Mentor 1 (ID 2) : Éric - L3 Génie Logiciel (Même filière, niveau supérieur -> Devrait être le MEILLEUR match)
INSERT INTO utilisateurs (role_id, filiere_id, niveau_id, nom, prenom, email, telephone, mot_de_passe, bio) VALUES
(2, 2, 3, 'KPADONOU', 'Éric', 'eric@ifri.bj', '90000002', 'pass123', 'Passionné de backend et d''architecture logicielle en L3.');

-- Mentor 2 (ID 3) : Marie - Master 2 Intelligence Artificielle (Filière différente, niveau très supérieur -> Doit passer le filtre de niveau)
INSERT INTO utilisateurs (role_id, filiere_id, niveau_id, nom, prenom, email, telephone, mot_de_passe, bio) VALUES
(2, 1, 5, 'SOSSOU', 'Marie', 'marie@ifri.bj', '90000003', 'pass123', 'Doctorante/Master 2 en IA, j''adore partager mes bases en Python et SQL.');

-- Mentor 3 (ID 4) : Marc - L1 Sécurité Informatique (Même niveau, filière différente -> Utile pour tester si un L1 peut aider un autre L1 sur une matière maîtrisée)
INSERT INTO utilisateurs (role_id, filiere_id, niveau_id, nom, prenom, email, telephone, mot_de_passe, bio) VALUES
(2, 4, 1, 'TCHEOU', 'Marc', 'marc@ifri.bj', '90000004', 'pass123', 'L1 en Systèmes Informatiques, fort en bases de données.');

-- Utilisateur Écarté (ID 5) : Chloé - L1 Génie Logiciel (Mais elle n'a que des demandes, pas d'offres)
INSERT INTO utilisateurs (role_id, filiere_id, niveau_id, nom, prenom, email, telephone, mot_de_passe, bio) VALUES
(2, 2, 1, 'AGBOSSA', 'Chloé', 'chloe@ifri.bj', '90000005', 'pass123', 'Besoin d''aide en programmation.');


-- =====================================================================
-- 3. INSERTION DES ANNONCES DE MENTORAT (OFFRES & DEMANDES)
-- =====================================================================

-- Daniel (ID 1) a deux DEMANDES ouvertes : il galère sur Python (ID 1) et Flask (ID 2)
INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut) VALUES
(1, 'DEMANDE', 1, 'PRESENTIEL', 'J''ai besoin d''aide pour comprendre les bases de Python.', 'OUVERTE'),
(1, 'DEMANDE', 2, 'LES_DEUX', 'Je bloque sur les routes et la connexion BDD avec Flask.', 'OUVERTE');

-- Éric (ID 2) propose une OFFRE sur Flask (ID 2) - Match parfait avec la demande de Daniel
INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut) VALUES
(2, 'OFFRE', 2, 'PRESENTIEL', 'Je peux vous coacher sur Flask et l''architecture MVC.', 'OUVERTE');

-- Marie (ID 3) propose une OFFRE sur Python (ID 1) - Match sur la compétence mais filière différente
INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut) VALUES
(3, 'OFFRE', 1, 'EN_LIGNE', 'Cours d''initiation et perfectionnement Python en ligne.', 'OUVERTE');

-- Marc (ID 4) propose une OFFRE sur Python (ID 1) - Même niveau académique que Daniel
INSERT INTO mentorat (utilisateur_id, type, competence_id, format, description, statut) VALUES
(4, 'OFFRE', 1, 'PRESENTIEL', 'Aide mémoire et exercices pratiques sur Python.', 'OUVERTE');


-- =====================================================================
-- 4. DONNÉES BONUS : COMPÉTENCES ET LACUNES SECONDAIRES
-- =====================================================================
-- Pour tester le "Critère 4" du code (Bonus compétences communes secondaires)

-- Daniel a une lacune secondaire en SQL (ID 3)
INSERT INTO utilisateur_lacunes (utilisateur_id, competence_id) VALUES
(1, 3);

-- Éric maîtrise le SQL (ID 3) -> Il va gagner les points bonus !
INSERT INTO utilisateur_competences (utilisateur_id, competence_id) VALUES
(2, 3);