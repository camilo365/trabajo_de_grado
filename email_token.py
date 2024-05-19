from itsdangerous import URLSafeTimedSerializer

#Generar token de confirmación

def generar_token(email, key, key2):
    """Generar token"""
    serializer = URLSafeTimedSerializer(key)
    return serializer.dumps(email, salt=key2)

#Confirmar token

def confirmar_token(token, key, key2, expiration=86400): #El correo expiración en 24 horas (86400 segundos)
    serializer = URLSafeTimedSerializer(key)
    try:
        email = serializer.loads(token, salt=key2, max_age=expiration) 
    except:
        return False
    return email