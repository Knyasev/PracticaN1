from flask import Blueprint, jsonify, make_response, request
# Importacion de los modelos de tablas de la base de datos
from controllers.productoController import ProductoController
from controllers.utils.errors import Error
from flask_expects_json import expects_json
from controllers.authenticate import token_required
api_producto = Blueprint('api_producto', __name__)

censoC= ProductoController()
schema = { 
    'type': 'object',
    'properties': {
        'fecha_prod': {'type': 'string'},
        'fecha_venc': {'type': 'string'},
        'estado': {'type': 'boolean'},
        'nombre': {'type': 'string'},
        
    },
    'required': ['fecha_prod', 'fecha_venc', 'estado' , 'nombre']}
censo_persona_schema = {
    "type": "object",
    'properties': {
        "latitud": {"type": "number"},
        "longitud": {"type": "number"},
        "motivo": {"type": "string"},
    },
    'required': ["latitud", "longitud", "motivo"]
}


@api_producto.route("/producto")
@token_required
def listar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": ([i.serialize for i in censoC.listar()])}),
        200
    )

@api_producto.route("/producto/caducados")
@token_required
def listarCaducados():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": ([i.serialize for i in censoC.listar_productos_caducados()])}),
        200
    )

@api_producto.route('/productos/por_caducar')
@token_required
def productos_por_caducar():
    productos_por_caducar_por_lote = censoC.listarporCaducar()
    return jsonify([i.serialize for i in censoC.listar_productos_por_caducar()]), 200

@api_producto.route("/producto/listar/caducados")
def listar_productos_caducados():
    productos = censoC.listarCaducados()
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize for i in censoC.listar_productos_caducados()]}),
        200
    )

@api_producto.route('/productos/buenos')
@token_required
def productos_buenos():
    productos_serializados = [producto.serialize for producto in censoC.listar_productos_buenos()]
    return jsonify(productos_serializados), 200


@api_producto.route('/<external_id>/registrar/produto', methods=['POST'])
@token_required
def registar_producto_persona_route(external_id):
    data = request.get_json()
    producto = censoC.registar_producto_persona(data,external_id)
    if producto == -1:
        return jsonify({'error': 'No se encontró la persona con el external_id proporcionado'}), 400
    elif producto == -2:
        return jsonify({'error': 'La cantidad de productos ya es igual a la cantidad del lote'}), 400
    else:
        return jsonify({'Datos Guardados': producto.serialize}), 200
    
@api_producto.route('/producto/<external_id>/subir_imagen', methods=['POST'])
@token_required
def subir_imagen_producto_route(external_id):
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se ha enviado ningún archivo'}), 400
    file = request.files['imagen']
    if file.filename == '':
        return jsonify({'error': 'No se ha seleccionado ningún archivo'}), 400
    if file and allowed_file(file.filename):
        if file.content_length > 5 * 1024 * 1024:  # 5MB
            return jsonify({'error': 'El archivo es demasiado grande. Tamaño máximo permitido: 5MB'}), 400
        resultado = ProductoController().subir_imagen_producto(external_id)
        return jsonify(resultado)
    else:
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS   

@api_producto.route("/producto/<external>")
def buscar_external(external):
    search = censoC.buscar_external(external)
    if search is not None:
        search = search.serialize()
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [] if search is None else search}),
        200
    )



@api_producto.route("/producto/modificar/<external>", methods=['POST'])
@expects_json(schema)
def modificar(external):
    data = request.get_json()
    data['external_id'] = external
    id = censoC.modificar(data)
    censo = censoC.buscar_external(external)
    if (id >=0):
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": "Datos Modificados"}),
            200
        )
    else:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Error.error[str(id)]}}), 
        )



@api_producto.route("/producto/<external_id>/desactivar", methods=['GET'])
def desactivar(external_id):
    censo = censoC.desactivar(external_id)
    if censo is None or censo == -1:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Error.error[str(id)]}}), 
        )

    censo = censoC.buscar_external(external_id)
    search = censo.serialize()
    return make_response(jsonify({"msg": "OK", "code": 200, "datos": search}), 200)

@api_producto.route("/producto/listar_estados")
def listar_estado():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": censoC.listar_estado()}),
        200
    )

