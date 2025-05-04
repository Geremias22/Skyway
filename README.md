# Skyway
# ✈️ Skyway - Generador Inteligente de Planes de Viaje

- Skyway es un proyecto que utiliza inteligencia artificial (Gemini API), la API de Amadeus y una base de datos 
  MongoDB para generar itinerarios de viaje personalizados, incluyendo vuelos, hoteles, coches, actividades y más.

---

## 🗂️ Estructura del Proyecto

SKYWAY/
│
├── controllers/ # Controladores principales (búsqueda de vuelos, etc.)
│ └── generador_vuelos.py
│     (faltan hoteles y actividades xd)
├── services/ # Servicios auxiliares (auth, almacenamiento, API Gemini)
│ ├── auth.py
│ ├── generador.py
│ └── alamcenamiento.py
|
├── templates/ # Plantillas HTML para renderizado con Jinja2
│ └── resultados_vuelos.html
│
├── static/ # Recursos estáticos (CSS, imágenes)
│ ├── styles.css
│ └── img/
│ ├── LogoSkyway.png
│ └── Skyway.png
│
├── data/ # Datos de entrada o configuraciones temporales (de momento nada no se ni para que usarlo)
│
├── output/ # Resultados generados (JSON y HTML)
│ ├── resultados_vuelos.json
│ └── resultados_vuelos.html
│
├── .env # Variables de entorno (NO INCLUIDO en el repo)
├── app.py # Punto de entrada del proyecto
├── db.py # Conexión con MongoDB Atlas
├── README.md # Documentación del proyecto
└──requirements.txt # directo para descargar todo

yaml
Copiar
Editar

---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

#### bash
git clone https://github.com/tu-usuario/skyway.git
cd skyway

### 2. Crear y configurar el entorno virtual
 - Usar entorno Conda (Es como lo tengo yo boba)
    ### bash
    conda create -n skyway python=3.11
    conda activate skyway
    pip install -r requirements.txt

### 3. Crear el archivo .env
- Este archivo contiene tus credenciales de acceso:
Copiar y Editar en .env

AMADEUS_CLIENT_ID=tu_id
AMADEUS_CLIENT_SECRET=tu_secret
MONGODB_URI=tu_uri_mongodb
GEMINI_API_KEY=tu_clave_gemini

---

## 🧠 Flujo de funcionamiento

### El usuari decide si sabe a donde quiere ir
### El usuario ingresa destino, fechas, duración y cantidad de personas etc...
### Se llama a generador.py (servicio) que conecta con Gemini AI para generar un plan.
### Se conecta con la API de Amadeus para obtener vuelos.(mas adelantes hoteles y coche)
### Se guardan resultados en MongoDB.
### Se generan archivos:
### output/resultados_vuelos.json: datos estructurados.
### output/resultados_vuelos.html: vista renderizada con plantilla Jinja2.

## 📦 Generar resultados manualmente
- Desde app.py, puedes correr el generador con datos simulados o reales.

### bash
python app.py

# Elga pedazo de boba #

### ✅ Pendientes / Ideas futuras

- Añadir hoteles y actividades con API de Amadeus.
-  Interfaz web con Flask.
-  Selección de viajes favoritos.
-  Descarga de PDF del itinerario.
-  Autenticación de usuarios.
-  Busqueda de por imagen

### Recursos
- Amadeus for Developers
- Gemini API (Google AI)
- MongoDB Atlas
