from models.lote import Lote
from app import db
import uuid
from models.persona import Persona
from models.rol import Rol
from datetime import datetime, timedelta,timezone
from models.tipoProducto import TipoProducto

class LoteController: 
    def listar(self):
        return Lote.query.all()
  
    def buscar_external(self, external):
        return Lote.query.filter_by(external_id=external).first()
    
    def listar_tiposP(self):
        return [e.value for e in TipoProducto] 
    
    def save(self, data):
        persona = Persona.query.filter_by(external_id=data.get("persona_id")).first()
        print(persona)
        if persona :
            lote = Lote()
            lote.fecha_entrada = data.get("fecha_entrada")
            lote.codigo = data.get("codigo")
            lote.nombre = data.get("nombre")
            lote.tipo_prdt = data.get("tipo_prdt")
            lote.cantidad = data.get("cantidad")
            lote.external_id = uuid.uuid4()
            lote.persona_id = persona.id
            db.session.add(lote)
            db.session.commit()
            return lote.id
        else: 
            return -6
    
    def modificar(self, data):
        lote = self.buscar_external(data.get("external_id"))
        if lote:
            lote.fecha_entrada = data.get("fecha_entrada")
            lote.codigo = data.get("codigo")
            lote.nombre = data.get("nombre")
            lote.tipo_prdt = data.get("tipo_prdt")
            lote.cantidad = data.get("cantidad")
            db.session.add(lote)
            db.session.commit()
            return lote.id
        else:
            return -1

    def restar_cantidad(self, external_id, cantidad):
        lote = self.buscar_external(external_id)
        if lote:
            lote.cantidad = lote.cantidad - cantidad
            db.session.commit()
            return lote.id
        else:
            return -1
