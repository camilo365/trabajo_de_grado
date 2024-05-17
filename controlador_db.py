from DB import conexion_2

def agregar_info_usuario():
    pass

def recuperar_info_usuario():
    pass

def agregar_mascota(nombre, edad, raza, nacimiento, peso, vucunado):
    conexion_DB = conexion_2() #Establecer Instancia de la base de datos

    conexion_DB.cursor()

    conexion_DB.query("INSERT INTO mascotas_info() VALUES ")