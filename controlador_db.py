from DB import conexion_2

def agregar_info_usuario(db, identificacion, correo, nombre, apellido, edad):

    try:
        conexion = db()
        cursor = conexion.cursor()

        cursor.execute("INSERT INTO usuario_info(identificacion, correo, nombre, apellidos, edad) VALUES (%s, %s, %s, %s, %s)", (identificacion, correo, nombre, apellido, edad))

        conexion.commit()
        cursor.close()
        conexion.close()
        
    except Exception as ex:
        raise Exception(ex)

def recuperar_info_usuario():
    pass

def agregar_mascota(nombre, edad, raza, nacimiento, peso, vucunado):
    conexion_DB = conexion_2() #Establecer Instancia de la base de datos

    conexion_DB.cursor()

    conexion_DB.query("INSERT INTO mascotas_info() VALUES ")