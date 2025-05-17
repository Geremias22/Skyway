import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from amadeus import Client, ResponseError
from jinja2 import Environment, FileSystemLoader


# Cargar el archivo .env para acceder a las claves
load_dotenv() 

CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")

# Obtener el token
# Inicializar cliente Amadeus (automáticamente gestiona el token)
amadeus = Client(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Tabla de códigos de avión traducidos
AIRCRAFTS = {
    "788": "Boeing 787-8",
    "32N": "Airbus A320neo",
    "321": "Airbus A321",
    "320": "Airbus A320",
    # Agrega más si quieres
}

# Enlaces de check-in por aerolínea (código IATA → URL)
CHECKIN_LINKS = {
    "UX": "https://www.aireuropa.com/checkin",
    "IB": "https://www.iberia.com/es/gestion-de-reservas/",
    "VY": "https://www.vueling.com/es/vuelos/gestion-de-reserva",
    "FR": "https://www.ryanair.com/es/es/check-in",
    # Añade más según necesites
}



def guardar_resultados(flights):
    # Preparar datos para la plantilla
    vuelos_procesados = procesar_vuelos(flights)

    # Guardar JSON
    with open("output/resultados_vuelos.json", "w", encoding="utf-8") as f_json:
        json.dump(flights, f_json, indent=2, ensure_ascii=False)

    # Renderizar con Jinja2
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('resultados_vuelos.html')
    contenido_html = template.render(
        vuelos=vuelos_procesados,
        origen=vuelos_procesados[0]['salida'],
        destino=vuelos_procesados[0]['llegada']
    )

    # Guardar HTML
    with open("output/resultados_vuelos.html", "w", encoding="utf-8") as f_html:
        f_html.write(contenido_html)



def formatear_tarifa_clase(cabin, brandedFare, class_code):
    # Traducción de la cabina
    cabinas = {
        "ECONOMY": "Clase turista",
        "PREMIUM_ECONOMY": "Turista premium",
        "BUSINESS": "Clase ejecutiva",
        "FIRST": "Primera clase"
    }

    nombre_cabina = cabinas.get(cabin, cabin.capitalize())

    # Mensaje final
    return f"{nombre_cabina} · Tarifa: {brandedFare} (Clase {class_code})"

def formatear_duracion(iso_duration):
    horas = minutos = 0
    if 'T' in iso_duration:
        tiempo = iso_duration.split('T')[1]
        if 'H' in tiempo:
            horas = int(tiempo.split('H')[0])
            tiempo = tiempo.split('H')[1]
        if 'M' in tiempo:
            minutos = int(tiempo.split('M')[0])
    return f"{horas}h {minutos}m"

# def buscar_vuelos():
#     try:
#         respuesta = amadeus.shopping.flight_offers_search.get(
#             originLocationCode="MAD",
#             destinationLocationCode="BCN",
#             departureDate="2025-05-10",
#             adults=3
#         )
#         vuelos = respuesta.data[:10]  # Limita a 10 resultados
#         print(f"✈️ Se encontraron {len(vuelos)} vuelos.")
#         guardar_resultados(vuelos)
#     except ResponseError as error:
#         print("❌ Error al buscar vuelos:", error)

# if __name__ == "__main__":
#     buscar_vuelos()


def buscar_vuelos(origen: str, destino: str, fecha: str, adultos: int = 1, guardar: bool = False):
    try:
        respuesta = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origen,
            destinationLocationCode=destino,
            departureDate=fecha,
            adults=adultos
        )
        vuelos = respuesta.data[:10]
        print(f"✈️ Se encontraron {len(vuelos)} vuelos.")
        
        if guardar:
            guardar_resultados(vuelos)
        
        return procesar_vuelos(vuelos)
    
    except ResponseError as error:
        print("❌ Error al buscar vuelos:", error)
        return []
    

def procesar_vuelos(flights):
    vuelos_procesados = []
    for vuelo in flights:
        segmentos_raw = vuelo['itineraries'][0]['segments']
        segmentos = []
        for seg in segmentos_raw:
            segmento = {
                "salida": seg['departure']['iataCode'],
                "llegada": seg['arrival']['iataCode'],
                "hora_salida": seg['departure']['at'][11:16],
                "hora_llegada": seg['arrival']['at'][11:16],
                "fecha_salida": seg['departure']['at'][:10],
                "fecha_llegada": seg['arrival']['at'][:10],
                "aerolinea": seg['carrierCode'],
                "numero_vuelo": f"{seg['carrierCode']}{seg['number']}",
                "avion": AIRCRAFTS.get(seg['aircraft']['code'], seg['aircraft']['code'])
            }
            segmentos.append(segmento)

        traveler = vuelo['travelerPricings'][0]
        clase = traveler['fareDetailsBySegment'][0]['class']
        tarifa = traveler['fareDetailsBySegment'][0].get('brandedFareLabel', 'N/A')
        detalle_tarifa = formatear_tarifa_clase(
            traveler['fareDetailsBySegment'][0]['cabin'],
            tarifa,
            clase
        )
        equip_mano = traveler['fareDetailsBySegment'][0]['includedCabinBags'].get('quantity', 0)
        equip_fact = traveler['fareDetailsBySegment'][0]['includedCheckedBags'].get('quantity', 0)
        amenities = traveler['fareDetailsBySegment'][0].get('amenities', [])
        lista_amenities = ', '.join(a['description'] for a in amenities if not a['isChargeable']) or 'Ninguna incluida'

        checkin_url = CHECKIN_LINKS.get(segmentos[0]["aerolinea"], "#")

        vuelos_procesados.append({
            "salida": segmentos[0]['salida'],
            "llegada": segmentos[-1]['llegada'],
            "fecha_salida": segmentos[0]['fecha_salida'],
            "fecha_llegada": segmentos[-1]['fecha_llegada'],
            "hora_salida": segmentos[0]['hora_salida'],
            "hora_llegada": segmentos[-1]['hora_llegada'],
            "duracion": formatear_duracion(vuelo['itineraries'][0]['duration']),
            "precio": vuelo['price']['total'],
            "detalle_tarifa": detalle_tarifa,
            "equip_mano": equip_mano,
            "equip_fact": equip_fact,
            "lista_amenities": lista_amenities,
            "checkin_url": checkin_url,
            "segmentos": segmentos
        })

    return vuelos_procesados





## Buscar vuelos y que sean directos:
# def procesar_vuelos(flights):
#     vuelos_procesados = []
#     for vuelo in flights:
#         segmentos = vuelo['itineraries'][0]['segments']
#         segment_inicio = segmentos[0]
#         segment_fin = segmentos[-1]

#         # ❗ Solo procesar si el destino final es VLC
#         if segment_fin['arrival']['iataCode'] != "VLC":
#             continue

#         salida = segment_inicio['departure']['iataCode']
#         llegada = segment_fin['arrival']['iataCode']
#         hora_salida = segment_inicio['departure']['at'][11:16]
#         hora_llegada = segment_fin['arrival']['at'][11:16]
#         fecha_salida = segment_inicio['departure']['at'][:10]
#         fecha_llegada = segment_fin['arrival']['at'][:10]
#         precio = vuelo['price']['total']
#         duracion = formatear_duracion(vuelo['itineraries'][0]['duration'])
#         aerolinea = segment_inicio['carrierCode']
#         avion_codigo = segment_inicio['aircraft']['code']
#         avion = AIRCRAFTS.get(avion_codigo, avion_codigo)
#         numero_vuelo = f"{aerolinea}{segment_inicio['number']}"

#         traveler = vuelo['travelerPricings'][0]
#         clase = traveler['fareDetailsBySegment'][0]['class']
#         tarifa = traveler['fareDetailsBySegment'][0].get('brandedFareLabel', 'N/A')
#         detalle_tarifa = formatear_tarifa_clase(
#             traveler['fareDetailsBySegment'][0]['cabin'],
#             tarifa,
#             clase
#         )
#         equip_mano = traveler['fareDetailsBySegment'][0]['includedCabinBags'].get('quantity', 0)
#         equip_fact = traveler['fareDetailsBySegment'][0]['includedCheckedBags'].get('quantity', 0)

#         amenities = traveler['fareDetailsBySegment'][0].get('amenities', [])
#         lista_amenities = ', '.join(a['description'] for a in amenities if not a['isChargeable']) or 'Ninguna incluida'
#         checkin_url = CHECKIN_LINKS.get(aerolinea, "#")

#         vuelos_procesados.append({
#             "salida": salida,
#             "llegada": llegada,
#             "hora_salida": hora_salida,
#             "hora_llegada": hora_llegada,
#             "fecha_salida": fecha_salida,
#             "fecha_llegada": fecha_llegada,
#             "precio": precio,
#             "duracion": duracion,
#             "avion": avion,
#             "numero_vuelo": numero_vuelo,
#             "detalle_tarifa": detalle_tarifa,
#             "equip_mano": equip_mano,
#             "equip_fact": equip_fact,
#             "lista_amenities": lista_amenities,
#             "checkin_url": checkin_url
#         })

#     return vuelos_procesados
