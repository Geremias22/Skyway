# controllers/generador_hoteles.py

import os
import json
from dotenv import load_dotenv
from amadeus import Client, ResponseError
from jinja2 import Environment, FileSystemLoader

load_dotenv()

amadeus = Client(
    client_id=os.getenv("AMADEUS_CLIENT_ID"),
    client_secret=os.getenv("AMADEUS_CLIENT_SECRET")
)


def buscar_hoteles(destino_code="BCN", check_in="2025-05-10", noches=2, adultos=2):
    try:
        check_out = calcular_checkout(check_in, noches)

        respuesta = amadeus.shopping.hotel_offers_search.get(
            cityCode=destino_code,
            checkInDate=check_in,
            checkOutDate=check_out,
            adults=adultos,
            roomQuantity=1
        )

        print("✅ Respuesta bruta de hoteles:")
        print(respuesta.body)  # Mostrar la respuesta original de la API (como texto)
        print("📦 Resultado en .data:", respuesta.data)

        hoteles = respuesta.data[:10]
        if not hoteles:
            print("⚠️ No se encontraron hoteles con estos parámetros.")
        guardar_resultados(hoteles)
        return procesar_hoteles(hoteles)

    except ResponseError as error:
        print("❌ Error al buscar hoteles:", error)
        return []


def calcular_checkout(check_in, noches):
    from datetime import datetime, timedelta
    entrada = datetime.strptime(check_in, "%Y-%m-%d")
    salida = entrada + timedelta(days=noches)
    return salida.strftime("%Y-%m-%d")


def guardar_resultados(hoteles):
    # Guardar JSON crudo
    with open("output/resultados_hoteles.json", "w", encoding="utf-8") as f_json:
        json.dump(hoteles, f_json, indent=2, ensure_ascii=False)

    # Renderizar HTML con Jinja2
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('resultados_hoteles.html')
    contenido_html = template.render(hoteles=procesar_hoteles(hoteles))

    with open("output/resultados_hoteles.html", "w", encoding="utf-8") as f_html:
        f_html.write(contenido_html)


def procesar_hoteles(hoteles):
    lista = []
    for hotel in hoteles:
        info = hotel["hotel"]
        oferta = hotel["offers"][0]  # Solo la primera oferta

        lista.append({
            "nombre": info.get("name", "Nombre no disponible"),
            "direccion": info.get("address", {}).get("lines", [""])[0],
            "ciudad": info.get("address", {}).get("cityName", ""),
            "estrellas": info.get("rating", "N/A"),
            "amenities": info.get("amenities", []),
            "precio": oferta.get("price", {}).get("total", "¿?"),
            "moneda": oferta.get("price", {}).get("currency", "EUR"),
            "checkin": oferta.get("checkInDate", "-"),
            "checkout": oferta.get("checkOutDate", "-"),
            "tipo_habitacion": oferta.get("room", {}).get("typeEstimated", {}).get("category", "Habitación"),
            "camas": oferta.get("room", {}).get("typeEstimated", {}).get("beds", 1),
            "descripcion": oferta.get("room", {}).get("description", {}).get("text", "")
        })
    return lista
