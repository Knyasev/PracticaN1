from app import db 
import uuid


class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    external_id = db.Column(db.String(60), default=str(uuid.uuid4()),nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    detalle_factura = db.relationship('DetalleFactura', back_populates='factura')
    @property
    def serialize(self):
        return {
            'fecha': self.fecha,
            'external_id': self.external_id,
        }