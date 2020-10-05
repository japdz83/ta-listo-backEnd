"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/ingresar", methods=["POST"])
def manejar_ingreso():
    """
        POST: revisamos si el usuario existe. Si existe, revisamos
        si el password que envía es correcto. ¿Cómo sabemos si el 
        usuario existe? Aquí vamos a recibir en el request un diccionario
        con cédula y password.
    """
    input_data = request.json
    if (
        "cedula" not in input_data or
        "password" not in input_data    
    ):
        return jsonify({
            "resultado": "Lo siento, persona, envíe los insumos correctos..."
        }), 400
    else:
        usuario = Donante.query.filter_by(
            cedula=input_data["cedula"]
        ).one_or_none()
        if usuario is None:
            return jsonify({
                "resultado": "En verdad el usuario no existe, pero le voy a decir que el password no es válido"
            }), 400
        else:
            if usuario.check_password(input_data["password"]):
                # success
                token = create_jwt(identity=usuario.id)
                return jsonify({
                    "token": token,
                    "cedula": usuario.cedula
                }), 200
            else:
                return jsonify({
                    "resultado": "El usuario sí existe y el password no sirve..."
                }), 400

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
