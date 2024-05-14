import pymysql

def conexion_1():
    return(pymysql.connect(host='localhost',
                            user='root',
                            password='',
                            database='usuario_credenciales'))

def conexion_2():
    return(pymysql.connect(host='localhost',
                            user='root',
                            password='',
                            database='id_pets'))