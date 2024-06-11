from src.modelos.modeloUsuario import ModeloUsuario
from DB import conexion_1, conexion_2

import json

class ModeloMascota():

    @classmethod
    def cargar_datos_mascota(self, db, id_usuario, id_mascota):
        #id_usuario = ModeloUsuario.obtener_info_usuario(conexion_2, correo_usuario)

        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT nombre, edad, raza, fecha_nacimiento, peso, vacunado FROM mascotas_info WHERE id_dueño=%s AND id_mascota=%s", (id_usuario, id_mascota))

            datos = cursor.fetchone()

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
    
    
    # modeloMascota.py

    @classmethod
    def mascotas_datos(cls, db, id_usuario):
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM mascotas_info m LEFT JOIN usuario_info u ON m.id_dueño = u.identificacion WHERE u.identificacion = %s", (id_usuario))
            mascotas = cursor.fetchall()  # Obtener todas las filas de resultados

            cursor.close()
            conexion.close()

            return mascotas  # Devolver los datos de las mascotas
        except Exception as ex:
            raise Exception("Error al obtener datos de mascotas: {}".format(ex))


    @classmethod
    def eliminar_mascota(cls, db, id, id_usuario):
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM mascotas_info WHERE id_mascota=%s AND id_dueño=%s", (id, id_usuario))

            conexion.commit()
            cursor.close()
            conexion.close()

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizar_mascota(self, db, datos_actuales, nuevos_datos, id_mascota):
        try:
            conexion = db()
            cursor = conexion.cursor()

            columnas = ("nombre", "edad", "raza", "fecha_nacimiento", "peso", "vacunado")

            valores_actuales = dict(zip(columnas, datos_actuales))

            nuevos_valores = dict(zip(columnas, nuevos_datos))

            # Filtrar solo los campos que han cambiado
            campos_a_actualizar = {k: nuevos_valores[k] for k, v in valores_actuales.items() if nuevos_valores[k] != v}

            set_clause = ", ".join([f"{campo}=%s" for campo in campos_a_actualizar.keys()])
            query = f"UPDATE mascotas_info SET {set_clause} WHERE id_mascota=%s"
            valores = list(campos_a_actualizar.values()) + [id_mascota]

            if set_clause:
                cursor.execute(query, valores)
                conexion.commit()

            cursor.close()
            conexion.close()

        except Exception as ex:
            raise Exception(ex)


