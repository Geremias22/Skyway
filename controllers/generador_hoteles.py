import os, json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from amadeus import Client, ResponseError
from controllers.google_places import get_place_details_by_text


load_dotenv()
amadeus = Client(client_id=os.getenv("AMADEUS_CLIENT_ID"),
                 client_secret=os.getenv("AMADEUS_CLIENT_SECRET"))

def buscar_hoteles(
        destino_code="BCN", 
        # check_in=None, 
        # check_out=None, 
        check_in="2025-08-18", 
        check_out="2025-08-22", 
        noches=5, 
        adultos=3, 
        rooms=2,
        max_hotels=50):
    # 1) Fechas por defecto: hoy +1
    if not check_in:
        check_in = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not check_out:
        check_out = (datetime.strptime(check_in, "%Y-%m-%d") + timedelta(days=noches)).strftime("%Y-%m-%d")

    try:
        # 2) Listar hoteles en la ciudad
        resp_city = amadeus.reference_data.locations.hotels.by_city.get(cityCode=destino_code)
        all_hotels = resp_city.data or []
        total_hotels = len(all_hotels)

        # Volcar crudo para inspección
        with open("output/raw_hotels_by_city.json", "w", encoding="utf-8") as f:
            json.dump(all_hotels, f, indent=2, ensure_ascii=False)

        # 3) Pedir ofertas para un subconjunto de hotels
        subset_ids = [h["hotelId"] for h in all_hotels[:max_hotels]]
        offers = []
        if subset_ids:
            resp_offers = amadeus.shopping.hotel_offers_search.get(
                hotelIds=",".join(subset_ids),
                checkInDate=check_in,
                checkOutDate=check_out,
                adults=adultos,
                roomQuantity=rooms
            )
            offers = resp_offers.data or []

        # Volcar crudo de ofertas
        with open("output/raw_offers.json", "w", encoding="utf-8") as f:
            json.dump(offers, f, indent=2, ensure_ascii=False)

        # 4) Organizar: crear un dict map de hotelId → lista de ofertas
        offers_by_hotel = {}
        for o in offers:
            hid = o["hotel"]["hotelId"]
            offers_by_hotel.setdefault(hid, []).append(o["offers"][0])

        # 5) Construir lista final
        hoteles_procesados = []

        for h in all_hotels[:max_hotels]:
            hid = h["hotelId"]
            listado_ofertas = offers_by_hotel.get(hid, [])
            
            detalles = []
            for o in listado_ofertas:
                room = o.get("room", {})
                te = room.get("typeEstimated", {})
                desc = room.get("description", {}).get("text", "—")
                
                detalles.append({
                    "precio": o.get("price", {}).get("total", "—"),
                    "moneda": o.get("price", {}).get("currency", "—"),
                    "checkin": o.get("checkInDate", "—"),
                    "checkout": o.get("checkOutDate", "—"),
                    "room_category": te.get("category", te.get("bedType", "—")),
                    "beds": te.get("beds", "—"),
                    "room_quantity": o.get("roomQuantity", "—"),
                    "rate_code": o.get("rateCode", "—"),
                    "board_type": o.get("boardType", "—"),
                    "taxes": o.get("price", {}).get("taxes", []),
                    "cancellation_policies": o.get("policies", {}).get("cancellations", []),
                    "payment_type": o.get("policies", {}).get("paymentType", "—"),
                    "description": desc
                })
            
            hoteles_procesados.append({
                "hotelId": hid,
                "nombre": h.get("name", "—"),
                "geo_lat": h.get("geoCode", {}).get("latitude"),
                "geo_lon": h.get("geoCode", {}).get("longitude"),
                "address_country": h.get("address", {}).get("countryCode", "—"),
                "num_offers": len(listado_ofertas),
                "offers": detalles
            })
        for hotel in hoteles_procesados:
            detalles_gm = get_place_details_by_text(hotel["nombre"], destino_code)
            hotel["gm_address"] = detalles_gm.get("address")
            hotel["gm_rating"]  = detalles_gm.get("rating")
            hotel["gm_photos"]  = detalles_gm.get("photos", [])

        return {
            "total_hotels": total_hotels,
            "total_offers": len(offers),
            "hoteles": hoteles_procesados,
            "check_in": check_in,
            "check_out": check_out
        }

    except ResponseError as error:
        # En caso de fallo completo, devolvemos vacíos para no romper la vista
        return {"total_hotels": 0, "total_offers": 0, "hoteles": [], "check_in": check_in, "check_out": check_out}
