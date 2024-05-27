from src.modelos.modeloUsuario import ModeloUsuario
from DB import conexion_1

class ModeloMascota():

    @classmethod
    def cargar_datos_mascota(self, db, correo_usuario):
        id_usuario = ModeloUsuario.obtener_info_usuario(conexion_1, correo_usuario)

        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT nombre, edad, raza, fecha_nacimiento, peso, vacunado FROM mascota_info WHERE id_dueño=%s",(id_usuario,))

            datos = cursor.fechtone()

            conexion.commit()
            cursor.close()
            conexion.close()

            if datos is not None:
                return datos
            else:
                return None

        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def ingresar_mascota(self, db, id_usuario, nombremascota, edad, raza, fecha_nacimiento, peso, vacunado):
        
        try:
            conexion = db()

            cursor = conexion.cursor()

            cursor.execute("INSERT INTO mascotas_info(id_dueño, nombre, edad, raza, fecha_nacimiento, peso, vacunado) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id_usuario, nombremascota, edad, raza, fecha_nacimiento, peso, vacunado))

            cursor.close()

            conexion.commit()
            conexion.close()

        except Exception as ex:
            raise Exception(ex)

