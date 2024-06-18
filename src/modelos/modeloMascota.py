from src.modelos.modeloUsuario import ModeloUsuario
from DB import conexion_1, conexion_2

import os

class ModeloMascota():

    @classmethod
    def cargar_datos_mascota(self, db, id_usuario, id_mascota):
        #id_usuario = ModeloUsuario.obtener_info_usuario(conexion_2, correo_usuario)

        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute("SELECT nombre, edad, raza, fecha_nacimiento, peso, vacunado, imagen FROM mascotas_info WHERE id_dueño=%s AND id_mascota=%s", (id_usuario, id_mascota))

            datos = cursor.fetchone()

            cursor.close()
            conexion.close()

            if datos is not None:
                mascota = list(datos)

                ruta = os.path.join('static', 'mascotas_img', f'{id_mascota}.jpg') 

                if not os.path.isfile(ruta):
                    mascota[6] = None
                else:
                    mascota[6] = f'mascotas_img/{id_mascota}.jpg'

                return mascota
            
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ingresar_mascota(self, db, id_usuario, nombremascota, edad, raza, fecha_nacimiento, peso, vacunado, imagen):
        
        try:
            conexion = db()

            cursor = conexion.cursor()

            cursor.execute("INSERT INTO mascotas_info(id_dueño, nombre, edad, raza, fecha_nacimiento, peso, vacunado, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id_usuario, nombremascota, edad, raza, fecha_nacimiento, peso, vacunado, imagen))

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

            #cursor.execute("SELECT * FROM mascotas_info m LEFT JOIN usuario_info u ON m.id_dueño = u.identificacion WHERE u.identificacion = %s", (id_usuario,))
            cursor.execute("SELECT * FROM mascotas_info WHERE id_dueño = %s", (id_usuario,))
            mascotas_info = cursor.fetchall()  # Obtener todas las filas de resultados

            cursor.close()
            conexion.close()

            mascotas = [list(tupla) for tupla in mascotas_info] #Convertir la tupla de tuplas en lista de listas

            for mascota in mascotas:

                ruta = os.path.join('static', 'mascotas_img', f'{mascota[0]}.jpg')

                if not os.path.isfile(ruta):
                    with open(ruta, 'wb') as archivo:
                        archivo.write(mascota[8])
                        mascota[8] = f'mascotas_img/{mascota[0]}.jpg'

                else:
                    mascota[8] = f'mascotas_img/{mascota[0]}.jpg'

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
        
    @classmethod
    def obtener_nombre_mascota(cls, db, id):
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute('SELECT nombre FROM mascotas_info WHERE id_mascota=%s', (id,))
            datos = cursor.fetchone()

            cursor.close()
            conexion.close()

            if datos:
                return datos[0]
            else:
                return None
            

        except Exception as ex:
                raise Exception(ex)

    @classmethod
    def guardar_nueva_imagen(self, db, imagen, id_mascota):

        print(imagen)
        print('Id mascota:', id_mascota)
        ruta_img = 'static\\mascotas_img' # Ruta de las carpetas donde se almacenan las imagenes de las mascotas

        for root, dirs, files in os.walk(ruta_img):
            for file in files:
                if file.startswith(f'{id_mascota}'):
                    file_path = os.path.join(root, file)
                    break 

        if os.path.exists(ruta_img):
            os.remove(file_path) #Eliminar imagen de la mascota
        
        try:
            conexion = db()
            cursor = conexion.cursor()

            cursor.execute('UPDATE mascotas_info SET imagen=%s WHERE id_mascota=%s', (imagen, id_mascota))

            conexion.commit()
            cursor.close()
            conexion.close()

        except Exception as ex:
                raise Exception(ex)
        