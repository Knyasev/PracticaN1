from models.persona import Persona
from models.rol import Rol
from models.cuenta import Cuenta
from app import db
from datetime import datetime, timedelta,timezone
from flask import current_app
import jwt
import uuid

class PersonaController:
    def listar(self):
        return Persona.query.all()
    
    def save(self, data):
        persona = Persona()
        persona.apellido = data.get("apellido")
        persona.nombre = data.get("nombre")
        persona.external_id = uuid.uuid4()
        persona.rol_id = data.get("rol_id")
        db.session.add(persona)
        db.session.commit()
        return persona.id
    
    def guardar_cajero(self,data):
        rol = Rol.query.filter_by(nombre="CAJERO").first()
        persona = Persona()
        if rol:
            persona.external_id = uuid.uuid4()
            persona.apellido = data.get("apellido")
            persona.nombre = data.get("nombre")
            persona.rol_id = rol.id
            db.session.add(persona)
            db.session.commit()
            return  persona.id
        else:
            return -1
        
    def guardar_cuenta(self,data):
        rol = Rol.query.filter_by(nombre="ADMINISTRADOR").first()
        persona = Persona()
        if rol:
            cuenta = Cuenta.query.filter_by(usuario=data.get("correo")).first()
            if cuenta:
                return -2
            else:

                persona.external_id = uuid.uuid4()
                persona.apellido = data.get("apellido")
                persona.nombre = data.get("nombre")
                persona.rol_id = rol.id
                db.session.add(persona)
                db.session.commit()
                cuenta = Cuenta()
                cuenta.usuario = data.get("correo")
                cuenta.clave = data.get("clave")
                cuenta.persona_id = persona.id
                cuenta.external_id = str(uuid.uuid4())
                db.session.add(cuenta)
                db.session.commit()
            return  cuenta.id
        else:
            return -1

    def buscar_external(self, external):
        return Persona.query.filter_by(external_id=external).first()
    
    
    def modificar(self, external_id, data):
        persona = self.buscar_external(external_id)
        if persona:
            persona.apellido = data.get("apellido")
            persona.nombre = data.get("nombre") 
            persona.fecha_nacimiento = data.get("fecha_nacimiento")
            persona.external_id = uuid.uuid4()
            db.session.add(persona)
            db.session.commit()
            return persona
        else:
            return -1

        
    def copiar(self, external_id):
            persona = self.buscar_external(external_id)
            if persona:
                nueva_persona = Persona()
                nueva_persona.apellido = persona.apellido
                nueva_persona.nombre = persona.nombre
                nueva_persona.fecha_nacimiento = persona.fecha_nacimiento
                nueva_persona.rol_id = persona.rol_id
                db.session.add(nueva_persona)
                db.session.commit()
                return nueva_persona
            else:
                return -1
        

    def desactivar(self, external_id):
        persona = self.buscar_external(external_id)
        if persona and persona.rol.nombre == 'ADMINISTRADOR':                
                cuenta = Cuenta.query.filter_by(persona_id=persona.id).first()
                if cuenta:
                    cuenta.estado = 0  # Cambia el estado de la cuenta a 0 (desactivado)
                    db.session.add(cuenta)
                    db.session.commit()
                return cuenta
        return False
    

    def activar_cuenta(self, external_id):
        persona = self.buscar_external(external_id)
        if persona and persona.rol.nombre == 'ADMINISTRADOR':                
                cuenta = Cuenta.query.filter_by(persona_id=persona.id).first()
                if cuenta:
                    cuenta.estado = 1  # Cambia el estado de la cuenta a 1 (activado)
                    db.session.add(cuenta)
                    db.session.commit()
                return cuenta
        return False
        
    def inicio_sesion(self, data):
        cuentaA = Cuenta.query.filter_by(usuario = data.get('usuario')).first()
        if cuentaA:
            # TODO encriptar
            if cuentaA.clave == data["clave"]:
                token = jwt.encode(
                    {
                        "external": cuentaA.external_id,
                        "expiracion": (datetime.utcnow()+ timedelta(minutes=30)).isoformat()
                    }, 
                    key = current_app.config["SECRET_KEY"],
                    algorithm="HS512"
                )
                cuenta = Cuenta.query.get(cuentaA.id)
                persona = cuenta.getPersona(cuentaA.persona_id)
                info = {
                    "token": token,
                    "user": persona.apellido + " " + persona.nombre
                }
                return info
            else:
                return -5
        else:
            return -5
        