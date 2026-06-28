from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

cliente = MongoClient(os.getenv("MONGODB_URI"))
db = cliente["adopcionesMascotas"]

# Limpia las colecciones
db.refugios.drop()
db.mascotas.drop()
db.solicitudes.drop()

refugios    = db["refugios"]
mascotas    = db["mascotas"]
solicitudes = db["solicitudes"]

# ── REFUGIOS ──────────────────────────────────────
result_refugios = refugios.insert_many([
    {"nombre": "Refugio Huellitas", "provincia": "Buenos Aires", "telefono": "011-9876-5432"},
    {"nombre": "Casa Peluda",       "provincia": "Mendoza",       "telefono": "0261-876-5432"},
    {"nombre": "Refugio Colitas",   "provincia": "Santa Fe",      "telefono": "0342-765-4321"},
])
ids = result_refugios.inserted_ids

# ── MASCOTAS ──────────────────────────────────────
hoy = datetime.now()

mascotas.insert_many([
    {
        "nombre": "Manchas", "especie": "perro", "raza": "dálmata",
        "edad_meses": 24, "estado": "disponible",
        "refugio_id": ids[0],
        "vacunas": [
            {"nombre": "Antirrábica", "fecha": hoy - timedelta(days=180)},
            {"nombre": "Séxtuple",    "fecha": hoy - timedelta(days=180)},
        ]
    },
    {
        "nombre": "Bigotes", "especie": "gato", "raza": "angora",
        "edad_meses": 48, "estado": "disponible",
        "refugio_id": ids[0],
        "vacunas": [
            {"nombre": "Triple felina", "fecha": hoy - timedelta(days=410)},
        ]
    },
    {
        "nombre": "Toby", "especie": "perro", "raza": "beagle",
        "edad_meses": 12, "estado": "disponible",
        "refugio_id": ids[1],
        "vacunas": [
            {"nombre": "Antirrábica", "fecha": hoy - timedelta(days=20)},
            {"nombre": "Séxtuple",    "fecha": hoy - timedelta(days=20)},
        ]
    },
    {
        "nombre": "Perla", "especie": "gato", "raza": "común",
        "edad_meses": 72, "estado": "disponible",
        "refugio_id": ids[2],
        "vacunas": [
            {"nombre": "Triple felina", "fecha": hoy - timedelta(days=520)},
        ]
    },
    {
        "nombre": "Trueno", "especie": "perro", "raza": "golden retriever",
        "edad_meses": 36, "estado": "disponible",
        "refugio_id": ids[2],
        "vacunas": []
    },
])

# ── SOLICITUDES ───────────────────────────────────
ids_mascotas = [m["_id"] for m in mascotas.find()]

solicitudes.insert_many([
    {
        "mascota_id": ids_mascotas[0],
        "adoptante": {"nombre": "Sofía Romero", "email": "sofi@gmail.com", "provincia": "Buenos Aires"},
        "estado": "aprobada",
        "fecha_solicitud": hoy - timedelta(days=10)
    },
    {
        "mascota_id": ids_mascotas[1],
        "adoptante": {"nombre": "Diego Herrera", "email": "diego@gmail.com", "provincia": "Mendoza"},
        "estado": "pendiente",
        "fecha_solicitud": hoy - timedelta(days=5)
    },
    {
        "mascota_id": ids_mascotas[2],
        "adoptante": {"nombre": "Camila Vega", "email": "cami@gmail.com", "provincia": "Buenos Aires"},
        "estado": "aprobada",
        "fecha_solicitud": hoy - timedelta(days=3)
    },
    {
        "mascota_id": ids_mascotas[3],
        "adoptante": {"nombre": "Nicolás Soto", "email": "nico@gmail.com", "provincia": "Santa Fe"},
        "estado": "aprobada",
        "fecha_solicitud": hoy - timedelta(days=8)
    },
])

print("✓ Datos cargados")
print(f"  Refugios:    {refugios.count_documents({})}")
print(f"  Mascotas:    {mascotas.count_documents({})}")
print(f"  Solicitudes: {solicitudes.count_documents({})}")


# ── PIPELINE 1: mascotas disponibles por refugio ──
print("\n=== PIPELINE 1: Mascotas disponibles por refugio ===")

pipeline1 = [
    { "$match": { "estado": "disponible" } },
    { "$group": {
        "_id": "$refugio_id",
        "total": { "$sum": 1 },
        "especies": { "$addToSet": "$especie" },
        "nombres": { "$push": "$nombre" }
    }},
    { "$lookup": {
        "from": "refugios",
        "localField": "_id",
        "foreignField": "_id",
        "as": "info_refugio"
    }},
    { "$unwind": "$info_refugio" },
    { "$project": {
        "_id": 0,
        "refugio": "$info_refugio.nombre",
        "provincia": "$info_refugio.provincia",
        "total": 1,
        "especies": 1,
        "nombres": 1
    }},
    { "$sort": { "total": -1 } }
]

for r in mascotas.aggregate(pipeline1):
    print(f" {r['refugio']} ({r['provincia']})-> {r['total']} mascotas:{', '.join(r['nombres'])}")
    
    
# ── PIPELINE 2: top provincias con más adopciones ──
print("\n=== PIPELINE 2: Top provincias con más adopciones ===")

pipeline2 = [
    { "$match": { "estado": "aprobada" } },
    { "$group": {
        "_id": "$adoptante.provincia",
        "total": { "$sum": 1 },
        "adoptantes": { "$push": "$adoptante.nombre" }
    }},
    { "$sort": { "total": -1 } },
    { "$limit": 5 },
    { "$project": {
        "_id": 0,
        "provincia": "$_id",
        "total": 1,
        "adoptantes": 1
    }}
]
for r in solicitudes.aggregate(pipeline2):
    print(f"  {r['provincia']}: {r['total']} adopciones — {', '.join(r['adoptantes'])}")
    
    
    
    # ── PIPELINE 3: mascotas con vacunas vencidas o sin vacunas ──
print("\n=== PIPELINE 3: Mascotas con vacunas vencidas o sin vacunas ===")

pipeline3 = [
    { "$facet": {
        "con_vacunas_vencidas": [
            { "$unwind": "$vacunas" },
            { "$match": { "vacunas.fecha": { "$lt": hoy } } },
            { "$group": {
                "_id": "$_id",
                "nombre": { "$first": "$nombre" },
                "refugio_id": { "$first": "$refugio_id" },
                "vacunas_vencidas": { "$push": "$vacunas.nombre" }
            }},
            { "$lookup": {
                "from": "refugios",
                "localField": "refugio_id",
                "foreignField": "_id",
                "as": "refugio"
            }},
            { "$unwind": "$refugio" },
            { "$project": {
                "_id": 0,
                "nombre": 1,
                "refugio": "$refugio.nombre",
                "motivo": "vacunas vencidas",
                "detalle": "$vacunas_vencidas"
            }}
        ],
        "sin_vacunas": [
            { "$match": { "vacunas": { "$size": 0 } } },
            { "$lookup": {
                "from": "refugios",
                "localField": "refugio_id",
                "foreignField": "_id",
                "as": "refugio"
            }},
            { "$unwind": "$refugio" },
            { "$project": {
                "_id": 0,
                "nombre": 1,
                "refugio": "$refugio.nombre",
                "motivo": "sin vacunas registradas",
                "detalle": []
            }}
        ]
    }}
]

resultado = list(mascotas.aggregate(pipeline3))[0]
todas = resultado["con_vacunas_vencidas"] + resultado["sin_vacunas"]

for r in todas:
    detalle = ', '.join(r['detalle']) if r['detalle'] else "ninguna"
    print(f"  {r['nombre']} ({r['refugio']}) → {r['motivo']}: {detalle}")