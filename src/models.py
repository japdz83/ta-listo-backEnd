from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime, timezone
import os
from base64 import b64encode

db = SQLAlchemy()

class usuarioCliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rif = db.Column(db.String(14), unique=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(15))
    password_hash = db.Column(db.String(250), nullable=False)
    razon_social = db.Column(db.string(20), nullable=False)
    direccion = db.Column(db.String(400))

    ordenTrabajo = db.relationship("ordenTrabajo", backref="usuarioCliente", uselist=False)
    consumidor = db.relationship("consumidor", backref="usuarioCliente", uselist=False)

    def __init__(self, rif, nombre, apellido, email, telefono, password_hash, razon_social, direccion):
        """ crea y devuelve una instancia de esta clase """
        self.rif = rif
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.set_password(password)
        self.razon_social = razon_social
        self.direccion = direccion

    def set_password(self, password):
        """ hash y guarda """
        self.password_hash = generate_password_hash(f"{password}{self.salt}")

    def check_password(self, password):
        """ checks if match """
        return check_password_hash(self.password_hash, f"{password}{self.salt}")

    @classmethod
    def cargar(cls):
        """
            abre el archivo donante.json y carga en la 
            variable donantes objetos donante para cada
            uno de los diccionarios de la lista
        """
        _usuario = []
        try:
            with open("./donante.json", "r") as usuario_archivo:
                usuario_diccionarios = json.load(usuario_archivo)
                for usuario in usuario_diccionarios:
                    nuevo_donante = cls.registrarse(
                        usuario["cedula"],
                        usuario["nombre"],
                        usuario["apellido"]
                    )
                    _donantes.append(nuevo_usuario)
        except:
            with open("./usuario.json", "w") as usuario_archivo:
                pass
        return _usuaruio

    @staticmethod
    def salvar(donantes):
        """
            guarda donantes en formato json en el archivo
            correspondiente
        """
        with open("./usuario.json", "w") as usuario_archivo:
            usuario_serializados = []
            for usuario in usuarios:
                usuarios_serializados.append(usuario.serializar())
            json.dump(usuarios_serializados, usuario_archivo)


class ordenTrabajo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_ot_usuario = db.Column(db.String(14), unique=True)
    id_ot_consumidor = db.Column(db.String(80), nullable=False)
    descripcion_ot = db.Column(db.String(80), nullable=False)
    Estatus = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime(timezone=True))
    fecha_resolucion = db.Column(db.DateTime(timezone=True))
    fecha_entrega = db.Column(db.DateTime(timezone=True))
    

    consumidor = db.relationship("consumidor", backref="ordenTrabajo", uselist=False)
    usuarioCliente = db.relationship("usuarioClienter", backref="ordenTrabajo", uselist=False)

def __init__(self, visita_id):






class consumidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(14), unique=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(400))
    
    ordenTrabajo = db.relationship("ordenTrabajo", backref="consumidor", uselist=False)
    usuarioCliente = db.relationship("usuarioCliente", backref="consumidor", uselist=False)

def __init__(self, cedula,nombre,apellido,email,telefono,direccion):