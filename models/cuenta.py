from app import db
from models.rol import Rol
import uuid

class Cuenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100))
    clave = db.Column(db.String(250))
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.String(60), default=str(uuid.uuid4()),nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)
    persona = db.relationship('Persona', back_populates='cuenta', lazy=True)

    def serialize(self):
        return {
        'usuario': self.usuario,
        'external_id': self.external_id,
        'estado': self.estado,
    }
    def getPersona(self, id_p):
        from models.persona import Persona
        return Persona.query.filter_by(id = id_p).first()

    def copy(self, value):
        self.usuario= value.get('usuario')
        self.clave = value.get('clave')
        self.estado = value.get('estado')
        self.id = value.get('id')
        self.external_id = str(uuid.uuid4())
        return self