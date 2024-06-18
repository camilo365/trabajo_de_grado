from .entidades.usuario import User

class ModeloUsuario():

    @classmethod
    def login(self, db, user):
        try:
            conexion = db()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, identificacion, nombre, apellido, edad, celular, usuario, correo, validado, contraseña_hash, salt FROM credenciales WHERE usuario=%s", (user.usuario,))

            datos = cursor.fetchone()
            conexion.close()
            cursor.close()

            if datos is not None:
                return User(id=datos[0], identificacion=datos[1], nombre=datos[2], apellido=datos[3], edad=datos[4], celular=datos[5], usuario=datos[6], correo=datos[7], validado=datos[8], contraseña_hash=User.validar_contrasena(datos[9], user.contraseña_hash + datos[10]))
            else:
                return None
            
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def validar_datos(self, db, user):
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT id, usuario, correo FROM credenciales WHERE usuario=%s", (user.usuario,))
            datos = cursor.fetchone()
            
            conexion.close()
            cursor.close()

            if datos is not None:
                if user.usuario == datos[1]: #datos[1] es el usuario
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
            cursor.execute("INSERT INTO credenciales(identificacion, nombre, apellido, edad, celular, usuario, correo, validado, contraseña_hash, salt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (user.identificacion, user.nombre, user.apellido, user.edad, user.celular, user.usuario, user.correo, user.validado, user.contraseña_hash, user.salt))
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

            cursor.execute("SELECT id, identificacion, nombre, apellido, celular, usuario, correo FROM credenciales WHERE id=%s", (id,))
            datos = cursor.fetchone()
            
            conexion.close()
            cursor.close()

            if datos is not None:
                return User(id=datos[0], identificacion=datos[1], nombre=datos[2], apellido=datos[3], celular=datos[4],  usuario=datos[5], correo=datos[6])
            else:
                return None
            
        except Exception as ex:
            raise Exception(ex)

    """ @classmethod
    def obtener_info_usuario(self, db, correo_usuario):
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT identificacion FROM usuario_info WHERE correo=%s", (correo_usuario,))

            datos = cursor.fetchone()

            conexion.close()
            cursor.close()

            if datos is not None:
                return datos
            else:
                return None

        except Exception as ex:
            raise Exception(ex) """

    @classmethod
    def obtener_correo_usuario(self, db, correo): #Verificar si el correo existe
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT EXISTS (SELECT 1 FROM credenciales WHERE correo=%s)", (correo,))
            datos = cursor.fetchone()[0]

            conexion.close()
            cursor.close()

            if datos is not None:
                return datos
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def validar_registro(self, db, usuario): #Función para validar el usuario en la base de datos(el usuario a valido el correo de confirmación)
        """ Valida el usuario en la base de datos """

        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("UPDATE credenciales SET validado = 1 WHERE usuario = %s", (usuario,))

            conexion.commit()
            conexion.close()
            cursor.close()

        except Exception as ex:
            raise Exception(ex)

    """ @classmethod
    def validar_p_completado(self, db, correo): #Función para validar que el usuario completo su perfil

        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("UPDATE credenciales SET p_completado = 1 WHERE correo = %s", (correo,))

            conexion.commit()
            conexion.close()
            cursor.close()

        except Exception as ex:
            raise Exception(ex) """
        
    @classmethod
    def cambiar_contraseña(self, db, contraseña, correo):
        try:
            conexion = db()
            cursor = conexion.cursor()

            salt = User.salt()
            contraseña_hash = User.incriptar(contraseña, salt)

            cursor.execute("UPDATE credenciales SET contraseña_hash=%s, salt=%s WHERE correo=%s", (contraseña_hash, salt, correo))

            conexion.commit()
            conexion.close()
            cursor.close()
            
        except Exception as ex:
            raise Exception(ex)