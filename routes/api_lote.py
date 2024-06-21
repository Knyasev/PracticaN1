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
    'required': ['fecha_entrada', 'codigo', 'nombre', 'tipo_prdt', 'cantidad']

}
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
    if lote_id>=0:
        # Si el lote se guardó correctamente, devolver la lista de lotes actualizada
        return make_response(
            jsonify({"msg": "Lote registrado con éxito", "code": 200, "datos": ([i.serialize for i in loteC.listar()])}),
            200
        )
    else:
        # Si hubo un error al guardar el lote, devolver un mensaje de error
        return make_response(
            jsonify({"msg": "Error al registrar el lote", "code": 400}),
            400
        )
@api_lote.route("/lote/<external_id>")
@token_required
def buscar_external(external_id):
    lote = loteC.buscar_external(external_id)
    if lote:
        # Devuelve el diccionario 'lote' directamente sin llamar a .serialize()
        return make_response(jsonify({"msg": "OK", "code": 200, "datos": lote.serialize}), 200)
    else:
        return make_response(jsonify({"msg": "Error", "code": 404, "datos": {"error": "Persona no encontrada"}}), 404)


@api_lote.route("/lote/<external>", methods=['POST'])
@token_required
@expects_json(schema)
def modificar(external):
    data = request.get_json()
    data['external_id'] = external
    id = loteC.modificar(data)
    lote = loteC.buscar_external(external)
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

@api_lote.route("/listar_tiposP", methods=['GET'])
def listar_estados():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": loteC.listar_tiposP()}),
        200
    )    
