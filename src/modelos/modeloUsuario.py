from .entidades.usuario import User

class ModeloUsuario():

    @classmethod
    def login(self, db, user):
        try:
            conexion = db()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, identificacion, celular, usuario, correo, validado, contraseña_hash, salt, p_completado FROM credenciales WHERE usuario=%s", (user.usuario,))
            datos = cursor.fetchone()
            conexion.close()
            cursor.close()

            if datos is not None:
                return User(id=datos[0], identificacion=datos[1], celular=datos[2], usuario=datos[3], correo=datos[4], validado=datos[5], contraseña_hash=User.validar_contrasena(datos[6], user.contraseña_hash + datos[7]), p_completado=datos[8])
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
            print(user.identificacion)
            print(user.usuario)
            print(user.correo)
            print(user.validado)
            print(user.contraseña_hash)
            print(user.salt)
            print(user.p_completado)
            cursor.execute("INSERT INTO credenciales(identificacion, celular, usuario, correo, validado, contraseña_hash, salt, p_completado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (user.identificacion, user.celular, user.usuario, user.correo, user.validado, user.contraseña_hash, user.salt, user.p_completado))
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

            cursor.execute("SELECT id, identificacion, usuario, correo FROM credenciales WHERE id=%s", (id,))
            datos = cursor.fetchone()
            
            conexion.close()
            cursor.close()

            if datos is not None:
                return User(id=datos[0], identificacion=datos[1], usuario=datos[2], correo=datos[3])
            else:
                return None
            
        except Exception as ex:
            raise Exception(ex)

    @classmethod
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
            raise Exception(ex)

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
    def validar_registro(self, db, usuario): #Función para validar el usuario en la base de datos(el usuario valido el correo de confirmación)
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

    @classmethod
    def validar_p_completado(self, db, correo): #Función para validar que el usuario completo su perfil
        """ Valida Que el usuario haya completado su registro """

        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("UPDATE credenciales SET p_completado = 1 WHERE correo = %s", (correo,))

            conexion.commit()
            conexion.close()
            cursor.close()

        except Exception as ex:
            raise Exception(ex)
        
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