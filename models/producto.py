from app import db
import uuid
from models.tipoProducto import TipoProducto
from models.estadoProducto import EstadoProducto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    fecha_prod = db.Column(db.DateTime)
    fecha_venc = db.Column(db.DateTime)
    tipo_prdt = db.Column(db.Enum(TipoProducto), nullable=False)
    estado = db.Column(db.Enum(EstadoProducto), nullable=False)
    stock = db.Column(db.Integer,default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    external_id = db.Column(db.String(60), default=str(uuid.uuid4()),nullable=False)
    persona_id =  db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)
    persona = db.relationship('Persona', back_populates='producto')
    
    @property
    def serialize(self):
        return {
            'fecha_prod': self.fecha_prod,
            'fecha_venc': self.fecha_venc,
            'tipo_prdt': self.tipo_prdt.serialize() if self.tipo_prdt else None,
            'estado': self.estado.serialize if self.estado else None,
            'external_id': self.external_id,
            'nombre': self.nombre,
        }