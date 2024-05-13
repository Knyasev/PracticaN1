from app import db
import uuid

class DetalleFactura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)
    total = db.Column(db.Float)
    external_id = db.Column(db.String(60), default=str(uuid.uuid4()),nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    factura_id =  db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    factura = db.relationship('Factura', back_populates='detalle_factura')
    producto_id =  db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    producto = db.relationship('Producto', back_populates='detalle_factura')