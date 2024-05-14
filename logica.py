from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
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

@app.route('/tu_familia', methods=['POST', 'GET'])
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.config['SECRET_KEY'] = '12345678'
    app.run(debug=True)