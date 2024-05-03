from flask import Flask, render_template, request, redirect ,flash
import mysql.connector

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/logica', methods=['POST'])
def home():
    
    usuario = request.form['user']
    contrasena = request.form['password']
    
    if usuario ==  "1004995500" and contrasena == "1004995500":
        conexionbd(usuario,contrasena)       
        return render_template('prueba.html')
    else:
        return render_template('index.html')

print("credenciales incorrectas")

@app.route('/ventana_registrar', methods=['POST'])
def registrar():
    return render_template('registrar.html')


@app.route('/datos_registrados', methods=['POST'])
def datos_registrar():
    
    if 'registrar' in request.form:
        email = request.form['email']
        usuario = request.form['usuario_registrar']
        password = request.form['password_registrar']
        confirmacion_password = request.form['confirmar_password']
        if email == '' or usuario == '' or password == "" or confirmacion_password == "":
            flash('complete todos los campos')
            redirect('/')
        else:
            return email +' '+ usuario +' '+ password +' '+ confirmacion_password
    else: 
        return redirect('/')
        


def conexionbd(usuario,contraseña):
    
    try:
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "proyecto"
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            insercion = "INSERT INTO credenciales(user,password) VALUES(%s,%s)"
            datos = (usuario,contraseña)
            cursor.execute(insercion,datos)
            conexion.commit()
            print("credenciales ingresadas correctamente")
            cursor.close()
    
    except mysql.connector.Error as error:
        print("Error al conectarse a la base de datos:" , error)
        
if __name__ == '__main__':
    app.run(debug=True)
    
    
    