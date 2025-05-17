import re
from services.generador import generar_itinerario_con_direccion, generar_guia_sin_direccion
from services.almacenamiento import guardar_guia
from services.auth import gestionar_usuario

def generar_guia_completa_sin_destino(desea_guardar=False, **kwargs):
    """
    kwargs esperados:
    - desde, epoca, lugar, fecha, personas, continente, pais
    """
    texto_guia = generar_guia_sin_direccion(
        kwargs["desde"],
        kwargs["epoca"],
        kwargs["lugar"],
        kwargs["fecha"],
        kwargs["personas"],
        kwargs.get("continente", ""),
        kwargs.get("pais", "")
    )

    if desea_guardar:
        usuario = gestionar_usuario()
        secciones = re.split(r"(?=^\d+\.)", texto_guia, flags=re.MULTILINE)
        for seccion in secciones:
            seccion = seccion.strip()
            if not seccion:
                continue
            numero = seccion.split(".")[0].strip()
            guardar_guia(usuario, f"destino-no-definido-opcion-{numero}", seccion)

    return texto_guia


def generar_itinerario_con_destino(destino, dias, fecha, personas, desea_guardar=False):
    guia = generar_itinerario_con_direccion(destino, dias, fecha, personas)

    if desea_guardar:
        usuario = gestionar_usuario()
        guardar_guia(usuario, destino, guia)

    return guia
