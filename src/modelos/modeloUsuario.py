from .entidades.usuario import User

class ModeloUsuario():

    @classmethod
    def login(self, db, user):
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT id, usuario, correo, contraseña_hash, salt FROM credenciales WHERE usuario=%s", (user.usuario))
            datos = cursor.fetchone()

            conexion.close()
            cursor.close()

            if datos != None:
                return User(id=datos[0], usuario=datos[1], correo=datos[2], contraseña_hash=User.validar_contrasena(datos[3], user.contraseña_hash + datos[4]))
            else:
                return None
            
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def validar_datos(self, db, user):
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT id, usuario, correo FROM credenciales WHERE usuario=%s", (user.usuario))
            datos = cursor.fetchone()
            
            conexion.close()
            cursor.close()

            if datos != None:
                ##return User(id=datos[0], usuario=datos[1], correo=datos[2])
                if user.usuario == datos[1]: #Usuario ya esta registrado
                    return 0
                else:
                    return 1 #El correo ya esta registrado
            else:
                return None
            
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def registrar_usuario(self, db, user):

        try:
            conexion = db()

            cursor = conexion.cursor()

            cursor.execute("INSERT INTO credenciales(usuario, correo, contraseña_hash, salt) VALUES (%s, %s, %s, %s)", (user.usuario, user.correo, user.contraseña_hash, user.salt))

            cursor.close()

            conexion.commit()
            conexion.close()

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def obtener_usuario(self, db, id):
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT id, usuario, correo FROM credenciales WHERE usuario=%s", (id))
            datos = cursor.fetchone()
            
            conexion.close()
            cursor.close()

            if datos != None:
                return User(id=datos[0], usuario=datos[1], correo=datos[2])
            else:
                return None
            
        except Exception as ex:
            raise Exception(ex)