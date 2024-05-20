from flask import Flask, render_template, request, redirect, flash, url_for, send_file
import qrcode
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from io import BytesIO
from DB  import *
import os
# Identidades
from src.modelos.entidades.usuario import User

# Modelos 
from src.modelos.modeloUsuario import ModeloUsuario

app = Flask(__name__)
csrf = CSRFProtect()
app.config['SECRET_KEY'] = 'bed026e0567e203d20527449faf89eb6f503e772dd319622559b31852a7b'

login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'

@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_usuario(conexion_1, id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User(usuario=request.form['usuario'], contraseña_hash=request.form['contraseña'])
        usuario_logiado = ModeloUsuario.login(conexion_1, user)

        if usuario_logiado is not None:
            if usuario_logiado.contraseña_hash:
                login_user(usuario_logiado)
                return redirect(url_for('main'))
            
            else:
                flash("Contraseña incorrecta.")
                return render_template('login.html')
        else:
            flash('El usuario no se encuentra registrado.')
            return render_template('login.html')
        
    #si la petición es GET
    else:
        return render_template('login.html')

"""Este se encarga de traer los valores de la plantilla agregar mascota y genera el codigo QR que al ser escaneado 
redirecciona a las personas a la plantilla mostrardatos que es donde van a estar los datos de forma organizada"""

@app.route('/agregar_familiar', methods=['POST', 'GET'])
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
            """ """ # Guarda la imagen en una carpeta estática
            img_path = os.path.join('static', 'qrcodes', f'{nombremascota}.png')
            img.save(img_path)

            # Generar la URL para la imagen
            img_url = url_for('static', filename=f'qrcodes/{nombremascota}.png')

            return render_template('main.html', 
                                   img_url=img_url, 
                                   nombremascota=nombremascota, 
                                   edad=edad, 
                                   raza=raza, 
                                   fecha_nacimiento=fecha_nacimiento, 
                                   peso=peso, 
                                   vacunado=vacunado)

            """ Guarda la imagen en un buffer de memoria""" 
            """ img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            return send_file(img_io, mimetype='image/png') """
            
        else:
            flash("Todos los campos son obligatorios")
            return render_template('agregarmascota.html')
         
        
    else:
        return render_template('agregarmascota.html')
        
@app.route('/registrar', methods=['POST', 'GET'])
def registrar():
    if request.method == 'POST':
        user = User(usuario=request.form['usuario_registrar'], correo=request.form['email'])
        usuario_registrado = ModeloUsuario.validar_datos(conexion_1, user)

        if usuario_registrado is not None and request.form['password_registrar'] == request.form['confirmar_password']:
            if usuario_registrado == 0:
                flash("El usuario ya se encuentra registrado.")
                return render_template('registrar.html')
            
            elif usuario_registrado == 1:
                flash("El correo ya se encuentra asociado a una cuenta.")
                return render_template('registrar.html')
            
            else:
                usuario = request.form['usuario_registrar']
                correo = request.form['email']
                salt = User.salt()
                credenciales = User(usuario=usuario, correo=correo, contraseña_hash=User.incriptar(request.form['password_registrar'], salt), salt=salt)
                ModeloUsuario.registrar_usuario(conexion_1, credenciales)
                flash("¡Usuario registrado correctamente!")
                return redirect(url_for('login'))
            
        else:
            flash("Las contraseñas no coinciden.")
    
            return render_template('registrar.html')
        
    #Si la petición es GET
    else:
        return render_template('registrar.html')
    
"""este se utiliza para mostrar los datos en la plantilla mostrardatos y este es el que va a ver la
persona cuando escanee el codigo"""

@app.route('/mostrardatos',methods = ['POST','GET'])
def mostrar_datos():
    datos = {
        'nombremascota' : request.args.get('nombremascota'),
        'edad' : request.args.get('edad'),
        'raza' : request.args.get('raza'),
        'fecha_nacimiento' : request.args.get('fecha_nacimiento'),
        'peso' : request.args.get('peso'),
        'vacunado' : request.args.get('vacunado'),
    }
    "flash datos obtenidos  correctamente"
    return render_template('mostrardatos.html', **datos)    

    """ se puede manejar de esta forma o de la otra de arriba como diccionario """
    
    """ nombremascota = request.args.get('nombremascota')
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
                            ) """

@app.route('/main', methods=['POST', 'GET'])
def main_redireccionar():
    return render_template('agregarmascota.html',)
    


@app.route('/tu_familia', methods=['POST', 'GET'])
@login_required
def main():
    return render_template('main.html')

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True,host='0.0.0.0')
