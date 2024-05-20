import secrets

class Config:
    SECRET_KEY = '9580bfa01a7b5cbcaf351e98cf24a425fc409e6d154394b18e19cdafc8a5' # Secret key                        
    #SECRET_KEY = secrets.token_hex(30)                                         # Secret key(aliatorio-No funciona como lo esperado)
    #SECURITY_PASSWORD_SALT = secrets.token_hex(15)                             # Salt (aliatorio-No funciona como lo esperado)
    SECURITY_PASSWORD_SALT = '05fd5d882a190af7c387c9fd8b769f'                   # Salt
    MAIL_SERVER = 'smtp.gmail.com'                                              # Servidor SMTP
    MAIL_PORT = 587                                                             # Puerto SMTP
    MAIL_USE_TLS = True                                                         # Usar TLS (Transport Layer Security)
    MAIL_USE_SSL = False                                                        # No usar SSL (Secure Sockets Layer)
    MAIL_USERNAME = 'williamandresariasherrera2@gmail.com'                      # Correo electrónico
    MAIL_PASSWORD = 'lfch tsxs xblm nmmj'                                       # Contraseña de correo electrónico
    MAIL_DEFAULT_SENDER = 'williamandresariasherrera2@gmail.com'                # Remitente por defecto