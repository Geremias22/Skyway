from db import db
from datetime import datetime

def guardar_guia(usuario, destino, contenido):
    guia = {
        "usuario": usuario,
        "destino": destino,
        "contenido": contenido,
        "fecha_creacion": datetime.utcnow()
    }
    db.guias.insert_one(guia)