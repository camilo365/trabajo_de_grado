

class ModeloMascota():
    
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

