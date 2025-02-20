"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Favorite
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import NoResultFound


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.

@api.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@api.route('/signup', methods=['POST'])
# @api.route('/signup/<int:id>', methods=['POST'])
def create_user():
    try :
        # si en try sucede algun tipo de error lo colocamos en el except:

        request_body = request.json
        print(request_body)
        user = db.session.execute(db.select(User) .filter_by (email=request_body ["email"])). scalar_one()

                # user = db.session.execute(db.select(Table) .filter_by (atributo de busqueda =request_body ["at de busqueda "])). scalar_one()

        return jsonify({"msg": "cannot create, user already exist"}), 400

    except: 
        user = User(email=request_body["email"], password=request_body["password"], is_active= request_body["is_active"])
        # crea user
        db.session.add(user)
        # agregar user
        db.session.commit()
        # commit = grabado en piedra
    

    return jsonify({"msg": "created"}), 201

@api.route("/login", methods=["POST"])
def login():
    try:
        #     # OBTIENE INFO CUERPO PETICION
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        # 1 registro de tabla específica
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
        # filtrar user por email y si lo encuentras muéstralo en print
        print(user)

        # establecer condiciones si el email que me envian desde el front es distinto envia error si no envia el token
        if email != user.email or password != user.password:
            return jsonify({"msg": "Bad password or email"}), 401

        access_token = create_access_token(identity=email)
        return jsonify({"access_token":access_token, "user": user.serialize()})
    # esta ultima de serialize no la entiendo

# # ESTE PROCESO DE DONDE SE GUARDA LOS LLEVA EL PERSONAL DE JWT    
    except NoResultFound:
        return jsonify ({"msg": "Bad password or email"}), 401


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/private", methods=["GET"])
# esto de abajo seria el portero de la analogia, entre la ruta y el metodo de autenticación 
@jwt_required()
# cuando el corrobora el token entra a la funcion y especifica
def protected():
    # Access the identity of the current user with get_jwt_identity
    # verifica la identidad ( de quien es el token ) , lo corrobora
    current_user = get_jwt_identity()

    # con la identidad anterior nosotros hacemos una busqueda

    # user = db.session.execute(db.select(User).filter_by(email=current_user)).scalar_one()


#con la busqueda del señor anterior en la tabla favoritos fijate cuantos tiene y traemelos 
# user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
    # la entidad verificada se guarda en el espacio de memoria
    return jsonify(logged_in_as=current_user), 200

@api.route('/favorites', methods=['GET'])
@jwt_required()
def protected_favorite():
    current_user = get_jwt_identity()

    user = db.session.execute(db.select(User).filter_by(email=current_user)).scalar_one()
    print(user.id)
    print(user.favorites)
    # favorites = db.session.execute(db.select(Favorite).filter_by(user_id=user.id)).scalars()
    # mapear
    results = list(map(lambda item: item.serialize(), user.favorites))
    print(results)
    

    
    return jsonify({"results" : results}), 200

