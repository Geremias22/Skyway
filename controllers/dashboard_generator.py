from controllers.planificador_wrapper import generar_itinerario_con_destino
from controllers.generador_vuelos import buscar_vuelos
from controllers.generador_hoteles import buscar_hoteles
from controllers.generador_actividades import buscar_actividades

def generar_dashboard_completo(origen, destino, dias, fecha, personas):
    guia = generar_itinerario_con_destino(destino, dias, fecha, personas)
    vuelos = buscar_vuelos(origen, destino, fecha, adultos=int(personas))
    hoteles_data = buscar_hoteles(destino_code=destino[:3].upper(), adultos=int(personas))  # Cuidado con el código
    actividades = buscar_actividades(48.8566, 2.3522)  # París por defecto

    return {
        "guia": guia,
        "vuelos": vuelos,
        "hoteles": hoteles_data["hoteles"],
        "check_in": hoteles_data["check_in"],
        "check_out": hoteles_data["check_out"],
        "actividades": actividades
    }
