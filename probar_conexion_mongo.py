from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import ssl

# 🔁 Reemplaza con tu URI exacta desde MongoDB Atlas
uri = "mongodb://jheremyvalda:1234@cluster0.oultf7c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tls=true"
# MONGO_ mongodb+srv://jheremyvalda:1234@cluster0.oultf7c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tls=true

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    db = client["usuarios"]  # o cualquier otra base
    print("✅ Conexión exitosa. Servidor:", client.server_info()["version"])
except ServerSelectionTimeoutError as err:
    print("❌ Error de conexión:")
    print(err)
