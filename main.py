from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  

uri = os.getenv("MONGODB_URI")
cliente = MongoClient(uri)
db = cliente["adopcionesMascotas"]

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

print("datos cargados")