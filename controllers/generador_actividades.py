import os
from dotenv import load_dotenv
from amadeus import Client, ResponseError

load_dotenv()
amadeus = Client(
    client_id=os.getenv("AMADEUS_CLIENT_ID"),
    client_secret=os.getenv("AMADEUS_CLIENT_SECRET")
)

def buscar_actividades(lat: float, lon: float, radius_km: int = 5, max_items: int = 20) -> list:
    """
    Llama a GET /v1/shopping/activities con lat/lon y radio en km.
    Devuelve una lista de actividades procesadas.
    """
    try:
        resp = amadeus.shopping.activities.get(
            latitude=lat,
            longitude=lon,
            radius=radius_km,
            radiusUnit="KM"
        )
        data = resp.data or []
    except ResponseError as err:
        print("❌ Error al buscar actividades:", err)
        return []

    resultados = []
    for act in data[:max_items]:
        resultados.append({
            "id":        act.get("id"),
            "nombre":    act.get("name"),
            "categoria": act.get("type"),
            "descripcion": act.get("shortDescription"),
            "precio":    act.get("price", {}).get("amount"),
            "moneda":    act.get("price", {}).get("currency"),
            "duracion":  act.get("duration"),
            "imagen":    (act.get("images") or [{}])[0].get("path")  # primera imagen
        })
    return resultados
