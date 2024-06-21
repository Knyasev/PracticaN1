from app import db
import uuid
from models.estadoProducto import EstadoProducto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    fecha_prod = db.Column(db.DateTime)
    fecha_venc = db.Column(db.DateTime)
    precio = db.Column(db.Float)
    estado = db.Column(db.Enum(EstadoProducto), nullable=False)
    status = db.Column(db.Boolean, default=True)
    stock = db.Column(db.Integer,default=0)
    imagen_producto = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    external_id = db.Column(db.String(60), default=str(uuid.uuid4()),nullable=False)
    detalle_factura = db.relationship('DetalleFactura', back_populates='producto')
    lote_id = db.Column(db.Integer, db.ForeignKey('lote.id'), nullable=False)
    lote = db.relationship('Lote', backref=db.backref('productos', lazy=True))

    @property
    def serialize(self):
        return {
            'fecha_prod': self.fecha_prod,
            'fecha_venc': self.fecha_venc,
            'estado': self.estado.serialize if self.estado else None,
            'external_id': self.external_id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            'lote': self.lote.cantidad if self.lote else None,
            'status': self.status,
            'imagen_producto': self.imagen_producto
        }