from datetime import datetime, timezone
from app import db
from models.tipoProducto import TipoProducto

class Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrada = db.Column(db.Date)
    codigo = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    tipo_prdt = db.Column(db.Enum(TipoProducto), nullable=False)
    cantidad = db.Column(db.Integer)
    persona_id =  db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    external_id = db.Column(db.String(100), unique=True, nullable=False)
    @property
    def serialize(self):
        return {
            'fecha_entrada': self.fecha_entrada,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'tipo_prdt': self.tipo_prdt.serialize() if self.tipo_prdt else None,
            'cantidad': self.cantidad,
            'external_id': self.external_id,
        }
