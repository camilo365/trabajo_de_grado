from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

class User(UserMixin):

    def __init__(self, id=None, identificacion=0, celular=3113702038, usuario=None, correo=None, validado=0, contraseña_hash=None,  salt=None, p_completado=0) -> None:
        self.id = id
        self.identificacion = identificacion
        self.celular = celular
        self.usuario = usuario
        self.correo = correo
        self.validado = validado
        self.contraseña_hash = contraseña_hash #Contraseña almacenada en la base de datos
        self.salt = salt
        self.p_completado = p_completado

    @classmethod
    def validar_contrasena(self, contraseña_hash, contrasena):
        return check_password_hash(contraseña_hash, contrasena)
    
    @classmethod
    def salt(self):
        return os.urandom(10).hex()

    @classmethod
    def incriptar(self, contraseña_hash, salt):
        return generate_password_hash(contraseña_hash + salt)