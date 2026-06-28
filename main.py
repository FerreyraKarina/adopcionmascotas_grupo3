from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

cliente = MongoClient(os.getenv("MONGODB_URI"))
db = cliente["adopcionesMascotas"]

# Limpia las colecciones antes de insertar
db.usuarios.drop()
db.mascotas.drop()
db.adopciones.drop()

usuarios  = db["usuarios"]
mascotas  = db["mascotas"]
adopciones = db["adopciones"]

usuarios.insert_many([
    {"nombre": "Ana",  "ciudad": "Avellaneda"},
    {"nombre": "Juan", "ciudad": "Lanús"}
])

mascotas.insert_many([
    {"nombre": "Luna",  "tipo": "perro", "edad": 2},
    {"nombre": "Michi", "tipo": "gato",  "edad": 1}
])

print("=== USUARIOS ===")
for u in usuarios.find():
    print(u)

print("=== MASCOTAS ===")
for m in mascotas.find():
    print(m)