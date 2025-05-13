import os
import os, requests

API_KEY = os.getenv("GOOGLE_API_KEY")

def get_place_details_by_text(name: str, city: str) -> dict:
    """
    Usa Text Search para encontrar un place_id a partir de "Hotel Name, City"
    y luego Place Details para extraer dirección, rating y fotos.
    """
    # 1) Text Search
    ts_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"{name}, {city}"
    ts_params = {"key": API_KEY, "query": query, "type": "lodging"}
    ts = requests.get(ts_url, params=ts_params).json()
    if not ts.get("results"):
        return {}
    place = ts["results"][0]
    place_id = place["place_id"]

    # 2) Place Details
    pd_url = "https://maps.googleapis.com/maps/api/place/details/json"
    pd_params = {
        "key": API_KEY,
        "place_id": place_id,
        "fields": "formatted_address,rating,photos"
    }
    r = requests.get(pd_url, params=pd_params).json().get("result", {})

    # 3) Monta URLs de fotos
    photos = []
    for p in r.get("photos", [])[:3]:
        ref = p["photo_reference"]
        photos.append(
            f"https://maps.googleapis.com/maps/api/place/photo"
            f"?key={API_KEY}"
            f"&photoreference={ref}"
            f"&maxwidth=400"
        )

    return {
        "address": r.get("formatted_address"),
        "rating":  r.get("rating"),
        "photos":  photos
    }