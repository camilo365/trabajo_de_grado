from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from DB  import *

# Identidades
from src.modelos.entidades.usuario import User

# Modelos 
from src.modelos.modeloUsuario import ModeloUsuario

app = Flask(__name__)
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

@app.route('/cerrar_sesion')
def cerrar_sesion():
    logout_user()
    return redirect(url_for('login'))

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

@app.route('/tu_familia', methods=['POST', 'GET'])
@login_required
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)