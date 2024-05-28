from src.modelos.modeloUsuario import ModeloUsuario
from DB import conexion_1, conexion_2

class ModeloMascota():

    @classmethod
    def cargar_datos_mascota(self, db, correo_usuario):
        id_usuario = ModeloUsuario.obtener_info_usuario(conexion_2, correo_usuario)

        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT nombre, edad, raza, fecha_nacimiento, peso, vacunado FROM mascotas_info WHERE id_dueño=%s",(id_usuario,))

            datos = cursor.fetchall()

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

    @classmethod
    def eliminar_mascota(self, db, id_usuario):
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM mascotas_info WHERE id_dueño=%s",(id_usuario,))

            conexion.commit()
            cursor.close()
            conexion.close()

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizar_mascota(self, db, datos_actuales, nuevos_datos):
        try:
            conexion = db()
            cursor = conexion.cursor()

            columnas = ("id_dueño","nombre","edad","raza","fecha_nacimiento","peso","vacunado")

            valores_actuales = dict(zip(columnas, datos_actuales))

            nuevos_valores = dict(zip(columnas, nuevos_datos))

            # Filtrar solo los campos que han cambiado
            campos_a_actualizar = {k: v for k, v in valores_actuales.items() if nuevos_valores[k] != v }

            set_clause = ", ".join([f"{campo}=%s" for campo in campos_a_actualizar.keys()])
            query = f"UPDATE mascotas_info SET {set_clause} WHERE id_dueño=%s"
            valores = list(campos_a_actualizar.values()) + [valores_actuales["id_dueño"]]

            cursor.execute(query, valores)

            conexion.commit()
            cursor.close()
            conexion.close()

        except Exception as ex:
            raise Exception(ex)


