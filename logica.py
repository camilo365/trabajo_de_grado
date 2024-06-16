from flask import Flask, render_template, request, redirect, flash, url_for
from config import Config
import qrcode
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_security import Security

import email_token
from DB import conexion_1, conexion_2
import os
from datetime import datetime

# Identidades
from src.modelos.entidades.usuario import User

# Modelos 
from src.modelos.modeloUsuario import ModeloUsuario
from src.modelos.modeloMascota import ModeloMascota

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

@app.route('/recuperar_contraseña', methods=['POST','GET'])
def recuperar_contraseña():
    if request.method == 'POST':

        correo = request.form['correo']

        if ModeloUsuario.obtener_correo_usuario(conexion_1, correo) == 1:
            email_token.enviar_correo_recuperacion(mail, Config.SECRET_KEY, Config.SECURITY_PASSWORD_SALT, correo)

            flash('Se envio un enlace de recuperación al correo')
            return redirect(url_for('login'))

        else:
            flash('El correo no se encuentra registrado')
            return render_template('Recuperar_Contraseña.html')

    else:
        return render_template('Recuperar_Contraseña.html')

@app.route('/confirmar/<token>/<usuario>/')
def confirmar_url(token, usuario):
    try:
        email = email_token.confirmar_token(token, key=Config.SECRET_KEY, key2=Config.SECURITY_PASSWORD_SALT, expiration=86400)
        if email:
            ModeloUsuario.validar_registro(conexion_1, usuario)
        else:
            flash('El enlace de confirmación es inválido o ha expirado', 'danger')
            return redirect(url_for('login'))
    except:
        flash('Lo sentimos, ha ocurrido un error inesperado. Por favor, inténtelo de nuevo')
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

                    login_user(usuario_logiado)
                    return redirect(url_for('main'))
                
                else:
                    flash("Debe verificar su cuenta. Para poder iniciar sesión")
                    return render_template('login.html')

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
@login_required
def codigoqr():
    if request.method == 'POST':
        nombremascota = request.form['nombremascota']
        imagen = request.files['image'] #Obtener la imagen
        edad = request.form['edad']
        raza = request.form['raza']
        fecha_nacimiento = request.form['fecha_nacimiento']
        peso = request.form['peso']
        vacunado = 1 if request.form.get('vacunado') == 'Si' else '0'

        if nombremascota and edad and raza and fecha_nacimiento and peso and vacunado:

            #Convertir la imagen en binario para poder guardarla en la base de datos
            imagen_binaria = imagen.read()

            ModeloMascota.ingresar_mascota(conexion_2, current_user.identificacion, nombremascota, edad, raza, fecha_nacimiento, peso, int(vacunado), imagen_binaria) 

            #generar la url con los datos dinamicamente 
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
            mascotas = ModeloMascota.mascotas_datos(conexion_2, current_user.identificacion)
            return render_template('main.html', 
                                    img_url=img_url, 
                                    nombremascota=nombremascota, 
                                    edad=edad, 
                                    raza=raza, 
                                    fecha_nacimiento=fecha_nacimiento, 
                                    peso=peso, 
                                    vacunado=vacunado,
                                    mascotas=mascotas
                                    )

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
            identificacion = request.form['identificacion']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            edad = request.form['edad']
            celular = request.form['celular']
            usuario = request.form['usuario_registrar']
            correo = request.form['email']
            salt = User.salt()

            credenciales = User(identificacion=identificacion, nombre=nombre, apellido=apellido, edad=edad, celular=celular, usuario=usuario, correo=correo, contraseña_hash=User.incriptar(request.form['password_registrar'], salt), salt=salt)

            #Para actuvar la funcion de confirmar registro : #Descomentar la lineas 201 y 202. Las lineas 203 y 204 deben de estar dentro del if.

            #if email_token.enviar_correo_confirmacion(mail, Config.SECRET_KEY, Config.SECURITY_PASSWORD_SALT, usuario=usuario, correo=correo):
                #flash('Usuario registrado exitosamente. Se envio un enlace de confirmación a su correo')
            ModeloUsuario.registrar_usuario(conexion_1, credenciales) 
            return redirect(url_for('login'))
            
        """  else:
                flash('Ocurrio un error inesperado. Intentelo de nuevo')
                return redirect(url_for('index')) """

    #Si la petición es GET
    else:
        return render_template('registrar.html')

@app.route('/restablecer/<token>/<correo>/', methods=['POST', 'GET'])
def restablecer_contraseña(token, correo):
    try:
        email = email_token.confirmar_token(token, key=Config.SECRET_KEY, key2=Config.SECURITY_PASSWORD_SALT, expiration=300)
        if email: #La confirmación del token fue correcta
            return render_template('cambiar_contraseña.html', correo=correo)
        else:
            flash('El enlace de confirmación es inválido o ha expirado.', 'danger')
            return redirect(url_for('login'))
    except:
        flash('Ocurrio un error inesperado. Intentelo de nuevo', 'danger')
        return redirect(url_for('login'))

@app.route('/cambiar', methods=['POST'])
def cambiar_contraseña():
    try:
        contraseña = request.form['contraseña']
        correo = request.form['correo']

        ModeloUsuario.cambiar_contraseña(conexion_1, contraseña, correo)
        flash('Contraseña cambiada satisfactoriamente', 'succes')
        return redirect(url_for('login'))

    except:
        flash('Lo sentimos, ha ocurrido un error inesperado. Por favor, inténtelo de nuevo')
        return redirect(url_for('login'))

"""este se utiliza para mostrar los datos en la plantilla mostrardatos y este es el que va a ver la
persona cuando escanee el codigo"""

@app.route('/mostrardatos', methods=['GET','POST'])
@login_required
def mostrar_datos():
    """ se puede manejar de esta forma o de la otra de arriba como diccionario """

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

@app.route('/tu_familia', methods=['GET'])
@login_required
def main():
    try:
        # Obtener el ID del usuario actual
        id_usuario = current_user.identificacion
        

        # Obtener todas las mascotas asociadas al usuario actual
        mascotas = ModeloMascota.mascotas_datos(conexion_2, id_usuario)

        # Pasar los datos de las mascotas a la plantilla
        return render_template('main.html', mascotas=mascotas)
    
    except Exception as e:
        flash(str(e))
        return render_template('main.html', mascotas=[])

@app.route('/cerrar_sesion')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/eliminar', methods=['POST'])
@login_required
def eliminar():
    try:
        if 'id' in request.form:
            id = int(request.form['id'])
            id_usuario = current_user.identificacion

            nombre_mascota = ModeloMascota.obtener_nombre_mascota(conexion_2, id)
            ModeloMascota.eliminar_mascota(conexion_2, id, id_usuario)
        
            #ruta_img = os.path.join('static', 'mascotas_img', f'{id}.jpg')
            ruta_qr = os.path.join('static', 'qrcodes', f'{nombre_mascota}.png')

            ruta_img = 'static\\mascotas_img' # Ruta de las carpetas donde se almacenan las imagenes de las mascotas

            # Recorrer todos los archivos del directorio
            for root, dirs, files in os.walk(ruta_img):
                for file in files:
                    if file.startswith(f'{id}'):
                        file_path = os.path.join(root, file)
                        break  

            if os.path.exists(ruta_qr) and os.path.exists(ruta_img):
                os.remove(file_path) #Eliminar QR de la mascota
                os.remove(ruta_qr) #Eliminar Imagen de la mascota

                return redirect(url_for('main'))

            else:
                raise     
    except:
        flash('Error al intentar eliminar mascota. Intentelo de nuevo')
        return redirect(url_for('main')) # Otra acción a realizar después de eliminar la mascota

@app.route('/editar_familiar', methods=['POST'])
@login_required
def editar():
    id_mascota = int(request.form['id'])
    mascota = ModeloMascota.cargar_datos_mascota(conexion_2, current_user.identificacion, id_mascota)

    return render_template('editar_familiar.html', mascota=mascota, id_mascota=id_mascota)

@app.route('/confirmar_editar_mascota', methods=['POST'])
@login_required
def confirmar_editar_mascota():
    #Agregar la clausura, try-except

        id_mascota = int(request.form['id'])

        if 'image' not in request.files:
            imagen = None
        else:
            imagen = request.files['image'].read() #Convertir la imagen en binario
    
        nombre_mascota = request.form['nombremascota']
        edad = int(request.form['edad'])
        raza = request.form['raza']
        fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], "%Y-%m-%d").date()
        #datetime.strptime(request.form['fecha_nacimiento'], "%Y-%m-%d").date() Nesecario para Convertir la fecha a un objeto datetime.date
        peso = int(request.form['peso'])
        vacunado = 1 if request.form.get('vacunado') == 'Si' else 0

        nuevos_datos = (nombre_mascota, edad, raza, fecha_nacimiento, peso, vacunado, imagen)

        #Cargar los datos de la mascota(en base al id) desde la base de datos
        datos_almacenados = ModeloMascota.cargar_datos_mascota(conexion_2, current_user.identificacion, id_mascota)

        #Actualizar los datos de la mascota en la base de datos
        ModeloMascota.actualizar_mascota(conexion_2, datos_almacenados, nuevos_datos, id_mascota)

        return redirect(url_for('main'))


if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True,host='0.0.0.0')