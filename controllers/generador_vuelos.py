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

# def guardar_resultados(flights):
#     with open("output/resultados_vuelos.json", "w", encoding="utf-8") as f_json:
#         json.dump(flights, f_json, indent=2, ensure_ascii=False)

#     with open("output/resultados_vuelos.html", "w", encoding="utf-8") as f_html:
#         f_html.write("<!DOCTYPE html><html><head><title>Resultados de Vuelos</title></head><body>")
#         # Obtener ciudad de llegada del primer vuelo para el titulo xd
#         ciudad_destino = primer_segmento['arrival']['iataCode']

#         f_html.write("<h1>🛫 Resultados de vuelos a {ciudad_destino}</h1><ul>")

#         for i, vuelo in enumerate(flights, 1):

#             # Recuperar variables para usarlo en el html
#             segment = vuelo['itineraries'][0]['segments'][0]
#             salida = segment['departure']['iataCode']
#             llegada = segment['arrival']['iataCode']
#             hora_salida = segment['departure']['at'][11:16]
#             hora_llegada = segment['arrival']['at'][11:16]
#             fecha_salida = segment['departure']['at'][:10]
#             fecha_llegada = segment['arrival']['at'][:10]
#             precio = vuelo['price']['total']
#             duracion_no_legible = vuelo['itineraries'][0]['duration']
#             duracion = formatear_duracion(duracion_no_legible)
#             aerolinea = segment['carrierCode']
#             avion_codigo = segment['aircraft']['code']
#             avion = AIRCRAFTS.get(avion_codigo, avion_codigo)
#             numero_vuelo = f"{aerolinea}{segment['number']}"

#             traveler = vuelo['travelerPricings'][0]
#             clase = traveler['fareDetailsBySegment'][0]['class']
#             tarifa = traveler['fareDetailsBySegment'][0].get('brandedFareLabel', 'N/A')
#             detalle_tarifa = formatear_tarifa_clase(
#                 traveler['fareDetailsBySegment'][0]['cabin'],
#                 tarifa,
#                 clase
#             )
#             equip_mano = traveler['fareDetailsBySegment'][0]['includedCabinBags'].get('quantity', 0)
#             equip_fact = traveler['fareDetailsBySegment'][0]['includedCheckedBags'].get('quantity', 0)

#             amenities = traveler['fareDetailsBySegment'][0].get('amenities', [])
#             lista_amenities = ', '.join(a['description'] for a in amenities if not a['isChargeable'])

#             checkin_url = CHECKIN_LINKS.get(aerolinea, "#")

#             f_html.write(f"""
# <li>
#   <strong>{salida} → {llegada}</strong> (Fecha: {fecha_salida} - {fecha_llegada})<br>
#   Salida: {hora_salida} — Llegada: {hora_llegada}<br>
#   Vuelo: {numero_vuelo} ({aerolinea})<br>
#   Avión: {avion}<br>
#   Precio(Aprox.): {precio} EUR<br>
#   Duracion: {duracion} <br>
#   <button onclick="document.getElementById('vuelo{i}').style.display='block'">Más detalles</button>
#   <div id="vuelo{i}" style="display:none; margin-top:10px">
#     <li>
#         - {detalle_tarifa}
#         - Equipaje: {equip_mano} de mano, {equip_fact} facturado
#         - Servicios incluidos: {lista_amenities or 'Ninguna incluida'}
#         - <a href="{checkin_url}" target="_blank">Check-in online</a>
#     </li>
#   </div>
# </li><br>
#             """)

#         f_html.write("</ul></body></html>")




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


def buscar_vuelos():
    try:
        respuesta = amadeus.shopping.flight_offers_search.get(
            originLocationCode="MAD",
            destinationLocationCode="BCN",
            departureDate="2025-05-10",
            adults=3
        )
        vuelos = respuesta.data[:10]
        print(f"✈️ Se encontraron {len(vuelos)} vuelos.")
        guardar_resultados(vuelos)  # sigue guardando si quieres
        return procesar_vuelos(vuelos)  # nueva función que devuelve lista procesada
    except ResponseError as error:
        print("❌ Error al buscar vuelos:", error)
        return []
    

def procesar_vuelos(flights):
    vuelos_procesados = []
    for vuelo in flights:
        segment = vuelo['itineraries'][0]['segments'][0]
        salida = segment['departure']['iataCode']
        llegada = segment['arrival']['iataCode']
        hora_salida = segment['departure']['at'][11:16]
        hora_llegada = segment['arrival']['at'][11:16]
        fecha_salida = segment['departure']['at'][:10]
        fecha_llegada = segment['arrival']['at'][:10]
        precio = vuelo['price']['total']
        duracion = formatear_duracion(vuelo['itineraries'][0]['duration'])
        aerolinea = segment['carrierCode']
        avion_codigo = segment['aircraft']['code']
        avion = AIRCRAFTS.get(avion_codigo, avion_codigo)
        numero_vuelo = f"{aerolinea}{segment['number']}"

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
        checkin_url = CHECKIN_LINKS.get(aerolinea, "#")

        vuelos_procesados.append({
            "salida": salida,
            "llegada": llegada,
            "hora_salida": hora_salida,
            "hora_llegada": hora_llegada,
            "fecha_salida": fecha_salida,
            "fecha_llegada": fecha_llegada,
            "precio": precio,
            "duracion": duracion,
            "avion": avion,
            "numero_vuelo": numero_vuelo,
            "detalle_tarifa": detalle_tarifa,
            "equip_mano": equip_mano,
            "equip_fact": equip_fact,
            "lista_amenities": lista_amenities,
            "checkin_url": checkin_url
        })
    return vuelos_procesados