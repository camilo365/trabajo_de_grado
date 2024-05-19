import secrets

class Config:
    SECRET_KEY = secrets.token_hex(30)                           # Secret key
    SECURITY_PASSWORD_SALT = secrets.token_hex(15)               # Salt
    MAIL_SERVER = 'smtp.gmail.com'                               # Servidor SMTP
    MAIL_PORT = 587                                              # Puerto SMTP
    MAIL_USE_TLS = True                                          # Usar TLS (Transport Layer Security)
    MAIL_USE_SSL = False                                         # No usar SSL (Secure Sockets Layer)
    MAIL_USERNAME = 'williamandresariasherrera2@gmail.com'       # Correo electrónico
    MAIL_PASSWORD = 'lfch tsxs xblm nmmj'                        # Contraseña de correo electrónico
    MAIL_DEFAULT_SENDER = 'williamandresariasherrera2@gmail.com' # Remitente por defecto