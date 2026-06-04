
CREATE DATABASE ifri_mentorlink;
USE ifri_mentorlink;


CREATE TABLE roles(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO roles(nom)
VALUES
('ADMIN'),
('UTILISATEUR');


CREATE TABLE filieres(
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL
);

INSERT INTO filieres(code,nom)
VALUES
('IA','Intelligence Artificielle'),
('GL','Génie Logiciel'),
('IM','Internet et Multimédia'),
('SI','Systèmes Informatiques'),
('SEIOT','Systèmes Embarqués et IoT');


CREATE TABLE niveaux(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO niveaux(nom)
VALUES
('Licence 1'),
('Licence 2'),
('Licence 3'),
('Master 1'),
('Master 2');


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

    FOREIGN KEY(role_id)
        REFERENCES roles(id),

    FOREIGN KEY(filiere_id)
        REFERENCES filieres(id),

    FOREIGN KEY(niveau_id)
        REFERENCES niveaux(id)
);


CREATE TABLE competences(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE utilisateur_competences(

    utilisateur_id INT,
    competence_id INT,

    PRIMARY KEY(utilisateur_id,competence_id),

    FOREIGN KEY(utilisateur_id)
        REFERENCES utilisateurs(id)
        ON DELETE CASCADE,

    FOREIGN KEY(competence_id)
        REFERENCES competences(id)
        ON DELETE CASCADE
);


CREATE TABLE utilisateur_lacunes(

    utilisateur_id INT,
    competence_id INT,

    PRIMARY KEY(utilisateur_id,competence_id),

    FOREIGN KEY(utilisateur_id)
        REFERENCES utilisateurs(id)
        ON DELETE CASCADE,

    FOREIGN KEY(competence_id)
        REFERENCES competences(id)
        ON DELETE CASCADE
);


CREATE TABLE disponibilites(

    id INT AUTO_INCREMENT PRIMARY KEY,

    utilisateur_id INT NOT NULL,

    jour ENUM(
        'Lundi',
        'Mardi',
        'Mercredi',
        'Jeudi',
        'Vendredi',
        'Samedi',
        'Dimanche'
    ),

    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,

    FOREIGN KEY(utilisateur_id)
        REFERENCES utilisateurs(id)
        ON DELETE CASCADE
);

CREATE TABLE mentorat(

    id INT AUTO_INCREMENT PRIMARY KEY,

    utilisateur_id INT NOT NULL,

    type ENUM(
        'OFFRE',
        'DEMANDE'
    ) NOT NULL,

    competence_id INT NOT NULL,

    format ENUM(
        'PRESENTIEL',
        'EN_LIGNE',
        'LES_DEUX'
    ) DEFAULT 'LES_DEUX',

    description TEXT,

    statut ENUM(
        'OUVERTE',
        'EN_COURS',
        'TERMINEE'
    ) DEFAULT 'OUVERTE',

    date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(utilisateur_id)
        REFERENCES utilisateurs(id),

    FOREIGN KEY(competence_id)
        REFERENCES competences(id)
);

CREATE TABLE matchings(

    id INT AUTO_INCREMENT PRIMARY KEY,

    mentor_id INT NOT NULL,

    mentore_id INT NOT NULL,

    score DECIMAL(5,2) NOT NULL,

    statut ENUM(
        'PROPOSE',
        'ACCEPTE',
        'REFUSE'
    ) DEFAULT 'PROPOSE',

    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(mentor_id)
        REFERENCES utilisateurs(id),

    FOREIGN KEY(mentore_id)
        REFERENCES utilisateurs(id)
);


CREATE TABLE conversations(

    id INT AUTO_INCREMENT PRIMARY KEY,

    utilisateur1_id INT NOT NULL,

    utilisateur2_id INT NOT NULL,

    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(utilisateur1_id)
        REFERENCES utilisateurs(id),

    FOREIGN KEY(utilisateur2_id)
        REFERENCES utilisateurs(id)
);


CREATE TABLE messages(

    id INT AUTO_INCREMENT PRIMARY KEY,

    conversation_id INT NOT NULL,

    expediteur_id INT NOT NULL,

    contenu TEXT NOT NULL,

    lu BOOLEAN DEFAULT FALSE,

    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE,

    FOREIGN KEY(expediteur_id)
        REFERENCES utilisateurs(id)
);



CREATE TABLE pieces_jointes(

    id INT AUTO_INCREMENT PRIMARY KEY,

    message_id INT NOT NULL,

    nom_fichier VARCHAR(255),

    chemin_fichier VARCHAR(255),

    type_fichier VARCHAR(100),

    date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(message_id)
        REFERENCES messages(id)
        ON DELETE CASCADE
);



CREATE TABLE sessions_mentorat(

    id INT AUTO_INCREMENT PRIMARY KEY,

    mentor_id INT NOT NULL,

    mentore_id INT NOT NULL,

    date_session DATETIME NOT NULL,

    duree INT NOT NULL,

    mode ENUM(
        'PRESENTIEL',
        'EN_LIGNE'
    ),

    compte_rendu TEXT,

    statut ENUM(
        'PLANIFIEE',
        'TERMINEE',
        'ANNULEE'
    ) DEFAULT 'PLANIFIEE',

    FOREIGN KEY(mentor_id)
        REFERENCES utilisateurs(id),

    FOREIGN KEY(mentore_id)
        REFERENCES utilisateurs(id)
);



CREATE TABLE evaluations(

    id INT AUTO_INCREMENT PRIMARY KEY,

    session_id INT NOT NULL,

    mentor_id INT NOT NULL,

    auteur_id INT NOT NULL,

    note INT CHECK(note BETWEEN 1 AND 5),

    commentaire TEXT,

    date_evaluation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(session_id)
        REFERENCES sessions_mentorat(id),

    FOREIGN KEY(mentor_id)
        REFERENCES utilisateurs(id),

    FOREIGN KEY(auteur_id)
        REFERENCES utilisateurs(id)
);


CREATE TABLE notifications(

    id INT AUTO_INCREMENT PRIMARY KEY,

    utilisateur_id INT NOT NULL,

    titre VARCHAR(255),

    contenu TEXT,

    est_lue BOOLEAN DEFAULT FALSE,

    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(utilisateur_id)
        REFERENCES utilisateurs(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_email
ON utilisateurs(email);

CREATE INDEX idx_telephone
ON utilisateurs(telephone);

CREATE INDEX idx_matching_score
ON matchings(score);

CREATE INDEX idx_messages_date
ON messages(date_envoi);

CREATE INDEX idx_session_date
ON sessions_mentorat(date_session);