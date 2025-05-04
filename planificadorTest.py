import os
from dotenv import load_dotenv
import google.generativeai as genai
from services.generador import (
    generar_destinos_sin_direccion,
    generar_itinerario_con_direccion,
    generar_guia_sin_direccion
)
from services.almacenamiento import guardar_guia
from services.auth import gestionar_usuario
import re

# Punto de entrada del script
if __name__ == "__main__":
    load_dotenv()  # Cargar variables de entorno
    print("🌐 Bienvenido a Skyway\n")

    # Preguntar si el usuario ya tiene un destino en mente
    respuesta = input("¿Sabes dónde quieres ir? (sí/no): ").strip().lower()

    if respuesta in ["no", "n"]:
        # Recoger parámetros para guía sin destino específico
        epoca = input("🌄 ¿En qué época quieres viajar?: ")
        lugar = input("🌍 ¿Qué tipo de lugar te gustaría visitar (playa, ciudad, naturaleza, etc.)?: ")
        desde = input("📍 ¿Desde dónde sales?: ")
        cuando = input("📆 ¿Sabes cuanto tiempo quieres quedarte?: ")
        

        if cuando in ["si", "s"]:
            fecha = input("📆 ¿Que fecha, desde cuando hasta cuando tienes pensado?")
        else:
            fecha = input("📆 ¿que epoca mas o menos te interesaria ir?")
        # duracion = input("📅 ¿Cuántos días disponibles tienes?: ")
        personas = input("👥 ¿Cuántas personas viajan?: ")
        continente = input("🌎 ¿Quieres filtrar por continente? (deja vacío si no): ")
        pais = input("🗺️ ¿Quieres filtrar por país? (deja vacío si no): ")

        # Generar las 3 guías en un solo texto
        texto_guia = generar_guia_sin_direccion(
            epoca, lugar, desde, fecha, personas, continente, pais
        )
        print("\n📝 Guías generadas (3 opciones):\n")
        print(texto_guia)

        # Preguntar si el usuario quiere guardar estas 3 guías
        if input("\n💾 ¿Quieres guardar estas 3 guías? (sí/no): ").strip().lower() in ["sí","si","s"]:
            usuario = gestionar_usuario()
            # Dividir el texto en secciones numeradas (1., 2., 3.)
            secciones = re.split(r"(?=^\d+\.)", texto_guia, flags=re.MULTILINE)
            for seccion in secciones:
                seccion = seccion.strip()
                if not seccion:
                    continue
                # Extraer número de la guía (1,2,3)
                numero = seccion.split(".")[0].strip()
                # Guardar cada guía por separado con identificador único
                guardar_guia(
                    usuario,
                    f"destino-no-definido-opcion-{numero}",
                    seccion
                )
            print("✅ Las 3 guías se han guardado correctamente.")

    else:
        # Recoger parámetros para destino específico
        destino = input("🌍 ¿A qué lugar quieres viajar?: ")
        dias = input("📅 ¿Cuántos días durará el viaje?: ")
        fecha = input("📆 ¿En qué fecha?: ")
        personas = input("👥 ¿Cuántas personas van?: ")

        # Generar itinerario detallado
        guia = generar_itinerario_con_direccion(destino, dias, fecha, personas)
        print("\n📝 Itinerario generado:\n")
        print(guia)

        # Mostrar resumen fijo de categorías
        print(
            "\n📌 Resumen del viaje y categorías:\n"
            "- Resumen general del viaje\n"
            "- Vuelos\n"
            "- Hotel\n"
            "- Transporte\n"
            "- Actividades\n"
            "- Restaurantes\n"
            "- Lista de cosas para llevar\n"
            "- Alquiler de coche\n"
        )

        # Preguntar si guardar esta guía
        if input("\n💾 ¿Quieres guardar esta guía? (sí/no): ").strip().lower() in ["sí","si","s"]:
            usuario = gestionar_usuario()
            guardar_guia(usuario, destino, guia)
            print("✅ Guía guardada correctamente.")