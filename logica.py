from flask import Flask, render_template, request, redirect, flash, url_for, send_file
#from flask_babel import Domain
from config import Config
import qrcode
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from flask_security import Security
import email_token
from DB import conexion_1, conexion_2
import os
import controlador_db
from io import BytesIO

# Identidades
from src.modelos.entidades.usuario import User

# Modelos 
from src.modelos.modeloUsuario import ModeloUsuario

app = Flask(__name__)
csrf = CSRFProtect()
app.config.from_object(Config)
segurity = Security(app)
mail = Mail(app)

login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'

@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_usuario(conexion_1, id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/recuperar_contraseña',methods=['POST','GET'])
def recuperar_contraseña():
    return render_template('Recuperar_Contraseña.html')

@app.route('/confirmar/<token>/<usuario>/')
def confirmar_url(token, usuario):
    try:
        email = email_token.confirmar_token(token, key=Config.SECRET_KEY, key2=Config.SECURITY_PASSWORD_SALT)
        if email:
            ModeloUsuario.validar_registro(conexion_1, usuario)
        else:
            flash('El enlace de confirmación es inválido o ha expirado.', 'danger')
            return redirect(url_for('login'))
    except:
        return redirect(url_for('login'))

    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User(usuario=request.form['usuario'], contraseña_hash=request.form['contraseña'])
        usuario_logiado = ModeloUsuario.login(conexion_1, user)

        if usuario_logiado is not None:

            if usuario_logiado.contraseña_hash:

                if usuario_logiado.validado == 1: #true

                    if usuario_logiado.p_completado == 1: #true

                        login_user(usuario_logiado)
                        return redirect(url_for('main'))

                    else:
                        login_user(usuario_logiado)
                        correo = usuario_logiado.correo
                        return redirect(url_for('completar_registro', correo=correo))

                else:
                    flash("Debe verificar su cuenta. Para poder iniciar sesión")
                    return render_template('login.html')
                    

            elif usuario_logiado.contraseña_hash is not True:
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

        if usuario_registrado is not None:
            if usuario_registrado == 0:
                flash("El usuario ya se encuentra registrado.")
                return render_template('registrar.html')
            
            else:
                flash("El correo ya se encuentra asociado a una cuenta.")
                return render_template('registrar.html')

        elif request.form['password_registrar'] != request.form['confirmar_password']:
            flash("Las contraseñas no coinciden.")
            return render_template('registrar.html')
        
        else:
            usuario = request.form['usuario_registrar']
            correo = request.form['email']
            salt = User.salt()
            credenciales = User(usuario=usuario, correo=correo, contraseña_hash=User.incriptar(request.form['password_registrar'], salt), salt=salt)

            if email_token.enviar_correo_confirmacion(mail, Config.SECRET_KEY, Config.SECURITY_PASSWORD_SALT, usuario=usuario, correo=correo):
                flash('Usuario registrado exitosamente. Se envio un enlace de confirmación a su correo')
                ModeloUsuario.registrar_usuario(conexion_1, credenciales) 
                return redirect(url_for('login'))
            
            else:
                flash('Ocurrio un error inesperado. Intentelo de nuevo')
                return redirect(url_for('index'))

    #Si la petición es GET
    else:
        return render_template('registrar.html')

@app.route('/completar_registro/<correo>/', methods=['POST', 'GET'])
def completar_registro(correo):
    if request.method == 'POST':
        identificacion = request.form['identificacion']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        correo = request.form['correo']

        controlador_db.agregar_info_usuario(conexion_2, identificacion, correo, nombre, apellido, edad)
        ModeloUsuario.validar_p_completado(conexion_1, correo) #consulta para modificar la variable : p_completado.
        return redirect(url_for('main'))

    else:
        flash('Complete todos los campos para poder continuar', 'succes')
        return render_template('completar_registro.html', correo=correo)

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
    

@app.route('/cerrar_sesion')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/tu_familia', methods=['POST', 'GET'])
@login_required
def main():
    return render_template('main.html')

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True,host='0.0.0.0')
