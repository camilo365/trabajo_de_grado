from flask import render_template, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import  Message 
from config import Config

#Generar token de confirmación
def generar_token(email, key, key2):
    """Generar token"""
    serializer = URLSafeTimedSerializer(key)
    return serializer.dumps(email, salt=key2)

def confirmar_token(token, key, key2, expiration): #El correo expiración en 24 horas (86400 segundos)
    serializer = URLSafeTimedSerializer(key)
    try:
        email = serializer.loads(token, salt=key2, max_age=expiration) 
    except:
        return False
    return email

#Enviar correo para confirmar la cuenta
def enviar_correo_confirmacion(mail, key, key2, usuario=None, correo=None):
    token = generar_token(email=correo, key=key, key2=key2)
    confirmar_url = url_for('confirmar_url', token=token, usuario=usuario, _external=True)

    try:
        msg = Message(
            subject="Por favor confirme su correo",
            recipients=[correo],
            html=render_template('activate.html', confirmar_url=confirmar_url, usuario=usuario),
            sender=Config.MAIL_DEFAULT_SENDER
        )

        mail.send(msg)
        return True
    except:
        return False

#Enviar correo para recuperar contraseña
def enviar_correo_recuperacion(mail, key, key2, correo=None):
    token = generar_token(email=correo, key=key, key2=key2)
    restablecer_contraseña = url_for('restablecer_contraseña', token=token, correo=correo, _external=True)

    try:
        msg = Message(
            subject="Restablecer contraseña",
            recipients=[correo],
            html=render_template('restablecer.html', restablecer_contraseña=restablecer_contraseña, correo=correo),
            sender=Config.MAIL_DEFAULT_SENDER
        )

        mail.send(msg)
        return True
    except:
        return False