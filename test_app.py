import unittest
import json
from app import app  # On importe ton serveur Flask actuel

class TestMentorLinkAuthErrors(unittest.TestCase):

    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.app = app.test_client()
        self.app.testing = True

    # Première erreur = Les champs manquants
    def test_register_missing_fields(self):
        payload = {
            "nom": "Lissassi",
            "prenom": "Meschac"
            # Il manque l'email, le mot de passe, etc.
        }
        response = self.app.post('/register', 
                                 data=json.dumps(payload), 
                                 content_type='application/json')
        
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Veuillez remplir tous les champs", data['error'])

    # Deuxième erreur : Une connexion avec des champs manquants
    def test_login_missing_fields(self):
        payload = {
            "email": "test@etudiant.com"
            # Il manque le mot de passe
        }
        response = self.app.post('/login', 
                                 data=json.dumps(payload), 
                                 content_type='application/json')
        
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Veuillez remplir tous les champs", data['error'])

    # Troisième erreur : Une connexion avec un compte inexistant ou n'ayant pas encore été créé
    def test_login_wrong_user(self):
        payload = {
            "email": "compte_qui_n_existe_pas_du_tout@ifri.com",
            "mot_de_passe": "password123"
        }
        response = self.app.post('/login', 
                                 data=json.dumps(payload), 
                                 content_type='application/json')
        
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Identifiants incorrects", data['error'])

    # Quatrième erreur : Quand l'utilisateur essaie d'accéder a des routes protégées de l'application sans etre connecté
    def test_dashboard_access_denied(self):
        # On tente d'accéder au dashboard sans avoir fait de /login au préalable
        response = self.app.get('/dashboard')
        
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Accès refusé. Veuillez vous connecter.", data['error'])

    # Cinquième erreur : Réinitialisation de mot de passe avec un email inconnu
    def test_reset_password_unknown_email(self):
        payload = {
            "email": "inconnu@ifri.com",
            "nouveau_mot_de_passe": "NewPass123!"
        }
        response = self.app.post('/reset-password', 
                                 data=json.dumps(payload), 
                                 content_type='application/json')
        
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertIn("Aucun compte associé à cet email", data['error'])

if __name__ == '__main__':
    unittest.main()