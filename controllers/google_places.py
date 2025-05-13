# controllers/google_places.py
import os
import requests

API_KEY = os.getenv("GOOGLE_API_KEY")

def get_place_details_by_text(name: str, city: str) -> dict:
    """
    Busca “name, city” con Text Search → luego Place Details.
    """
    # 1) Text Search
    ts = requests.get(
        "https://maps.googleapis.com/maps/api/place/textsearch/json",
        params={
          "key": API_KEY,
          "query": f"{name}, {city}",
          "type": "lodging"
        }
    ).json()
    if not ts.get("results"):
        return {}
    place_id = ts["results"][0]["place_id"]

    # 2) Place Details
    detail = requests.get(
        "https://maps.googleapis.com/maps/api/place/details/json",
        params={
          "key": API_KEY,
          "place_id": place_id,
          "fields": "formatted_address,rating,photos"
        }
    ).json().get("result", {})

    # 3) Monta URLs de fotos (hasta 3)
    photos = []
    for p in detail.get("photos", [])[:3]:
        ref = p["photo_reference"]
        photos.append(
          f"https://maps.googleapis.com/maps/api/place/photo"
          f"?key={API_KEY}&photoreference={ref}&maxwidth=400"
        )

    return {
      "address": detail.get("formatted_address"),
      "rating":  detail.get("rating"),
      "photos":  photos
    }
