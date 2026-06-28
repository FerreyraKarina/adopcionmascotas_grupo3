from pymongo import MongoClient

uri ="mongodb+srv://Grupo3:adopcionesMascotasg3@adpcionmascotas.kksh2gj.mongodb.net/?appName=adpcionMascotas"

cliente= MongoClient(uri)

db = cliente["adopcionesMascotas"]

usuarios = db["usuarios"]
mascotas = db["mascotas"]
adopciones = db["adopciones"]

usuarios.insert_many([
    {"nombre" : "Ana", "cuidad": "Avellaneda"},
    {"nombre": "Juan", "cuidad": "Lanus"}
])


mascotas.insert_many([
    {"nombre": "Luna", "tipo": "Perro", "edad": 2},
    {"nombre": "Michi", "tipo": "gato", "edad": 1}
])


print("datos cargados")