from flask import Flask, render_template, request, jsonify
from controllers.generador_vuelos import buscar_vuelos
from controllers.generador_hoteles import buscar_hoteles
from controllers.google_places import get_place_details_by_text
from controllers.generador_actividades import buscar_actividades
from controllers.dashboard_generator import generar_dashboard_completo


app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/vuelos")
def mostrar_vuelos():
    vuelos = buscar_vuelos(
        origen="MAD",
        destino="BCN",
        fecha="2025-06-01"
    )
    return render_template(
        "resultados_vuelos.html",
        vuelos=vuelos,
        origen="MAD",
        destino="BCN"
    )
    # return render_template("resultados_vuelos.html", vuelos=vuelos, origen=vuelos[0]["salida"], destino=vuelos[0]["llegada"])

@app.route('/buscar', methods=['GET', 'POST'])
def procesar_busqueda_con_destino():
    if request.method == 'POST':
        # Procesar formulario
        location = request.form.get('location')
        personas = request.form.get('days')
        fecha = request.form.get('date')

        # Aquí puedes hacer validaciones, generar datos, etc.
        return redirect(url_for('mostrar_dashboard', 
                                origen=location, 
                                destino="LEN",  # esto lo puedes ajustar luego
                                dias=personas, 
                                fecha=fecha,
                                personas=personas))
    else:
        # Mostrar el formulario
        return render_template("buscar.html")


@app.route('/explorar', methods=['GET', 'POST'])
def procesar_busqueda_sin_destino():
    if request.method == 'POST':
        # Procesar formulario
        location = request.form.get('location')
        personas = request.form.get('days')
        fecha = request.form.get('date')

        # Aquí puedes hacer validaciones, generar datos, etc.
        return redirect(url_for('mostrar_dashboard', 
                                origen=location, 
                                destino="LEN",  # esto lo puedes ajustar luego
                                dias=personas, 
                                fecha=fecha,
                                personas=personas))
    else:
        # Mostrar el formulario
        return render_template("explorar.html")


@app.route("/hotel/<hotel_id>/gm-info")
def ruta_gm_info(hotel_id):
    datos = buscar_hoteles(destino_code="BCN", noches=2)
    hotel = next((h for h in datos["hoteles"] if h["hotelId"] == hotel_id), None)
    if not hotel:
        return jsonify({"error": "Hotel no encontrado"}), 404

    # Directamente Text Search + Details
    detalles = get_place_details_by_text(hotel["nombre"], "Barcelona")
    if not detalles:
        return ("", 204)
    return jsonify(detalles)

@app.route("/hoteles")
def ruta_hoteles():
    datos = buscar_hoteles(destino_code="BCN", noches=2)
    return render_template(
        "resultados_hoteles.html",
        total_hotels=datos["total_hotels"],
        total_offers=datos["total_offers"],
        hoteles=datos["hoteles"],
        check_in=datos["check_in"],
        check_out=datos["check_out"]
    )

# @app.route('/actividades')
# def ruta_actividades():
#     actividades = buscar_actividades()
#     return render_template('resultados_actividades.html', actividades=actividades)

@app.route("/actividades")
def ruta_actividades():
    # Para BCN usamos coordenadas aproximadas del centro
    lat_bc, lon_bc = 41.3851, 2.1734
    actividades = buscar_actividades(lat_bc, lon_bc, radius_km=5)
    return render_template(
        "resultados_actividades.html",
        actividades=actividades,
        ciudad="Barcelona"
    )


@app.route("/dashboard")
def mostrar_dashboard():
    # ⚠️ Puedes hacerlo dinámico leyendo de query params o base de datos
    datos = generar_dashboard_completo(
        origen="BCN",
        destino="LEN",
        dias="4",  
        fecha="2025-08-18",
        personas="2"
    )
    return render_template("dashboard.html", **datos)
    
if __name__ == "__main__":
    app.run(debug=True)
