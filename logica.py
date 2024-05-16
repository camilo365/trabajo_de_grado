from flask import Flask, render_template, request, redirect, flash, url_for, send_file
import qrcode
from flask_login import LoginManager, login_user, logout_user, login_required
from io import BytesIO
from DB  import *

#Identidades
from src.modelos.entidades.usuario import User

#Modelos 
from src.modelos.modeloUsuario import ModeloUsuario

app = Flask(__name__)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_usuario(conexion_1, id)

@app.route('/')
def index():
    return render_template('index.html') #Renderiza la landing page

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        user = User(usuario=request.form['usuario'], contraseña_hash=request.form['contraseña'])
        usuario_logiado = ModeloUsuario.login(conexion_1, user)

        if usuario_logiado != None:
            if usuario_logiado.contraseña_hash:
                login_user(usuario_logiado)
                return render_template('main.html')
            else:
                flash("CONTRASEÑA INCORECTA...")
                return render_template('login.html')
        
        else:
            flash("USUARIO NO ENCONTRADO...")
            return render_template('login.html')
        
    else:
        return render_template('login.html')


"""Este se encarga de traer los valores de la plantilla agregar mascota y genera el codigo QR que al ser escaneado 
redirecciona a las personas a la plantilla mostrardatos que es donde van a estar los datos de forma organizada"""
@app.route('/qrcode', methods=['POST'])
def codigoqr():
    if request.method == 'POST':
        nombremascota = request.form['nombre_mascota']
        edad = request.form['edad']
        raza = request.form['raza']
        fecha_nacimiento = request.form['fecha_nacimiento']
        peso = request.form['peso']
        vacunado = request.form['vacunado']

        if nombremascota and edad and raza and fecha_nacimiento and peso and vacunado:
            """ generar la url con los datos dinamicamente """
            data_url = url_for('mostrar_datos', 
                               nombremascota=nombremascota,
                               edad=edad,
                               raza=raza,
                               fecha_nacimiento=fecha_nacimiento,
                               peso=peso,
                               vacunado=vacunado, 
                               _external=True)
            # Genera el código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            """ Guarda la imagen en un buffer de memoria"""
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            return send_file(img_io, mimetype='image/png')
            
        else:
            flash("Todos los campos son obligatorios")
            return render_template('agregarmascota.html')
@app.route('/registrar', methods=['POST', 'GET'])
def registrar():

    if request.method == 'POST':
        user = User(usuario=request.form['usuario_registrar'], correo=request.form['email'])
        usuario_registrado = ModeloUsuario.validar_datos(conexion_1, user)

        if usuario_registrado != None:
            #if usuario_registrado.usuario == request.form['usuario_registrar']:
            if usuario_registrado == 0:
                flash("EL USUARIO YA SE ENCUENTRA REGISTRADO...")
                return render_template('registrar.html')
            
            #elif usuario_registrado.usuario == request.form['email']:
            else:
                flash("EL CORREO YA SE ENCUENTRA ASOCIADO A UNA CUENTA...")
                return render_template('registrar.html')
            
        else:
            if request.form['password_registrar'] == request.form['confirmar_password']:
                
                usuario = request.form['usuario_registrar'] 
                correo = request.form['email']
                salt = User.salt()
                credenciales = User(usuario=usuario, correo=correo, contraseña_hash=User.incriptar(request.form['password_registrar'], salt), salt=salt)

                ModeloUsuario.registrar_usuario(conexion_1, credenciales)
                flash("¡USUARIO REGISTRADO CORRECTAMENTE!")
                return render_template('login.html')
            
            else:
                flash("LAS CONTRASEÑAS NO COINCIDEN")
                return render_template('registrar.html')
    else:
        return render_template('registrar.html')
    
"""este se utiliza para mostrar los datos en la plantilla mostrardatos y este es el que va a ver la
persona cuando escanee el codigo"""

@app.route('/mostrardatos',methods = ['POST','GET'])
def mostrar_datos():
    nombremascota = request.args.get('nombremascota')
    edad = request.args.get('edad')
    raza = request.args.get('raza')
    fecha_nacimiento = request.args.get('fecha_nacimiento')
    peso = request.args.get('peso')
    vacunado = request.args.get('vacunado')
    

    return render_template('mostrardatos.html', 
                           nombremascota=nombremascota, 
                           edad=edad, 
                           raza=raza, 
                           fecha_nacimiento=fecha_nacimiento, 
                           peso=peso, 
                           vacunado=vacunado
                           )
    
@app.route('/agregarmascota', methods=['POST', 'GET'])
def datosmascotas():
    return render_template('agregarmascota.html')

@app.route('/tu_familia', methods=['POST', 'GET'])
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.config['SECRET_KEY'] = '12345678'
    app.run(debug=True, host='0.0.0.0')