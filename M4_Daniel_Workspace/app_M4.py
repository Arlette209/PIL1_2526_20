from flask import Flask
from flask_cors import CORS
from M4_Daniel_Workspace.backend_M4.matching import matching_bp
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, ressources={r"*/": {"origins": "*"}})

app.register_blueprint(matching_bp)

@app.route('/')
def index():
    return "Le serveur Flask du Module 4 (Matching) est en ligne et prêt !", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')