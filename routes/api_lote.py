from flask import Blueprint, jsonify, make_response, request
# Importacion de los modelos de tablas de la base de datos
from controllers.loteController import LoteController
from controllers.utils.errors import Error
from flask_expects_json import expects_json
from controllers.authenticate import token_required
api_lote = Blueprint('api_lote', __name__)

loteC= LoteController()
schema = { 
    'type': 'object',
    'properties': {
        'fecha_entrada': {'type': 'string'},
        'codigo': {'type': 'string'},
        'nombre': {'type': 'string'},
        'tipo_prdt': {'type': 'string'},
        'cantidad': {'type': 'integer'},
    },
    'required': ['fecha_entrada', 'codigo', 'nombre', 'tipo_prdt', 'cantidad']}



@api_lote.route("/lote")
@token_required
def listar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": ([i.serialize for i in loteC.listar()])}),
        200
    )

@api_lote.route('/registrar/lote', methods=['POST'])
@token_required
@expects_json(schema)
def save():
    data = request.get_json()
    lote_id = loteC.save(data)
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": ([i.serialize for i in loteC.listar()])}),
        200
    )

@api_lote.route("/producto/<external>")
def buscar_external(external):
    search = loteC.buscar_external(external)
    if search is not None:
        search = search.serialize()
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [] if search is None else search}),
        200
    )



@api_lote.route("/producto/modificar/<external>", methods=['POST'])
@token_required
@expects_json(schema)
def modificar(external):
    data = request.get_json()
    data['external_id'] = external
    id = loteC.modificar(data)
    censo = loteC.buscar_external(external)
    if (id >=0):
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": "Datos Modificados"}),
            200
        )
    else:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Error.error[str(id)]}}), 
        )



@api_lote.route("/producto/<external_id>/desactivar", methods=['GET'])
def desactivar(external_id):
    censo = loteC.desactivar(external_id)
    if censo is None or censo == -1:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Error.error[str(id)]}}), 
        )

    censo = loteC.buscar_external(external_id)
    search = censo.serialize()
    return make_response(jsonify({"msg": "OK", "code": 200, "datos": search}), 200)

