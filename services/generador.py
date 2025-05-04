import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar API Key\load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key no encontrada en .env")

genai.configure(api_key=api_key)

# Modelo para respuestas creativas
modelo_pro = genai.GenerativeModel("gemini-1.5-pro-latest")
# Modelo para respuestas rápidas
modelo_flash = genai.GenerativeModel("gemini-1.5-flash-latest")

# def generar_destinos_sin_direccion(epoca, desde, duracion, personas):
#     prompt = f"""
#     Sugiere 10 posibles destinos de viaje para {personas} personas, saliendo desde {desde},
#     con una duración aproximada de {duracion} días, en la época de {epoca}.
#     Clasifica los destinos en categorías como naturaleza, cultura, relax, ciudad, etc.
#     Para cada destino, incluye una descripción breve, el país y continente donde está ubicado,
#     y un tipo de experiencia predominante.
#     Presenta el resultado de forma estructurada, clara y sin texto adicional innecesario.
#     """
#     respuesta = modelo_flash.generate_content(prompt)
#     return respuesta.text

def generar_itinerario_con_direccion(destino, dias, fecha, personas):
    prompt = f"""
    Planifica un viaje a {destino} para {personas} personas, durante {dias} días.
    La fecha estimada del viaje es {fecha}.

    Estructura la respuesta de la siguiente forma:

    1. ✨ Resumen general del viaje:
       Describe brevemente el tipo de experiencia que vivirán las personas que viajan (clima, actividades generales, ambiente).

    2. ✈️ Opciones de viaje:
       - Más económica
       - Con menos escalas
       - Intermedia

    3. 📅 Itinerario detallado por día:
       Actividades programadas, horarios sugeridos, tiempo libre y consejos.

    4. 🏨 Hotel sugerido:
       Nombre, ubicación y por qué es recomendable.

    5. ✈️ Vuelos recomendados:
       Rutas aproximadas, duración, escalas.

    6. 🚌 Transporte local:
       Opciones dentro del destino (bus, metro, taxis, alquiler).

    7. 🎭 Actividades destacadas:
       Visitas, excursiones, museos, experiencias.

    8. 🍽️ Restaurantes recomendados:
       Variedad de opciones locales, precios estimados.

    9. 🛅 Lista de cosas para llevar:
       Según el clima, cultura y tipo de actividades.

    10. 🚗 Alquiler de coche:
        Si aplica, indica compañías sugeridas y coste estimado.

    Redáctalo todo de forma clara, estructurada y profesional.
    """
    respuesta = modelo_pro.generate_content(prompt)
    return respuesta.text

def generar_guia_sin_direccion(epoca, lugar, desde, fecha, personas, continente, pais):
    """
    Genera tres guías completas sin destino fijo, usando todos los parámetros disponibles.
    """
    prompt = f"""
    Planifica 3 viajes completos y variados sin destino fijo para {personas} personas.
    Parámetros conocidos:
    - Época: {epoca}
    - Tipo de lugar: {lugar}
    - Punto de salida: {desde}
    - Fecha aproximada: {fecha} 
      (tener en cuenta si no es una fecha exacta o dias especificados se pondra un intenerario de 5 dias dentro de la epoca especificada ({epoca}) )
    - Filtro por continente: {continente or 'sin filtro'}
    - Filtro por país: {pais or 'sin filtro'}

    Estructura la respuesta en tres secciones claramente delimitadas añadiendo variedad entre ellas:
    ---
    ## Guía 1
    (Contenido completo de la primera guía siguiendo la misma estructura de itinerario detallado)
    ---
    ## Guía 2
    (Contenido completo de la segunda guía siguiendo la misma estructura de itinerario detallado)
    ---
    ## Guía 3
    (Contenido completo de la tercera guía siguiendo la misma estructura de itinerario detallado)

    Cada guía debe incluir:
    1. ✨ Resumen general
    2. 📍 Destino sugerido y por qué
    3. 🗓️ Itinerario diario
    4. 🏨 Hotel
    5. ✈️ Vuelos
    6. 🚍 Transporte local
    7. 🎭 Actividades
    8. 🍽️ Restaurantes
    9. 🎒 Lista de cosas para llevar
    10. 🚗 Alquiler de coche

    Redáctalo de forma clara y profesional.
    """
    respuesta = modelo_pro.generate_content(prompt)
    return respuesta.text

