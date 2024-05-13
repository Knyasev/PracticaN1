from flask import Blueprint, jsonify, make_response, request
# Importacion de los modelos de tablas de la base de datos
from models.rol import Rol
from models.persona import Persona
from models.producto import Producto
from models.cuenta import Cuenta
from models.lote import Lote
from models.detalleFactura import DetalleFactura
from models.factura import Factura

api = Blueprint('api', __name__)
