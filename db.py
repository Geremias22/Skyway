import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Cargar .env
load_dotenv()

# Obtener URI de conexión
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise ValueError("MONGO_URI no está definido en el archivo .env")

# Crear el cliente y base de datos
client = MongoClient(mongo_uri)

# Aquí defines el nombre de tu base de datos (puede ser 'skyway' por ejemplo)
db = client.skyway
