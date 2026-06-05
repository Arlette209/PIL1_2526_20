from flask import Flask
from flask_cors import CORS
from backend_matching.matching import matching_bp

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@Advent7JR'
app.config['MYSQL_DB'] = 'ifri_mentorlink'

app.register_blueprint(matching_bp)

@app.route('/')
def index():
    return "Le serveur Flask connecté à la base ifri_mentorlink est en ligne !", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')