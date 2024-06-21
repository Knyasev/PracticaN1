from models.producto import Producto
from app import db
import uuid
from models.persona import Persona
from models.rol import Rol
from datetime import datetime, timedelta,timezone
from models.lote import Lote    
from models.estadoProducto import EstadoProducto
import os
from flask import request
from werkzeug.utils import secure_filename
class ProductoController:
    def listar(self):
        return Producto.query.all()
    
    def listar_productos_buenos(self):
        return Producto.query.filter_by(estado="BUENO").all()
        
    def listar_productos_caducados(self):
        return Producto.query.filter_by(estado="CADUCADO").all()
    
    def listar_productos_por_caducar(self):
        return Producto.query.filter_by(estado="POR_CADUCAR").all()

    def listar_estado(self):
        return [e.value for e in EstadoProducto]
    
    def modificar(self, data):
        producto = self.buscar_external(data.get("external_id"))
        if producto:
            producto.nombre = data.get("nombre")
            producto.fecha_prod = data.get("fecha_prod")
            producto.fecha_venc = data.get("fecha_venc")
            producto.estado = data.get("estado")
            producto.precio = data.get("precio")
            producto.status = data.get("status")
            db.session.merge(producto)
            db.session.commit()
            
            return producto.id

    def buscar_external(self, external):
        return Producto.query.filter_by(external_id=external).first()    

   
    def desactivar(self,external_id):
        producto = self.buscar_external(external_id)
        if producto:
            producto.estado = "Caducado"
            db.session.commit()
            return producto.id
        else:
            return -1

        
    def registar_producto_persona(self, data,external_id_lote):
        lote = Lote.query.filter_by(external_id=external_id_lote).first()
        if lote:
            productos_existentes = Producto.query.filter_by(lote_id=lote.id).count()
            if productos_existentes >= lote.cantidad:
                return -2  
            producto = Producto()  
            producto.external_id = str(uuid.uuid4())
            producto.nombre = lote.nombre
            producto.fecha_prod = data.get("fecha_prod")
            producto.fecha_venc = data.get("fecha_venc")
            producto.estado = data.get("estado")
            producto.lote_id= lote.id
            producto.precio = data.get("precio")
            producto.status = True
    
            # Sumar las cantidades de todos los lotes con el mismo nombre
            lotes_mismo_nombre = Lote.query.filter_by(nombre=lote.nombre).all()
            total_cantidad = sum([lote_mismo.cantidad for lote_mismo in lotes_mismo_nombre])
            producto.stock = total_cantidad
    
            db.session.add(producto)
            db.session.commit() 
            return producto
        else:
            return -1
        

    
    def subir_imagen_producto(self, external_id):
        producto = Producto.query.filter_by(external_id=external_id).first()
        if producto:
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file.filename == '':
                    return {'error': 'No se ha seleccionado ningún archivo'}, 400
                if file:
                    filename = secure_filename(file.filename)
                    # Ruta base fuera del backend, por ejemplo, en un directorio 'imagenes' en el mismo nivel que el directorio 'backend'
                    ruta_base = r'C:\Users\Gonzalez G\Desktop\Wilson Gonzalez\5 Ciclo\Desarrollo de plataformas\PracticaN3\backend'
                    ruta_imagenes = os.path.join(ruta_base, 'imagenes')
                    if not os.path.exists(ruta_imagenes):
                        os.makedirs(ruta_imagenes)
                    file_path = os.path.join(ruta_imagenes, filename)
                    file.save(file_path)
                    # Modificación aquí: guardar solo la parte relativa de la ruta
                    relative_path = os.path.join('imagenes', filename)
                    producto.imagen_producto = relative_path
                    db.session.add(producto)  # Asegúrate de agregar el objeto modificado a la sesión.
                    db.session.commit()
                    return {'mensaje': 'Imagen subida correctamente'}, 200
            return {'error': 'Archivo no encontrado'}, 400
        else:
            return {'error': 'Producto no encontrado'}, 404

    def listarporCaducar(self):
        fecha_caducar = datetime.now(timezone.utc) + timedelta(days=5)
        lotes = Lote.query.all()
        productos_por_caducar_por_lote = {}

        for lote in lotes:
            productos_por_caducar = Producto.query.filter(Producto.fecha_venc <= fecha_caducar, Producto.lote_id == lote.id).all()
            productos_por_caducar_por_lote[lote.nombre] = productos_por_caducar

            for producto in productos_por_caducar:
                if producto.status == True :
                    producto.estado = producto.estado.POR_CADUCAR 
                    producto.stock -= len(productos_por_caducar)
                    producto.status = False
                else :
                    producto.estado = producto.estado.POR_CADUCAR
                    

            # Reducir el stock de los productos buenos y los productos por caducar de todos los lotes con el mismo nombre
            lotes_mismo_nombre = Lote.query.filter_by(nombre=lote.nombre).all()
            for lote_mismo_nombre in lotes_mismo_nombre:
                productos_a_reducir_stock = Producto.query.filter((Producto.estado == "BUENO") | (Producto.id.in_([p.id for p in productos_por_caducar])), Producto.lote_id == lote_mismo_nombre.id).all()
                for producto in productos_a_reducir_stock:
                    producto.stock -= len(productos_por_caducar)
            db.session.commit()
        return productos_por_caducar_por_lote
    
    def listarCaducados(self):
        fecha_actual = datetime.now(timezone.utc)
        lotes = Lote.query.all()
        productos_caducados_por_lote = {}

        for lote in lotes:
            productos_caducados = Producto.query.filter((Producto.fecha_venc < fecha_actual) | (Producto.estado == "POR_CADUCAR"), Producto.lote_id == lote.id).all()
            productos_caducados_por_lote[lote.nombre] = [{'id': producto.id, 'nombre': producto.nombre, 'estado': producto.estado, 'stock': producto.stock, 'fecha_venc': producto.fecha_venc} for producto in productos_caducados]

            for producto in productos_caducados:
                producto.estado = "CADUCADO"
                if producto.status == True:
                    producto.stock -= 1
                    producto.status = False
            db.session.commit()

        print(productos_caducados_por_lote)  # Imprime el resultado en la consola
        return productos_caducados_por_lote
    
    
    