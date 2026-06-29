# Adopción de Mascotas 

Proyecto Parcial 2 — Bases de Datos 2 | UTN FRA | División 133 | Grupo 3

---

## ¿Qué hace el programa?

Sistema de gestión de adopción de mascotas conectado a MongoDB Atlas.
Ejecuta tres consultas avanzadas mediante el Aggregation Pipeline:

1. **¿Qué mascotas disponibles tiene cada refugio?**
2. **¿De qué provincias provienen más adoptantes aprobados?**
3. **¿Qué mascotas tienen vacunas vencidas o no tienen vacunas?**

---

## Cómo ejecutarlo

### Requisitos
- Python 3.8 o superior
- Cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (gratuita)

### Instalación

```bash
git clone https://github.com/FerreyraKarina/adopcionmascotas_grupo3.git
cd adopcionmascotas_grupo3
pip install pymongo python-dotenv
cp .env.example .env
# Editar .env y pegar la URI de MongoDB Atlas
```

### Ejecutar

```bash
python main.py
```

---

## Estructura del proyecto

adopcionmascotas_grupo3/

├── main.py          # carga datos y ejecuta los 3 pipelines

├── .env             # URI de Atlas (NO se sube al repo)

├── .env.example     # ejemplo de configuración

├── .gitignore       # excluye el .env

└── README.md        


---

## Colecciones

- `refugios` — organizaciones que alojan mascotas
- `mascotas` — con vacunas embebidas y referencia al refugio
- `solicitudes` — con datos del adoptante embebidos como snapshot



---

## Integrantes del Grupo 3

- Karina Ferreyra
- Erika Tamara Paredes
- Jose Enriquez Bishop
- Agustin Rodriguez

---

UTN FRA · Bases de Datos 2 · División 133 · 2026